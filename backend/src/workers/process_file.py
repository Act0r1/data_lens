import asyncio
import logging

from sqlalchemy import select

from src.deps import async_session
from src.models.file import UploadedFile
from src.services.s3_storage import download_from_s3, upload_to_s3
from src.services.file_parser import parse_file
from src.services.data_profiler import profile_dataframe
from src.services.domain_detector import detect_domain

logger = logging.getLogger(__name__)


async def _process(file_id: str):
    async with async_session() as db:
        result = await db.execute(select(UploadedFile).where(UploadedFile.id == file_id))
        f = result.scalar_one_or_none()
        if not f:
            logger.error("File not found: %s", file_id)
            return

        try:
            f.status = "processing"
            await db.commit()

            raw = await download_from_s3(f.s3_key)
            df = parse_file(raw, f.original_name)

            profile = profile_dataframe(df)
            domain = detect_domain(list(df.columns))

            parquet_key = f.s3_key.rsplit(".", 1)[0] + ".parquet"
            parquet_bytes = df.to_parquet(index=False)
            await upload_to_s3(parquet_key, parquet_bytes, "application/octet-stream")

            preview_rows = df.head(50).fillna("").to_dict(orient="records")
            preview = {"columns": list(df.columns), "rows": preview_rows}

            f.parquet_s3_key = parquet_key
            f.row_count = len(df)
            f.column_count = len(df.columns)
            f.profile = profile
            f.domain = domain
            f.preview = preview
            f.status = "ready"
            await db.commit()
            logger.info("File processed: %s", file_id)

        except Exception as e:
            logger.exception("Error processing file %s", file_id)
            f.status = "error"
            f.error_message = str(e)[:500]
            await db.commit()


def process_file_task(file_id: str):
    asyncio.run(_process(file_id))
