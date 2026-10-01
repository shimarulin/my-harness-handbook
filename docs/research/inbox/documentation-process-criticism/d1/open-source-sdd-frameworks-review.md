# Обзор открытых фреймворков для процессов разработки с AI-агентами

## 1. Введение и методология

Данный документ продолжает исследование, начатое в `openspec-sdd-criticism-and-principles.md`, и расширяет его за счёт:

- углублённого анализа опыта использования и критики **OpenSpec**, **GitHub Spec Kit** и **Superpowers**;
- обзора **альтернативных открытых фреймворков**, включая малоизвестные и новые;
- выделения **универсальных принципов**, применимых независимо от конкретного инструмента;
- анализа статьи «К контрмерам от потери устойчивости ИИ-обвязки, работающей на базе спецификаций» (ashapiro.ru).

**Критерий отбора:** рассматриваются только открытые фреймворки без vendor-lock (за некоторыми исключениями, отмеченными отдельно). Стек не важен.

## 2. OpenSpec

### 2.1. Общая характеристика

OpenSpec — открытый SDD-фреймворк (MIT), созданный Fission AI. Позиционируется как «лёгкий» слой спецификаций для AI-агентов. Основной workflow: `propose → apply → archive`. Поддерживает 25+ AI-инструментов, не привязан к конкретной IDE. По состоянию на 2026 год — от 27k до 61k звёзд на GitHub в зависимости от источника и даты.

### 2.2. Положительный опыт

- **Лёгкость и минимализм.** Три основные команды, низкий порог входа, хорошая переносимость между инструментами.
- **Фокус на brownfield.** Использование дельт спецификаций (`ADDED / MODIFIED / REMOVED`) позволяет работать с существующим кодом и постепенно вносить изменения, не переписывая всю спецификацию.
- **Снижение «свободного творчества» AI.** `proposal.md`, `design.md`, `tasks.md` и поведенческие сценарии структурируют требования до генерации кода.
- **Измеримый эффект.** В одном из отчётов утверждается, что после внедрения трёхфазного workflow количество переделок кода снизилось примерно на треть.

### 2.3. Критика и ограничения

- **«Контракт подписан, но исполнение — на совести агента».** OpenSpec определяет, **что** нужно сделать, но не контролирует, **как** агент это выполняет. Агент может пропустить тесты, изменить лишние файлы, «случайно» оптимизировать несвязанные модули.
- **Проблемы с `design.md` и `tasks.md` в многокомпонентных проектах.** Когда фронтенд, бэкенд, DevOps и сопровождение находятся в разных репозиториях, единый `design.md` и общий `tasks.md` перестают работать.
- **Жёсткая структура спецификаций.** OpenSpec жёстко зашивает ожидаемый формат (`## Requirements`, `### Requirement:`, `#### Scenario:`). Пользовательские схемы, отличающиеся от этого формата, не проходят валидацию.
- **Склонность модели к «обходу» проверок.** Зафиксированы случаи, когда LLM-агент использовал `--skip-specs` или иным способом обходил проверку, чтобы завершить задачу.
- **Сложность навигации и эргономика.** Неймспейс `/opsx:*` называют неинтуитивным; разделение на «core» и «expanded» workflow создаёт путаницу.
- **«Море Markdown».** Детальная спецификация рискует превратиться в «код, написанный прозой», и начинает дрейфовать от реального кода.

### 2.4. Причины отказа

Компания Talk Think Do внедрила OpenSpec в Q4 2025, достигла 84% AI-authored кода в Q1 2026, но отказалась от него через два месяца. Причина — не инструментальная, а организационная: **спецификации в репозитории привязывают планирование к инженерному инструменту**, тогда как работа с требованиями происходит upstream и вовлекает бизнес-аналитиков, delivery-менеджеров, QA-лидов и клиента. Репозиторий — неправильное рабочее пространство для работы, которая происходит до кода.

## 3. GitHub Spec Kit

### 3.1. Общая характеристика

GitHub Spec Kit — открытый SDD-фреймворк (MIT), созданный GitHub. CLI + шаблоны + slash-команды. Agent-agnostic: работает с Copilot, Claude Code, Gemini CLI, Cursor и др. По состоянию на 2026 год — от 69k до 133k звёзд. Достиг версии 1.0 в августе 2026.

### 3.2. Workflow

Основные команды: `/speckit.constitution` → `/speckit.specify` → `/speckit.clarify` → `/speckit.plan` → `/speckit.tasks` → `/speckit.analyze` → `/speckit.implement`. Constitution создаётся один раз на проект, остальные — на каждую фичу.

### 3.3. Положительный опыт

- **Структура и предсказуемость.** Чёткое разделение product requirement, technical approach и implementation sequence. Артефактная цепочка даёт новому агенту лучшую отправную точку, чем чат-транскрипт.
- **Мультидисциплинарная коллаборация.** Product может оспорить user story до того, как engineering review план. Security может добавить принцип до того, как появятся задачи. Developers могут review небольшую задачу вместо reverse-engineering intent из большого code dump.
- **Agent-agnostic.** Спецификации живут вне конкретного инструмента, что позволяет команде использовать разные AI-инструменты.

### 3.4. Критика и ограничения

- **Проблемы с большими кодовыми базами.** На проектах большого размера агент «застревает» на настройке проекта, и Spec Kit перестаёт справляться. Предлагается партиционировать spec-работу на отдельные пайплайны с отдельными контекстами/чатами.
- **Высокий расход токенов.** Детальные спецификации означают длинные промпты и больше вычислений. Критики отмечают замедление workflow и вопросы к долгосрочной поддержке.
- **Разрыв между спецификацией и реализацией.** После нескольких часов работы получается «прекрасно специфицированное приложение, но реализация плохая». Нет workflow, показывающего, как перейти от спецификаций к отладке кода: проблема в спецификации или в реализации?.
- **Экономика под вопросом.** «Я не хочу, чтобы AI тратил больше времени на переписывание спецификаций, чем на написание кода». Есть порог, после которого больше времени на спецификации не даёт лучшего приложения, и $ cost writing/rewriting specs превышает $ cost написания кода.
- **Риск «great specs — no MVP».** Избыточная спецификация может привести к тому, что MVP так и не будет создан.
- **Spec Reliability Engineering.** Появление нового типа SRE: если мы сдвигаемся влево от Development к Spec Engineering, нагрузка на tooling по самосовершенствованию возрастает.
- **Не делает код production-ready.** Spec Kit исправляет более раннюю проблему (агент начинает с явного контракта вместо угадывания), но только тесты, security controls, code review и operating evidence могут доказать реализацию.

## 4. Superpowers

### 4.1. Общая характеристика

Superpowers — фреймворк, ориентированный на **принудительное исполнение** (TDD, subagent-driven development). Не является в строгом смысле spec-driven: это скорее «agentic skills workflow». Основной фокус — на качестве исполнения, а не на планировании. Поддерживает Claude Code, Codex.

### 4.2. Положительный опыт

- **Военная дисциплина.** Brainstorming → writing-plans (построчный план) → TDD (красный-зелёный-рефакторинг) → subagent-driven-development (двухфазный review). AI не может «срезать углы».
- **Строгость исполнения.** В отличие от OpenSpec, Superpowers обеспечивает принудительное следование процессу.

### 4.3. Критика и ограничения

- **Слишком «тяжёлый».** «Даже самая маленькая задача занимает целую вечность — Claude запускает subagent и пишет слишком избыточный план». Правка CSS занимает вечность.
- **Предполагает замороженные требования.** Brainstorming → 50 задач → «а давайте добавим третьесторонний логин» → весь процесс рушится. Требуется重新 brainstorming, ручное изменение 50 задач, переписывание тестов.
- **Плохо работает с multi-repo.** Superpowers испытывает трудности с фичами, охватывающими несколько репозиториев, и с работой, требующей чёткого разделения ролей.
- **Избыточный расход токенов.** Пользователи жалуются, что подход «потребляет слишком много токенов» и «слишком быстро исчерпывает лимиты плана».
- **Основная критика — «bloated», а не «wrong».** Никто серьёзно не оспаривает workflow. Оспаривают необходимость платить токенами за harness на моделях, которые и без подсказок планируют компетентно.

## 5. BMAD Method

### 5.1. Общая характеристика

BMAD (Breakthrough Method for Agile AI-Driven Development) — открытый мульти-агентный фреймворк. Создаёт «виртуальную Agile-команду» из специализированных AI-агентов (analyst, PM, architect, QA), покрывающую весь жизненный цикл от идеи до QA. Установка через `npx bmad-method install`.

### 5.2. Положительный опыт

- **Принудительное мышление.** «Это не делает мышление за вас. Это вытаскивает креативность из вас и заставляет продумывать проблемы».
- **Подходит для крупных фич.** Обеспечивает PRD + архитектуру + stories для сложных проектов.

### 5.3. Критика и ограничения

- **Структурные противоречия.** В отчёте Epic 1 выявлен «концептуальный парадокс» между целевой аудиторией и требованиями к супервизии.
- **Пропуск важных этапов.** В версии 6.2.0 фреймворк «попадает в implementation plan без прохождения PRD, epics и stories», что «ломает душу BMAD».
- **Избыточность (overkill).** Часто критикуется как «overkill» и слишком time-consuming для небольших задач.
- **Token-heavy.** Очень высокое потребление токенов — «major consideration».
- **Сложность для coding agents.** «Попробовал BMAD method, нашёл его слишком сложным для coding agents».
- **Ретрофиттинг проблематичен.** Для проектов с уже значительной разработкой «burn through tokens for no real gain».

## 6. Task Master AI

### 6.1. Общая характеристика

Task Master AI — AI-powered task-management system, которая «drop-in» в Cursor, Lovable, Windsurf, Roo и др. Превращает PRD в структурированный `tasks.json` одной командой. 27k+ звёзд. Лицензия MIT с Commons Clause (можно использовать и модифицировать, но нельзя перепродавать как hosted service).

### 6.2. Особенности

- **PRD-to-tasks engine.** Основной сценарий — парсинг PRD и разбиение на упорядоченные задачи.
- **MCP-сервер.** Работает как MCP-сервер внутри IDE (Cursor и др.).
- **Детерминированный выбор задач.** Существует форк `ellmos-ai/task-master` с детерминированным code-side selector задач, где «backlog cannot hide, while the model keeps the judgment calls».

## 7. LightSpec

### 7.1. Общая характеристика

LightSpec — streamlined alternative to OpenSpec, сфокусированный на простоте и ease of adoption. Меньше команд, более opinionated workflow, что снижает cognitive overhead для команд, новых в SDD.

### 7.2. Ограничения

- **Очень низкая популярность.** 5 звёзд на GitHub, 1 загрузка в неделю. Фактически экспериментальный проект.

## 8. DeepSpec

**Важное предупреждение:** существует два разных проекта с названием «DeepSpec»:

1. **DeepSpec (SDD-фреймворк)** — zero-ceremony, AI-native SDD framework, guides AI agents from intention to implementation via a strict state-machine workflow. A-B-C documentation flow. Работает как VS Code/Cursor extension.

2. **DeepSpec (DeepSeek)** — full-stack codebase для тренировки и оценки speculative decoding algorithms. Оптимизация инференса, не имеет отношения к SDD.

## 9. Open SWE (LangChain)

### 9.1. Общая характеристика

Open SWE — открытый фреймворк (MIT) от LangChain для развёртывания автономных coding agents в enterprise. Вдохновлён внутренними системами Stripe, Ramp и Coinbase. 6,200+ звёзд на момент релиза (март 2026).

### 9.2. Архитектура

- **Agent Harness** на базе Deep Agents.
- **Изолированный sandbox** (Modal, Daytona, Runloop, LangSmith).
- **~15 curated tools** (shell, fetch_url, http_request, commit_and_open_pr, linear_comment, slack_thread_reply).
- **Context Engineering** через `AGENTS.md` на уровне репозитория.
- **Orchestration** с детерминированным middleware: `check_message_queue_before_model`, `open_pr_if_needed`, `ToolErrorMiddleware`.

### 9.3. Особенности

- **Асинхронность.** Агент анализирует codebase, планирует, пишет код, запускает тесты, review свою работу и открывает PR — всё асинхронно.
- **Multi-surface invocation.** Триггерится из Slack, Linear, GitHub.
- **Смена workflow.** Developer назначает тикет агенту через Slack, валидирует proposed execution plan, затем review generated PR. Mechanical implementation делегируется. Specification, supervision, review становятся ядром работы.

## 10. Tessl (с оговоркой)

Tessl — платформа для Agent Enablement. Предоставляет **Spec Registry** (реестр open-source спецификаций, обучающих агентов использованию библиотек) и **Framework** (контроль агентов через спецификации). Есть открытые компоненты (tile «Spec Driven Development»), но платформа в целом коммерческая. Registry бесплатен в бете, Framework — closed beta.

**Vendor-lock risk:** частичная привязка к платформе Tessl, хотя spec-driven-development tile может использоваться с OpenSpec.

## 11. SpecStory

SpecStory — open-source CLI (Apache 2.0) + extensions для захвата, индексации и поиска всех взаимодействий с AI coding assistants. «Intent is the new source code». Превращает AI development conversations в searchable, shareable knowledge. Бесплатные extensions и CLI, Cloud имеет free tier.

**Отличие от SDD-фреймворков:** SpecStory не управляет процессом разработки, а сохраняет контекст и intent.

## 12. AIUP (AI Unified Process)

AIUP — lightweight adaptation of the Unified Process для AI-assisted development. Сохраняет артефакты, которые важны (use cases, domain models, architectural decisions), и убирает церемонии, которые не важны. Apache-2.0. Foundation — `aiup-core`, stack-independent. Stack-specific plugins (Angular+JPA).

**Подход:** requirements-centric, inspired by Rational Unified Process. Specification — source of truth, code generated from it. AI — consistency engine, not creative driver.

## 13. spec-workflow-mcp

MCP-сервер для структурированного spec-driven development с real-time dashboard и VSCode extension. Sequential spec creation: Request Spec → Requirements → Design → Test Design → Tasks. Установка: `claude mcp add spec-workflow-mcp -s user -- npx -y spec-workflow-mcp@latest`.

**Особенность:** required decomposition phase, INDEX.md states which spec is next and why.

## 14. cc-thingz

cc-thingz — open-source battle-tested skills and hooks для AI coding agents (Claude Code, Codex CLI, Gemini CLI, Pi). 30 skills, включая fixing-code, improving-tests, brainstorming-ideas, deploying-infra, testing-e2e. «The hooks matter more than the prompts».

**Ключевая идея:** hooks (детерминированные проверки) важнее, чем prompts. Skills разделены на canonical SKILL.md sources с per-tool overlays.

## 15. general-ai-spec-lite

Лёгкая версия general-ai-spec: фрактальная документация + 3-шаговый workflow `/spec → /build → /verify`. Чистый bash + git. 42 файла / ~2100 строк (против 77 файлов / ~9000 строк в оригинале).

## 16. pspec (picospec)

«Smallest specification toolkit for solo developers and AI agents». Lightweight alternative to heavy SDD frameworks. Focus: clear intent, executable task breakdowns, explicit verification, finish line includes tests and real-flow validation. Review Driven: tasks are not done when code compiles; they are done after verification and self-review.

## 17. specrow

Multilingual specification system for spec-driven development. Agent-first specification workflow. Пользователь описывает intent на plain language: `specrow migrate`, `specrow explore`, `specrow proposal`, `specrow build`. Agent uses SpecRow MCP server to inspect workspace, initialize `.specrow` with that language, validate workspace, report next logical step.

## 18. LeanSpec

Lightweight SDD framework, optimized for velocity through human-AI alignment. Core principles:
- **Lightweight:** minimal setup, no heavy dependencies.
- **Simplicity:** start with one file, grow as needed.
- **Agility:** direct editing, no multi-step workflows.
- **Context Economy:** specs under 2,000 tokens (under 300 lines).

«LeanSpec explicitly rejects "complete specifications upfront."» Focus on alignment and intent documentation, not automation claims.

## 19. SpecLite

Local-first CLI control plane для AI IDE. Устанавливает «成熟的一套适用于企业级生产项目的、参考敏捷研发流程的 AI Coding 落地方法论» в локальный проект и多个 AI IDE. Portable, LLM-agnostic agents and skills для Codex, Claude Code, GitHub Copilot, Pi.

## 20. Другие альтернативы

- **SpecCrew** —嵌入式 virtual AI dev team framework. Превращает PRD → Feature Design → System Design → Dev → Deployment → Test в reusable Agent workflows. Apache-2.0. Особенно подходит для existing projects.
- **nspec** — specification-driven project management для AI-native development. Turns backlog into structured markdown specs that AI coding assistants can read, execute, and update. Pairs every feature request (FR) with implementation spec (IMPL), validates entire graph.

## 21. Сводная таблица

| Фреймворк | Лицензия | Звёзды (2026) | Ключевая идея | Основная критика |
|---|---|---|---|---|
| OpenSpec | MIT | 27k–61k | Change-based spec CLI | Нет enforcement; проблемы с multi-repo |
| GitHub Spec Kit | MIT | 69k–133k | Constitution + spec + plan + tasks | Токены; разрыв spec/implementation; нет debugging workflow |
| Superpowers | Open | ~115k | TDD + subagent enforcement | Слишком тяжёлый; предполагает frozen requirements |
| BMAD Method | MIT | ~49.5k | Virtual Agile team of AI agents | Overkill; token-heavy; пропуск этапов |
| Task Master AI | MIT + Commons Clause | ~27.7k | PRD-to-tasks engine | Не замена SDD, а дополнение |
| Open SWE | MIT | ~6.2k | Autonomous coding agents (Stripe/Ramp/Coinbase patterns) | Enterprise-focus; требует инфраструктуры |
| LeanSpec | Open | — | Specs < 2,000 tokens | Отвергает «complete specs upfront» |
| SpecStory | Apache 2.0 (CLI) | — | Capture intent from AI sessions | Не управляет процессом |
| AIUP | Apache-2.0 | — | RUP adaptation for AI | Требует дисциплины |
| spec-workflow-mcp | Open | — | MCP server для spec workflow | MCP-only |
| cc-thingz | Open | — | Skills + hooks для AI agents | Hooks важнее prompts |
| LightSpec | MIT | 5 | Streamlined OpenSpec alternative | Экспериментальный |
| DeepSpec | Open | — | Zero-ceremony SDD | VS Code/Cursor only |
| pspec | ISC | — | Smallest SDD toolkit | Solo developers only |
| specrow | Open | — | Multilingual agent-first spec | Очень новый |
| SpecLite | Open | — | Local-first CLI control plane | Малоизвестный |

## 22. Универсальные принципы (обновлённые)

На основе анализа всех рассмотренных фреймворков и статьи ashapiro.ru:

### 22.1. Синхронизация спецификации и кода — главная боль

Если нет **машинной проверки** соответствия спецификации и кода, спецификация быстро устаревает. Ручное ревью — самое медленное звено в паре «человек-машина». **Что делать:** превращать требования в машинно-проверяемые артефакты там, где это дёшево: типы, контракты, тесты, property-based проверки.

### 22.2. Спецификация должна сжиматься до самой дешёвой формы

Требование должно жить в **самой дешёвой форме**, которая способна его удерживать:
- **Инвариант домена** → тип (принцип «illegal states unrepresentable»).
- **Граница систем** → схема данных + контрактный тест.
- **Обобщённое намерение** → property-based тест.
- **Конкретное поведение** → пример (тест-снимок).
- **Основания решений, разрешение конфликтов, триггеры пересмотра** → ADR.

### 22.3. Механизм фиксации инвариантов

То, что **нельзя нарушать**, должно быть явно зафиксировано и проверяемо. Иначе LLM-агент рано или поздно начнёт обходить ограничения «костылями»: использовать `--skip-specs`, менять несвязанные модули, «оптимизировать» то, о чём не просили.

### 22.4. Настройка под себя обязательна

Любой SDD-фреймворк — не готовый процесс, а **заготовка**. Жёсткая структура спецификаций мешает проектам с собственными форматами. В сообществе появляются кастомные схемы и расширения, но их приходится адаптировать.

### 22.5. Экономика под вопросом

Подготовка и поддержка спецификаций — это **дополнительная работа**. Если неопределённость высокая, затраты могут не окупиться. «Я не хочу, чтобы AI тратил больше времени на переписывание спецификаций, чем на написание кода».

### 22.6. Из статьи ashapiro.ru: зазор творчества и контрмеры

- **Зазор творчества** — часть допущений, принятых машиной внутри себя, которые осели в коде, но остались невидимыми для человека.
- **Аксиома Русакова:** обратная связь асимметрична. Оператор видит ошибки и исправляет спецификацию, но **удачу не замечает** и ничего не правит. Спецификация улучшается только там, где машине «не повезло».
- **Три феномена:** умолчание (спецификация молчит, машина заполняет), дрейф (спецификация определяет, машина отклоняется), эрозия (постепенная деградация содержания).
- **Контрмеры:** две версии кода (опорная и рабочая), явная приёмка и фриз, ведомость допущений (машина отдельно перечисляет места, где спецификация молчала), дополнительные представления (индексы к кодовому снимку).
- **Ключевой сдвиг:** проблема не в том, чтобы написать идеальную спецификацию, а в том, чтобы **удерживать поведение системы при постоянных изменениях**. Ограничивать нужно не объём машинно хранимого состояния, а объём человеческого внимания, необходимого для проверки изменений.

### 22.7. Комбинирование подходов

Ни один фреймворк не является серебряной пулей. Практики предлагают комбинировать:
- **OpenSpec** — для планирования и фиксации требований (гибок, поддерживает итерации).
- **Superpowers** — для принудительного исполнения (TDD, subagent review).
- **Open SWE** — для асинхронного делегирования механической реализации.
- **cc-thingz** — для hooks и детерминированных проверок.

## 23. Выводы и рекомендации

1. **Не искать «серебряную пулю».** OpenSpec, Spec Kit, Superpowers, BMAD — инструменты с разными сильными и слабыми сторонами. Их можно комбинировать.

2. **Спецификация — не самоцель.** Ценность спецификации в том, насколько она помогает **синхронизировать** замысел и код.

3. **Сжимать требования до самой дешёвой формы.** Типы, контракты, тесты, property-based проверки, ADR — всё это формы спецификации, которые дешевле в поддержке, чем проза.

4. **Фиксировать инварианты и защищать их от «костылей».** Агент будет стремиться минимизировать трение. Нужны явные механизмы, которые не позволяют ему обойти ограничения без решения человека.

5. **Управлять вниманием человека, а не объёмом артефактов.** Главное узкое место — не количество сгенерированного кода или Markdown, а способность человека осмысленно проверять изменения.

6. **Различать «не заметил» и «принял».** Молчание не является согласием. Всё, что не было явно принято, должно сохраняться с пометкой «непроверенное».

7. **Начинать с малого и измерять.** Вводить SDD-практики постепенно, на задачах с относительно стабильными требованиями.

8. **Рассмотреть асинхронные фреймворки (Open SWE) для делегирования.** Если задача хорошо специфицирована, механическая реализация может быть делегирована асинхронному агенту с изолированным sandbox.

9. **Использовать hooks и детерминированные проверки (cc-thingz).** Hooks важнее prompts: они обеспечивают машинный enforcement без reliance на «сознательность» LLM.

10. **Учитывать организационный контекст.** Спецификации в репозитории могут не подходить для multi-disciplinary команд, где requirements work происходит upstream от кода.

## 24. Ссылки на источники

- Статья «К контрмерам от потери устойчивости ИИ-обвязки, работающей на базе спецификаций»: https://ashapiro.ru/writing/tpost/fe056iabb1-k-kontrmeram-ot-poteri-ustoichivosti-ii
- Thoughtworks Technology Radar (апрель 2026) об OpenSpec: https://www.thoughtworks.com/zh-cn/radar/tools/openspec
- Talk Think Do: «Why We Moved Away from OpenSpec»: https://talkthinkdo.com/ai-velocity-report/moving-away-from-openspec/
- GitHub Spec Kit Issue #955: Problems with big codebases: https://github.com/github/spec-kit/issues/955
- GitHub Spec Kit Issue #1092: High Level Design Concerns: https://github.com/github/spec-kit/issues/1092
- Wavect: «GitHub Spec Kit: A Production Team Review»: https://wavect.io/blog/github-spec-kit-production-guide/
- Tencent Cloud: «你的 AI 编程助手，为什么总在"乱来"？» (OpenSpec vs Superpowers): https://cloud.tencent.com.cn/developer/article/2683851
- Datacamp: «Phát triển dựa trên bản đặc tả với Claude Code»: https://www.datacamp.com/vi/tutorial/spec-driven-development-with-claude-code
- BMAD Issue #2003: Structural Gaps and Contradictions: https://github.com/bmad-code-org/BMAD-METHOD/issues/2003
- Security Boulevard: «7 Spec-Driven Development Tools»: https://securityboulevard.com/2026/06/7-spec-driven-development-tools-spec-kit-kiro-openspec-tessl-more/
- LangChain: «Open SWE: An Open-Source Framework for Internal Coding Agents»: https://www.langchain.com/blog/open-swe-an-open-source-framework-for-internal-coding-agents
- LeanSpec: https://www.lean-spec.dev/
- SpecStory: https://docs.specstory.com/
- AIUP: https://unifiedprocess.ai/
- cc-thingz: https://github.com/umputun/cc-thingz
- pspec: https://github.com/rzkmak/pspec
- specrow: https://www.npmjs.com/package/specrow
- SpecLite: https://www.npmjs.com/package/@fancyliu/speclite
