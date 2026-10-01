# Markdown Linting Tools — Research

Дата исследования: 2026-10-01

## Обзор

Markdown-линтеры проверяют разметку на соответствие стилевым правилам (структура заголовков, пробелы, списки, ссылки и т.д.), помогают поддерживать единообразие документации в репозитории и предотвращают типичные ошибки авторов. Ниже — детальное сравнение основных инструментов, их окружения, количества правил, возможностей автофикса и интеграций.

## Сводная таблица

| Инструмент | Язык / окружение | Тип | Число правил | Автофикс | Формат конфигурации | Плагины | LSP |
|---|---|---|---|---|---|---|---|
| **rumdl** | Rust (нативный бинарник) | Линт + форматирование | 88 | Да | TOML, JSON, YAML | Нет | Да |
| **markdownlint-cli** | Node.js | Линт | 53 | Да | JSON, JSONC, YAML, TOML | Да (JS) | Нет |
| **markdownlint-cli2** | Node.js | Линт | 53 | Да | JSONC, YAML, JS | Да (JS) | Нет |
| **remark-lint** | Node.js | Линт | ~80 (через пресеты) | Нет | JS, JSON, YAML | Да (JS) | Нет |
| **pymarkdown** | Python | Линт | 46 | Да | JSON, YAML, TOML | Да (Python) | Нет |
| **mdl** | Ruby | Линт | ~30 | Нет | Ruby-стили | Да (Ruby) | Нет |
| **mdformat** | Python | Форматирование | — | — | TOML | Да (Python) | Нет |
| **mado** | Rust | Линт | 38 | Нет | TOML | Нет | Нет |
| **Prettier** | Node.js | Форматирование | — | — | JSON, YAML, JS | Да (JS) | Нет |
| **textlint** | Node.js | Линт (естественный язык) | зависит от правил | Частично | JSON, YAML | Да (JS) | Нет |

Источник таблицы: официальное сравнение на сайте rumdl【turn10click0】【turn11fetch0】.

## 1. rumdl

**rumdl** — быстрый линтер и форматировщик Markdown, написанный на Rust. Реализует все 53 правила из `markdownlint` и добавляет 35 собственных правил (итого 88), включая проверку относительных ссылок (MD057), сносок (MD066–MD068), вложенных кодовых блоков (MD070) и TOC (MD073)【turn11fetch0】.

Ключевые особенности:
- **Нативный бинарник** — не требует установки Node.js, Python или Ruby. Доступен через pip, cargo, npm, Homebrew【turn12fetch0】.
- **Встроенная поддержка диалектов Markdown**: MkDocs, MDX, Obsidian, Pandoc, Quarto, kramdown (Jekyll), Azure DevOps, MyST, Hugo, Gherkin【turn11fetch0】.
- **LSP-сервер** (`rumdl server`) для интеграции в редакторы (VS Code, Neovim)【turn12fetch0】.
- **Автофикс** большинства нарушений и режим форматирования (`rumdl fmt`)【turn9fetch1】.
- **Высокая скорость**: по бенчмаркам на репозитории Rust Book (февраль 2026, без кэша) — 217 мс, что в ~10 раз быстрее `markdownlint-cli2` (2.2 с)【turn9fetch1】【turn12fetch0】.

Установка (одна из опций):
```bash
uvx rumdl check .
```

Ресурсы:
- Официальный сайт: <https://rumdl.dev>【turn9fetch1】
- Репозиторий: <https://github.com/rvben/rumdl>【turn0search0】【turn0search1】
- Документация по сравнение с markdownlint: <https://rumdl.dev/comparison/>【turn10click0】

## 2. markdownlint / markdownlint-cli / markdownlint-cli2

**markdownlint** — самый популярный Node.js-линтер для Markdown, изначально разработанный David Anson (Microsoft)【turn0search1】【turn4fetch1】. Существует в виде библиотеки и двух CLI-обёрток.

- **markdownlint** — базовая библиотека правил для Node.js【turn4fetch1】.
- **markdownlint-cli** — первая CLI-обёртка, поддерживает JSON/JSONC/YAML/TOML-конфиги и кастомные правила на JavaScript【turn10click0】.
- **markdownlint-cli2** — улучшенная версия: добавляет JSONC-конфиги, более тесную интеграцию с VS Code (расширение `vscode-markdownlint`) и туже поддержку конфигурационных файлов【turn10click0】【turn3search0】.

Особенности:
- 53 правила с идентификаторами MD001–MD053 (проверка уровней заголовков, стилей списков, длины строк, пробелов и т.д.)【turn10click0】.
- Автофикс (`--fix`) для части нарушений【turn10click0】.
- Расширение для VS Code и GitHub Action (`markdownlint-cli2-action`)【turn4fetch1】【turn6search3】.
- Большая экосистема и наибольшая распространённость в open-source проектах.

Ресурсы:
- Репозиторий markdownlint: <https://github.com/DavidAnson/markdownlint>【turn0search1】
- Репозиторий markdownlint-cli2: <https://github.com/DavidAnson/markdownlint-cli2>【turn0search0】【turn2search3】
- npm: <https://www.npmjs.com/package/markdownlint-cli2>【turn1fetch0】
- Расширение VS Code: <https://marketplace.visualstudio.com/items?itemName=DavidAnson.vscode-markdownlint>【turn0search7】
- Блог автора: <https://dlaa.me/markdownlint>【turn4fetch1】【turn3search0】

## 3. remark-lint

**remark-lint** — часть коллективного проекта **unified** (remarkjs), экосистемы для обработки Markdown/HTML через синтаксические деревья【turn1fetch1】. Отличается модульным подходом:

- Правила распространяются как отдельные npm-пакеты и объединяются в пресеты (например, `remark-preset-lint-recommended`, `remark-preset-lint-consistent`)【turn10click0】.
- Около 80 правил через пресеты, но нет встроенного автофикса (lint-правила только сообщают о нарушениях)【turn10click0】.
- Конфигурация через JS, JSON, YAML; поддержка плагинов на JavaScript【turn10click0】.
- Языковой сервер `remark-language-server` для интеграции в редакторы через LSP【turn12fetch0】.
- Поддержка MDX и JSX-синтаксиса через плагины (например, `eslint-plugin-mdx`)【turn1search10】【turn6search6】.

Ресурсы:
- Unified collective: <https://unifiedjs.com>【turn1fetch1】
- Список проектов: <https://unifiedjs.com/explore/project/>【turn3search5】
- Примеры правил на npm: <https://www.npmjs.com/package/remark-lint-first-heading-level>【turn3search3】

## 4. pymarkdown

**pymarkdown** — Python-линтер для Markdown, реализующий 46 правил с собственным GFM-совместимым парсером【turn10click0】.

- Поддерживает автофикс и кастомные расширения правил на Python【turn10click0】.
- Конфигурация через JSON, YAML, TOML【turn10click0】.
- Аналогия с PyLint: «PyLint — для Python, PyMarkdown — для Markdown»【turn6search0】.
- Хорошо подходит для команд, уже работающих с Python-инструментарием (pytest, pre-commit и т.д.)【turn6search0】.

Ресурсы:
- Документация: <https://pymarkdown.readthedocs.io>【turn6search0】
- Интеграция с pre-commit: <https://pymarkdown.readthedocs.io/en/latest/pre-commit/>【turn6search0】

## 5. mdl (Markdown Lint Tool)

**mdl** — Ruby-линтер для Markdown, один из старейших инструментов в этой категории【turn0search5】【turn0search7】.

- Реализован как Ruby-гем, устанавливается через `gem install mdl`【turn0search5】.
- Правила настраиваются через файлы стилей на Ruby【turn0search5】.
- Простой и лёгкий, но число правил (~30) и развитие отстают от markdownlint или rumdl【turn0search7】【turn0search8】.
- Доступен в Arch Linux, Debian, Ubuntu и других дистрибутивах【turn0search7】【turn0search8】.

Ресурсы:
- Документация (book edition): <https://updownpress.github.io/markdownlint/>【turn1fetch0】
- Репозиторий: <https://github.com/markdownlint/markdownlint>【turn0search7】
- Man-страница Ubuntu: <https://manpages.ubuntu.com/manpages/jammy/man1/mdl.1.html>【turn0search8】

## 6. mdformat

**mdformat** — Python-форматировщик Markdown (не линтер), ориентированный на консистентный вывод CommonMark【turn10click0】.

- Не имеет правил линтинга, но нормализует пробелы, отступы, стили списков и т.д.【turn10click0】.
- Расширенный синтаксис (GFM-таблицы, frontmatter) поддерживается через плагины【turn10click0】.
- Конфигурация через TOML, установка через pip и Homebrew【turn12fetch0】.
- Сравнение с rumdl: rumdl совмещает линтинг и форматирование и в ~18 раз быстрее (217 мс против 4.0 с на бенчмарке Rust Book)【turn12fetch0】.

Ресурсы:
- PyPI: <https://pypi.org/project/mdformat/>
- Сравнение с rumdl: <https://rumdl.dev/comparison/>【turn10click0】

## 7. Prettier

**Prettier** — широко распространённый «мнение-ориентированный» форматировщик кода с поддержкой Markdown【turn10click0】.

- Не линтер: только нормализует стиль (пробелы, маркеры списков, эмфаз)【turn10click0】.
- Минимальная конфигурация — «одно правильное форматирование»【turn10click0】.
- Поддержка Markdown описана на официальном сайте: <https://prettier.io/docs/en/>
- Сравнение производительности с rumdl: 4.8 с против 217 мс на том же бенчмарке (22.3× медленнее)【turn12fetch0】.

## 8. mado

**mado** — быстрый Rust-линтер для Markdown с 38 правилами (33 стабильные, 5 нестабильных)【turn10click0】.

- Не поддерживает автофикс и плагины【turn10click0】.
- Самый быстрый из сравниваемых линтеров: 77 мс на бенчмарке Rust Book【turn12fetch0】.
- Не имеет интеграций с редакторами или LSP【turn12fetch0】.
- Подходит для простых сценариев, где нужна скорость и минимальный набор правил.

Ресурсы:
- Репозиторий: <https://github.com/akiomik/mado>【turn0search4】【turn0search5】
- Arch Linux пакет: <https://archlinux.org/packages/extra/x86_64/mado/>【turn0search4】

## 9. textlint

**textlint** — «подключаемый линтер для естественного языка и Markdown», написанный на JavaScript и вдохновлённый ESLint【turn8search2】【turn6search2】.

- Фокусируется не на структуре Markdown, а на стиле письма: грамматика, чувствительные формулировки, согласованность терминологии【turn8search2】【turn6search1】.
- Правила реализуются как плагины; доступно множество готовых (например, для проверки терминологии, запятых, стиля)【turn8search3】.
- Частично поддерживает автофикс в зависимости от правила【turn6search1】.
- Используется в связке с markdownlint или remark-lint для покрытия и синтаксиса, и стиля текста【turn8search2】.

Ресурсы:
- Репозиторий: <https://github.com/textlint/textlint>
- Обзор: <https://pabloestrada.us/blog/2019/12/02/linters/>【turn8search2】
- Контейнерная версия: <https://github.com/uhooi/docker-textlint>【turn6search1】

## Интеграции с редакторами и CI

### VS Code
- **rumdl** — встроенная поддержка через LSP (`rumdl server`)【turn12fetch0】.
- **markdownlint-cli2** — официальное расширение `vscode-markdownlint`【turn0search7】【turn12fetch0】.
- **remark-lint** — через расширение или `remark-language-server`【turn12fetch0】.
- **Prettier** — официальное расширение Prettier【turn12fetch0】.

### Neovim
- **rumdl** — через LSP【turn12fetch0】.
- **markdownlint-cli2** — через efm/null-ls【turn12fetch0】.
- **remark-lint** — через LSP или efm【turn12fetch0】.
- **mdformat** — через conform.nvim【turn12fetch0】.

### CI/CD
- **rumdl** — GitHub Action, GitLab, Azure, SARIF, JUnit, JSON-вывод【turn9fetch1】.
- **markdownlint-cli2** — GitHub Action `markdownlint-cli2-action`【turn6search3】.
- **pre-commit** — поддержка rumdl, markdownlint-cli2, pymarkdown【turn2search3】【turn6search0】.

## Производительность

Бенчмарки на репозитории Rust Book (февраль 2026, холодный старт, без кэша):

| Инструмент | Тип | Среднее время | Относительно rumdl |
|---|---|---|---|
| **mado** | Линт | 77 мс | 0.4× |
| **rumdl** | Линт | 217 мс | 1.0× |
| **pymarkdown** | Линт | 240 мс | 1.1× |
| **remark-lint** | Линт | 671 мс | 3.1× |
| **markdownlint-cli2** | Линт | 2.2 с | 10.2× |
| **markdownlint-cli** | Линт | 2.7 с | 12.5× |
| **mdformat** | Формат | 4.0 с | 18.5× |
| **Prettier** | Формат | 4.8 с | 22.3× |

Источник: <https://rumdl.dev/comparison/>【turn12fetch0】.

## Рекомендации по выбору

### Для нового проекта (2026)
- **rumdl** — если нужен быстрый нативный инструмент с автофиксом, LSP и поддержкой диалектов (MkDocs, MDX, Obsidian, Pandoc и т.д.)【turn9fetch1】【turn11fetch0】.
- **markdownlint-cli2** — если важна максимальная совместимость с существующей экосистемой (VS Code, GitHub Actions, pre-commit) и вы готовы работать с Node.js【turn3search0】【turn6search3】.

### Для существующего проекта с markdownlint
- **rumdl** — миграция без изменения конфигурации: rumdl автоматически обнаруживает существующие конфиги markdownlint【turn9fetch1】.
- Подробное руководство по миграции: <https://rumdl.dev/comparison/>【turn10click0】.

### Для Python-проектов
- **pymarkdown** — если команда уже использует Python-инструменты и хочет остаться в одной экосистеме【turn10click0】【turn6search0】.

### Для Ruby-проектов
- **mdl** — простой и лёгкий вариант, но с меньшим числом правил【turn0search5】【turn0search7】.

### Для проверки стиля текста (не синтаксиса)
- **textlint** — в связке с любым Markdown-линтером для проверки естественного языка【turn8search2】【turn6search2】.

### Для форматирования (без линтинга)
- **Prettier** — если нужен «мнение-ориентированный» форматировщик с минимальной конфигурацией【turn10click0】.
- **mdformat** — если нужен Python-форматировщик с CommonMark-выводом【turn10click0】.

## Источники

1. rumdl — официальный сайт и сравнение инструментов: <https://rumdl.dev>【turn9fetch1】, <https://rumdl.dev/comparison/>【turn10click0】【turn11fetch0】【turn12fetch0】
2. rumdl — репозиторий на GitHub: <https://github.com/rvben/rumdl>【turn0search0】【turn0search1】
3. markdownlint — репозиторий: <https://github.com/DavidAnson/markdownlint>【turn0search1】
4. markdownlint-cli2 — npm: <https://www.npmjs.com/package/markdownlint-cli2>【turn1fetch0】
5. markdownlint-cli2 — блог David Anson: <https://dlaa.me>【turn4fetch1】【turn3search0】
6. markdownlint — расширение VS Code: <https://marketplace.visualstudio.com/items?itemName=DavidAnson.vscode-markdownlint>【turn0search7】
7. remark-lint — unified collective: <https://unifiedjs.com>【turn1fetch1】【turn3search5】
8. remark-lint — примеры правил: <https://www.npmjs.com/package/remark-lint-first-heading-level>【turn3search3】
9. pymarkdown — документация: <https://pymarkdown.readthedocs.io>【turn6search0】
10. mdl — документация: <https://updownpress.github.io/markdownlint/>【turn1fetch0】
11. mdl — репозиторий: <https://github.com/markdownlint/markdownlint>【turn0search7】
12. mado — репозиторий: <https://github.com/akiomik/mado>【turn0search4】【turn0search5】
13. textlint — обзор: <https://pabloestrada.us/blog/2019/12/02/linters/>【turn8search2】
14. textlint — сравнение: <https://stackshare.io/stackup/textlint-vs-php-codesniffer>【turn6search2】
15. mdformat — сравнение с rumdl: <https://rumdl.dev/comparison/>【turn10click0】
16. Анализ инструментов — analysis-tools.dev: <https://www.analysis-tools.dev/>【turn0search4】
17. Mega-Linter — конфигурация remark-lint: <https://megalinter.io/>【turn0search4】【turn1search5】
18. Выбор линтера для docs pipeline — dev.to: <https://dev.to/>【turn0search3】

