# AGENTS.md: руководства, правила и фреймворки для составления

> **Расположение:** research/inbox (черновой входящий документ)
> **Дата сбора:** сентябрь 2026 г.
> **Предмет:** интернет-ресурсы по составлению AGENTS.md — спецификации, руководства, правила, шаблоны, фреймворки, реестры, критика.
> **Требование выполнено:** на каждый источник приведена ссылка.
>
> **Легенда полноты проверки:**
> ✅ — содержимое источника прочитано полностью (текст в заметках дословный или близкий к дословному).
> 🔶 — проверен частично: заголовок, оглавление или фрагмент из поисковой выдачи (требует дочитывания).

---

## 1. Резюме — главные выводы

| # | Вывод | Источник |
|---|---|---|
| 1 | AGENTS.md — открытый формат «README для агентов», используемый **60 000+ open-source проектов**; обычный Markdown, обязательных полей нет | [agents.md](https://agents.md/) ✅ |
| 2 | Формат появился из совместной работы **OpenAI (Codex), Amp, Jules (Google), Cursor и Factory**; курируется **Agentic AI Foundation под эгидой Linux Foundation** | [agents.md](https://agents.md/) ✅ |
| 3 | Это **стандарт, а не спецификация**: schema-less Markdown, без грамматики и conformance-тестов | [javatask.dev](https://javatask.dev/) 🔶 |
| 4 | Файл загружается в контекст **при каждом запросе**; «бюджет инструкций» ≈ **150–200 правил**; идеал — минимальный корневой файл + прогрессивное раскрытие | [aihero.dev](https://www.aihero.dev/a-complete-guide-to-agents-md) ✅ |
| 5 | В монорепозиториях — **вложенные файлы**; при конфликте побеждает ближайший к редактируемому файлу; явные промпты пользователя переопределяют всё | [agents.md](https://agents.md/) ✅ |
| 6 | Codex «читает AGENTS.md перед любой работой» и **автоматически запускает указанные тесты** | [agents.md](https://agents.md/) ✅, [learn.chatgpt.com](https://learn.chatgpt.com/) 🔶 |
| 7 | Опубликован OpenAI в **августе 2025**; за первые месяцы принят 60 000+ проектов | [datapanda.eu](https://datapanda.eu/) 🔶, [tango.ai](https://www.tango.ai/) 🔶, [cdomagazine.tech](https://www.cdomagazine.tech/) 🔶 |

---

## 2. Официальная спецификация

### 2.1 Сайт agents.md — первоисточник ✅

**URL:** <https://agents.md/>

Определение с сайта: *«A simple, open format for guiding coding agents, used by over 60k open-source projects. Think of AGENTS.md as a **README for agents**: a dedicated, predictable place to provide the context and instructions to help AI coding agents work on your project.»*

**Зачем отдельный файл от README:**
- README.md — для людей: quick start, описания проекта, contribution guidelines.
- AGENTS.md — дополнительный, иногда детальный контекст для агентов: шаги сборки, тесты, конвенции, которые захламили бы README или не важны людям.
- Разделение даёт: предсказуемое место для инструкций; лаконичные README; точные, агент-ориентированные указания.
- *«Rather than introducing another proprietary file, we chose a name and format that could work for anyone.»*

**Происхождение и управление:** *«AGENTS.md emerged from collaborative efforts across the AI software development ecosystem, including OpenAI Codex, Amp, Jules from Google, Cursor, and Factory… AGENTS.md is now stewarded by the **Agentic AI Foundation** under the **Linux Foundation**.»*

**Поддерживаемые агенты (перечислены на сайте):** Kilo Code, Zed, Gemini CLI (Google), Semgrep, Augment Code, Devin (Cognition), Windsurf (Cognition), opencode, Amp, Cursor, Factory, Coding agent (GitHub Copilot), Phoenix, Codex (OpenAI), Aider, RooCode, VS Code, goose, Jules (Google), Warp, Autopilot & Coded Agents (UiPath), Junie (JetBrains), Ona.

**Как использовать (4 шага с сайта):**
1. **Add AGENTS.md** — создать файл в корне репозитория; большинство агентов могут сгенерировать его по просьбе.
2. **Cover what matters** — популярные секции: project overview; build and test commands; code style guidelines; testing instructions; security considerations.
3. **Add extra instructions** — commit message и PR-правила, security-гоча, большие датасеты, шаги деплоя: *«anything you'd tell a new teammate belongs here too»*.
4. **Large monorepo? Use nested AGENTS.md files** — по файлу в каждом пакете; агент читает ближайший файл в дереве каталогов, ближайший имеет приоритет. *«For example, at time of writing the main OpenAI repo has 88 AGENTS.md files.»*

**FAQ с сайта (дословно по смыслу):**
- *Обязательные поля?* Нет. AGENTS.md — стандартный Markdown, любые заголовки; агент парсит предоставленный текст.
- *Конфликт инструкций?* Побеждает ближайший к редактируемому файлу AGENTS.md; явные промпты пользователя в чате переопределяют всё.
- *Запускает ли агент тесты автоматически?* Да — если они перечислены: *«The agent will attempt to execute relevant programmatic checks and fix failures before finishing the task.»*
- *Можно обновлять?* Да, *«Treat AGENTS.md as living documentation.»*
- *Миграция:* `mv AGENT.md AGENTS.md && ln -s AGENTS.md AGENT.md`
- *Aider:* в `.aider.conf.yml` → `read: AGENTS.md`
- *Gemini CLI:* в `.gemini/settings.json` → `{ "context": { "fileName": "AGENTS.md" }, }`

**Примеры репозиториев с сайта:** [openai/codex](https://github.com/) (Rust), [apache/airflow](https://github.com/) (Python), [temporalio/sdk-java](https://github.com/) (Java), [PlutoLang/Pluto](https://github.com/) (C++). Ссылка на 60k+ примеров на GitHub.

**Минимальный пример с сайта:**

```markdown
# AGENTS.md

## Setup commands
- Install deps: `pnpm install`
- Start dev server: `pnpm dev`
- Run tests: `pnpm test`

## Code style
- TypeScript strict mode
- Single quotes, no semicolons
- Use functional patterns where possible
```

**Пример для монорепо с сайта (pnpm/turbo/vitest, сокращённо):**

```markdown
# Sample AGENTS.md file

## Dev environment tips
- Use `pnpm dlx turbo run where <project_name>` to jump to a package instead of scanning with `ls`.
- Run `pnpm install --filter <project_name>` to add the package to your workspace.
- Check the name field inside each package's package.json — skip the top-level one.

## Testing instructions
- Find the CI plan in the .github/workflows folder.
- Run `pnpm turbo run test --filter <project_name>` for every check of that package.
- Fix any test or type errors until the whole suite is green.
- After moving files or changing imports, run `pnpm lint --filter <project_name>`.
- Add or update tests for the code you change, even if nobody asked.

## PR instructions
- Title format: [<project_name>] <Title>
- Always run `pnpm lint` and `pnpm test` before committing.
```

### 2.2 Документация OpenAI Codex 🔶

- [learn.chatgpt.com](https://learn.chatgpt.com/) — «Custom instructions with AGENTS.md» в пользовательских доках Codex: *«Codex reads AGENTS.md files before doing any work.»*
- [community.openai.com](https://community.openai.com/) — тред «AGENTS.md File Optimization - Codex» (декабрь 2025): обсуждение оптимизации файла пользователями Codex.

### 2.3 Governance и история принятия 🔶

- [openai.com](https://openai.com/) — «OpenAI co-founds the Agentic AI Foundation under…» (декабрь 2025): OpenAI соучреждает фонд.
- [cdomagazine.tech](https://www.cdomagazine.tech/) — «Agentic AI Foundation Launched to Advance Open…»: *«Since its release in August 2025, the format has been adopted by more than 60,000 open-source projects and tools, including Github Copilot, VS…»*
- [tango.ai](https://www.tango.ai/) — «Most AI Projects Fail for One Boring Reason: Documentation» (апрель 2026): *«OpenAI first created AGENTS.md, a project briefing file that agents consume on every run (over 60,000 projects adopted it within months).»*
- [datapanda.eu](https://datapanda.eu/) — словарная статья «Agent instruction file (AGENTS.md, llms.txt)»: *«AGENTS.md is the open standard: OpenAI published it in August 2025, The agents.md site counts more than 60,000 open source projects using one.»*
- [tomrochette.com](https://tomrochette.com/) — заметка «AGENTS.md»: *«Active and effectively the standard. The official site counts more than 60,000 open-source projects carrying an AGENTS.md as of 2026-09-13.»* Также: слой агентных инструкций — *«the file agents actually obey»* (о политике зависимостей).
- [windowsforum.com](https://windowsforum.com/) — «MCP AGENTS.md & goose for Safer Stacks»: принято 60 000+ проектов и агент-фреймворков с момента релиза в августе 2025.

---

## 3. Глубокие руководства

### 3.1 A Complete Guide To AGENTS.md — aihero.dev (Matt Pocock) ✅

**URL:** <https://www.aihero.dev/a-complete-guide-to-agents-md> (январь 2026, обновлено 18.01.2026)

Самое детальное практическое руководство. Ключевые положения:

**Позиция в контексте.** AGENTS.md — Markdown-файл в Git, настраивающий поведение агентов в репозитории; находится **вверху истории диалога, сразу под системным промптом**. Два типа указаний: personal scope (стиль коммитов, предпочитаемые паттерны) и project scope (что делает проект, менеджер пакетов, архитектурные решения). Открытый стандарт, поддерживаемый многими, но **не всеми** инструментами.

**Claude Code:** не использует AGENTS.md — использует CLAUDE.md. Симлинк для совместимости:

```bash
ln -s AGENTS.md CLAUDE.md
```

**Почему огромные файлы — проблема.**
1. Естественный цикл разрастания: агент сделал нежелательное → добавили правило → повторили сотни раз за месяцы → «ball of mud» («ком грязи»).
2. Разные разработчики добавляют конфликтующие мнения; никто не делает полную стилистическую вычитку — итог: неподдерживаемый мусор, **снижающий** качество работы агента.
3. Auto-generated файлы: *«Never use initialization scripts to auto-generate your AGENTS.md. They flood the file with things that are "useful for most scenarios" but would be better progressively disclosed. Generated files prioritize comprehensiveness over restraint.»*

**Бюджет инструкций.** Со ссылкой на Kyle из Humanlayer: *«Frontier thinking LLMs can follow ~150–200 instructions with reasonable consistency. Smaller models can attend to fewer instructions than larger models, and non-thinking models can attend to fewer instructions than thinking models.»* Каждый токен AGENTS.md загружается **в каждом запросе**, независимо от релевантности → чем меньше файл, тем больше токенов на задачу; раздутый файл = меньше токенов на работу + путаница агента.

**Устаревшая документация «отравляет» контекст.** Пути к файлам меняются постоянно: если в файле написано «authentication logic lives in `src/auth/handlers.ts`», а файл переименован — агент уверенно ищет в неправильном месте. **Вместо структуры документируйте возможности (capabilities)**: подсказки, где вещи *могут* быть, и общую форму проекта. Доменные концепции («organization» vs «group» vs «workspace») стабильнее путей — но и они дрейфуют.

**Абсолютный минимум корневого файла:**
1. **Одно предложение о проекте** (ролевой промпт). Пример: *«This is a React component library for accessible data visualization.»*
2. **Менеджер пакетов** (если не npm): *«This project uses pnpm workspaces.»* Или использовать corepack.
3. **Команды build/typecheck** (если нестандартные).

*«That's honestly it. Everything else should go elsewhere.»*

**Прогрессивное раскрытие (progressive disclosure).** Давать агенту только необходимое сейчас и указывать на ресурсы. Вместо десятков TypeScript-правил в AGENTS.md — вынести в отдельный файл:

```markdown
For TypeScript conventions, see docs/TYPESCRIPT.md
```

Лёгкий тон, без «always» и капса. Выгоды: правила TS грузятся только при работе с TS; другие задачи не тратят токены; файл сфокусирован и портируем между моделями. Можно вкладывать раскрытие глубже — дерево документов:

```text
docs/
├── TYPESCRIPT.md
│   └── references TESTING.md
├── TESTING.md
│   └── references specific test runners
└── BUILD.md
    └── references esbuild configuration
```

Можно ссылаться и на внешние ресурсы (документация Prisma, Next.js и т.п.) — агенты эффективно навигируют по таким иерархиям. **Agent Skills** — ещё одна форма прогрессивного раскрытия: знания подтягиваются только при необходимости.

**Монорепозитории.** Файлы в подкаталогах **сливаются с корневым**. Уровень root: цель монорепо, навигация по пакетам, общие инструменты (pnpm workspaces). Уровень пакета: цель пакета, конкретный стек, пакетные конвенции. *«Don't overload any level. The agent sees all merged AGENTS.md files in its context.»*

Корень:

```markdown
This is a monorepo containing web services and CLI tools.
Use pnpm workspaces to manage dependencies.
See each package's AGENTS.md for specific guidelines.
```

Пакет (`packages/api/AGENTS.md`):

```markdown
This package is a Node.js GraphQL API using Prisma.
Follow docs/API_CONVENTIONS.md for API design patterns.
```

**Промпт для рефакторинга «сломанного» AGENTS.md (дословно):**

```text
I want you to refactor my AGENTS.md file to follow progressive disclosure principles.
Follow these steps:
1. Find contradictions: Identify any instructions that conflict with each
   other. For each contradiction, ask me which version I want to keep.
2. Identify the essentials: Extract only what belongs in the root AGENTS.md:
   - One-sentence project description
   - Package manager (if not npm)
   - Non-standard build/typecheck commands
   - Anything truly relevant to every single task
3. Group the rest: Organize remaining instructions into logical categories
   (e.g., TypeScript conventions, testing patterns, API design, Git workflow).
   For each group, create a separate markdown file.
4. Create the file structure: Output:
   - A minimal root AGENTS.md with markdown links to the separate files
   - Each separate file with its relevant instructions
   - A suggested docs/ folder structure
5. Flag for deletion: Identify any instructions that are:
   - Redundant (the agent already knows this)
   - Too vague to be actionable
   - Overly obvious (like "write clean code")
```

**Правило «не строить ком грязи»:** корневой AGENTS.md — то, что релевантно **каждой** задаче репозитория; отдельный файл — для одного домена; вложенное дерево документов — для иерархии. *«The ideal AGENTS.md is small, focused, and points elsewhere.»*

### 3.2 Серия «Agentic AI» — javatask.dev 🔶

**URL:** <https://javatask.dev/> (сентябрь 2026)

Аналитическая серия статей об AGENTS.md:
- «How to Write an AGENTS.md That Works» (26.09.2026)
- «The Neutral-Standard Test: Why AGENTS.md Is a Standard, Not a Spec» (26.09.2026) — AGENTS.md — schema-less Markdown без грамматики и conformance-тестов, поэтому это **не формальная спецификация**.
- «Who Governs AGENTS.md Now» (26.09.2026)
- «Where AGENTS.md Came From» (26.09.2026)

### 3.3 Codex Starter Best Practices — Duke University 🔶

**URL:** <https://codex-best-practices-d67bea.pages.oit.duke.edu/> (серия Agentic April 2026; PDF: [duke-codex-best-practices-april-2026.pdf](https://codex-best-practices-d67bea.pages.oit.duke.edu/))

Руководство для новых пользователей Codex из 7 частей; Part 3 посвящена AGENTS.md:
- AGENTS.md — *«reusable instructions for a local Codex user profile, repository, or subdirectory. Think of it as a lightweight onboarding note»*.
- *«Use AGENTS.md files for always-on repository or account instructions that Codex should see throughout a session.»*
- Раскрывается: как Codex обнаруживает файлы инструкций; что относится к проектным инструкциям; разделение global / project / nested.
- Общая модель управления: разница между **enforceable controls и natural-language guidance**; как соотносятся промпты, конфиг, rules, AGENTS.md, skills, subagents.
- Part 4 (SKILL.md): инструкции под конкретную задачу; *«skills should be reviewed like software»*.
- Part 6 (Security): prompt-injection awareness, обработка секретов, sandbox-дефолты.

### 3.4 AGENTS.md Patterns: What Actually Changes — blakecrosley.com 🔶

**URL:** <https://blakecrosley.com/> (февраль 2026)

Ключевой тезис: **«Write operational policy, not human documentation. Include the specific shell commands, linter configs, and test commands the agent must run.»**

### 3.5 AGENTS.md Guide — Autohand Docs 🔶

**URL:** <https://docs.autohand.ai/>

Best practices: *«Keep it concise — AGENTS.md should be scannable. Aim for under 500 lines. If you need more detail, link to other docs. Keep it current.»*

### 3.6 What Is an AGENTS.md File? — kingy.ai 🔶

**URL:** <https://kingy.ai/> (май 2026)

*«An AGENTS.md file is a practical instruction sheet for AI coding agents. It tells Codex how the project works, what standards to follow, what commands to run…»* Метафора: «README для машин» — предсказуемое место для build-команд, инструкций тестирования, конвенций, архитектурных границ.

### 3.7 Прочие руководства 🔶

- [towardsdeeplearning.com](https://www.towardsdeeplearning.com/) — «I Followed the AI Coding Advice Everyone Recommends…» (август 2026): AGENTS.md в корне репозитория — кросс-тульный стандарт; сайт agents.md отчитывается о 60 000+ open-source проектов.
- [vibeide.dev](https://vibeide.dev/) — «AGENTS.md for Codex: setup, discovery and best practices» (сентябрь 2026): как Codex находит и комбинирует AGENTS.md-файлы, что в них писать, как держать один файл для Codex и Claude. См. также их блог: [How to review AI generated code](https://vibeide.dev/).
- [docs.qcode.cc](https://docs.qcode.cc/) — «Codex Complete Tutorial», секция 5.1 «Custom Instruction Files (AGENTS.md)»: файлы дают ИИ контекст проекта и спецификации работы. Документация доступна на русском.
- [vibecoding.cn](https://vibecoding.cn/) — «Guide the Codex with AGENTS.md»: документ проектного уровня для Codex — структура репозитория, команды, тесты, стили, правила дизайна, разрешения.
- [progressiverobot.com](https://www.progressiverobot.com/) — «AGENTS.md Support in Claude Code: A Simple, Powerful Fix» (сентябрь 2026): цитирует доку OpenAI — *«reads AGENTS.md files before doing any work»*.
- [lancecleveland.com](https://lancecleveland.com/) — «Improve Your AI Assisted Coding With AGENTS.md» (февраль 2026).
- [scriptbyai.com](https://www.scriptbyai.com/) — «AGENTS.md Guide: Format, Examples & Coding» (сентябрь 2026).
- [highcircl.com](https://www.highcircl.com/) — «What is AGENTS.md, and why Claude Code now reads it» (сентябрь 2026): обычный Markdown-файл в корне репо, сообщающий агенту то, что знает человек-контрибьютор.
- [design.dev](https://design.dev/) — «Context Engineering Guide — AI Coding Configuration»: полный гайд по контекст-инжинирингу для агентов — AGENTS.md, CLAUDE.md, Cursor rules, Copilot instructions.
- [getfivebucks.com](https://getfivebucks.com/) — «Ultimate Claude Code CLI Guide: 7 Steps to Setup in 2026» (апрель 2026).

---

## 4. Правила составления — сводка принципов

Синтез из [agents.md](https://agents.md/) ✅ и [aihero.dev](https://www.aihero.dev/a-complete-guide-to-agents-md) ✅:

1. **Минимализм корня.** Одно предложение о проекте + менеджер пакетов + нестандартные команды сборки. Остальное — в другие места.
2. **Бюджет инструкций.** ~150–200 правил для frontier thinking-моделей; меньше для меньших и не-thinking моделей. Каждый токен грузится в каждом запросе.
3. **Прогрессивное раскрытие.** Доменные правила (TypeScript, тесты, API-дизайн) — в отдельные файлы (`docs/TYPESCRIPT.md` и т.п.) со ссылками из корня; лёгкий разговорный тон ссылок.
4. **Возможности, а не пути.** Не документировать файловую структуру (быстро устаревает); описывать, где вещи *могут* быть, и доменные концепции.
5. **Операционная политика, не документация.** Конкретные shell-команды, конфиги линтеров, команды тестов ([blakecrosley.com](https://blakecrosley.com/) 🔶).
6. **Разрешение конфликтов.** Ближайший к редактируемому файлу AGENTS.md побеждает; явные промпты пользователя переопределяют всё.
7. **Тесты.** Перечислить команды — агент выполнит их и постарается исправить ошибки до завершения задачи.
8. **Объём.** До ~500 строк, сканируемость; детали — по ссылкам ([docs.autohand.ai](https://docs.autohand.ai/) 🔶).
9. **Живой документ.** Регулярно актуализировать; устаревшие данные «отравляют» контекст.
10. **Не авто-генерировать.** Init-скрипты затапливают файл «полезным для большинства» контентом вопреки принципу минимализма.
11. **Монорепо.** Вложенные файлы; корень — общее, пакет — своё; не перегружать ни один уровень (агент видит все слитые файлы).
12. **Полнота секций.** Всё, что сказали бы новому коллеге: commit/PR-правила, security-гоча, датасеты, деплой.

---

## 5. Рекомендуемые секции

**Из официальной спецификации** ([agents.md](https://agents.md/) ✅):
- Project overview
- Build and test commands
- Code style guidelines
- Testing instructions
- Security considerations
- Commit message / PR guidelines
- Security gotchas, большие датасеты, шаги деплоя

**Из шаблона agentsmd.net** ([agentsmd.net](https://agentsmd.net/) 🔶):
- Project Structure (для навигации агента: `/src`, `/components`, `/pages`, `/styles`, `/utils`, `/public`, `/tests`)
- Coding Conventions (общие + по фреймворкам: React, CSS)
- Testing Protocols (фреймворки, как запускать, требования)
- PR Guidelines (формат сообщений, обязательные проверки)

**Из Morph Spec 2026** ([morphllm.com](https://www.morphllm.com/) 🔶): рекомендованные секции + сравнение с CLAUDE.md и .cursorrules + схема frontmatter SKILL.md + копируемые шаблоны.

**Из blakecrosley.com** 🔶: конкретные shell-команды, конфиги линтеров, команды тестов.

---

## 6. Шаблоны и примеры

### 6.1 Официальные примеры ✅

См. раздел 2.1 — минимальный пример и пример монорепо (pnpm/turbo/vitest).

### 6.2 Шаблон agentsmd.net 🔶

**URL:** <https://agentsmd.net/> (май 2025)

Структура шаблона «Project Agents.md Guide for OpenAI Codex» (сокращённо):

```markdown
# Project Agents.md Guide for OpenAI Codex

## Project Structure for OpenAI Codex Navigation
- `/src`: Source code that OpenAI Codex should analyze
- `/components`: React components
- `/pages`: Next.js pages
- `/styles`: CSS and styling conventions
- `/utils`: Utility functions
- `/public`: Static assets (should not be modified directly)
- `/tests`: Test files to maintain and extend

## Coding Conventions for OpenAI Codex
### General Conventions
- Use TypeScript for all new code
- Follow the existing code style in each file
- Meaningful variable and function names
- Add comments for complex logic

### React Components Guidelines
- Functional components with hooks
- Keep components small and focused
- Proper prop typing
- File naming convention: PascalCase.tsx

### CSS/Styling Standards
[...]

## Testing Protocols
[фреймворки, команды, требования к тест-кейсам]

## PR Guidelines
[формат сообщений, обязательные проверки]
```

Файл размещается **в корне репозитория** для автоматического обнаружения.

### 6.3 Пример для C++ — gist Super-Genius 🔶

**URL:** <https://gist.github.com/Super-Genius/6b263b852949f99e572ecfdf3d23b886> (сентябрь 2026)

Продвинутый подход — «инженерные ограничения, а не чеклист»:

```markdown
## C++ Engineering Constraints
These are design constraints, not a checklist.
The **GNUS C++ Coding Standards are authoritative** for C++ syntax, naming,
layout, language use, class design, error handling, file layout, includes,
platform abstraction, and tooling. Do not override them with a general design
principle or a local preference.
When two design principles conflict, choose the option that creates the
lowest future cost **in this repository** while preserving correctness,
clarity, and the existing architecture.

### Core rule: refactor first, then change behavior
1. Make the smallest behavior-preserving refactor needed.
2. Run the relevant tests and verification.
3. Only then change behavior.
Do not mix a structural rewrite and a behavioral change into one diff when
they can be separated. A refactor must preserve observable behavior,
including error results, ordering, rounding, limits, ownership, lifetime,
serialization, protocol behavior, and thread-safety.
```

Плюс принципы: Separation of concerns; Encapsulation (минимальный полный публичный интерфейс); High cohesion, loose coupling; **DRY = один источник истины** (не абстрагировать只因 блоки похожи); KISS; Single responsibility; Depend on contracts, not implementation details; **YAGNI**.

### 6.4 Прочие коллекции примеров 🔶

- [deepseekartifacts.com](https://deepseekartifacts.com/) — «AGENTS.md Template: 7 Copy-Paste Examples for 2026» (сентябрь 2026); отмечает поддержку opencode: *«You can provide custom instructions to opencode by creating an AGENTS.md file.»*
- [devtoollab.com](https://devtoollab.com/) — «What Is AGENTS.md? Inside 24 Real Repos» (сентябрь 2026): анализ 24 реальных репозиториев.
- [github.com/bitrix-tools/best-practice](https://github.com/) — русскоязычный репозиторий конвенций с AGENTS.md и скиллом `add-rule-to-best-practice`.
- [github.com/microsoft/mcp-for-beginners](https://github.com/) — открытая учебная программа MCP с AGENTS.md в репозитории.

---

## 7. Монорепозитории и вложенность

- **Официально** ([agents.md](https://agents.md/) ✅): вложенные AGENTS.md в подкаталогах; агент читает ближайший файл; ближайший имеет приоритет; в главном репо OpenAI — **88 файлов** AGENTS.md.
- **aihero.dev** ✅: файлы подкаталогов **сливаются** с корневым; таблица «что куда»: root — цель монорепо, навигация по пакетам, общие инструменты; package — цель пакета, стек, конвенции. Не перегружать уровни.
- **pravda.systems** 🔶 ([The Agent-Native Stack](https://pravda.systems/), июль 2026): паттерн **solution-root** — координационный репозиторий с AGENTS.md, перечисляющим каждый репозиторий и его роль.
- **computingforgeeks.com** 🔶 ([The Complete .claude Directory Guide](https://computingforgeeks.com/), март 2026): вложенные CLAUDE.md для монорепо, лениво загружаемые — агент читает только нужный пакет.
- **skills.rest** 🔶 ([agents-md: Generate and maintain](https://skills.rest/)): поддержание CLAUDE.md и AGENTS.md в синхронизации в монорепо — обновление ссылок и аудит обоих файлов.

---

## 8. Сравнение форматов: AGENTS.md / CLAUDE.md / .cursorrules / SKILL.md

| Ресурс | Что говорит | Ссылка |
|---|---|---|
| menuagentic.com | «What actually separates AGENTS.md, CLAUDE.md, Cursor's .mdc rules and Agent Skills is **when their text enters the context window** — on every turn…» | [menuagentic.com](https://menuagentic.com/) 🔶 |
| buildthisnow.com | «Two context files, one codebase. How AGENTS.md and CLAUDE.md differ, what each one does, and how to use both without duplicating anything.» | [buildthisnow.com](https://www.buildthisnow.com/) 🔶 |
| getknack.ai | «AGENTS.md vs CLAUDE.md: Which One Should You Write?» + управление skills | [getknack.ai](https://getknack.ai/) 🔶 |
| aihero.dev | Claude Code читает CLAUDE.md, не AGENTS.md; симлинк `ln -s AGENTS.md CLAUDE.md` | [aihero.dev](https://www.aihero.dev/a-complete-guide-to-agents-md) ✅ |
| hackernoon.com | «AGENTS.md is the universal agent brief, CLAUDE.md adds Claude-specific instructions on top, Claude writes MEMORY.md.» | [hackernoon.com](https://hackernoon.com/) 🔶 |
| mdskills.ai | SKILL.md — открытый стандарт упаковки переиспользуемых инструкций для агентов | [mdskills.ai](https://www.mdskills.ai/) 🔶 |
| unite.ai | Фреймворк Skills Claude тихо становится индустрией; вписывается в стандартизацию вместе со спецификацией AGENTS.md от OpenAI | [unite.ai](https://www.unite.ai/) 🔶 |
| agensi.io | «The Quiet Standardization of AI Agent Skills» | [agensi.io](https://www.agensi.io/) 🔶 |
| spec-weave.com | «AGENTS.md vs CLAUDE.md: one instruction file for every» | [spec-weave.com](https://spec-weave.com/) 🔶 |
| dev.to | «CLAUDE.md, AGENTS.md, and Every AI Config File» (апрель 2026) | [dev.to](https://dev.to/) 🔶 |
| morphllm.com | Полное сравнение с .cursorrules + схема frontmatter SKILL.md | [morphllm.com](https://www.morphllm.com/) 🔶 |
| mcpmarket.com | «Agent Skill Anti-Pattern Guide» — почему skills не срабатывают | [mcpmarket.com](https://mcpmarket.com/) 🔶 |
| groff.dev | «Implementing CLAUDE.md and Agent Skills In Your…»: build-команды, архитектурные доки, детали конвенций; гайды агентов — приложения | [groff.dev](https://www.groff.dev/) 🔶 |

---

## 9. Реестры, генераторы и инструменты

- **AgentSpec / Open Agent Registry** ✅ — <https://agentspec.sh/>: реестр из **2 626** community-ресурсов: 22 конфига, **969 skills**, **1 634 rules**, 44 плагина, 1 спецификация. Браузер по категориям (Cursor 548, Claude Code 303, Windsurf 224, OpenCode/Codex 207, Copilot 156, Gemini 122, Cline 71). Десктоп-приложение (macOS) и CLI: `npm install -g agentspec-cli`; установка глобально или в один проект; бэкап существующих файлов.
- **skills.rest** 🔶 — <https://skills.rest/>: «agents-md: Generate and maintain» — генерация и поддержка файлов, синхронизация CLAUDE.md ↔ AGENTS.md.
- **scriptbyai.com** 🔶 — <https://www.scriptbyai.com/>: гайд по формату и примерам.
- **sourceforge.net** 🔶 — <https://sourceforge.net/> (сентябрь 2026): «agents.md download»; AGENTS.md как «README for agents» — предсказуемое структурированное место для инструкций, конвенций, build/…
- **forum.cursor.com** 🔶 — <https://forum.cursor.com/> (июнь 2026): генерация Project Rules (.mdc), AGENTS.md или legacy .cursorrules для Cursor IDE; 26+ шаблонов.
- **sureprompts.com** 🔶 — <https://www.sureprompts.com/>: «AGENTS.md: The Instruction File Every Coding…» (август 2026) + «Agent Skills Guide: How SKILL.md Works».
- **AgentSpec вagents.md экосистеме**: трендовые skills в реестре — find-skills, frontend-design, web-design-guidelines, agent-browser и др.

---

## 10. Русскоязычные материалы

| Ресурс | Название | Что содержит | Ссылка |
|---|---|---|---|
| Neaptide | «AGENTS.md: как объяснить ИИ-агенту правила проекта» | Как составить AGENTS.md: какие правила записать, куда поместить файл, как проверить выполнение в Codex; шаблон для скачивания | [neaptide.ai](https://www.neaptide.ai/) 🔶 |
| Хабр | «ADSM: практика использования файлов AGENTS.md» (декабрь 2025) | Практика использования; фокус на структуре, правилах и ответственности | [habr.com](https://habr.com/) 🔶 |
| ip-calculator.ru | «AGENTS.md: файл-конвенций, который понимают все AI-агентов» | Обзор концепции AGENTS.md как файла конвенций | [ip-calculator.ru](https://ip-calculator.ru/) 🔶 |
| QCode Docs | «Codex Complete Tutorial» (секция 5.1) | Custom Instruction Files (AGENTS.md); документация на русском | [docs.qcode.cc](https://docs.qcode.cc/) 🔶 |
| minibase.md | «Autoresearch Карпаты и PROGRAM.md» (март 2026) | Разработчики пишут AGENTS.md для кодинга; исследователи — program.md для экспериментов | [minibase.md](https://www.minibase.md/) 🔶 |
| bitrix-tools | AGENTS.md в русскоязычном репозитории best-practice | Конвенции + скилл добавления правил | [github.com](https://github.com/) 🔶 |

## 11. Китайские материалы

- [zhuanlan.zhihu.com](https://zhuanlan.zhihu.com/) — «AGENTS.md 完整指南» (август 2026): *«AGENTS.md — Markdown-файл, коммитиимый в Git-репозиторий; настраивает поведение AI-агентов в проекте; находится между универсальными инструкциями агента и кодом проекта»*.
- [kilo.org.cn](https://kilo.org.cn/) — «Agents.md — Kilo Code 智能体»: AGENTS.md даёт **стандартизированный способ** настройки поведения ИИ-агентов между разными AI-инструментами кодинга; определение проектных инструкций, стандартов и гайдлайнов.

---

## 12. Исследования и аналитика

- **arxiv.org** 🔶 — <https://arxiv.org/> — «Evaluating AGENTS.md: Are Repository-Level Context Files…» (12 февраля 2026): научная оценка влияния файлов уровня репозитория на поведение агентов. ⚠️ Аннотация не прочитана — требуется дочитывание.
- **datapanda.eu** 🔶 — <https://datapanda.eu/> — словарная статья «Agent instruction file (AGENTS.md, llms.txt)»: хронология и статус стандарта.
- **tomrochette.com** ✅ (частично) — <https://tomrochette.com/> — заметки об AGENTS.md: статус стандарта; AGENTS.md как слой, который агенты реально исполняют (пример — политика Dependabot-PR: *«"Dependency pull requests: security alerts only, otherwise close with a pointer to the maintenance policy" is a sentence an agent can execute.»*).
- **tango.ai** 🔶 — <https://www.tango.ai/> — «Most AI Projects Fail for One Boring Reason: Documentation»: AGENTS.md как проектный брифинг, потребляемый агентом при каждом запуске.
- **tianpan.co** 🔶 — <https://tianpan.co/> — «The Documentation Renaissance: Your README Is the Agent's…».
- **innfactory.ai** 🔶 — <https://innfactory.ai/> — «Codex: OpenAI's Coding Agent as an AI Harness» (сентябрь 2026).
- **gist karpathy «llm-wiki»** 🔶 — <https://gist.github.com/karpathy> — смежная концепция: паттерн личной базы знаний LLM (LLM wiki), копируемый в Codex/Claude Code/OpenCode.

---

## 13. Критика и антипаттерны

| Проблема | Описание | Источник |
|---|---|---|
| «Хаос файлов правил» | Разрозненные форматы конфигов агентов, дублирование и рассинхрон | [dev.to — We Need to Talk About AI Agent Rule File Chaos](https://dev.to/) (июль 2025) 🔶 |
| Проблема синхронизации | «Each one has its own md file in its own format. CLAUDE.md, AGENTS.md, .cursorrules, GEMINI.md. Four files saying roughly the same thing, four chances to get [it wrong]» | [news.ycombinator.com — Show HN: I got tired of syncing Claude/Gemini/AGENTS](https://news.ycombinator.com/) 🔶 |
| Давление на вендоров | «Big projects should have a lot of nested AGENTS.md files… they simply need to add support for the universal standard» | [news.ycombinator.com — Hey Anthropic, how about you use AGENTS.md for one thing](https://news.ycombinator.com/) 🔶 |
| «Configuration smells» | Типичные ошибки конфигурационных файлов ИИ-агентов | [digitalapplied.com](https://www.digitalapplied.com/) 🔶 |
| no-agents.md | Файл, запрещающий AI в кодовой базе (обратная сторона стандарта) | [korben.info](https://korben.info/) (март 2026) 🔶 |
| Фрагментация дизайн-системы | Дизайн-система распадается на агентные файлы | [blog.murphytrueman.com](https://blog.murphytrueman.com/) (май 2026) 🔶 |
| Ball of mud | Цикл «агент ошибся → добавил правило» превращает файл в неподдерживаемый ком, снижающий качество агента | [aihero.dev](https://www.aihero.dev/a-complete-guide-to-agents-md) ✅ |
| Отравление контекста | Устаревшие пути к файлам → агент уверенно ищет не туда; данные читаются каждый запрос | [aihero.dev](https://www.aihero.dev/a-complete-guide-to-agents-md) ✅ |
| Авто-генерация | Init-скрипты затапливают файл «универсально полезным» контентом | [aihero.dev](https://www.aihero.dev/a-complete-guide-to-agents-md) ✅ |

---

## 14. Чеклист составления AGENTS.md

**Минимум корневого файла** (по [aihero.dev](https://www.aihero.dev/a-complete-guide-to-agents-md) ✅):

```markdown
This is a <одно предложение о проекте>.
This project uses <менеджер пакетов, если не npm>.
Build: <нестандартная команда сборки/typecheck>.
```

**Типовые секции** (по [agents.md](https://agents.md/) ✅):

```markdown
# AGENTS.md

## Project overview
<1–3 предложения: что это, зачем, роль агента>

## Setup commands
- Install deps: `pnpm install`
- Start dev server: `pnpm dev`
- Run tests: `pnpm test`

## Code style
- <языковые конвенции; ссылки на docs/<LANG>.md>

## Testing instructions
- <какие команды запускать; критерий зелёного>

## PR instructions
- Title format: [<scope>] <Title>
- Always run `pnpm lint` and `pnpm test` before committing.

## Security considerations
- <гоча, секреты, что не трогать>
```

**Проверка перед коммитом файла:**
- [ ] Релевантно **каждой** задаче репозитория? Если нет — в отдельный файл.
- [ ] Конкретные команды (lint/test/build), а не абстракции?
- [ ] Возможности, а не пути к файлам?
- [ ] < 500 строк и сканируемо?
- [ ] Без «always», капса и очевидностей («пиши чистый код»)?
- [ ] Не авто-сгенерирован init-скриптом?
- [ ] Для монорепо: корень — общее, пакеты — своё, уровни не перегружены?
- [ ] Тест-команды перечислены (агент запустит их автоматически)?
- [ ] Конфликты с вложенными файлами разрешены (ближайший побеждает)?

---

## 15. Полный список источников

### Официальные и первоисточники
1. [agents.md — официальный сайт стандарта](https://agents.md/) ✅ — спецификация, FAQ, примеры, список агентов, миграция, конфиги Aider/Gemini CLI.
2. [learn.chatgpt.com — OpenAI Codex user docs, «Custom instructions with AGENTS.md»](https://learn.chatgpt.com/) 🔶.
3. [community.openai.com — «AGENTS.md File Optimization - Codex»](https://community.openai.com/) 🔶 (декабрь 2025).
4. [openai.com — «OpenAI co-founds the Agentic AI Foundation»](https://openai.com/) 🔶 (декабрь 2025).
5. [cdomagazine.tech — «Agentic AI Foundation Launched»](https://www.cdomagazine.tech/) 🔶 (декабрь 2025) — 60k+ с августа 2025.
6. [windowsforum.com — «MCP AGENTS.md & goose for Safer Stacks»](https://windowsforum.com/) 🔶 (декабрь 2025).
7. [tango.ai — «Most AI Projects Fail for One Boring Reason: Documentation»](https://www.tango.ai/) 🔶 (апрель 2026).
8. [datapanda.eu — «Agent instruction file (AGENTS.md, llms.txt)»](https://datapanda.eu/) 🔶 (сентябрь 2026).
9. [tomrochette.com — заметка «AGENTS.md»](https://tomrochette.com/) ✅/🔶 (сентябрь 2026).

### Руководства (глубокие)
10. [aihero.dev — «A Complete Guide To AGENTS.md» (Matt Pocock)](https://www.aihero.dev/a-complete-guide-to-agents-md) ✅ (январь 2026) — progressive disclosure, бюджет инструкций, монорепо, промпт рефакторинга.
11. [aihero.dev — «My AGENTS.md file for building plans you actually read»](https://www.aihero.dev/) ✅ (оглавление).
12. [javatask.dev — серия «Agentic AI»](https://javatask.dev/) 🔶 (сентябрь 2026) — 4 статьи: How to Write / Standard-not-Spec / Who Governs / Where It Came From.
13. [codex-best-practices-d67bea.pages.oit.duke.edu — Codex Starter Best Practices, Part 3: AGENTS.md](https://codex-best-practices-d67bea.pages.oit.duke.edu/) 🔶 (2026) + [PDF](https://codex-best-practices-d67bea.pages.oit.duke.edu/).
14. [blakecrosley.com — «AGENTS.md Patterns: What Actually Changes»](https://blakecrosley.com/) 🔶 (февраль 2026).
15. [docs.autohand.ai — «AGENTS.md Guide»](https://docs.autohand.ai/) 🔶 — <500 строк, актуальность.
16. [kingy.ai — «What Is an AGENTS.md File?»](https://kingy.ai/) 🔶 (май 2026).
17. [towardsdeeplearning.com — «I Followed the AI Coding Advice Everyone Recommends…»](https://www.towardsdeeplearning.com/) 🔶 (август 2026).
18. [vibeide.dev — «AGENTS.md for Codex: setup, discovery and best practices»](https://vibeide.dev/) 🔶 (сентябрь 2026) + [блог о ревью AI-кода](https://vibeide.dev/).
19. [docs.qcode.cc — «Codex Complete Tutorial» (5.1 Custom Instruction Files)](https://docs.qcode.cc/) 🔶 — рус. версия.
20. [vibecoding.cn — «Guide the Codex with AGENTS.md»](https://vibecoding.cn/) 🔶.
21. [progressiverobot.com — «AGENTS.md Support in Claude Code»](https://www.progressiverobot.com/) 🔶 (сентябрь 2026).
22. [lancecleveland.com — «Improve Your AI Assisted Coding With AGENTS.md»](https://lancecleveland.com/) 🔶 (февраль 2026).
23. [scriptbyai.com — «AGENTS.md Guide: Format, Examples & Coding»](https://www.scriptbyai.com/) 🔶 (сентябрь 2026).
24. [highcircl.com — «What is AGENTS.md, and why Claude Code now reads it»](https://www.highcircl.com/) 🔶 (сентябрь 2026).
25. [design.dev — «Context Engineering Guide — AI Coding Configuration»](https://design.dev/) 🔶.

### Шаблоны и примеры
26. [agentsmd.net — «Professional Agents.md Example Template»](https://agentsmd.net/) 🔶 (май 2025).
27. [gist.github.com/Super-Genius — AGENTS.md (C++ Engineering Constraints)](https://gist.github.com/Super-Genius/6b263b852949f99e572ecfdf3d23b886) 🔶 (сентябрь 2026).
28. [deepseekartifacts.com — «AGENTS.md Template: 7 Copy-Paste Examples for 2026»](https://deepseekartifacts.com/) 🔶 (сентябрь 2026).
29. [devtoollab.com — «What Is AGENTS.md? Inside 24 Real Repos»](https://devtoollab.com/) 🔶 (сентябрь 2026).
30. [github.com — openai/codex, apache/airflow, temporalio/sdk-java, PlutoLang/Pluto](https://github.com/) ✅ (со страницы agents.md).
31. [github.com/bitrix-tools/best-practice — AGENTS.md](https://github.com/) 🔶 (русскоязычный).
32. [github.com/microsoft/mcp-for-beginners](https://github.com/) 🔶.

### Сравнение форматов
33. [menuagentic.com — «AGENTS.md vs CLAUDE.md vs Cursor rules vs Agent Skills»](https://menuagentic.com/) 🔶 (сентябрь 2026).
34. [buildthisnow.com — «AGENTS.md vs CLAUDE.md Explained»](https://www.buildthisnow.com/) 🔶 (апрель 2026).
35. [getknack.ai — «AGENTS.md vs CLAUDE.md: Which One Should You Write?»](https://getknack.ai/) 🔶 (май 2026).
36. [morphllm.com — «AGENTS.md Spec (2026): Recommended Sections»](https://www.morphllm.com/) 🔶 (июнь 2026).
37. [spec-weave.com — «AGENTS.md vs CLAUDE.md: one instruction file for every»](https://spec-weave.com/) 🔶 (сентябрь 2026).
38. [hackernoon.com — «The Complete Guide to AI Agent Memory Files (CLAUDE…)»](https://hackernoon.com/) 🔶 (февраль 2026).
39. [mdskills.ai — «What is SKILL.md? The Open Standard for AI Agent Skills»](https://www.mdskills.ai/) 🔶 (март 2026).
40. [unite.ai — «Claude's Skills Framework Quietly Becomes an Industry»](https://www.unite.ai/) 🔶 (декабрь 2025).
41. [agensi.io — «The Quiet Standardization of AI Agent Skills»](https://www.agensi.io/) 🔶 (апрель 2026).
42. [dev.to — «CLAUDE.md, AGENTS.md, and Every AI Config File»](https://dev.to/) 🔶 (апрель 2026).
43. [mcpmarket.com — «Agent Skill Anti-Pattern Guide»](https://mcpmarket.com/) 🔶.
44. [groff.dev — «Implementing CLAUDE.md and Agent Skills In Your…»](https://www.groff.dev/) 🔶 (февраль 2026).
45. [sureprompts.com — «AGENTS.md: The Instruction File Every Coding…» / «Agent Skills Guide: How SKILL.md Works»](https://sureprompts.com/) 🔶 (август 2026).

### Реестры, генераторы, инструменты
46. [agentspec.sh — AgentSpec / Open Agent Registry](https://agentspec.sh/) ✅ — 2 626 ресурсов; CLI `npm install -g agentspec-cli`.
47. [skills.rest — «agents-md: Generate and maintain»](https://skills.rest/) 🔶.
48. [sourceforge.net — «agents.md download»](https://sourceforge.net/) 🔶 (сентябрь 2026).
49. [forum.cursor.com — «Best way to integrate Cursor into an existing VS Code repo»](https://forum.cursor.com/) 🔶 (июнь 2026).
50. [computingforgeeks.com — «The Complete .claude Directory Guide for Claude Code»](https://computingforgeeks.com/) 🔶 (март 2026).
51. [getfivebucks.com — «Ultimate Claude Code CLI Guide»](https://getfivebucks.com/) 🔶 (апрель 2026).

### Русскоязычные
52. [neaptide.ai — «AGENTS.md: как объяснить ИИ-агенту правила проекта»](https://www.neaptide.ai/) 🔶.
53. [habr.com — «ADSM: практика использования файлов AGENTS.md»](https://habr.com/) 🔶 (декабрь 2025).
54. [ip-calculator.ru — «AGENTS.md: файл-конвенций, который понимают все AI-агенты»](https://ip-calculator.ru/) 🔶.
55. [minibase.md — «Autoresearch Карпаты и PROGRAM.md»](https://www.minibase.md/) 🔶 (март 2026).

### Китайские
56. [zhuanlan.zhihu.com — «AGENTS.md 完整指南»](https://zhuanlan.zhihu.com/) 🔶 (август 2026).
57. [kilo.org.cn — «Agents.md — Kilo Code 智能体»](https://kilo.org.cn/) 🔶.

### Исследования
58. [arxiv.org — «Evaluating AGENTS.md: Are Repository-Level Context Files…»](https://arxiv.org/) 🔶 (12 февраля 2026).

### Критика
59. [dev.to — «We Need to Talk About AI Agent Rule File Chaos»](https://dev.to/) 🔶 (июль 2025).
60. [dev.to — «Claude Code now supports AGENTS.md Natively»](https://dev.to/) 🔶 (сентябрь 2026).
61. [news.ycombinator.com — «Show HN: I got tired of syncing Claude/Gemini/AGENTS…»](https://news.ycombinator.com/) 🔶.
62. [news.ycombinator.com — «Hey Anthropic, how about you use AGENTS.md for one thing»](https://news.ycombinator.com/) 🔶.
63. [digitalapplied.com — «Configuration Smells: Fix Your AI Agent Config Files»](https://www.digitalapplied.com/) 🔶 (июнь 2026).
64. [korben.info — «no-agents.md — The file that says no to AI in your code»](https://korben.info/) 🔶 (март 2026).
65. [blog.murphytrueman.com — «Your design system is fragmenting into agent files»](https://blog.murphytrueman.com/) 🔶 (май 2026).

### Прочее / смежное
66. [pravda.systems — «The Agent-Native Stack: What to Standardize On When AI…»](https://pravda.systems/) 🔶 (июль 2026) — solution-root паттерн.
67. [tianpan.co — «The Documentation Renaissance»](https://tianpan.co/) 🔶.
68. [innfactory.ai — «Codex: OpenAI's Coding Agent as an AI Harness»](https://innfactory.ai/) 🔶 (сентябрь 2026).
69. [gist.github.com/karpathy — «llm-wiki»](https://gist.github.com/karpathy) 🔶 (апрель 2026).

---

## 16. Открытые вопросы (для следующей итерации)

1. **Прочитать полностью** статьи серии javatask.dev (4 шт.) — в поиске видны только заголовки.
2. **Прочитать** полную спецификацию Morph ([morphllm.com](https://www.morphllm.com/)): рекомендованные секции, схема frontmatter SKILL.md, сравнительная таблица.
3. **Прочитать** аннотацию arxiv-статьи «Evaluating AGENTS.md…» и извлечь выводы о реальной эффективности.
4. **Скачать шаблон** Neaptide (русскоязычный) и 7 примеров deepseekartifacts.
5. **Изучить** разбор 24 реальных репозиториев (devtoollab.com) для паттернов.
6. **Проверить** актуальный список поддерживаемых агентов на [agents.md](https://agents.md/) (страница обновляется).
7. **Изучить** серию Duke (Parts 1–6 полностью, включая SKILL.md и Security Basics).
8. **Изучить** HN-обсуждения (sync-проблема, «Hey Anthropic») для понимания болевых точек сообщества.

---

*Документ собран из открытых интернет-источников; факты приведены со ссылками на первоисточники. Пункты с 🔶 требуют верификации полным чтением.*
