# AI Gateway: агрегация LLM-провайдеров для Pi Coding Agent

Исследование инструментов и архитектурных подходов для подключения харнессов (в первую очередь Pi Coding Agent) к агрегированному LLM-шлюзу с полными метаданными о моделях.

## Задача

Настроить локальный сервис на машине разработчика, который:

1. Агрегирует нескольких LLM-провайдеров — включая произвольные OpenAI-совместимые.
2. Предоставляет единый OpenAI-совместимый эндпойнт для всех харнессов.
3. Автоматически обнаруживает доступные модели у провайдеров.
4. Обогащает модели метаданными: цены, contextWindow, maxTokens, reasoning, input modalities.
5. Поддерживает fallback при ошибке (5xx, 429, timeout) или высоком пинге.
6. Отслеживает расходы и потребление токенов.
7. Передаёт данные в Pi Coding Agent через `models.json`.

## Хронология исследования

Тема развивалась в несколько этапов. Ниже — ключевые вехи.

### Этап 1: Поиск шлюзов общего назначения

Первоначальный обзор показал, что задача решается классом инструментов **AI Gateway** (LLM-роутеров). Основные кандидаты: LiteLLM Proxy, Portkey AI Gateway, Aurora OSS, LLM Router (radlab), Ferro Labs AI Gateway, OpenHinge, Starport, RouteHub, Proxym, StratifyAI.

Заметки: `05`–`17`.

### Этап 2: Интеграция с Pi

Выяснилось, что Pi Coding Agent **не запрашивает** `/v1/models` автоматически — он читает провайдеров из `~/.pi/agent/models.json`. Провайдер с шлюзом нужно добавлять явно, с полями `contextWindow`, `maxTokens`, `cost`, `reasoning`.

Заметки: `08`, `24`.

### Этап 3: Авто-генерация `models.json`

Обнаружено ключевое ограничение: `/v1/models` в большинстве шлюзов отдаёт только `id` и `object`. Для полного `models.json` нужны дополнительные источники метаданных. Найдены Pi-расширения: `pi-openai-api-models-sync`, `pi-model-discovery`, `pi-provider-litellm`, `pi-diy-provider`, `@haukuen/auto-models`.

Заметки: `25`, `26`.

### Этап 4: Model Discovery в LiteLLM

LiteLLM умеет динамически запрашивать список моделей у провайдера через wildcard-конфигурацию и `check_provider_endpoint: true`. Однако для **кастомных** OpenAI-совместимых провайдеров эта функция не работает (открытый issue #20064).

Заметки: `06`, `07`.

### Этап 5: Лёгкие альтернативы

Поиск single-binary решений: `femtollm`, `ldrouter`, `llmproxy`, `nanollm`, `@khanglvm/llm-router`, `Manifest LLM Gateway`, `llm-conduit`, `vanex-lite`, `local-llm-router`.

Заметки: `14`, `15`, `16`.

### Этап 6: Перепроверка кандидатов

Повторная проверка списка из этапа 1 по четырём критериям (auto-discovery, кастомные OpenAI, fallback, метаданные). Выяснилось, что **Aurora OSS** — единственный, кто явно удовлетворяет всем четырём; **Ferro Labs** — близок, но не имеет отдельного типа `custom_openai`.

Заметки: `03`, `04`, `10`–`13`.

### Этап 7: Декомпозиция на независимые компоненты

Задача разделена на **шесть независимых компонентов**, каждый из которых можно заменить отдельным инструментом:

1. Auto-discovery моделей.
2. Обогащение данных (цены, contextWindow, maxTokens).
3. Поддержка any OpenAI-compatible service.
4. Роутинг и fallback.
5. Передача данных в харнесс.
6. Отслеживание стоимости и токенов.

Заметки: `01`, `02`, `18`–`23`.

## Структура заметок

### Секция 1: Методология и архитектура

- `01.component-architecture.md` — декомпозиция задачи на шесть компонентов.
- `02.architecture-approaches.md` — три подхода к генерации `models.json`.
- `03.tool-selection-matrix.md` — матрица выбора по четырём критериям.
- `04.tool-recheck-aurora-ferro.md` — повторная проверка кандидатов.

### Секция 2: Шлюзы

- `05.litellm-proxy.md` — LiteLLM Proxy: настройка, fallback, кастомные цены.
- `06.litellm-model-discovery.md` — Model Discovery через wildcard.
- `07.litellm-custom-provider-discovery-issue.md` — ограничение для кастомных провайдеров.
- `08.litellm-pi-integration.md` — подключение LiteLLM к Pi.
- `09.portkey-gateway.md` — Portkey AI Gateway.
- `10.aurora-oss.md` — Aurora OSS: обзор.
- `11.aurora-oss-setup-guide.md` — Aurora OSS: пошаговая настройка.
- `12.ferro-labs-gateway-setup.md` — Ferro Labs: настройка, установка бинарника.
- `13.ferro-labs-custom-provider.md` — Ferro Labs: произвольный OpenAI-совместимый провайдер через `BASE_URL` override.
- `14.manifest-gateway-setup.md` — Manifest LLM Gateway.
- `15.llmproxy-lordraw77-setup.md` — llmproxy (lordraw77).
- `16.lightweight-gateways-model-discovery.md` — обзор лёгких шлюзов с Model Discovery.
- `17.alternatives.md` — 9Router, OpenHinge, Routerly, LLM Router, llm-proxy, Petsitter.

### Секция 3: Обогащение цен и метаданных

- `18.pricing-custom-logic.md` — кастомная логика получения цен.
- `19.pricing-enrichment-tools.md` — llmux, claudescope, genai-prices, openai-cost-calculator.
- `20.cost-tracking-tools.md` — inferrail, tracetokens, @bryxen/pulse, OngoingAI.
- `21.kosha-discovery-enrichment.md` — kosha-discovery.
- `22.routehub-enrichment.md` — RouteHub (Swarms).
- `23.pi-model-metadata-enrichment-tools.md` — инструменты обогащения для Pi.

### Секция 4: Интеграция с Pi

- `24.pi-models-json-schema.md` — справочник по схеме `models.json`.
- `25.pi-models-auto-generation.md` — расширения для авто-генерации.
- `26.pi-openai-api-models-sync-setup.md` — пошаговая настройка.

## Ключевые находки

### Шлюзы

| Инструмент | Auto-discovery | Кастомные OpenAI | Fallback | Метаданные | Лёгкость |
|---|---|---|---|---|---|
| **Aurora OSS** | ✅ env-var discovery | ✅ 14 provider types | ✅ 5xx/429 | ✅ cost tracking | Go, single binary |
| **Ferro Labs** | ✅ DiscoveryProvider | ⚠️ BASE_URL override | ✅ 4 стратегии | ⚠️ не подтверждено | Go, single binary |
| **Manifest** | ✅ dynamic catalogs | ✅ any custom endpoint | ✅ до 5 fallback | ✅ `?cost=true` | Docker |
| **llmproxy** | ✅ multi-model | ✅ any OpenAI-compatible | ✅ automatic failover | ⚠️ частично | Flask |
| **LiteLLM** | ⚠️ не для кастомных | ✅ custom_openai | ✅ цепочки | ✅ `/model/info` | Python, тяжёлый |

### Подходы к `models.json`

1. **CLI-скрипт** (`@seqyuan/pimodel`, `xsync-cli`) — ручной запуск или cron.
2. **Pi-расширение** (`pi-openai-api-models-sync`, `pi-model-discovery`, `better-custom-provider`) — авто при старте Pi.
3. **Sidecar-прокси** (llmux, kosha-discovery) — обогащённый `/v1/models`.

### Ключевое ограничение

Стандартный `/v1/models` возвращает только `id` и `object`. Для полного `models.json` нужны внешние источники метаданных: Sub2API metadata repository, LiteLLM cost map, models.dev, kosha-discovery.

## Рекомендации

### Минимальная конфигурация

**Aurora OSS** (шлюз + auto-discovery + fallback + cost tracking) + **`pi-openai-api-models-sync`** (Pi-расширение с enrichment из Sub2API). Покрывает все шесть компонентов.

### Максимальная гибкость

**Ferro Labs** (лёгкий шлюз, single binary) + **kosha-discovery** (discovery + enrichment) + **llmux** (cost tracking + route-aware pricing) + собственный sidecar для Pi. Каждый компонент заменяем.

### Альтернатива для максимальной лёгкости

**Ferro Labs** + **`@brglng/pi-model-discovery`** с ручными overrides метаданных в `models.json`. Минимум зависимостей, но требует ручного заполнения `cost`/`contextWindow`.

## Источники

### Шлюзы

- [LiteLLM GitHub](https://github.com/BerriAI/litellm/)
- [LiteLLM Model Discovery](https://docs.litellm.ai/docs/proxy/model_discovery)
- [LiteLLM Custom Provider Discovery Issue #20064](https://github.com/BerriAI/litellm/issues/20064)
- [Portkey AI Gateway Docs](https://portkey.ai/docs)
- [Aurora OSS — Docker Hub](https://hub.docker.com/r/aurorahq/aurora)
- [Ferro Labs — Quickstart](https://docs.ferrolabs.ai/getting-started/quickstart/)
- [Ferro Labs — Provider Configuration](https://docs.ferrolabs.ai/providers/configuration/)
- [Manifest LLM Gateway](https://manifest.build/llm-gateway/docs/introduction/)
- [llmproxy — GitHub](https://github.com/lordraw77/llmproxy)

### Обогащение

- [llmux — GitHub](https://github.com/vul-os/llmux)
- [kosha-discovery — npm](https://www.npmjs.com/package/@sriinnu/kosha-discovery)
- [RouteHub — GitHub](https://github.com/The-Swarm-Corporation/RouteHub)
- [openai-cost-calculator — PyPI](https://pypi.org/project/openai-cost-calculator/)

### Pi Coding Agent

- [Pi Coding Agent — Models Configuration](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/models.md)
- [pi-openai-api-models-sync — GitHub](https://github.com/riverscn/pi-openai-api-models-sync)
- [@brglng/pi-model-discovery — GitHub](https://github.com/brglng/pi-model-discovery)
- [pi-provider-litellm — pi.dev](https://pi.dev/packages/pi-provider-litellm)

## Соглашения

- Секции пронумерованы в логическом порядке: методология → шлюзы → обогащение → интеграция с Pi.
- Каждый файл — самостоятельная заметка; перекрёстные ссылки указываются как `NN.filename.md`.
- Источники указываются в формате `[title](url)` в конце каждой заметки.
