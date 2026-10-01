# Инструменты для линтинга Markdown: детальный обзор

## Введение

Линтинг Markdown помогает поддерживать единообразие документации, находить структурные ошибки и автоматизировать проверки в CI/CD. В этом обзоре собраны основные инструменты, их возможности, конфигурация и способы интеграции.

## Обзор инструментов

| Инструмент | Язык | Ключевые особенности | Источник |
| :--- | :--- | :--- | :--- |
| **markdownlint (DavidAnson)** | JavaScript / Node.js | Эталонный линтер, ~60 правил, расширения для редакторов, CLI и библиотека | [GitHub](https://github.com/DavidAnson/markdownlint) |
| **markdownlint-cli2** | JavaScript / Node.js | Быстрый CLI на базе markdownlint, гибкая конфигурация | [GitHub](https://github.com/DavidAnson/markdownlint-cli2) |
| **remark-lint** | JavaScript / Node.js | Работа на уровне AST, возможность создания собственных правил | [GitHub](https://github.com/remarkjs/remark-lint) |
| **pymarkdown** | Python | 46 правил, собственный GFM-парсер, автопсправление | [GitHub](https://github.com/jackdewinter/pymarkdown) |
| **rumdl** | Rust | Высокая скорость, 85 правил, форматирование, LSP | [GitHub](https://github.com/rvben/rumdl) |
| **mado** | Rust | 38 правил, скорость в 49–60 раз выше markdownlint | [GitHub](https://github.com/akiomik/mado) |
| **mdsmith** | Go | Автоисправление, проверка целостности ссылок между файлами | [GitHub](https://github.com/jeduden/mdsmith) |
| **gomarklint** | Go | Один бинарный файл, проверка HTTP-ссылок, JSON-вывод | [GitHub](https://github.com/shinagawa-web/gomarklint) |
| **checkmark** | Rust | Форматирование, линтинг, проверка орфографии и ссылок, ИИ-обзоры | [GitHub](https://github.com/vvvar/checkmark) |
| **Vale** | Go | Линтер прозы, проверка стиля и терминологии | [GitHub](https://github.com/errata-ai/vale) |

---

## markdownlint (DavidAnson)

### Описание

Самый распространённый линтер Markdown. Реализует около 60 правил, охватывающих заголовки, списки, пробелы, ссылки, блоки кода и таблицы. Доступен как библиотека Node.js, CLI и расширение для VS Code.

**Источник:** [GitHub — DavidAnson/markdownlint](https://github.com/DavidAnson/markdownlint)

### Правила

Полный список правил с описанием: [Rules.md](https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md). Каждое правило имеет идентификатор (например, MD013 — длина строки, MD033 — встроенный HTML, MD041 — первый заголовок должен быть H1).

**Источник:** [markdownlint Rules.md](https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md)

### Конфигурация

Файл `.markdownlint.yaml` позволяет включать, отключать и настраивать правила. Пример из проекта mcp.odoo:

```yaml
default: true
MD013: false          # Отключена длина строки
MD033: false          # Разрешён встроенный HTML
MD041: false          # Разрешён первый заголовок не H1
MD024:
  siblings_only: true # Дублирование заголовков только среди соседей
MD046:
  style: fenced       # Единый стиль блоков кода
MD049:
  style: asterisk     # Единый стиль выделения
MD050:
  style: asterisk     # Единый стиль жирного текста
```

**Источник:** [Пример конфигурации mcp.odoo](https://git.vauxoo.com/ai/mcp.odoo/-/blob/main/.markdownlint.yaml)

### Интеграция в pre-commit

Типичный хук pre-commit для markdownlint-cli2:

```yaml
- repo: https://github.com/DavidAnson/markdownlint-cli2
  rev: v0.22.0
  hooks:
    - id: markdownlint-cli2
      args: ["--fix"]
```

**Источник:** [GitHub — markdownlint-cli2](https://github.com/DavidAnson/markdownlint-cli2)

### Расширенные возможности

- Автоматическое исправление нарушений (флаг `--fix`).
- Создание пользовательских правил через API.
- Поддержка конфигураций в JSON, YAML и JSONC.

**Источник:** [markdownlint GitHub](https://github.com/DavidAnson/markdownlint)

---

## markdownlint-cli2

### Описание

Более быстрый и гибкий CLI-инструмент на основе markdownlint. Поддерживает те же правила, но оптимизирован для параллельной обработки и удобной настройки.

**Источник:** [GitHub — DavidAnson/markdownlint-cli2](https://github.com/DavidAnson/markdownlint-cli2)

### Конфигурация

Файл `.markdownlint-cli2.yaml` или `.markdownlint-cli2.jsonc`. Пример из проекта GitLab:

```yaml
ignores:
  - "doc/architecture"
customRules:
  - "./doc/.markdownlint/rules/unnecessary_traversal.js"
config:
  default: true
  code-block-style:
    style: "fenced"
  emphasis-style: false
  header-style:
    style: "atx"
  hr-style:
    style: "---"
  line-length:
    code_blocks: false
    tables: false
    headings: true
    heading_line_length: 100
    line_length: 800
  no-duplicate-heading:
    siblings_only: true
  no-emphasis-as-heading: false
  no-inline-html: false
  no-trailing-punctuation:
    punctuation: ".,;:!。，；：！"
  no-trailing-spaces: false
  ol-prefix:
    style: "one"
  reference-links-images: false
  ul-style:
    style: "dash"
  proper-names:
    code_blocks: false
    html_elements: false
    names: [ "Akismet", "Alertmanager", "AlmaLinux", "API", "Asana", "Auth0", "Azure", "Bamboo", "Bitbucket", "Bugzilla", "CAS", "CentOS", "Consul", "Debian", "DevOps", "Docker", "DockerSlim", "Elasticsearch", "Facebook", "fastlane", "fluent-plugin-redis-slowlog", "GDK", "Geo", "Git LFS", "git-annex", "git-credential-oauth" ]
```

**Источник:** [GitLab documentation — markdownlint](https://dev-ops.gitlab.cn/gitlab-cn/gitlab/-/blob/master/doc/development/documentation/testing/markdownlint.md)

### Пример JSONC-конфигурации

```jsonc
{
  // Разрешить дублирование заголовков под разными родителями
  "MD024": { "siblings_only": true },
  // Разрешить определённые встроенные HTML-элементы
  "MD033": { "allowed_elements": ["details", "summary"] },
  // Отключить принудительный стиль блоков кода
  "MD046": false,
  // Отключить ограничение длины строки
  "MD013": false
}
```

**Источник:** [Пример конфигурации simple-python-boilerplate](https://github.com/JoJo275/simple-python-boilerplate/blob/main/.markdownlint-cli2.jsonc)

### Интеграция в CI

Пример вызова в GitHub Actions:

```yaml
- name: Markdown Lint
  run: npx markdownlint-cli2 "**/*.md"
```

**Источник:** [npm — markdownlint-cli2](https://www.npmjs.com/package/markdownlint-cli2)

---

## remark-lint

### Описание

Линтер на основе remark — мощного процессора Markdown с AST (абстрактным синтаксическим деревом). Позволяет создавать собственные правила и использовать пресеты.

**Источник:** [GitHub — remarkjs/remark-lint](https://github.com/remarkjs/remark-lint)

### Создание собственного правила

Официальное руководство: [Create a custom rule](https://github.com/remarkjs/remark-lint/blob/main/doc/create-a-custom-rule.md). Пример правила, запрещающего GIF-изображения:

```js
// rules/no-gif-allowed.js
import { lintRule } from 'unified-lint-rule'
import { visit } from 'unist-util-visit'

const noGifAllowed = lintRule('remark-lint:no-gif-allowed', (tree, file) => {
  visit(tree, 'image', (node) => {
    if (node.url.endsWith('.gif')) {
      file.message('GIF images are not allowed', node)
    }
  })
})

export default noGifAllowed
```

**Источник:** [Create a custom remark-lint rule](https://github.com/remarkjs/remark-lint/blob/main/doc/create-a-custom-rule.md)

### Конфигурация

Файл `.remarkrc.js` или `.remarkrc`:

```js
module.exports = {
  plugins: [
    'remark-preset-lint-recommended',
    ['remark-lint-maximum-line-length', 100]
  ]
}
```

**Источник:** [remark-lint Rules](https://github.com/remarkjs/remark-lint/blob/main/doc/rules.md)

### Интеграция в GitHub Actions

Действие `reviewdog/action-remark-lint` запускает линтер и публикует комментарии в Pull Request:

```yaml
- uses: reviewdog/action-remark-lint@v5
  with:
    github_token: ${{ secrets.GITHUB_TOKEN }}
    reporter: github-pr-review
```

**Источник:** [reviewdog/action-remark-lint](https://github.com/reviewdog/action-remark-lint)

---

## pymarkdown

### Описание

Python-реализация линтера Markdown. Поддерживает 46 правил, имеет собственный GFM-совместимый парсер и режим автоматического исправления (`fix`).

**Источник:** [GitHub — jackdewinter/pymarkdown](https://github.com/jackdewinter/pymarkdown)

### Автоисправление

Команда `pymarkdown fix` автоматически исправляет нарушения, которые можно исправить однозначно. Например, удаление лишних пробелов в заголовках:

```bash
pymarkdown fix README.md
```

**Источник:** [PyMarkdown README](https://github.com/jackdewinter/pymarkdown)

### Список правил

Полный список с указанием поддержки автопсправления: [Rules](https://pymarkdown.readthedocs.io/en/latest/rules/). Пример правила MD046:

> **MD046**: Code block style. Autofix Available: Yes. Enabled By Default: Yes.

**Источник:** [PyMarkdown Rules — MD046](https://pymarkdown.readthedocs.io/en/latest/plugins/rule_md046/)

### Интеграция в pre-commit

```yaml
- repo: https://github.com/jackdewinter/pymarkdown
  rev: v0.9.29
  hooks:
    - id: pymarkdown
      args: [fix]
```

**Источник:** [PyMarkdown pre-commit](https://github.com/jackdewinter/pymarkdown)

---

## rumdl

### Описание

Высокопроизводительный линтер и форматтер на Rust. Реализует все правила markdownlint и дополнительные (всего 85). Поддерживает LSP для интеграции с редакторами.

**Источник:** [GitHub — rvben/rumdl](https://github.com/rvben/rumdl)

### Возможности

- Форматирование: `rumdl fmt` (алиас `check --fix`).
- Работа со stdin/stdout: `rumdl fmt -`.
- Чёткое разделение диагностики (stderr) и форматированного вывода (stdout).

**Источник:** [rumdl README](https://github.com/rvben/rumdl)

### Производительность

Согласно бенчмаркам, rumdl в 16–29 раз быстрее markdownlint-cli2 на реальных репозиториях.

**Источник:** [rumdl — markdownlint comparison](https://rumdl.dev/markdownlint-comparison)

### Интеграция в pre-commit

```yaml
- repo: https://github.com/rvben/rumdl
  rev: v0.2.7
  hooks:
    - id: rumdl
      args: [check --fix]
    - id: rumdl-fmt
```

**Источник:** [rumdl-pre-commit repository](https://github.com/rvben/rumdl-pre-commit)

### LSP-сервер

Встроенный LSP обеспечивает:

- Диагностику в реальном времени.
- Быстрые исправления (code actions).
- Автодополнение для языков в блоках кода и путей к файлам.
- Переход к определению и поиск ссылок.

**Источник:** [rumdl — Editor Integration](https://github.com/rvben/rumdl/blob/main/docs/usage/editors.md)

---

## mado

### Описание

Быстрый линтер Markdown на Rust. Совместим с CommonMark и GFM. Поддерживает большинство правил markdownlint.

**Источник:** [GitHub — akiomik/mado](https://github.com/akiomik/mado)

### Производительность

По бенчмаркам, mado примерно в 49–60 раз быстрее markdownlint на наборе из ~1500 файлов:

| Инструмент | Время (сек) |
| :--- | :--- |
| mado (Rust) | 0.129 |
| markdownlint-cli (Node.js) | 6.381 |
| markdownlint (Ruby) | 6.609 |
| markdownlint-cli2 (Node.js) | 7.817 |

**Источник:** [mado — Performance](https://github.com/akiomik/mado#performance)

### Поддерживаемые правила

Mado поддерживает большинство правил markdownlint. Полный список с указанием статуса поддержки: [Supported Rules](https://github.com/akiomik/mado#supported-rules).

**Источник:** [mado — Supported Rules](https://github.com/akiomik/mado#supported-rules)

### Конфигурация

Файл `mado.toml` или `.mado.toml` в текущей директории, либо глобальный конфиг:

- Linux: `~/.config/mado/mado.toml`
- macOS: `~/Library/Application Support/mado/mado.toml`

**Источник:** [mado — Configuration](https://github.com/akiomik/mado#configuration)

### Установка

```bash
# Homebrew
brew tap akiomik/mado
brew install mado

# Arch Linux
pacman -S mado

# Scoop (Windows)
scoop install https://raw.githubusercontent.com/akiomik/mado/refs/heads/main/pkg/scoop/mado.json
```

**Источник:** [mado — Installation](https://github.com/akiomik/mado#installation)

---

## mdsmith

### Описание

Линтер и форматтер на Go с автоисправлением. Проверяет стиль, читаемость, структуру и целостность ссылок между файлами.

**Источник:** [GitHub — jeduden/mdsmith](https://github.com/jeduden/mdsmith)

### Ключевые особенности

- **Автоисправление**: `mdsmith fix` переписывает пробелы, заголовки, блоки кода, голые URL, отступы списков и выравнивание таблиц.
- **Кросс-файловая целостность**: проверка ссылок и включений между файлами.
- **Генерируемые секции**: поддержка синхронизации сгенерированного контента.
- **Конвенции и flavors**: привязка к определённому рендереру (например, GitHub, GitLab).
- **Ограничения размера и читаемости**: максимальный размер файла, секции, токенов, оценка читабельности.

**Источник:** [mdsmith — Features](https://github.com/jeduden/mdsmith#features)

### Производительность

Один статический бинарник на Go проверяет весь репозиторий менее чем за секунду — на порядок быстрее Node markdownlint.

**Источник:** [mdsmith README](https://github.com/jeduden/mdsmith)

### Интеграция с редакторами

- VS Code расширение.
- Claude Code плагин.
- LSP-сервер `mdsmith lsp` для диагностики и fix-on-save.

**Источник:** [mdsmith — Editors and agents](https://github.com/jeduden/mdsmith#one-engine-every-surface)

### Миграция с markdownlint

```bash
mdsmith init --from-markdownlint
```
Конвертирует существующую конфигурацию markdownlint.

**Источник:** [mdsmith — Migration](https://github.com/jeduden/mdsmith#why-mdsmith)

### Установка

```bash
go install github.com/jeduden/mdsmith/cmd/mdsmith@latest
# или через npm
npm install -g @mdsmith/cli
```

**Источник:** [mdsmith — Installation](https://github.com/jeduden/mdsmith#installation)

---

## gomarklint

### Описание

Лёгкий линтер Markdown на Go, поставляемый как один бинарный файл без зависимостей от Node.js.

**Источник:** [GitHub — shinagawa-web/gomarklint](https://github.com/shinagawa-web/gomarklint)

### Возможности

- Проверка согласованности заголовков, дублирования заголовков, незакрытых блоков кода.
- Опциональная проверка внешних HTTP-ссылок (проверяет, отвечают ли URL).
- Вывод в текстовом и JSON-формате (удобно для CI).
- Ненулевой код возврата только в CI (переменная `GITHUB_ACTIONS=true`).

**Источник:** [gomarklint — Features](https://github.com/shinagawa-web/gomarklint)

### Конфигурация

```bash
gomarklint init  # создаёт .gomarklint.json
gomarklint ./docs
```

**Источник:** [gomarklint — Quick Start](https://shinagawa-web.github.io/)

### Интеграция в GitHub Actions

Официальное действие: [gomarklint-markdown-linter](https://github.com/marketplace/actions/gomarklint-markdown-linter).

**Источник:** [gomarklint GitHub Action](https://github.com/marketplace/actions/gomarklint-markdown-linter)

### Установка

```bash
go install github.com/shinagawa-web/gomarklint@latest
```

**Источник:** [gomarklint — Installation](https://pkg.go.dev/github.com/shinagawa-web/gomarklint@v1.5.0/cmd)

---

## checkmark

### Описание

CLI-инструмент для Markdown, объединяющий форматирование, линтинг, проверку орфографии, проверку ссылок и ИИ-обзоры.

**Источник:** [GitHub — vvvar/checkmark](https://github.com/vvvar/checkmark)

### Команды

| Команда | Описание |
| :--- | :--- |
| `checkmark fmt` | Автоформатирование всех Markdown-файлов |
| `checkmark lint` | Линтинг (частичный порт markdownlint) |
| `checkmark links` | Проверка битых ссылок (веб и локальных) |
| `checkmark review` | ИИ-обзор документов через OpenAI API |
| `checkmark compose` | ИИ-помощь в создании новых документов |
| `checkmark spelling` | Проверка орфографии |
| `checkmark render` | Конвертация в HTML |
| `checkmark remote check` | Проверка документов из удалённого Git-репозитория |

**Источник:** [checkmark — Features](https://github.com/vvvar/checkmark#features)

### Установка

```bash
cargo install --git https://github.com/vvvar/checkmark.git --locked
```

**Источник:** [checkmark — Installation](https://github.com/vvvar/checkmark#installation)

### CI-режим

Флаг `--ci-mode` отключает интерактивные запросы и выводит отчёты в формате, подходящем для CI/CD.

**Источник:** [checkmark — CI mode](https://github.com/vvvar/checkmark#features)

---

## Vale

### Описание

Линтер прозы, поддерживающий Markdown, MDX, reStructuredText, AsciiDoc и комментарии в исходном коде. Проверяет стиль, терминологию и грамматику. Vale работает на уровне абстрактного синтаксического дерева (AST), а не как обычный текстовый анализатор, что позволяет ему игнорировать код, URL и синтаксис разметки, проверяя только тот текст, который читает человек.

**Источник:** [Vale — Official site](https://vale.sh)

### Поддержка русского языка

Vale **поддерживает русский язык**, но это поддержка несколько иного уровня, чем для английского. Если для английского языка Vale «из коробки» предлагает готовые стили и словари, то для русского языка инструмент предоставляет **гибкую платформу**, которую нужно настроить под свои задачи.

#### Определение языка

Vale позволяет явно указать, что документ написан на русском языке. В файле конфигурации `.vale.ini` для этого используется параметр `Lang`:

```ini
[*.md]
Lang = ru
```

Это сообщает Vale, что при анализе нужно использовать языковые правила, соответствующие русскому языку. Параметр `Lang` также влияет на проверку орфографии и NLP-анализ.

**Источник:** [Vale — .vale.ini documentation](https://docs.vale.sh/keys/vale-ini)

#### Проверка орфографии через Hunspell-словари

Встроенный словарь Vale по умолчанию — это американский английский. Для проверки русской орфографии необходимо подключить собственный словарь в формате, совместимом с **Hunspell**. Vale использует чистую Go-библиотеку для работы с Hunspell-совместимыми словарями, поэтому сам Hunspell устанавливать не требуется.

Словарь Hunspell состоит из двух файлов:

1. **`.aff`** — файл аффиксов, определяющий морфологические правила (префиксы, суффиксы, грамматические особенности).
2. **`.dic`** — файл словаря, содержащий список корневых слов и связанные с ними коды аффиксов.

Файлы должны быть названы согласованно, например `ru_RU.aff` и `ru_RU.dic`. В конфигурации Vale путь к словарям указывается через ключ `dictionaries` в секции `spelling`:

```ini
[*.md]
Lang = ru
[spelling]
dictionaries = ru_RU
```

**Источник:** [Vale — Hunspell guide](https://docs.vale.sh/guides/hunspell)

Где найти русские Hunspell-словари:

- [wooorm/dictionaries](https://github.com/wooorm/dictionaries) — коллекция словарей для разных языков, включая русский.
- [LibreOffice/dictionaries](https://github.com/LibreOffice/dictionaries) — официальные словари LibreOffice.
- [Firefox Language Tools](https://addons.mozilla.org/en-US/firefox/language-tools) — языковые пакеты Firefox со встроенными словарями.

**Источник:** [Vale — Hunspell dictionaries](https://docs.vale.sh/guides/hunspell)

#### Правила стиля и терминологии

Самая сильная сторона Vale для русского языка — это возможность создавать **собственные правила** для проверки стиля, терминологии и структуры текста. Правила хранятся в YAML-файлах и не зависят от自然 языка текста, поэтому вы можете создавать правила для русского языка так же, как и для английского.

Пример правила, запрещающего использование канцеляризмов (файл `styles/MyStyle/Terms.yml`):

```yaml
extends: existence
message: "Избегайте канцеляризма '%s'. Используйте более простую формулировку."
level: warning
ignorecase: true
tokens:
  - 'данный'
  - 'осуществлять'
  - 'производить'
  - 'в целях'
  - 'в соответствии с'
```

Пример правила для единообразия написания термина (файл `styles/MyStyle/BrandTerms.yml`):

```yaml
extends: substitution
message: "Используйте '%s' вместо '%s'."
level: error
ignorecase: true
swap:
  'API': 'АПИ'
  'API': 'апи'
  'GitLab': 'ГитЛаб'
  'Docker': 'Докер'
```

**Источник:** [Vale — Styles documentation](https://vale.sh/docs/styles)

**Примеры правил от российских команд:**

- **Cloud.ru** — команда из более чем 20 технических писателей разработала около 30 правил редакционной политики, включая использование буквы «ё» и постановку точек в таблицах. Они используют Vale в связке с GitLab CI/CD для автоматической проверки документации в формате reStructuredText. Статья на Habr: [«Проверяем текст: кейс автоматизации с линтером Vale»](https://habr.com/ru/companies/cloud_ru/articles/865604/).
- **FreeBSD** — проект использует Vale для проверки документации, включая правила для английского языка с возможностью адаптации. Конфигурация доступна в репозитории: [freebsd-doc/.vale.ini](https://codeberg.org/FreeBSD/freebsd-doc/src/branch/main/.vale.ini).

**Источник:** [Habr — Cloud.ru Vale case](https://habr.com/ru/companies/cloud_ru/articles/865604/) · [FreeBSD .vale.ini](https://codeberg.org/FreeBSD/freebsd-doc/src/branch/main/.vale.ini)

#### Конфигурация `.vale.ini` для русского языка

Пример полной конфигурации для русскоязычного проекта:

```ini
StylesPath = .vale/styles
MinAlertLevel = suggestion

[*.md]
BasedOnStyles = Vale, MyStyle
Lang = ru
Vale.Spelling = YES

[spelling]
dictionaries = ru_RU
```

**Источник:** [Vale — Configuration](https://vale.sh/docs/vale-ini)

#### NLP-анализ для русского языка

Vale развивает поддержку NLP-анализа для русского языка. В экспериментальном режиме (в рамках интеграции со spaCy) Vale Studio поддерживает тегирование и анализ контента на русском языке. Это открывает возможности для более глубоких проверок, например, на согласованность времен или пассивный залог, но пока эта функциональность находится в стадии разработки. Обсуждение в GitHub: [Multilingual, spaCy-powered NLP · Issue #356](https://github.com/errata-ai/vale/issues/356).

**Источник:** [GitHub — Vale Issue #356](https://github.com/errata-ai/vale/issues/356)

#### Интеграция в CI для русскоязычных проектов

Пример запуска Vale в GitLab CI (адаптировано из опыта Cloud.ru):

```yaml
vale-lint:
  image: jdkato/vale:latest
  script:
    - vale --config=.vale.ini --minAlertLevel=warning --output=JSON doc/
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
```

**Источник:** [Vale — CI integrations](https://vale.sh/docs/integrations/ci)

### Конфигурация `.vale.ini` (общая)

```ini
StylesPath = .vale/styles
MinAlertLevel = suggestion

[*.md]
BasedOnStyles = Vale, write-good
write-good.E-Prime = NO
write-good.TooWordy = NO
write-good.Passive = suggestion
```

**Источник:** [Vale — Configuration](https://vale.sh)

### Настройка отдельных правил

```ini
[*.md]
BasedOnStyles = Vale, MyStyle
Vale.Spelling = NO

# Включить только одно правило из стиля, не включая весь стиль
Style1.Rule = YES
```

**Источник:** [Vale — Styles](https://vale.sh/docs/styles)

### Уровни серьёзности

```ini
[*.md]
BasedOnStyles = proselint
proselint = suggestion        # Все правила proselint — suggestion
proselint.Typography = warning # Кроме этого — warning
```

**Источник:** [Vale — Severity levels](https://vale.sh/docs/topics/styles)

### Интеграция в CI

Пример из GitLab CI:

```bash
echo $FILES | xargs vale --minAlertLevel error --output=docs/.vale/vale.tmpl --config "${GIT_ROOT}/.vale.ini"
```

**Источник:** [Vale — GitLab CI](https://docs.vale.sh/integrations/ci)

### Поддержка MDX

Требуется Vale версии 3.10.0 или выше.

**Источник:** [Vale — MDX support](https://vale.sh/docs/mdx)

---

## Сравнение производительности

| Инструмент | Язык | Относительная скорость | Источник |
| :--- | :--- | :--- | :--- |
| mado | Rust | 49–60x быстрее markdownlint | [mado GitHub](https://github.com/akiomik/mado#performance) |
| rumdl | Rust | 16–29x быстрее markdownlint-cli2 | [rumdl comparison](https://rumdl.dev/markdownlint-comparison) |
| mdsmith | Go | На порядок быстрее Node markdownlint | [mdsmith README](https://github.com/jeduden/mdsmith) |
| gomarklint | Go | Тысячи строк за ~50 мс | [gomarklint DEV Community](https://dev.to/shinagawa-web/inside-gomarklint-building-a-high-performance-markdown-linter-in-go-4a1d) |

---

## Интеграция в CI/CD

### GitHub Actions

- **markdownlint-cli2**: `npx markdownlint-cli2 "**/*.md"` — [GitHub Action](https://github.com/DavidAnson/markdownlint-cli2-action)
- **remark-lint**: `reviewdog/action-remark-lint@v5` — [reviewdog/action-remark-lint](https://github.com/reviewdog/action-remark-lint)
- **gomarklint**: официальное действие `gomarklint-markdown-linter` — [Marketplace](https://github.com/marketplace/actions/gomarklint-markdown-linter)

### Pre-commit хуки

| Инструмент | Репозиторий | ID хука |
| :--- | :--- | :--- |
| markdownlint-cli2 | [DavidAnson/markdownlint-cli2](https://github.com/DavidAnson/markdownlint-cli2) | `markdownlint-cli2` |
| pymarkdown | [jackdewinter/pymarkdown](https://github.com/jackdewinter/pymarkdown) | `pymarkdown` |
| rumdl | [rvben/rumdl](https://github.com/rvben/rumdl) | `rumdl` |

**Источник:** [pre-commit hooks documentation](https://pre-commit.com/hooks.html)

### GitLab CI

Пример job для markdownlint-cli2:

```yaml
lint-markdown:
  image: node:20-slim
  script:
    - npx markdownlint-cli2 "**/*.md"
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
    - if: $CI_COMMIT_TAG
```

**Источник:** [GitLab documentation — markdownlint](https://dev-ops.gitlab.cn/gitlab-cn/gitlab/-/blob/master/doc/development/documentation/testing/markdownlint.md)

---

## Рекомендации по выбору

| Сценарий | Рекомендуемый инструмент | Источник |
| :--- | :--- | :--- |
| Стандартная документация, широкая экосистема | **markdownlint** или **markdownlint-cli2** | [GitHub](https://github.com/DavidAnson/markdownlint) |
| Максимальная скорость, Rust-стек | **rumdl** или **mado** | [GitHub](https://github.com/rvben/rumdl) |
| Go-стек, один бинарник | **mdsmith** или **gomarklint** | [GitHub](https://github.com/jeduden/mdsmith) |
| Python-стек, автопсправление | **pymarkdown** | [GitHub](https://github.com/jackdewinter/pymarkdown) |
| Гибкие правила на AST | **remark-lint** | [GitHub](https://github.com/remarkjs/remark-lint) |
| Проверка стиля и терминологии прозы | **Vale** | [Vale](https://vale.sh) |
| Русскоязычная документация, стиль и терминология | **Vale** (с Hunspell-словарём и кастомными правилами) | [Vale + Hunspell](https://docs.vale.sh/guides/hunspell) |
| Всё в одном (линтинг + орфография + ИИ) | **checkmark** | [GitHub](https://github.com/vvvar/checkmark) |

---

## Заключение

Выбор инструмента зависит от технологического стека, требований к скорости и необходимой глубины проверки. Для большинства проектов достаточно **markdownlint-cli2** с расширением для VS Code. Если критична производительность в больших репозиториях — стоит рассмотреть **rumdl** или **mado**. Для Python-проектов естественным выбором будет **pymarkdown**, для Go — **mdsmith** или **gomarklint**. **Vale** дополняет любой из них проверкой стиля прозы.

Для русскоязычных технических руководств Vale становится особенно ценным инструментом: он позволяет автоматизировать проверку редакционной политики, терминологии и орфографии, как это делает команда Cloud.ru с более чем 20 техническими писателями и 30 правилами. Ключевые шаги для настройки Vale на русском языке: указание `Lang = ru` в `.vale.ini`, подключение Hunspell-совместимого словаря (`ru_RU.aff` и `ru_RU.dic`) и создание собственных YAML-правил для терминологии и стиля.

Все перечисленные инструменты активно поддерживаются, имеют открытый исходный код и могут быть интегрированы в CI/CD и pre-commit хуки.
