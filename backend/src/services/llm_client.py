import json
import logging
from typing import AsyncGenerator

import httpx

from src.config import settings
from src.services.llm_prompts import SYSTEM_PROMPT, ANALYSIS_PROMPT, CHART_PROMPT, CHAT_PROMPT

logger = logging.getLogger(__name__)

YANDEX_GPT_URL = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"


async def _call_yandex_gpt(messages: list[dict], stream: bool = False) -> str | AsyncGenerator[str, None]:
    headers = {
        "Authorization": f"Api-Key {settings.yandex_gpt_api_key}",
        "x-folder-id": settings.yandex_gpt_folder_id,
    }
    body = {
        "modelUri": f"gpt://{settings.yandex_gpt_folder_id}/{settings.yandex_gpt_model}",
        "completionOptions": {"stream": stream, "temperature": 0.3, "maxTokens": 2000},
        "messages": messages,
    }

    if stream:
        async def _stream():
            async with httpx.AsyncClient(timeout=60) as client:
                async with client.stream("POST", YANDEX_GPT_URL, json=body, headers=headers) as resp:
                    async for line in resp.aiter_lines():
                        if not line:
                            continue
                        try:
                            data = json.loads(line)
                            text = data.get("result", {}).get("alternatives", [{}])[0].get("message", {}).get("text", "")
                            if text:
                                yield text
                        except json.JSONDecodeError:
                            continue
        return _stream()

    async with httpx.AsyncClient(timeout=60) as client:
        resp = await client.post(YANDEX_GPT_URL, json=body, headers=headers)
        resp.raise_for_status()
        data = resp.json()
        return data["result"]["alternatives"][0]["message"]["text"]


async def get_business_insights(profile: dict, statistical_insights: list[dict], domain: str) -> list[dict]:
    prompt = ANALYSIS_PROMPT.format(
        domain=domain,
        profile=json.dumps(profile, ensure_ascii=False, indent=2),
        statistical_insights=json.dumps(statistical_insights, ensure_ascii=False, indent=2),
    )
    messages = [
        {"role": "system", "text": SYSTEM_PROMPT},
        {"role": "user", "text": prompt},
    ]
    result = await _call_yandex_gpt(messages)
    try:
        return json.loads(result)
    except json.JSONDecodeError:
        logger.error("Failed to parse LLM insights: %s", result[:200])
        return [{"type": "business_insight", "title": "Анализ", "description": result, "severity": "info"}]


async def get_chart_specs(profile: dict, insights: list[dict]) -> list[dict]:
    prompt = CHART_PROMPT.format(
        profile=json.dumps(profile, ensure_ascii=False, indent=2),
        insights=json.dumps(insights, ensure_ascii=False, indent=2),
    )
    messages = [
        {"role": "system", "text": SYSTEM_PROMPT},
        {"role": "user", "text": prompt},
    ]
    result = await _call_yandex_gpt(messages)
    try:
        return json.loads(result)
    except json.JSONDecodeError:
        logger.error("Failed to parse chart specs: %s", result[:200])
        return []


async def stream_chat_response(analysis, history, question: str) -> AsyncGenerator[str, None]:
    context = json.dumps(analysis.insights or {}, ensure_ascii=False)[:3000]
    history_text = "\n".join(f"{m.role}: {m.content}" for m in history[-10:])

    prompt = CHAT_PROMPT.format(context=context, history=history_text, question=question)
    messages = [
        {"role": "system", "text": SYSTEM_PROMPT},
        {"role": "user", "text": prompt},
    ]

    result = await _call_yandex_gpt(messages, stream=True)
    if isinstance(result, str):
        yield result
    else:
        async for chunk in result:
            yield chunk
