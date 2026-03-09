import asyncio
import logging
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.deps import async_session
from src.models.analysis import Analysis, AnalysisFile
from src.models.file import UploadedFile
from src.services.s3_storage import download_from_s3
from src.services.file_parser import parse_file
from src.services.insight_engine import run_statistical_analysis
from src.services.llm_client import get_business_insights, get_chart_specs

logger = logging.getLogger(__name__)


async def _run(analysis_id: str):
    async with async_session() as db:
        result = await db.execute(
            select(Analysis)
            .options(selectinload(Analysis.files))
            .where(Analysis.id == analysis_id)
        )
        analysis = result.scalar_one_or_none()
        if not analysis:
            logger.error("Analysis not found: %s", analysis_id)
            return

        try:
            analysis.status = "running"
            await db.commit()

            file_ids = [af.file_id for af in analysis.files]
            files_result = await db.execute(
                select(UploadedFile).where(UploadedFile.id.in_(file_ids))
            )
            files = files_result.scalars().all()

            all_insights = []
            combined_profile = {"files": []}

            for f in files:
                raw = await download_from_s3(f.s3_key)
                df = parse_file(raw, f.original_name)

                statistical = run_statistical_analysis(df)
                all_insights.extend(statistical)

                combined_profile["files"].append({
                    "name": f.original_name,
                    "domain": f.domain,
                    "profile": f.profile,
                })

            domain = files[0].domain if files else "generic"
            business_insights = await get_business_insights(combined_profile, all_insights, domain)
            all_insights.extend(business_insights)

            chart_specs = await get_chart_specs(combined_profile, all_insights)

            analysis.insights = all_insights
            analysis.chart_specs = chart_specs
            analysis.title = f"Анализ: {', '.join(f.original_name for f in files)}"
            analysis.status = "done"
            analysis.completed_at = datetime.now(timezone.utc)
            await db.commit()
            logger.info("Analysis completed: %s", analysis_id)

        except Exception as e:
            logger.exception("Error running analysis %s", analysis_id)
            analysis.status = "error"
            await db.commit()


def run_analysis_task(analysis_id: str):
    asyncio.run(_run(analysis_id))
