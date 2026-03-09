SYSTEM_PROMPT = """Ты — AI-аналитик данных для российского бизнеса. Отвечай на русском.
Анализируй данные и давай конкретные бизнес-рекомендации.
Используй термины, понятные предпринимателям, не техническую статистику."""

ANALYSIS_PROMPT = """Проанализируй данные и дай бизнес-инсайты.

Домен: {domain}
Профиль данных:
{profile}

Статистические находки:
{statistical_insights}

Дай 3-5 конкретных бизнес-инсайтов в формате JSON:
[{{"title": "...", "description": "...", "severity": "info|warning|critical", "type": "business_insight"}}]

Только JSON, без markdown."""

CHART_PROMPT = """На основе данных предложи 2-3 графика в формате Vega-Lite.

Профиль данных:
{profile}

Инсайты:
{insights}

Верни JSON массив Vega-Lite спецификаций. Каждая спека должна содержать:
- $schema: "https://vega.github.io/schema/vega-lite/v5.json"
- description на русском
- data.values — пустой массив (данные подставятся позже)
- mark, encoding

Только JSON массив, без markdown."""

CHAT_PROMPT = """Ты анализируешь данные пользователя.

Контекст анализа:
{context}

История чата:
{history}

Вопрос: {question}

Отвечай конкретно, с цифрами из данных. На русском."""
