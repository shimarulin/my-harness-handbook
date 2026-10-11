# Обзор существующих инструментов для построения model-harness bridge

## Назначение документа

Этот документ фиксирует результаты поиска готовых решений и компонентов, которые можно использовать как части или основу для инструмента, описанного в обсуждении:

- **Обнаружение (discovery):** опрос OpenAI-совместимых API и других источников для получения списка доступных моделей.
- **Обогащение (enrichment):** дополнение данных информацией о контекстном окне, возможностях, цене за вход и выход токенов.
- **Сохранение в промежуточный формат:** приведение данных к стабильному внутреннему представлению.
- **Компиляция под harness:** генерация конфигурации для конкретного harness через плагины.

Ниже перечислены инструменты, которые закрывают отдельные части этого пайплайна, а также расширения и плагины, которые можно использовать как основу для плагинов harness-ов.

---

## Блок 1: Ядро — Обнаружение и инвентаризация моделей

Этот блок отвечает за опрос OpenAI-совместимых эндпоинтов и составление списка доступных моделей.

### llm-discovery

**Назначение:** Python-инструмент для мониторинга доступных моделей в реальном времени через OpenAI, Google AI Studio/Vertex AI и Anthropic. Работает без API-ключей (использует предсобранные данные возрастом до 24 часов), поддерживает обнаружение изменений и экспорт в JSON, CSV, YAML, Markdown и TOML.

**Релевантные компоненты:**
- CLI-команды `llm-discovery update`, `llm-discovery list`, `llm-discovery export --format json`.
- Обнаружение изменений (`--detect-changes`) — отслеживание добавления и удаления моделей.
- Python API для использования как библиотеки.

**Ссылка:** [llm-discovery (PyPI)](https://pypi.org/project/llm-discovery/)

### Kosha Discovery

**Назначение:** реестр обнаружения моделей и провайдеров для LLM-приложений. Опрашивает 45+ провайдеров и локальных рантаймов, находит API-ключи в переменных окружения и CLI-инструментах, обогащает модели данными о ценах и лимитах контекста из `models.dev` и LiteLLM.

**Релевантные компоненты:**
- CLI-команды `kosha discover`, `kosha list`, `kosha model`, `kosha routes`, `kosha cheapest`, `kosha refresh`.
- Стабильный манифест `~/.kosha/registry.json` — готовый промежуточный формат.
- Библиотека, HTTP API, OpenAI-совместимый прокси и MCP-сервер.

**Ссылка:** [Kosha Discovery (npm)](https://www.npmjs.com/package/@sriinnu/kosha-discovery) · [Kosha Discovery (GitHub)](https://github.com/sriinnu/kosha-discovery)

### Starmap

**Назначение:** версионированный каталог AI-моделей, доступный как Go-пакет, CLI-инструмент и HTTP-сервер с REST и SSE. Объединяет данные из API провайдеров и сообщества (`models.dev`), поддерживает многоисточниковую реконсиляцию и событийные обновления.

**Релевантные компоненты:**
- CLI-команды для синхронизации и экспорта каталога.
- Событийные хуки (`ModelAddedHook`, `ModelUpdatedHook`, `ModelRemovedHook`) — готовый механизм для реакции на изменения.
- Кэширование и гибкое хранение (in-memory, persistent).

**Ссылка:** [Starmap (pkg.go.dev)](https://pkg.go.dev/github.com/agentstation/starmap) · [Starmap (GitHub)](https://github.com/agentstation/starmap)

---

## Блок 2: Обогащение — Метаданные, цены и возможности

Здесь собраны инструменты и библиотеки, которые добавляют к «сырым» данным о моделях информацию о ценах, контекстных окнах и поддерживаемых функциях.

### llm-registry

**Назначение:** Python-пакет и CLI-инструмент для управления метаданными моделей (цены, контекст, поддержка tools/vision) с единым интерфейсом. Предоставляет CLI `llmr` для взаимодействия с реестром из терминала.

**Релевантные компоненты:**
- CLI-команды `llmr list`, `llmr get`, `llmr add`, `llmr update`, `llmr delete`.
- Python API для интеграции в код.
- Встроенный реестр с 100+ моделями и локальное хранилище для кастомных конфигураций.
- Отслеживание цен за вход/выход токенов, кэшированных цен и лимитов контекстного окна.

**Ссылка:** [llm-registry (PyPI)](https://pypi.org/project/llm-registry/) · [llm-registry (GitHub)](https://github.com/yamanahlawat/llm-registry)

### llm-providers-list

**Назначение:** библиотека, которая хранит курируемый JSON с информацией о моделях и компилирует его в Rust-крейт для доступа с нулевой задержкой. Данные встраиваются на этапе компиляции, что исключает сетевые запросы и I/O во время выполнения.

**Релевантные компоненты:**
- Rust-крейт с типизированными структурами (Provider, Model).
- Python-биндинги через PyO3 (`pip install llm-providers-list`).
- Включает цены, длину контекста и флаги поддержки инструментов для OpenAI, Anthropic, DeepSeek и других.

**Ссылка:** [llm-providers-list (PyPI)](https://pypi.org/project/llm-providers-list/) · [llm_providers (docs.rs)](https://docs.rs/llm_providers/)

### llm-aggregator

**Назначение:** комплексный сервис-агрегатор для обнаружения, обогащения и каталогизации LLM от множества локальных бэкендов. Использует настраиваемую «мозговую» LLM для интеллектуального обогащения метаданных (семейство, контекст, квантование, возможности).

**Релевантные компоненты:**
- AI-Powered Enrichment: использует «мозговую» LLM для заполнения пробелов в данных.
- Web-каталог для просмотра коллекции моделей с фильтрацией и сортировкой.
- REST API для программного доступа к данным.
- Работает с любым LLM-сервером, реализующим OpenAI-совместимый `/v1/models` API.

**Ссылка:** [llm-aggregator (PyPI)](https://pypi.org/project/llm-aggregator/)

### models.dev

**Назначение:** открытая база данных спецификаций AI-моделей, цен и возможностей. Содержит как провайдер-агностичные метаданные, так и данные о конкретных провайдерах.

**Релевантные компоненты:**
- JSON-endpoint `https://models.dev/catalog.json` для получения полного каталога.
- Провайдер-агностичные метаданные (название, семейство, дата выпуска, knowledge cutoff).

**Ссылка:** [models.dev](https://models.dev)

### @kud/models-dev-cli

**Назначение:** CLI для исследования и запросов к каталогу `models.dev` (неинтерактивный и интерактивный TUI).

**Релевантные компоненты:**
- Интерактивный split-pane TUI с детальной информацией о модели, ценах и лимитах.
- Неинтерактивный режим с JSON-выводом для скриптов.
- Фильтрация по провайдеру, поддержке tool calling и reasoning.

**Ссылка:** [@kud/models-dev-cli (npm)](https://www.npmjs.com/package/@kud/models-dev-cli)

---

## Блок 3: Генерация конфигураций для Harness-ов

Инструменты, которые преобразуют промежуточный формат в конфигурацию для конкретного harness-а.

### everyharness

**Назначение:** генератор плагинов для разных harness-ов (Claude Code, Codex, Gemini CLI, Cursor, Copilot CLI, OpenCode, Pi и других) из одного конфигурационного файла `everyharness.yaml`. Поддерживает 11 адаптеров, покрывающих 12 harness-ов.

**Релевантные компоненты:**
- Команды `everyharness init`, `everyharness import`, `everyharness generate`, `everyharness validate`, `everyharness matrix`, `everyharness test`.
- Генерация нативных манифестов плагинов, bootstrap-обвязки, документации и тестов.
- `everyharness validate` проверяет drift в CI.

**Ссылка:** [everyharness (npm)](https://www.npmjs.com/package/everyharness) · [everyharness (GitHub)](https://github.com/prime-radiant-inc/everyharness)

### harness-compile

**Назначение:** компилирует единый `harness.yaml` в нативные файлы конфигурации для Claude Code, Cursor и GitHub Copilot. Поддерживает детерминированную кросс-инструментальную компиляцию, генерацию MCP-серверов и безопасное обновление с маркерами.

**Релевантные компоненты:**
- Генерация нативных инструкций для Claude Code, Cursor и GitHub Copilot.
- Генерация `.mcp.json`, `.cursor/mcp.json`, `.vscode/mcp.json` из секции `mcp-servers`.
- Флаги `--target`, `--dry-run`, `--clean`, `--verbose`.

**Ссылка:** [harness-compile (skills.rest)](https://skills.rest/skill/harness-compile)

### harnage

**Назначение:** инструмент, который по текстовому описанию создаёт полноценный TypeScript-харнесс. Генерирует кастомный системный промпт, инструменты, slash-команды и навыки с использованием build brain и цикла compile-and-repair.

**Релевантные компоненты:**
- Команда `harnage init "<what you want>"` — превращает промпт в компилируемый TypeScript-харнесс.
- Референсный харнесс с goal-driven loop engine, 9 инструментами, sandboxed bash, контекстной компакцией и долговременной памятью.
- Поддержка MCP dual-mode (сервер и клиент).

**Ссылка:** [harnage (npm)](https://www.npmjs.com/package/harnage) · [harnage (GitHub)](https://github.com/PDgit12/harnage)

---

## Блок 4: Расширения и плагины для существующих Harness-ов

Готовые плагины, которые можно использовать как референс или как часть инструмента для поддержки конкретных harness-ов.

### Для Pi (Coding Agent)

#### pi-openai-api-models-sync

**Назначение:** расширение для Pi, которое при старте находит все OpenAI-совместимые провайдеры в `~/.pi/agent/models.json`, запрашивает `/models` с их аутентификацией, получает метаданные о ценах и возможностях из внешнего источника и регистрирует модели через `pi.registerProvider()`.

**Релевантные компоненты:**
- Пересечение доступных ID моделей с метаданными о контекстных окнах, лимитах вывода, входных модальностях, ценах и уровнях рассуждений.
- Регистрация моделей в конкретном harness (Pi).

**Ссылка:** [pi-openai-api-models-sync (Pi)](https://pi.dev/packages/pi-openai-api-models-sync)

#### cpa-provider

**Назначение:** расширение для Pi, которое читает OpenAI-совместимый endpoint `/v1/models`, регистрирует возвращённые модели в Pi и обогащает известные ID моделей данными о контекстных лимитах, поддержке рассуждений, вводе изображений и лимитах вывода из встроенного каталога моделей Pi.

**Релевантные компоненты:**
- Обогащение из встроенного каталога без дополнительных сетевых запросов.
- Консервативные значения по умолчанию для неизвестных ID (128K контекста, 16K вывода, только текст).

**Ссылка:** [cpa-provider (Pi)](https://pi.dev/packages/cpa-provider)

#### pi-diy-provider

**Назначение:** расширение для Pi, которое позволяет создавать кастомные API-провайдеры без ручного редактирования JSON. Записывает определения провайдеров и моделей в `~/.pi/agent/models.json`, обновляет реестр моделей Pi и безопасно перезагружает runtime расширения.

**Релевантные компоненты:**
- Интерактивные команды `/provider-add` и `/provider-model-sync`.
- Поддержка OpenAI Chat Completions, OpenAI Responses, Anthropic Messages и Google Generative AI.

**Ссылка:** [pi-diy-provider (Pi)](https://pi.dev/packages/pi-diy-provider)

#### pi-sync-models

**Назначение:** расширение для Pi, которое синхронизирует ID моделей OpenAI-совместимых провайдеров в `models.json` с интеллектуальным выводом контекстного окна, обновлением возможностей и безопасным удалением устаревших моделей.

**Релевантные компоненты:**
- Вывод контекстного окна и возможностей на основе встроенного каталога Pi и эвристик.
- Безопасное удаление моделей, исчезнувших из upstream endpoint.

**Ссылка:** [pi-sync-models (Pi)](https://pi.dev/packages/pi-sync-models)

#### pi-models-discovery

**Назначение:** расширение для Pi, которое обнаруживает модели через `{baseUrl}/models` для провайдеров, помеченных `discoverModels` в `models.json`. После первого успешного обнаружения список моделей кэшируется.

**Релевантные компоненты:**
- Интерактивная конфигурация через `/config:model-discovery`.
- Поддержка локальных и self-hosted LLM-прокси (Ollama, vLLM, LM Studio).

**Ссылка:** [pi-models-discovery (Pi)](https://pi.dev/packages/pi-models-discovery)

#### pi-model-discovery

**Назначение:** расширение для Pi, которое обнаруживает модели провайдеров, обогащает метаданные, кэширует результаты и динамически регистрирует их через `pi.registerProvider()`.

**Релевантные компоненты:**
- Поддержка OpenAI-совместимых, Ollama, Anthropic-совместимых, LM Studio и llama.cpp каталогов.
- Кэширование и фоновая синхронизация.

**Ссылка:** [pi-model-discovery (GitHub, MasuRii)](https://github.com/MasuRii/pi-model-discovery) · [pi-model-discovery (npm)](https://www.npmjs.com/package/pi-model-discovery)

#### pi-live-models

**Назначение:** расширение для Pi, которое обеспечивает «живое» обнаружение моделей через `/v1/models` для любого OpenAI-совместимого или Anthropic-шлюза. Обновляет список моделей при каждом открытии `/model`.

**Релевантные компоненты:**
- Config-driven filters (glob, regex, field-level rules).
- Metadata merge ladder: defaults < static definitions < live endpoint hints < public catalog < overrides.
- Credential reuse и offline cache.

**Ссылка:** [pi-live-models (npm)](https://www.npmjs.com/package/pi-live-models) · [pi-live-models (Pi)](https://pi.dev/packages/pi-live-models)

#### pi-models-metadata

**Назначение:** расширение для Pi, которое дополняет метаданные сторонних моделей из каталогов `pi.dev` и `models.dev`, регистрирует провайдерские модели с обогащением метаданных.

**Релевантные компоненты:**
- Обновление ID моделей, отображаемых имён, контекстного окна, максимального вывода, поддержки reasoning и цен.
- Кэширование на 1 час по умолчанию.

**Ссылка:** [pi-models-metadata (npm)](https://www.npmjs.com/package/pi-models-metadata)

#### @maheidem/model-discovery

**Назначение:** интерактивный TUI-плагин для Pi, который обнаруживает и управляет локальными AI-endpoint-ами (llama.cpp, oMLX, Ollama, vLLM, SGLang, LM Studio и любой OpenAI-совместимый сервер).

**Релевантные компоненты:**
- Чтение реальных конфигураций, сообщаемых сервером (контекстное окно, max tokens, флаги рассуждений, входные модальности).
- Сохранение провайдеров в `~/.pi/agent/model-discovery.json`.

**Ссылка:** [@maheidem/model-discovery (GitHub)](https://github.com/Maheidem/model-discovery) · [@maheidem/model-discovery (npm)](https://www.npmjs.com/package/@maheidem/model-discovery)

#### pi-model-manager

**Назначение:** TUI-расширение для Pi для управления провайдерами и моделями с нативным сохранением в `models.json`, профилями заголовков запросов, прокси-маршрутизацией и совместимостью протоколов.

**Релевантные компоненты:**
- Единый источник правды — `models.json`.
- Визуальное редактирование моделей и провайдеров.

**Ссылка:** [pi-model-manager (GitHub)](https://github.com/Qihuanxishini/pi-model-manager)

### Для OpenCode

#### opencode-models-discovery

**Назначение:** универсальный плагин для OpenCode для динамического обнаружения моделей у любого OpenAI-совместимого провайдера. Обнаруживает модели через `/v1/models` и автоматически добавляет их в конфигурацию провайдера OpenCode.

**Релевантные компоненты:**
- Обнаружение моделей из любого OpenAI-совместимого провайдера (LM Studio, Ollama, LocalAI, шлюзы).
- Настройка через `plugin` array в `opencode.json` с поддержкой фильтрации провайдеров и моделей.
- Кэширование с TTL.

**Ссылка:** [opencode-models-discovery (npm)](https://www.npmjs.com/package/opencode-models-discovery) · [opencode-models-discovery (GitHub)](https://github.com/yuhp/opencode-models-discovery)

#### opencode-model-scout

**Назначение:** плагин для OpenCode, который автоматически обнаруживает модели и обогащает их размерами контекстного окна, флагами возможностей и метаданными. Поддерживает Atlas, Ollama, oMLX, vLLM, TGI, SGLang, LM Studio, KoboldCpp, llama.cpp и LocalAI.

**Релевантные компоненты:**
- Трёхуровневый пайплайн обогащения метаданных: discovery + keyword categorization → provider-specific probes → models.dev fallback.
- Пробинг провайдерских API для получения авторитетных метаданных.

**Ссылка:** [opencode-model-scout (npm)](https://www.npmjs.com/package/opencode-model-scout) · [opencode-model-scout (GitHub)](https://github.com/rmk40/opencode-model-scout)

#### opencode-autodiscover

**Назначение:** плагин для OpenCode, который обнаруживает модели от локальных OpenAI-совместимых endpoint-ов и загружает метаданные (контекст, стоимость) из `Models.dev` и OpenRouter.

**Релевантные компоненты:**
- Загрузка метаданных из Models.dev и OpenRouter (контекстное окно, возможности, стоимость).
- Кэширование метаданных с 24-часовым TTL.
- Поддержка нескольких endpoint-ов с фильтрацией моделей.

**Ссылка:** [opencode-autodiscover (npm)](https://www.npmjs.com/package/opencode-autodiscover)

### Для DeepSeek Harness (dsh)

#### dsh-llm-discovery

**Назначение:** плагин для DeepSeek Harness, который предоставляет endpoint-пробинг моделей и каталог-сервис `models.dev` для других плагинов.

**Релевантные компоненты:**
- Пробинг локальных и удалённых endpoint-ов (Ollama, LM Studio, llama.cpp, LiteLLM, OpenAI-совместимые шлюзы).
- Кэширование каталога `models.dev` в `$DSH_HOME/storages/llm_models_dev_catalog.json`.

**Ссылка:** [dsh-llm-discovery (npm)](https://www.npmjs.com/package/dsh-llm-discovery) · [DeepSeek Harness model discovery plugins (GitHub)](https://github.com/Decrabbityyy/dsh-discovery)

#### dsh-client-ui-settings-discovery

**Назначение:** UI-плагин для DeepSeek Harness, который добавляет в веб-настройки страницу «Модель discovery» с двумя зонами: endpoint-пробинг и adoption провайдеров, а также управление динамической маршрутизацией.

**Релевантные компоненты:**
- Интерактивное обнаружение моделей через веб-интерфейс.
- Зависимость от `dsh-llm-discovery` для каталог-сервиса.

**Ссылка:** [dsh-client-ui-settings-discovery (npm)](https://www.npmjs.com/package/dsh-client-ui-settings-discovery)

#### dsh-model-sync

**Назначение:** плагин для DeepSeek Harness, который поддерживает каталог моделей маршрутов провайдера `llm-pi-ai` в актуальном состоянии относительно шлюза `pi.dev`.

**Релевантные компоненты:**
- Add-only, change-only запись — новые модели добавляются, существующие обновляются, неизменённые маршруты не трогаются.
- Планируемое обновление по интервалу.

**Ссылка:** [dsh-model-sync (GitHub, fan56)](https://github.com/fan56/dsh-model-sync)

#### dsh-openrouter-providers

**Назначение:** плагин для DeepSeek Harness, который настраивает список провайдеров и ограничения квантования для запросов через OpenRouter. Инжектирует `provider.only` / `provider.order` / `provider.quantizations` в запросы ко всем моделям OpenRouter.

**Релевантные компоненты:**
- Конфигурация через веб-интерфейс DSH (страница «Плагины»).
- Персистентное хранение в `$DSH_HOME/openrouter-providers.json`.
- Инжекция параметров маршрутизации в запросы.

**Ссылка:** [dsh-openrouter-providers (npm)](https://www.npmjs.com/package/dsh-openrouter-providers) · [dsh-openrouter-providers (GitHub)](https://github.com/MoRanYue/dsh-openrouter-providers)

#### dsh-codebuddy

**Назначение:** неофициальный плагин-провайдер для DeepSeek Harness, который подключает CodeBuddy (Tencent) к DSH. Поддерживает WorkBuddy API Key и CodeBuddy China login token.

**Релевантные компоненты:**
- Автоматическое получение списка доступных моделей от CodeBuddy.
- Управление моделями через WebUI (редактирование ID, имени, контекстного окна, лимитов вывода).
- Поддержка двух режимов аутентификации.

**Ссылка:** [dsh-codebuddy (GitHub)](https://github.com/zhang-tod/dsh-codebuddy) · [dsh-llm-codebuddy (dshbase)](https://dshbase.com/zh/plugins/dsh-llm-codebuddy/)

#### dsh-commandcode-provider

**Назначение:** неофициальный плагин-провайдер для DeepSeek Harness, который подключает Command Code к DSH. Порт `pi-commandcode-provider` на плоскость DSH LLM seam.

**Релевантные компоненты:**
- Регистрация провайдера commandcode на `ctx.llm` с живым каталогом моделей.
- Поддержка reasoning effort, image input, web search и multi-account.
- Офлайн-кэш каталога моделей в `<dsh home>/commandcode/commandcode-models.json`.

**Ссылка:** [dsh-commandcode-provider (npm)](https://www.npmjs.com/package/dsh-commandcode-provider) · [dsh-commandcode-provider (GitHub)](https://github.com/Mars-Sea/dsh-commandcode-provider)

### litellm-controller (litellmctl)

**Назначение:** TUI-инструмент для управления LiteLLM Proxy: модели, группы маршрутизации, метаданные (цены и контекстные окна). Позволяет генерировать JSON с ценами и контекстными окнами и экспортировать его для CI/CD.

**Релевантные компоненты:**
- Управление метаданными моделей (цены, контекстные окна).
- Неинтерактивный экспорт через `litellmctl metadata-gen`.

**Ссылка:** [litellm-controller (PyPI)](https://pypi.org/project/litellm-controller/)

---

## Заключение

Анализ показал, что экосистема уже насыщена готовыми компонентами. **Нет необходимости создавать всё с нуля.** Уникальная ценность оригинального инструмента может заключаться не в изобретении каждого колеса, а в **сборке** этих частей в единый, универсальный и расширяемый инструмент.

**Ключевая идея — разделение ядра (абстрактный провайдер → абстрактный harness) и плагинов — полностью реализуема на базе существующих решений.**

### Рекомендуемая стратегия

1. **Ядро:** взять за основу логику `@sriinnu/kosha-discovery` или `starmap` для сбора и хранения данных.
2. **Обогащение:** использовать библиотеки вроде `llm-registry` или `llm-providers-list` для добавления метаданных.
3. **Плагины провайдеров:** реализовать через адаптеры, вдохновляясь примерами `pi` и `dsh`.
4. **Плагины harness-ов:** взять за образец архитектуру `everyharness` или `harness-compile` для генерации конфигураций.

Такой подход позволит сосредоточиться на создании **универсального моста** между провайдерами и harness-ами, используя лучшее из существующих наработок.

### Сводная таблица компонентов

| Компонент | Роль | Ссылка |
|---|---|---|
| llm-discovery | Обнаружение (OpenAI, Google, Anthropic) | [PyPI](https://pypi.org/project/llm-discovery/) |
| Kosha Discovery | Обнаружение + обогащение (45+ провайдеров) | [npm](https://www.npmjs.com/package/@sriinnu/kosha-discovery) |
| Starmap | Каталог моделей (Go, CLI, HTTP) | [pkg.go.dev](https://pkg.go.dev/github.com/agentstation/starmap) |
| llm-registry | Обогащение (цены, контекст, возможности) | [PyPI](https://pypi.org/project/llm-registry/) |
| llm-providers-list | Обогащение (Rust/Python, zero-latency) | [PyPI](https://pypi.org/project/llm-providers-list/) |
| llm-aggregator | Обогащение (AI-powered) | [PyPI](https://pypi.org/project/llm-aggregator/) |
| models.dev | Источник метаданных | [models.dev](https://models.dev) |
| @kud/models-dev-cli | CLI для models.dev | [npm](https://www.npmjs.com/package/@kud/models-dev-cli) |
| everyharness | Генерация плагинов для harness-ов | [npm](https://www.npmjs.com/package/everyharness) |
| harness-compile | Компиляция harness.yaml | [skills.rest](https://skills.rest/skill/harness-compile) |
| harnage | Prompt-to-harness builder | [npm](https://www.npmjs.com/package/harnage) |
| pi-live-models | Pi: live discovery | [npm](https://www.npmjs.com/package/pi-live-models) |
| pi-models-metadata | Pi: обогащение из models.dev | [npm](https://www.npmjs.com/package/pi-models-metadata) |
| opencode-models-discovery | OpenCode: discovery | [npm](https://www.npmjs.com/package/opencode-models-discovery) |
| opencode-model-scout | OpenCode: discovery + enrichment | [npm](https://www.npmjs.com/package/opencode-model-scout) |
| opencode-autodiscover | OpenCode: discovery + models.dev | [npm](https://www.npmjs.com/package/opencode-autodiscover) |
| dsh-llm-discovery | DSH: discovery + models.dev | [npm](https://www.npmjs.com/package/dsh-llm-discovery) |
| dsh-model-sync | DSH: синхронизация каталога | [GitHub](https://github.com/fan56/dsh-model-sync) |
| dsh-openrouter-providers | DSH: маршрутизация OpenRouter | [npm](https://www.npmjs.com/package/dsh-openrouter-providers) |
| dsh-codebuddy | DSH: провайдер CodeBuddy | [GitHub](https://github.com/zhang-tod/dsh-codebuddy) |
| dsh-commandcode-provider | DSH: провайдер Command Code | [npm](https://www.npmjs.com/package/dsh-commandcode-provider) |
| litellm-controller | Управление LiteLLM Proxy | [PyPI](https://pypi.org/project/litellm-controller/) |
