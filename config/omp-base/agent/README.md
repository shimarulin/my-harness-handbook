# Oh My Pi Agent

curl https://models.dev/api.json      # с эндпоинтами и метаданными провайдеров
curl https://models.dev/models.json   # метаданные моделей без привязки к провайдеру

Внутренняя рабочая директория агента Oh My Pi.

## Структура директории

| Элемент | Назначение |
|---------|------------|
| `config.yml` | Настройки агента (модель по умолчанию, уровень мышления) |
| `models.yml` | Конфигурация провайдеров и список доступных моделей |
| `agent.db` | Состояние сессий агента (SQLite) |
| `history.db` | История разговоров (SQLite) |
| `models.db` | Метаданные моделей (SQLite) |
| `sessions/` | Хранение активных сессий (по одному каталогу на сессию) |
| `terminal-sessions/` | Записи сессий терминалов (`pts-*`) |
| `.env` | API-ключи и другие переменные окружения |

## Файлы конфигурации

### `config.yml`

```yaml
setupVersion: 1
modelRoles:
  default: kodikrouter/z-ai/glm-5.3-flash
defaultThinkingLevel: auto
```

- `modelRoles.default` — сокращённый идентификатор модели в формате `провайдер/id`; агент разрешает его через `models.yml`.
- `defaultThinkingLevel` — управление режимом мышления (`auto` | `off` | `on`).

### `models.yml`

Определяет провайдеров, их конечные точки и модели, которые они предоставляют. В данный момент настроен один провайдер:

**Провайдер: `kodikrouter`** — `https://api.kodikrouter.ru/v1` (OpenAI-совместимый API).

```yaml
providers:
  kodikrouter:
    baseUrl: https://api.kodikrouter.ru/v1
    apiKey: KODIKROUTER_API_KEY
    api: openai-completions
    auth: apiKey
    authHeader: true
    models:
      # --- DeepSeek ---
      - id: deepseek/deepseek-v4.1-flash
        name: DeepSeek V4.1 Flash
        contextWindow: 1048576
        maxTokens: 384000
        input: [text, image]
        reasoning: true
        cost: { input: 0.1, output: 0.5, cacheRead: 0, cacheWrite: 0 }

      # --- MiniMax ---
      - id: minimax/minimax-m3
        name: MiniMax M3
        contextWindow: 1048576
        maxTokens: 524288
        input: [text, image, video]
        reasoning: true
        cost: { input: 0.3, output: 1.2, cacheRead: 0, cacheWrite: 0 }

      # --- Qwen ---
      - id: qwen/qwen3.8-flash
        name: Qwen 3.8 Flash
        contextWindow: 1000000
        maxTokens: 131072
        input: [text, image, video]
        reasoning: true
        cost: { input: 0.15, output: 0.47, cacheRead: 0, cacheWrite: 0 }

      - id: qwen/qwen3.8-max
        name: Qwen 3.8 Max
        contextWindow: 1000000
        maxTokens: 131072
        input: [text, image, video]
        reasoning: true
        cost: { input: 2.0, output: 6.0, cacheRead: 0, cacheWrite: 0 }

      # --- Kimi ---
      - id: moonshotai/kimi-k2.7-code
        name: Kimi K2.7 Code
        contextWindow: 262144
        maxTokens: 32768                # ← Default to be 32k aka 32768, see https://platform.kimi.ai/docs/guide/kimi-k2-7-code-quickstart
        input: [text, image, video]
        reasoning: true
        cost: { input: 0.7062, output: 3.3, cacheRead: 0, cacheWrite: 0 }

      - id: moonshotai/kimi-k3
        name: Kimi K3
        contextWindow: 1048576
        maxTokens: 131072
        input: [text, image, video]
        reasoning: true
        cost: { input: 3.0, output: 15.0, cacheRead: 0, cacheWrite: 0 }

      # --- GLM ---
      - id: z-ai/glm-5.3-flash
        name: GLM 5.3 Flash
        contextWindow: 1310720
        maxTokens: 131072
        input: [text, image, video]
        reasoning: true
        cost: { input: 0.15, output: 0.5, cacheRead: 0, cacheWrite: 0 }

      - id: z-ai/glm-5.3
        name: GLM 5.3
        contextWindow: 1310720
        maxTokens: 131072
        input: [text]
        reasoning: true
        cost: { input: 0.5614, output: 1.7644, cacheRead: 0, cacheWrite: 0 }
```

### `.env`

Простые пары `КЛЮЧ=ЗНАЧЕНИЕ` (без `export`). OMP читает `.env`-файлы при запуске, проверяя эти места в порядке приоритета (побеждает первый найденный):

1. **Системное окружение** — переменные, экспортированные в shell (`export MWS_GPT_API_KEY=...`).
2. **Проектный `.env`** — `$PWD/.env`, в директории, из которой запущен OMP.
3. **Файл агента OMP** — `~/.omp/agent/.env` (рекомендуется для ключей кастомных провайдеров).
4. **Глобальный OMP** — `~/.omp/.env`.
5. **Домашний `.env`** — `~/.env` (самый низкий приоритет).

В данный момент загружен: `KODIKROUTER_API_KEY` (из `~/.omp/agent/.env`).

## Базы данных

`agent.db`, `history.db`, `models.db` вместе с их WAL/SHM-файлами управляются агентом. Не редактируйте их вручную.
