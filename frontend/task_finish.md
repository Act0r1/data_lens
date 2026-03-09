# DataLens Frontend — Итог реализации

## Стек
- SvelteKit + TypeScript, Svelte 5 runes
- pnpm, Vite, Tailwind CSS v4, shadcn-svelte
- vega-embed (Vega-Lite графики), marked + DOMPurify (markdown)
- @sveltejs/adapter-node (Docker-ready)

## Структура файлов

```
frontend/src/
├── app.css                          # Soft Glass дизайн-система + shadcn theme
├── app.html                         # lang="ru", Google Fonts (DM Sans + Fraunces)
├── lib/
│   ├── api/
│   │   ├── client.ts                # Fetch wrapper, JWT, auto-refresh 401, lock
│   │   ├── auth.ts                  # register, login, getMe
│   │   ├── files.ts                 # uploadFile, listFiles, getFilePreview, deleteFile
│   │   ├── analysis.ts             # runAnalysis, listAnalyses, getAnalysis
│   │   ├── chat.ts                  # getChatHistory, sendMessage (SSE async generator)
│   │   ├── charts.ts               # getChartSpecs, generateChart
│   │   └── billing.ts              # getPlans, getUsage, subscribe
│   ├── stores/
│   │   ├── auth.ts                  # user, loading, isAuthenticated, init, setSession, logout
│   │   ├── files.ts                 # files, uploading, load, upload, remove, updateFile
│   │   ├── analysis.ts             # current, chartSpecs, loading, load, reset
│   │   └── chat.ts                  # messages, streamingContent, isStreaming, loadHistory, send, reset
│   ├── mock/
│   │   ├── index.ts                 # USE_MOCK = VITE_USE_MOCK === 'true'
│   │   ├── files.ts                 # 4 mock файла (WB, Ozon, 1C)
│   │   ├── analysis.ts             # insights + 2 Vega-Lite спеки
│   │   └── chat.ts                  # 4 сообщения + mockStreamChunks
│   ├── components/
│   │   ├── shared/
│   │   │   ├── GlassCard.svelte
│   │   │   └── Logo.svelte
│   │   ├── landing/
│   │   │   ├── Nav.svelte           # Floating pill navbar, glass
│   │   │   ├── Hero.svelte          # Анимированные бары, статистика
│   │   │   ├── Features.svelte      # 6 карточек, lucide иконки
│   │   │   ├── Pricing.svelte       # 4 тарифа, Business выделен
│   │   │   └── Footer.svelte
│   │   ├── dashboard/
│   │   │   ├── Sidebar.svelte       # Glass sidebar, 4 nav items, logout
│   │   │   ├── UploadZone.svelte    # Drag & drop, CSV/Excel
│   │   │   ├── FileTable.svelte     # Список файлов, click → анализ
│   │   │   └── StatusPill.svelte    # ready/processing/error/uploaded
│   │   ├── analysis/
│   │   │   ├── AnalysisHeader.svelte
│   │   │   ├── InsightCard.svelte   # Цветные теги типа + severity
│   │   │   ├── InsightsGrid.svelte  # 2-колоночная сетка
│   │   │   └── ChartView.svelte     # Dynamic import vega-embed, SVG
│   │   ├── chat/
│   │   │   ├── ChatPanel.svelte     # Sticky, auto-scroll, streaming
│   │   │   ├── ChatMessage.svelte   # Markdown (marked + DOMPurify)
│   │   │   ├── ChatInput.svelte     # Enter to send, disabled при streaming
│   │   │   └── TypingIndicator.svelte
│   │   └── ui/                      # shadcn-svelte компоненты
│   │       ├── button/
│   │       ├── card/
│   │       ├── table/
│   │       ├── badge/
│   │       ├── dialog/
│   │       ├── input/
│   │       ├── progress/
│   │       ├── tabs/
│   │       ├── sheet/
│   │       ├── skeleton/
│   │       ├── tooltip/
│   │       └── separator/
│   ├── types/
│   │   └── api.ts                   # 14 интерфейсов (UserResponse, FileResponse, etc.)
│   └── utils/
│       ├── format.ts                # formatBytes, formatDate, formatCurrency, formatNumber
│       └── cn.ts                    # Re-export cn
├── routes/
│   ├── +layout.svelte               # Root layout, import app.css
│   ├── +page.svelte                 # Landing: Nav + Hero + Features + Pricing + Footer
│   ├── login/+page.svelte           # Форма входа, glass card
│   ├── register/+page.svelte        # Форма регистрации, glass card
│   └── dashboard/
│       ├── +layout.ts               # Auth guard (ssr=false), mock bypass
│       ├── +layout.svelte           # Grid: sidebar 220px + main
│       ├── +page.svelte             # Файлы: UploadZone + FileTable, polling
│       └── analysis/[id]/
│           ├── +page.ts             # params.id → analysisId
│           └── +page.svelte         # Insights + Charts + ChatPanel, polling
```

## Дизайн — Soft Glass

- Glass: `rgba(255,255,255,0.45)` + `backdrop-filter: blur(24px) saturate(180%)`
- Шрифты: DM Sans (body), Fraunces (headings)
- Цвета: accent `#e8450e`, bg `#f0ede8`, green `#1a8a4a`, blue `#2563eb`
- Border-radius: 20px, ambient gradients на body

## Ключевые паттерны

- **JWT auth**: auto-refresh на 401, lock для concurrent refresh
- **SSE streaming**: async generator в `chat.ts`, посимвольный вывод в ChatPanel
- **Mock mode**: `VITE_USE_MOCK=true` — все stores подменяют API на локальные данные
- **Polling**: dashboard и analysis polling каждые 3 сек для processing статусов
- **Dynamic import**: vega-embed (~350KB) загружается только на странице анализа

## Запуск

```bash
# Mock режим (без бэкенда)
cd frontend && VITE_USE_MOCK=true pnpm dev

# С бэкендом
cd frontend && pnpm dev

# Production build
pnpm build
```

## Статус

- `pnpm build` — проходит без ошибок
- 90+ файлов создано
- Все фазы плана реализованы (1-8)
