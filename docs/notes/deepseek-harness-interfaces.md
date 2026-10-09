# DeepSeek Harness: установка и интерфейсы для локального запуска

> Целевая аудитория: разработчики на Linux / macOS, запускающие `dsh` локально.
> Актуально на октябрь 2026. DeepSeek Harness всё ещё находится в стадии
> предрелиза — API и требования могут меняться.

DeepSeek Harness (команда `dsh`) — открытый фреймворк AI-агентов от DeepSeek.
Официально поддерживает два режима: **Web UI** и **CLI**. Десктопные клиенты
и TUI-интерфейсы — это надстройки от сообщества поверх официального рантайма.

---

## 1. Установка официального deepseek-harness

Единственное жёсткое требование — **Node.js**. Точные версии:

| Канал | Требование |
|---|---|
| `package.json` (engines) | `^22.19.0` или `>=24.0.0` |
| CI-валидация | 22.19, 24, 26 |
| Рекомендуется | 22.19+ или 24.x (чётная LTS-линия) |

Официального OS-пакетника (`brew`/`apt`/`winget`) или standalone-бинарника
на момент v0.1 не существует — только `npx`/`npm` и сборка из исходников.

### 1.1. Быстрый запуск через `npx` (без клонирования)

Если нужный Node.js уже активен:

```bash
npx @deepseek-ai/dsh web
```

Web UI поднимется на `http://127.0.0.1:3080`.

### 1.2. Глобальная установка через `npm`

```bash
npm install -g @deepseek-ai/dsh@latest
dsh web
```

### 1.3. Сборка из исходников (для разработки)

```bash
git clone https://github.com/deepseek-ai/deepseek-harness.git
cd deepseek-harness
pnpm install
pnpm run build
pnpm dsh web
```

Требуется `pnpm` 11+.

### 1.4. Фиксация версии Node.js через `mise` (рекомендуемый способ)

Проблема с `nvm` и системным Node: «глобальная» версия может не совпадать с
той, что ожидает `dsh`, а переключение между проектами легко забыть. `mise`
позволяет зафиксировать версию **на уровне проекта** и автоматически
подхватывать её при входе в каталог.

**Установка `mise`:**

```bash
curl https://mise.run | sh
# добавьте в ~/.bashrc / ~/.zshrc:
eval "$(~/.local/bin/mise activate bash)"   # или zsh
```

**Фиксация Node.js для проекта DeepSeek Harness:**

```bash
cd ~/projects/deepseek-harness
mise use node@24
```

`mise` создаст `.mise.toml` (или дополнит существующий):

```toml
[tools]
node = "24"
```

Теперь при входе в этот каталог `mise` автоматически активирует Node 24.
Проверка:

```bash
node --version   # v24.x.x
npx @deepseek-ai/dsh web
```

**Почему это удобно для `dsh`:**

- версия Node зафиксирована в репозитории вместе с кодом;
- не нужно вручную переключаться между проектами с разными требованиями к Node;
- `mise` понимает и `npm`-пакеты: например, можно установить
  `mise use -g npm:dsh-omarchy-agent` для системных утилит.

**Альтернатива — `.nvmrc` + `nvm`:**

```bash
echo "24" > .nvmrc
nvm use
```

Работает, но требует ручного вызова `nvm use` (или хука в shell) и не
управляет другими инструментами (pnpm, Python SDK и т.д.).

### 1.5. Установка `dsh` как глобального инструмента через `mise`

Предыдущий вариант фиксирует версию Node.js **внутри проекта**. Но `dsh`
удобно иметь доступным **из любого каталога** — как системную утилиту.
`mise` умеет и это: команда `mise use -g` записывает инструмент в
глобальный конфиг (`~/.config/mise/config.toml`), и `dsh` попадает в
`PATH` через шимы.

**Ключевой момент:** `dsh` — это npm-пакет, и `mise` устанавливает его
через **npm backend**, но **не добавляет Node.js автоматически**. Если
`node` не объявлен в `[tools]`, `dsh` просто не запустится — ему нужен
рантайм.

**Правильная последовательность:**

```bash
# 1. Глобально ставим Node.js (или фиксируем версию)
mise use -g node@24

# 2. Глобально ставим dsh как npm-пакет
mise use -g npm:@deepseek-ai/dsh

# 3. Убеждаемся, что оба инструмента активны
mise ls --current
# node  24.x.x
# npm:@deepseek-ai/dsh  latest

# 4. dsh теперь доступен из любого каталога
dsh --version
```

**Что происходит «под капотом»:**

- `mise use -g node@24` записывает `node = "24"` в глобальный конфиг и
  создаёт шим `node` в `~/.local/share/mise/shims/`.
- `mise use -g npm:@deepseek-ai/dsh` запускает встроенный пакетный
  менеджер `aube`, который скачивает `@deepseek-ai/dsh` и его
  зависимости в **изолированную директорию** под управлением `mise`
  (не в глобальный `node_modules` активной версии Node.js).
- `mise` создаёт шим `dsh`, который при каждом запуске **резолвит
  активную версию Node.js** через `mise` и использует именно её.
  Это значит: если вы переключите `node` на `22.19.0` — `dsh` будет
  запускаться на `22.19.0`. Если на `24` — на `24`.

**Проверка, что `dsh` использует правильный Node.js:**

```bash
# какой node активен в текущем каталоге
mise which node
# /home/user/.local/share/mise/installs/node/24.x.x/bin/node

# какой node реально использует dsh
head -1 "$(mise which dsh)"
# #!/home/user/.local/share/mise/installs/node/24.x.x/bin/node
```

Шим `dsh` — это скрипт, первой строкой которого является shebang с
путём к **текущему активному** `node`. При переключении версии `mise`
пересоздаёт шимы, и `dsh` автоматически начинает использовать новую
версию.

**Обновление `dsh`:**

```bash
mise upgrade npm:@deepseek-ai/dsh
```

**Важно: `mise` не гарантирует совместимость с требованиями `dsh` к
Node.js.** Если глобально активна версия Node.js, не входящая в
`^22.19.0 || >=24.0.0`, `dsh` может упасть с ошибкой движка. Проверяйте
`node --version` перед запуском.

**Альтернатива: `npm install -g` с активным `mise`-Node.** Если вы
хотите, чтобы `dsh` был привязан к **конкретной** версии Node.js и не
переключался вслед за глобальным `mise use -g node@...`, можно
установить его обычным `npm install -g` при активном `mise`:

```bash
mise use -g node@24
npm install -g @deepseek-ai/dsh
```

В этом случае `dsh` окажется внутри директории Node 24 (`~/.local/share/mise/installs/node/24.x.x/lib/node_modules/`),
а шим `dsh` будет указывать именно на этот Node. При переключении на
другую версию Node.js `dsh` пропадёт из `PATH` — это осознанный
компромисс: стабильность вместо гибкости.

### 1.6. Headless-режим (для скриптов и CI)

Помимо Web UI, `dsh` поддерживает one-shot headless-режим: задача
передаётся аргументом, агент выполняет её и печатает финальный ответ,
после чего процесс завершается. Ни GUI, ни сервера, ни открытых портов —
это делает режим удобным для скриптов, CI-пайплайнов и разовых задач.

```bash
dsh --profile headless "запусти тесты и покажи результат"
npx @deepseek-ai/dsh --profile headless "найди TODO в этом репозитории"
```

Headless-профиль использует те же модели, инструменты и политики
безопасности, что и остальные поверхности; доступен также JSON event
stream (`--json`) для программной обработки событий.

Практические наблюдения сообщества:

- headless-режим удобен для батч-обработки файлов и фоновых задач;
- в headless-режиме нет интерактивных approval-запросов, поэтому
  политика разрешений (`--mode read-only` / `workspace-write`) должна
  быть задана явно;
- при запуске в контейнере/SSH headless часто проще, чем возня с
  Web UI и портами.

### 1.7. Установка через Docker (опционально)

Для изоляции окружения и серверного деплоя сообщество поддерживает
готовые Docker-образы. Официального образа от DeepSeek нет, но есть два
популярных community-варианта:

| Образ | Что внутри | Особенности |
|---|---|---|
| [`smanx/deepseek-harness`](https://hub.docker.com/r/smanx/deepseek-harness) | Официальный `@deepseek-ai/dsh` в Node.js-рантайме | «Из коробки», порт 3080 наружу, данные в volume `dsh-data` |
| [`runzhliu/deepseek-harness`](https://hub.docker.com/r/runzhliu/deepseek-harness) | Пиннингованная версия `@deepseek-ai/dsh` (не `latest`) | Multi-stage build, non-root, Compose-стек и Helm chart для K8s |

Быстрый старт с `smanx/deepseek-harness`:

```bash
docker run -d \
  --name dsh-harness \
  -p 3080:3080 \
  -v dsh-data:/root/.dsh \
  --restart unless-stopped \
  smanx/deepseek-harness
```

Для `runzhliu/deepseek-harness` доступен Compose-стек с volume `dsh-home`
и Helm chart (StatefulSet + PVC). Подходит, если нужно запускать
Harness в Kubernetes или держать несколько изолированных инстансов.

**Важно:** образы community, обновляются с задержкой относительно
официальных релизов; проверяйте тег версии перед продакшн-использованием.

### 1.8. Кастомные провайдеры (OpenAI Compatible API)

`dsh` не привязан к моделям DeepSeek: встроенный каталог покрывает
`anthropic`, `openai`, `moonshotai` (Kimi) и `zai` (GLM), а карточка
**Custom model API** принимает любой OpenAI-совместимый эндпоинт —
OpenRouter, LM Studio, vLLM, корпоративный gateway или self-hosted relay.

**Минимальный набор полей** (через Settings → Models → Add a custom
provider или напрямую в `$DSH_HOME/profiles/<profile>/cordis.patch.yml`):

```yaml
- id: llm-pi-ai
  config:
    providers:
      my-gateway:
        apiKeyEnv: GATEWAY_API_KEY   # имя переменной окружения, не сам ключ
        api: openai-completions      # или openai-responses / anthropic-messages
        baseURL: https://gateway.example/v1
        models:
          - id: legacy-chat
          - id: vision-preview
            input: [text, image]
```

Пять обязательных полей:

- **Provider ID** (lowercase, постоянный — на него ссылаются запросы,
  сессии и credentials; переименовать нельзя, только пересоздать);
- **`baseURL`** — корень эндпоинта, заканчивается на `/v1`;
- **`api`** — протокол: `openai-completions`, `openai-responses` или
  `anthropic-messages` (провайдер говорит на одном протоколе; gateway
  с двумя протоколами = два провайдера);
- **`apiKeyEnv`** — имя env-переменной; сам ключ хранится в
  `$DSH_HOME/.credentials.yaml`, а не в `settings.yaml`;
- **`models`** — хотя бы одна запись с `id`.

Изменения вступают в силу со следующего запроса, рестарт сервера не нужен.

**Совместимость (compat-переключатели)** — самая частая причина отказов.
Неопознанный URL пи-ай адресует как OpenAI, и gateway, отличающийся от
OpenAI хоть в чём-то, отклоняет запросы. Два поля чинят большинство:

```yaml
compat:
  supportsDeveloperRole: false   # не отправлять system prompt как role: "developer"
  maxTokensField: max_tokens     # вместо max_completion_tokens
```

Для reasoning-моделей за OpenAI-совместимым gateway (например, DeepSeek V4
через relay) может понадобиться `compat.thinkingFormat: deepseek`.

**Типичные ошибки** и их решения:

| Ошибка | Причина / решение |
|---|---|
| `MISSING_CREDENTIAL` | Ключ не сохранён через Models page или env-переменная не задана |
| `UNKNOWN_MODEL` | Выбрана модель, не настроенная в провайдере |
| Discovery `/models` возвращает 401 | Неверный ключ; введите модели вручную |
| Gateway отказывает при верном ключе и URL | Форма запроса отличается от OpenAI — попробуйте `compat.supportsDeveloperRole: false` + `compat.maxTokensField: max_tokens` |
| Fails только у reasoning-моделей | Gateway отклоняет developer role — `compat.supportsDeveloperRole: false` |
| Нет Effort-меню у вручную добавленной модели | Модель не объявляет уровни — добавьте `reasoningEfforts` в `cordis.patch.yml` |

Полный справочник по всем compat-переключателям — `PiAiCompatProfile`
в сгенерированном конфиг-каталоге `dsh-llm-pi-ai`.

---

## 2. Интерфейсы TUI

TUI для `dsh` — это не один проект, а несколько конкурирующих плагинов.
Все они запускаются поверх официального рантайма и рендерят интерфейс
прямо в терминале.

| Пакет | Установка | Особенности |
|---|---|---|
| [`deepseek-harness-tui`](https://www.npmjs.com/package/deepseek-harness-tui) | `dsh plugin --profile tui add deepseek-harness-tui` | Рендерит в **основной экран** терминала (без alternate screen) — история остаётся в scrollback. Работает в том же процессе, что и агент |
| [`@nexlineai/dsh-tui`](https://www.npmjs.com/package/@nexlineai/dsh-tui) | `npx @nexlineai/dsh-tui` | Полноэкранный TUI, «Web UI, переосмысленный для терминала». Кросс-платформенный (iTerm2, Terminal.app, kitty, alacritty, xterm) |
| [`@brianynwu/dsh-tui`](https://www.npmjs.com/package/@brianynwu/dsh-tui) | `dsh plugin add @brianynwu/dsh-tui` | Out-of-tree плагин поверх официального `@deepseek-ai/dsh-base`, использует `pi-tui` для рендеринга |
| [`papachong/deepseek-harness-tui`](https://github.com/papachong/deepseek-harness-tui) | См. README | Standalone-терминал на OpenTUI (SolidJS), поддерживает потоковый markdown |

**Практический выбор:** если вы живёте в терминале и не хотите держать
браузер открытым — `deepseek-harness-tui` (сохраняет историю) или
`@nexlineai/dsh-tui` (полноэкранный). Для быстрого «попробовать» хватит
`npx @nexlineai/dsh-tui`.

---

## 3. Десктопные клиенты для Linux

**Официальный десктопный клиент DeepSeek Harness для Linux не выпущен.**
На октябрь 2026 официально доступны только macOS и Windows, Linux-версии
нет. Для Linux рекомендуется запуск через `@deepseek-ai/dsh`
в npm.

Однако сообщество поддерживает несколько неофициальных Linux-сборок:

| Проект | Форматы | Комментарий |
|---|---|---|
| [`dsh-tauri/deepseek-harness-desktop`](https://github.com/dsh-tauri/deepseek-harness-desktop) | `.AppImage`, `.deb` (Ubuntu 22.04+) | Кроссплатформенное Tauri-приложение. Есть offline-бандлы (`_Bundle`) для запуска без сети |
| [`ffyfox/dsh-desktop-linux`](https://github.com/ffyfox/dsh-desktop-linux) | AppImage, deb, rpm, PKGBUILD | Портирует официальный Electron-пайплайн упаковки. Явно неофициальный |
| [`Zhou-Yujing114514/deepseek-harness-linux`](https://github.com/Zhou-Yujing114514/deepseek-harness-linux) | AppImage, .deb, .tar.gz (x64/arm64) | «First-class» Linux-упаковка с нативным CI и авто-обновлением AppImage |
| [`lql341/deepseek-harness-linux-desktop`](https://github.com/lql341/deepseek-harness-linux-desktop) | AppImage, deb | Патч-сет для поведения, аналогичного macOS-сборке |
| [`TommyFang2077/dsh-linux-desktop`](https://github.com/TommyFang2077/dsh-linux-desktop) | deb, rpm | Неофициальный Electron-порт, поддерживает системный трей и подписанные обновления |
| [`westanke/dsh-desktop-deepin`](https://github.com/westanke/dsh-desktop-deepin) | deb, AppImage | Сборка для Deepin / UOS / Linux |
| [`wanghongjian0119/deepseek-harness-desktop`](https://github.com/wanghongjian0119/deepseek-harness-desktop) | deb, AppImage | Форк с десктопной оболочкой исключительно для Linux |
| [Snap Store: DSH Desktop (Community)](https://snapcraft.io/dsh-desktop-community) | Snap | Нативная десктопная оболочка для Snap-дистрибутивов |
| [`harness-desktop`](https://www.npmjs.com/package/harness-desktop) | AppImage (через npm) | Пакет-загрузчик: `npm install` скачивает актуальный AppImage с GitHub Releases |

**Важно:** все перечисленные сборки — **неофициальные**. DeepSeek не
поддерживает их и не несёт за них ответственности. Перед установкой
проверяйте источник и подписи релизов.

---

## 4. Нужен ли десктопный клиент?

Короткий ответ: **для локального запуска на Linux — скорее нет, чем да.**
Десктопный клиент имеет смысл только при определённых сценариях.

### Плюсы десктопного клиента по сравнению с Web UI

- **Нативное окно и системный трей.** Не нужно держать вкладку браузера;
  приложение живёт отдельно, можно свернуть в трей.
- **Автозапуск и фоновый режим.** Десктопная оболочка может стартовать
  вместе с системой и держать агента «тёплым».
- **Интеграция с ОС.** Уведомления, ассоциации файлов, drag-and-drop
  рабочей области, интеграция с файловым менеджером (в некоторых сборках).
- **Офлайн-бандлы.** Некоторые сборки (например, `dsh-tauri`) поставляются
  с предупакованным ядром и работают без сети при первом запуске.
- **Меньше зависимостей от браузера.** Не нужно помнить, какой браузер
  открыт, какие расширения блокируют локальные порты и т.д.

### Минусы и риски

- **Неофициальность.** Любая Linux-сборка — это community-проект.
  Обновления, безопасность и совместимость не гарантированы DeepSeek.
- **Задержка обновлений.** Пока сообщество портирует новую версию,
  вы можете оставаться на старой.
- **Дублирование инфраструктуры.** Десктопный клиент — это ещё один
  слой поверх `dsh`; отладка усложняется, если что-то пойдёт не так.
- **Web UI уже решает 95% задач.** Локальный `http://127.0.0.1:3080`
  полностью функционален и обновляется вместе с `dsh`.

### Вердикт

Если вы запускаете `dsh` **локально для разработки или экспериментов** —
Web UI + TUI-плагин закрывают почти все потребности. Десктопный клиент
стоит рассматривать только если вам принципиально нужен нативный оконный
опыт, работа в трее или офлайн-бандл. Для Linux это всегда компромисс:
вы получаете удобство окна, но теряете официальную поддержку и
предсказуемость обновлений.

---

## 5. Комбинации интерфейсов на одной машине

`dsh` — это рантайм, а интерфейсы — это клиенты к нему. На одной машине
можно держать несколько интерфейсов одновременно; они не конфликтуют,
если не занимают один и тот же порт (Web UI по умолчанию `3080`).

### Вариант A: Web UI + TUI-плагин (рекомендуемый для большинства)

**Схема:** один экземпляр `dsh web` на `127.0.0.1:3080` + TUI-плагин,
подключающийся к тому же рантайму.

**Когда использовать:**

- днём — Web UI в браузере для визуальной работы с файлами и настройками;
- в терминале — TUI для быстрых запросов, не переключая контекст;
- `deepseek-harness-tui` рендерит в основной экран, поэтому история
  остаётся в scrollback и не теряется при выходе.

**Установка:**

```bash
# основной рантайм
npx @deepseek-ai/dsh web

# в другом терминале — TUI поверх того же рантайма
npx @nexlineai/dsh-tui
```

### Вариант B: Web UI + десктопный клиент

**Схема:** Web UI для отладки и «тяжёлых» операций + десктопный клиент
для повседневного использования.

**Когда использовать:**

- если десктопный клиент оказался удобнее браузера, но вы не хотите
  терять доступ к Web UI для диагностики;
- десктопный клиент может работать как отдельный процесс, не мешая
  Web UI.

**Внимание:** проверьте, что десктопная сборка не запускает собственный
экземпляр `dsh` на том же порту. Если запускает — либо остановите
`dsh web`, либо укажите другой порт.

### Вариант C: Только TUI

**Схема:** никакого Web UI, только терминальный интерфейс.

**Когда использовать:**

- полностью headless-среда (SSH, контейнер, сервер без GUI);
- вы принципиально не хотите открывать браузер;
- нужен минимальный оверхед по памяти.

```bash
npx @nexlineai/dsh-tui
# или
dsh plugin --profile tui add deepseek-harness-tui
dsh
```

### Вариант D: Web UI + TUI + десктопный клиент (полный стек)

**Схема:** три интерфейса на одной машине, каждый для своей задачи.

**Когда использовать:**

- разработка плагинов или интеграций: Web UI для отладки, TUI для
  быстрых проверок, десктопный клиент для демонстрации конечным
  пользователям;
- тестирование совместимости между интерфейсами.

**Риск:** три процесса, три набора логов, потенциальные конфликты
портов. Имеет смысл только на мощной рабочей станции и при реальной
необходимости.

### Сводная таблица

| Сценарий | Что использовать |
|---|---|
| Локальная разработка, визуальная работа | Web UI (`npx @deepseek-ai/dsh web`) |
| `dsh` из любого каталога, без привязки к проекту | `mise use -g node@24 && mise use -g npm:@deepseek-ai/dsh` |
| Быстрые запросы, не выходя из терминала | TUI (`@nexlineai/dsh-tui` или `deepseek-harness-tui`) |
| Headless / SSH | TUI |
| Нативный оконный опыт, трей | Неофициальный десктопный клиент |
| Отладка плагинов | Web UI + TUI |
| Демонстрация «как приложение» | Десктопный клиент |
| Максимальная гибкость | Web UI + TUI (вариант A) |

---

## 6. Сравнение с Pi Agent (pi.dev)

[Pi](https://pi.dev) — минималистичный terminal-агент от Earendil Works
(Mario Zechner), ~100k звёзд на GitHub. Часто упоминается как «взрослый»
соперник `dsh`, и сравнение имеет занимательный подтекст: DeepSeek Harness
**использует модельный слой Pi** (`pi-ai`) для подключения сторонних
провайдеров, а руководитель Harness-проекта Tianyi Cui публично называл
Pi любимым daily-driver'ом многих в DeepSeek.

### Сводная таблица

| Критерий | DeepSeek Harness (`dsh`) | Pi (`pi`) |
|---|---|---|
| Философия | «Everything is a plugin» на Cordis; заменяем даже agent loop | Минимальное ядро + 4 инструмента (`read`/`write`/`edit`/`bash`), остальное строите сами |
| Архитектура | 53 встроенных инструмента, MCP, subagents, LSP, sandbox, Web UI | Маленький terminal-процесс, расширения через TypeScript extensions |
| Поддержка моделей | ~40 провайдеров через pi-ai (включая сам Pi-слой) | 25+ провайдеров, очень простое переключение; лучше поддержка локальных (Ollama/vLLM) |
| Sandbox | 3 встроенных режима | Нет в ядре |
| Сессии | Append-only траектория + replay | Читаемое session tree (`/tree`), ветвление |
| Benchmarks (Composio, DeepSeek V4 Pro) | 20/30 задач, $0.028/успех, 252.1s медиана | 21/30 задач, $0.031/успех, 362.9s медиана |
| Повседневный запуск | Требует Node.js 22.19+/24+, больше настройки | npm-установка, сразу работает, легко держать в фоне |
| Зрелость | Developer preview, ломающие изменения | Достаточно зрел для ежедневной работы |

### Когда что выбрать

- **Pi** — если нужен маленький, понятный, модель-агностичный агент,
  который легко модифицировать; если много работаете с локальными
  моделями; если важна скорость запуска.
- **`dsh`** — если нужна первоклассная интеграция с DeepSeek-моделями,
  Web UI, встроенный sandbox, subagents, LSP, планировщик; если хотите
  экспериментировать с заменой agent loop и глубоким хуками в Turn/Step
  события (`turn/start`, `system-prompt/assemble`, `tools/pre-execute`).

### Статьи с практическим опытом сравнения

| Материал | Что освещает |
|---|---|
| [DSH vs Pi Agent (Composio, Sep 2026)](https://composio.dev/content/deepseek-harness-vd-pi-agent) | Подробное сравнение: философия, архитектура, benchmark на 30 задачах, оценка по 12 критериям. Scorecard: Pi 6, DSH 6 |
| [DSH vs Pi (bswen.com, Aug 2026)](https://docs.bswen.com/blog/2026-08-14-deepseek-harness-vs-pi) | Сравнение для новичков: functionality, architecture, installation, user impact; вывод — DSH для traceability, Pi для model-agnostic |
| [DSH vs Pi vs OpenCode vs Hermes vs Claude (TencentCloud)](https://www.tencentcloud.com/techpedia/147665) | Сравнение пяти harness'ов, критерии выбора под разные workload |
| [DeepSeek Harness vs Pi Agent converging (Reddit r/PiCodingAgent)](https://www.reddit.com/r/PiCodingAgent/comments/1vnzn48/deepseek_harness_vs_pi_agent_are_they_converging) | Дискуссия сообщества: «DSH scientific-grade, Pi — vibe of quality» |
| [DSH In Depth (Justin3go)](https://justin3go.com/en/posts/2026/08/15-deepseek-harness-review) | Глубокий разбор исходников, включая сравнение с Pi по plugin lifecycle |
| [Pi vs DSH: Which Free Coding Agent Wins (YouTube)](https://www.youtube.com/watch?v=gGqi-wcyHc4) | Видео-сравнение: Terminal-Bench, cost per task, reasoning-настройки |

**Ключевой вывод из сравнений:** это не конкуренты в прямом смысле —
`dsh` использует Pi-слой под капотом, а Pi остаётся более зрелым для
ежедневной terminal-работы. Многие держат оба: Pi для быстрых задач,
`dsh` для сложных agent-workflow'ов с Web UI.

---

## 7. Где искать плагины: официальные и community

Экосистема плагинов `dsh` выросла до **~19k репозиториев** за два месяца.
Вот основные источники для поиска.

### GitHub Topics (самые свежие)

| Источник | Что содержит |
|---|---|
| [github.com/topics/dsh](https://github.com/topics/dsh) | ~9,5k репозиториев по основному topic; всё, что связано с DeepSeek Harness — форки, обёртки, инструменты, конфиги |
| [github.com/topics/dsh-plugin](https://github.com/topics/dsh-plugin) | ~18,6k репозиториев; строго сторонние плагины, расширяющие `dsh` новыми tools, connectors и UI |

Topic `dsh-plugin` — это то, как сама экосистема DeepSeek Harness
обнаруживает плагины: он заявлен в README как канал дистрибуции.
Плагин обычно поставляется как host-bundle + опциональная client-часть
и регистрируется через Cordis.

### Curated списки (awesome)

| Источник | Что содержит |
|---|---|
| [awesome-dsh-plugin/awesome-dsh-plugin](https://github.com/awesome-dsh-plugin/awesome-dsh-plugin) | Официальный curated list: **18.1k звёзд**, 3.9k форков, 7,521 коммитов. Сайт: [awesome-dsh-plugin.com](https://awesome-dsh-plugin.com). Категоризированный, активно поддерживается |
| [kejixiaoliang/awesome-dsh-plugins](https://github.com/kejixiaoliang/awesome-dsh-plugins) | Альтернативный индекс: bilingual (EN/中文), каждая запись со звёздами и `dsh plugin add`-командой, auto-sync CI |
| [Alex-Yanggg/awesome-DSH-plugin](https://github.com/Alex-Yanggg/awesome-DSH-plugin) | Community-curated vendor-neutral каталог по категориям: developer tools, data, DevOps, AI/media, business |

### Marketplace и каталоги

| Источник | Что содержит |
|---|---|
| [dshplugin.io](https://dshplugin.io) | Поисковый directory из **3,729** community-плагинов с source links и install-командами |
| [dsh-market/dsh-market](https://github.com/dsh-market/dsh-market) | Plugin market внутри DeepSeek: web-directory с фильтрами по категориям |
| [SpringBrand plugin directory](https://springbrand.ai/deepseek-harness/plugins) | Индекс по capability-группам: model access, tools, browser control, UI shells, memory, permissions |
| [dsh.so plugin registry](https://www.dsh.so) | Registry с automated security scan'ами и install-верификацией |
| [apimodels.app: 44 of 795 plugins](https://apimodels.app/dsh-plugins) | Аналитика: какие плагины реально используются (public repo + 100+ weekly downloads) |

### Официальные каналы

| Источник | Что содержит |
|---|---|
| [deepseek-ai/deepseek-harness](https://github.com/deepseek-ai/deepseek-harness) | Основной репозиторий: встроенные плагины, документация, discussions для plugin announcements |
| [GitHub discussions #1045](https://github.com/deepseek-ai/deepseek-harness/discussions/1045) | Community-каталог плагинов внутри официального репо |
| [Composio: Best DSH Plugins](https://composio.dev/content/best-deepseek-harness-plugins) | Редакторский обзор 10 лучших плагинов 2026 с install-командами |

**Как устанавливать найденное:**

```bash
# типичный паттерн установки
dsh plugin --profile web add <package-name>

# из GitHub-репозитория
dsh plugin --profile web add github:<owner>/<repo>

# пример: vision-плагин modlens
dsh plugin --profile web add @liustack/modlens

# после установки — рестарт профиля
dsh web
```

**Предостережение:** плагины исполняются внутри harness-процесса с полными
привилегиями и без sandbox'а. Перед `dsh plugin add` из непроверенного
источника — читайте исходники, пиньте версию/commit и проверяйте
permissions в manifest'е.

---

## 8. Итоговая рекомендация для Linux/macOS

`dsh` не привязан к моделям DeepSeek: адаптерный слой поддерживает около
40 провайдеров, включая OpenAI, Anthropic, Google, Kimi и любые
OpenAI-совместимые эндпоинты. Это позволяет подключить локальную модель
через Ollama или vLLM.

### 6.1. Ollama

Самый простой путь — `ollama launch dsh`: Ollama сам скачает и запустит
Harness, настройки хранятся в `~/.ollama/launch/dsh/settings.yaml`.

```bash
# установка Ollama (если ещё не стоит)
curl -fsSL https://ollama.com/install.sh | sh

# запуск dsh через Ollama
ollama launch dsh
ollama launch dsh --model qwen3:32b
```

Ручная настройка через Web UI: **Settings → Models** → добавить
провайдер с эндпоинтом `http://127.0.0.1:11434/v1` и полем
`api: openai-completions`. Выберите модель, поддерживающую tools.

### 6.2. vLLM

Для self-hosted vLLM-сервера: поднимите сервер с поддержкой
tool-calling (флаги `--enable-auto-tool-choice` и
`--tool-call-parser`), затем в Web UI добавьте OpenAI-совместимый
эндпоинт `http://<host>:<port>/v1`.

Практические заметки:

- локальные модели подходят для приватных/офлайн-сценариев и экономии
  на токенах, но требуют подготовки железа и весов;
- не все локальные модели корректно работают с tool-calling — проверяйте
  совместимость модели перед использованием;
- первый запуск часто падает из-за неверного имени модели или
  отсутствия credentials — см. раздел Troubleshooting.

---

## 7. Troubleshooting: частые проблемы и решения

### 7.1. `dsh: command not found`

**Причина:** Node.js не в `PATH`, или `npx`/глобальная установка не
выполнена. Проверьте:

```bash
node --version        # должно быть ^22.19.0 или >=24.0.0
which node
mise which node       # если используете mise
```

### 7.2. Порт 3080 занят / `EACCES` при старте

На Windows порт 3080 может попасть в Hyper-V reserved range
(`netsh interface ipv4 show excludedportrange protocol=tcp`). Решения:

```bash
# указать другой порт
npx @deepseek-ai/dsh web --port 3081

# или найти и остановить процесс, занимающий порт
lsof -i :3080   # macOS/Linux
```

Ошибка выводится как нечитаемый stack trace без указания адреса —
известная проблема (GitHub discussion #8159), диагностируйте через
`lsof`/`netstat` вручную.

### 7.3. `MISSING_CREDENTIAL` / модель не найдена

Web UI требует настроенный ключ модели (Settings → Models). Для
source-чекаута задайте переменные окружения:

```bash
export DEEPSEEK_API_KEY="sk-..."
# опционально:
export DEEPSEEK_BASE_URL="https://api.deepseek.com"
```

Не коммитьте реальные ключи; используйте `.env` в корне репозитория
(добавьте его в `.gitignore`).

### 7.4. Node.js несовместимой версии

`dsh` падает с ошибкой engine, если Node < 22.19 или между 23.x.
Зафиксируйте версию через `mise` (см. раздел 1.4) или `.nvmrc`.

### 7.5. Composer отключён / Web UI не открывается

Если страница `http://127.0.0.1:3080` не грузится:

1. Убедитесь, что `dsh web` действительно запущен (процесс жив, порт
   слушается).
2. Проверьте, что браузер не блокирует loopback (расширения privacy,
   firewall).
3. Composer в Web UI остаётся недоступным, пока не выбран workspace —
   это ожидаемое поведение, а не баг.

### 7.6. Workspace не выбран

Сессия не начнётся без указанного workspace. Кнопка **Choose
workspace** в Web UI обязательна; workspace задаёт рабочую директорию
и (в режиме `workspace-write`) границу мутаций файлов.

---

## 8. Статьи и материалы с практическим опытом

Ниже — подборка независимых обзоров, гайдов и обсуждений, полезных для
понимания реального опыта работы с `dsh` (проверено на октябрь 2026).

### Обзоры и first impressions

| Материал | Что освещает |
|---|---|
| [DeepSeek Harness In Depth (Justin3go)](https://justin3go.com/en/posts/2026/08/15-deepseek-harness-review) | Глубокий разбор исходников, сравнение с Pi/Codex CLI/Claude Code/OpenCode, анализ 90k звёзд за 2 дня |
| [DeepSeek Harness Reality Check (Medium)](https://medium.com/coding-nexus/deepseek-harness-reality-check-0851d7a545e1) | Критический взгляд: режимы (Standard/Minimal/Code/Creator), сильные и слабые стороны |
| [DeepSeek Harness Review (DeepInfra)](https://deepinfra.com/blog/deepseek-harness-review) | Установка и тестирование с не-DeepSeek моделями, delegation к Claude Code/Codex |
| [My First Impressions (Reddit)](https://www.reddit.com/r/DeepSeek/comments/1vnpt5n/my_first_impressions_of_deepseek_harness) | Впечатления сообщества: скорость, расход токенов, cache hit rate |
| [DeepSeek Harness explained (eesel.ai)](https://www.eesel.ai/blog/deepseek-harness) | Обзор архитектуры "everything is a plugin", статистика npm-загрузок |

### Гайды по установке и настройке

| Материал | Что освещает |
|---|---|
| [DeepSeek Harness Installation (Verdent)](https://www.verdent.ai/guides/agents/install-deepseek-harness-dsh) | Безопасная первая сессия: API key, выбор тест-репозитория, approvals |
| [Step-by-Step Setup Guide (Medium)](https://medium.com/@techlatest.net/how-to-install-deepseek-harness-a-step-by-step-setup-guide-for-developers-9bedadfb584d) | Установка с nvm, настройка Ollama/OpenRouter |
| [How to Install in 10 Minutes (AtlasCloud)](https://www.atlascloud.ai/blog/tips/how-to-install-deepseek-harness) | Быстрая установка, «3 конфиг-дефолта, которые молча ломают DeepSeek» |
| [Tutorial (DataCamp)](https://www.datacamp.com/tutorial/deepseek-harness) | Установка Node.js + dsh + pnpm, добавление API-ключей |
| [6 Methods to Deploy Locally (CometAPI)](https://www.cometapi.com/how-to-install-and-deploy-deepseek-harness-locally) | Сравнение способов деплоя: npx, source, desktop, Docker |
| [Install on Linux (deepseekdsh.com)](https://deepseekdsh.com/tutorials/linux) | Linux-специфика: Node.js, Web UI, модель, тест-папка |

### Web UI и workflow

| Материал | Что освещает |
|---|---|
| [Use dsh web (dsh-plugin.org)](https://dsh-plugin.org/tutorials/configure-dsh-web-ui) | 4 шага после запуска: launch → API key → workspace → tasks |
| [DSH plugin tasks and approvals](https://dsh-plugin.org/tutorials/configure-web-ui-usage) | Работа с approvals, зоны Web UI, установка интерфейс-плагинов |
| [Best plugins (Composio)](https://composio.dev/content/best-deepseek-harness-plugins) | Обзор популярных плагинов, паттерн `dsh plugin --profile web add` |
| [44 of 795 plugins (apimodels.app)](https://apimodels.app/dsh-plugins) | Какие плагины реально используются сообществом |

### Локальные модели

| Материал | Что освещает |
|---|---|
| [Run on Ollama or vLLM (ComputingForgeeks)](https://computingforgeeks.com/deepseek-harness-local-model) | Ручная настройка провайдера, credential-ловушка, compat-флаги vLLM |
| [DeepSeek Harness + Ollama (Medium)](https://medium.com/@MarkAiCode/deepseek-harness-ollama-run-local-models-setup-guide-9c89ec9b9dfe) | `ollama launch dsh`, YAML-patch для провайдера |
| [Ollama integration docs](https://docs.ollama.com/integrations/deepseek-harness) | Официальная документация Ollama по интеграции с dsh |
| [Use Local AI Models (dsh-plugin.org)](https://dsh-plugin.org/tutorials/configure-local-model) | LM-Kit / llama.cpp / Ollama через OpenAI-совместимый протокол |

### Docker и деплой

| Материал | Что освещает |
|---|---|
| [runzhliu/deepseek-harness-docker](https://github.com/runzhliu/deepseek-harness-docker) | Multi-stage Dockerfile, hardened Compose, Helm chart |
| [smanx/deepseek-harness-docker](https://github.com/smanx/deepseek-harness-docker) | Out-of-the-box образ с volume для данных |
| [Harness in a Container (Medium)](https://medium.com/open-intelligence/deepseek-harness-in-a-container-without-breaking-the-security-boundary-b1a38ace493f) | Почему dsh отвергает `--host 0.0.0.0` и как это обойти безопасно |

### Troubleshooting

| Материал | Что освещает |
|---|---|
| [dsh won't start: triage (dsh-plugin.org)](https://dsh-plugin.org/tutorials/dsh-startup-failed) | Трёхслойная диагностика: command → startup → access |
| [Debug desktop app (dsh-plugin.org)](https://dsh-plugin.org/tutorials/configure-desktop-debug) | Отладка десктоп-приложения, конфликты портов 9222/9229/9230 |
| [Official FAQ](https://deepseekdocs.com/en/docs/reference/faq) | Частые вопросы: install/start, конфигурация, плагины, обновления |
| [Windows compatibility (handbook)](https://github.com/sandbaseai/deepseek-harness-handbook/blob/main/docs/en/troubleshooting/windows-compatibility.md) | Windows-специфика: pwsh, ACL, partial enforcement |

### Сравнения с альтернативами

| Материал | Что освещает |
|---|---|
| [DeepSeek Harness vs OpenCode (Winder.AI)](https://winder.ai/deepseek-harness-vs-opencode) | Сравнение из опыта эксплуатации обоих: архитектура, модели, cost |
| [DeepSeek Harness vs Claude Code (Composio)](https://composio.dev/content/deepseek-harness-vs-claude-code) | Benchmarks, скорость, sandboxing, экосистема |
| [Best Coding Harness for DeepSeek V4 (Verdent)](https://www.verdent.ai/guides/coding/best-coding-harnesses-deepseek-v4) | Пять вариантов harness для DeepSeek-моделей |
| [AI Agent Harnesses Comparison (Winder.AI)](https://winder.ai/ai-agent-harness-comparison) | Девять продуктов, «какой слой вам нужен» |

---

## 9. Итоговая рекомендация для Linux/macOS

1. **Установите Node.js через `mise`** и зафиксируйте версию в
   `.mise.toml` — это избавит от «плавающих» проблем с версиями.
   Для системного `dsh` используйте `mise use -g node@24` +
   `mise use -g npm:@deepseek-ai/dsh`: инструмент будет доступен из
   любого каталога и автоматически подхватит активную версию Node.js,
   управляемую `mise`.
2. **Запускайте официальный `dsh web`** как основной рантайм:
   `npx @deepseek-ai/dsh web`.
3. **Добавьте TUI-плагин** (`deepseek-harness-tui` или
   `@nexlineai/dsh-tui`) для работы в терминале.
4. **Десктопный клиент** на Linux — опционально, только если нужен
   нативный оконный опыт. Выбирайте сборку с активной поддержкой и
   проверяйте релизы.
5. **Не запускайте несколько интерфейсов одновременно без нужды** —
   это усложняет отладку и может привести к конфликтам портов.
6. **Для приватных сценариев** рассмотрите подключение локальной модели
   через Ollama — это избавляет от API-ключей и сетевых round-trip'ов.
7. **Для CI/скриптов** используйте `dsh --profile headless` вместо
   Web UI.
