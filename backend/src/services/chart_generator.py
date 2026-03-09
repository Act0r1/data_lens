import logging

from src.services.llm_client import get_chart_specs as _get_specs

logger = logging.getLogger(__name__)


async def generate_chart_specs(profile: dict, insights: list[dict]) -> list[dict]:
    return await _get_specs(profile, insights)


async def generate_chart_spec(analysis, prompt: str) -> dict:
    from src.services.llm_client import _call_yandex_gpt
    from src.services.llm_prompts import SYSTEM_PROMPT
    import json

    messages = [
        {"role": "system", "text": SYSTEM_PROMPT},
        {"role": "user", "text": f"Создай Vega-Lite спецификацию для графика: {prompt}\n\nКонтекст: {json.dumps(analysis.insights or {}, ensure_ascii=False)[:2000]}\n\nВерни только JSON объект Vega-Lite."},
    ]
    result = await _call_yandex_gpt(messages)
    try:
        return json.loads(result)
    except json.JSONDecodeError:
        return {"error": "Failed to generate chart"}
