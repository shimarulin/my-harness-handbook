# Открытые SDD-фреймворки: расширенное сравнение опыта и критики

Дата: 2026-09-29
Критерий отбора: открытая лицензия, отсутствие vendor-lock, публичная критика и реальный опыт. Стек неважен.
Исключены: Kiro (платный AWS IDE), Augment Intent (closed beta), CodeMySpec и EasySpecs.ai (коммерческие продукты), Tessl Framework (closed beta; Registry частично открыт).

Звёзды и цифры из разных независимых источников за май–сентябрь 2026; расходятся из-за разных дат среза.

---

# Часть 1. Сводная таблица

| Фреймворк | Лицензия | Runtime | Звёзды | Bus factor | Контекст-модель | Параллельная работа | Зрелость |
|---|---|---|---|---|---|---|---|
| OpenSpec (Fission-AI) | MIT | Node 20.19+ | ~47–70K | **1** | 1 агент | 5/5 — дельта-спеки | Активный, Discord-сообщество |
| Spec Kit (GitHub) | MIT | Python 3.11+ (uv) | ~95–133K | 2 | 1 агент | 5/5 — branch-per-spec | 533 issues / 36.8% close, PR backlog 62 дня |
| BMAD-METHOD | OSS | Node 20+ | ~43K | 2 | 19+ role-агентов | 2/5 — shared directory по умолчанию | 458 commits/90d, 94.3% close rate |
| GSD (get-shit-done) | MIT | Node | ~61.5K | n/a | Fresh subagent per task | 2/5 | **Архивирован 2026-06-26** |
| Superpowers (obra) | MIT | агностик | ~293K | 1 + Prime Radiant | Subagent dispatch | Да — worktrees | v6.4.2, 26.2K forks |
| agent-skills (addyosmani) | MIT | агностик | ~99.8K | 1 | 1 агент | n/a | 590 commits, 24 skills |
| specs.md | — | Node | new | малый | 3 phase-агента | Да — FIRE flow | Родился Dec 2025 |
| Spec Kitty | — | Node | 1.7K | community | Worktree isolation | Да — work-package lanes | 13,737 commits, 341 branches |
| Taskmaster AI | — | Node | 25.5K | ? | Multi-model | Да — dependency-aware | 1200+ commits |
| Tessl Registry | mixed | Node | n/a | company | n/a | Да | Open beta, Snyk partnership |

Параллельная работа и контекст-модель — оценки Ran Isenberg [2] (шкала 1–5) и Somniosoftware [4].

---

# Часть 2. Проверенные фреймворки: опыт и критика

## 2.1. OpenSpec (Fission-AI)

**Технические данные.** MIT, `@fission-ai/openspec` npm (Node 20.19+). Дельта-спеки ADDED/MODIFIED/REMOVED, brownfield-first, 25+ агентов, `AGENTS.md`, нулевой lock-in [4].

**Опыт.** Самый лёгкий в освоении SDD-фреймворк; типичный change ~250 строк против ~800 у более тяжёлых тулкитов [3]. Приоритет для существующих кодовых баз: «cleanest delta model I have seen in this category» [3].

**Критика.**

- **Bus factor = 1.** «OpenSpec is built by one person. You're betting on these teams as much as these tools» [2].
- Спек-дрейфт как дефолтный исход: спеки не обновляются сами, `/opsx:sync` — advisory, не gate [3].
- «A pretty easy to miss something in large codebase (especially when there is lots of legacy stuff)» [3].
- Issue health: 201 open / 24.2% close rate, PR backlog 37 / 30 дней [2].
- Мульти-репо: Stores (beta) частичен, кластер issues (#725, #662, #594, #435, #581, #697) без решения [8].
- Любая кастомизация сверх лёгкой — fork воркфлоу [2].

## 2.2. Spec Kit (GitHub)

**Технические данные.** MIT, Python 3.11+ через uv, CLI `specify`. 133K звёзд (сент 2026), 30+ агентных интеграций, v1.0.4. Phase-gated: constitution → specify → clarify → plan → tasks → analyze → implement [5].

**Сильные стороны.** Constitution-подход — самый прямой ответ на проблему агентов, принимающих неконсистентные решения на длинных проектах [4]. Штатные artifacts дают командам с несколькими ролями общий decision trail [5]. Brownfield с repository analysis — strong fit [5].

**Критика.**

- **Project health.** 533 открытых issues / 36.8% close rate; PR backlog 94 / 62 дня; нет community-канала [2]. Известные проблемы с апгрейдом, которые затирают кастомизационные файлы [2].
- **Артефактная тяжесть.** Один spec генерирует восемь файлов; для трёх-поинтовой истории это трудно оправдать [4]. Analysis Birgitta Böckeler (martinfowler.com) [4].
- **Greenfield-bias.** Branch-per-spec модель трактует спеки как change-артефакты, не долгоживущие capability-контракты. На зрелой кодовой базе каждая фича начинается с reverse-engineering; артефакты не компаундятся в system-level документацию [1].
- **Что не решает.** Плохую спеку (агент не может валидировать бизнес-допущение), корректность имплементации, security, production readiness, дрейф спеки от кода (модель maintenance явно оставлена каждой команде) [5].
- **Iteration по(direction) = регенерация.** Изменение направления — re-run affected команд, каждая регенерирует полный документ; отревьюенный план заменяется целиком, без diff изменённых секций [2].
- Ran Isenberg scoring: specification quality 2/5 — код не точно мапится на spec intent [2].

**Опыт Wavect.** «Worth piloting for consequential feature work, existing systems, teams that need a shared decision trail. Usually too much process for a disposable prototype, tiny bug fix, or a task already expressed by a precise failing test» [5]. Рекомендация: пилотировать 3–5 репрезентативных фич (одна маленькая, одна brownfield, одна с security/data), измерять clarification time, escaped defects, rework, lead time; принимать только если accepted-change rate улучшается [5].

## 2.3. BMAD-METHOD

**Технические данные.** Open source (bmad-code-org), Node 20+. 19+ role-агентов (Analyst → PM → Architect → Scrum Master → Developer → QA), Markdown «Agent-as-Code» [1][6].

**Сильные стороны.**

- **Самое здоровое сообщество** из трёх major: 458 commits/90 дней, 94.3% close rate, responsive Discord [2].
- Глубочайшие planning-артефакты: полный PRD, architecture doc, story breakdown [2].
- Adversarial code review (`/bmad-bmm-code-review`) «поймал вещи, которые standard review бы пропустил» [2].
- Party Mode — мульти-агентная элиситация [2].
- Quick Flow: 2 шага, один документ, то же качество элиситации, что и полный flow [2].
- Bus factor = 2 [2].

**Критика.**

- **Время и стоимость.** Полный flow: 6 дней total (2 дня planning + 4 дня implementation), $200 total против 1 дня / $70 у OpenSpec и 1 дня / $75 у Spec Kit [2].
- **Параллельная разработка.** 2/5 — все outputs в shared directory по умолчанию; изоляция настраиваема, но не enforced [2].
- «Process multiplier, not process creator». Если у команды нет структурированных процессов, BMAD воспроизведёт хаос на семи агентах [1].
- «Handoff failures — реальная поверхность дебага. Когда Architect-агент делает допущение, не задокументированное PM-агентом, Scrum Master распространяет его в stories, Developer уверенно имплементирует — обнаруживается в QA или production. Pipeline хорош настолько, насколько хорош слабейший handoff» [1].
- «The 19-Agent Trap» (paddo.dev, Jan 2026): 19 агентских system prompts конкурируют за внимание в одном контекстном окне; каждый слой scaffolding потребляет токены [7].
- EasySpecs: «higher overhead and cost surface; still does not replace a human Spec Review + Document Review product workspace» [6].
- Developer experience: 2/5 — 12 агентов, тяжёлый артефакт-сет, крутая кривая обучения; `/bmad-help` существует в основном чтобы спасать от собственной сложности BMAD [2].

## 2.4. GSD (Get Shit Done)

**Статус: архивирован 26 июня 2026.** `gsd-build/get-shit-done` — read-only [8]. Философия наследуется эволюцией — Buildomator (см. Часть 3).

**Технические данные.** MIT, Node, Claude Code-first, 16+ runtimes. Фазовая модель: discuss → plan → execute → verify → ship; каждый execution unit получает fresh ~200K-token context; atomic commit per task [4]. «Nyquist auditor» — plan-checker отклоняет планы без automated verify command, до трёх раз [4].

**Критика (из опыта Vitor Norton, Jun 2026 [9]).**

- **Auto-commit как дизайн-принцип.** «Task completed → YES → Atomic unit of work (1 commit per task)». Issue #745: предложение откладывать все коммиты и оставить рабочее дерево dirty для ревью всей фазы как одного diff. Ответ maintainer: «this is how its designed, not interested in changing the design at this time… this would be a redesign of how it works, not an enhancement» [9].
- **Автономный оркестратор vs human-in-the-loop.** «GSD is an autonomous orchestrator. It spawns subagents, commits per task, advances on its own. Human approves at checkpoints. Its made for a different operator than me» [9]. «My job is to be helped, not replaced. GSD is built to take the wheel» [9].
- **Grain of drift.** «It latches onto one reading of what you said and drives hard in that direction, confidently, past the point where it still makes sense… By the time the drift is visible it's already downstream in a plan, then in code» [9]. На 70-фазном проекте — «redo or restructure at least 50 of them… every ~5 phases I had to stop and fix things in the code by hand so the next 5 wouldn't wander off» [9].
- **Overengineering.** 33 агента, ~67 skills, 11 hooks, capability registry, supply-chain gate против hallucinated packages; 104 модуля CLI; 10,700-строчный инсталлер. «90% surface area I don't need but would inherit the moment I forked» [9].
- **Токен-overhead.** 4:1 — на каждый токен кода 4 токена оркестрации; Pro plan недостаточен, Max или API напрямую [4][10].
- **Fork graveyard.** 250 forks; «не один успешный divergent "lite"». Вывод: «for a public tool that re-opinionates the flow, a fork is the worst quadrant» [9].
- Практика Kai Hendry (dabase.com): «most bureaucratic… discord feels dead… confused by the numbering… The way the SDD frameworks blew through tokens was also worrying… iterations slow compared to just chatting with AI» [10].

## 2.5. Superpowers (obra)

**Технические данные.** MIT, 293K звёзд (сент 2026), v6.4.2, 683 commits, 26.2K forks. Jesse Vincent (создатель Request Tracker, Perl 5 language releases) + Prime Radiant [11][12].

**Философия.** Behavioral methodology, не planning-artifact-центричная: skills инструктируют поведение агента, а не порождают артефакты для ревью [1][12].

**Сильные стороны.**

- **Масштабирование process по типу работы** [12]:

| Тип | Документированный процесс |
|---|---|
| Spike | Сформулировать вопрос и короткий подход; результат — exploratory |
| Bounded change | Компактный дизайн в чате; без отдельного specification/plan документа |
| Architectural change | Письменная спецификация и план имплементации |

  Все три пути требуют явного human approval перед кодингом; лёгкие пути снижают ceremony, не убирая checkpoint [12].

- TDD skill: RED-GREEN-REFACTOR; отличает behavioral tests от assertions, merely exercising mocks [12].
- Completion skill: требует свежий verification output; отличает passing linter от successful build, changed file от fixed bug, subagent success message от reviewed diff [12].
- Subagent development: fresh implementer для независимой задачи, task reviewer (spec compliance + code quality), broader branch review; пять раундов фиксов перед adjudication [12].
- Установлен в Anthropic official Claude plugin marketplace [12].

**Критика.**

- **Skills инструктируют, не гарантируют.** «Its skills instruct agents to follow workflows and produce verification evidence. They are not a substitute for repository tests, permissions, or human review» [12]. Master-skill-инъекция («YOU MUST USE IT. This is not negotiable») — behavioral guidance, интерпретируемая host-моделью; «describing it as mechanical enforcement overstates what the source establishes» [12].
- Prime Radiant предлагает commercial services; сама библиотека MIT, но хост-агент несёт собственные расходы [12].
- Из HN-обсуждения GSD: «That was my impression of superpowers as well. Maybe not highly overengineered…» [13].

## 2.6. agent-skills (addyosmani)

**Технические данные.** MIT, 99.8K звёзд, 590 commits. 24 lifecycle skills + `using-agent-skills` meta-skill. `npx skills add addyosmani/agent-skills`. Работает с 70+ агентами (Claude Code, Codex, Cursor, Copilot, Windsurf, Cline, Antigravity, OpenCode, Kiro и др.) [14].

**Философия.** Encode workflows, quality gates и judgment senior engineers в production — packaged, чтобы агент следовал им консистентно через каждую фазу [14].

**Структура.** Каждый skill — structured workflow with steps, verification gates, anti-rationalization tables. Фазы lifecycle: Define Idea (`/spec`), и далее по циклу — каждый slash-command активирует нужные skills для момента [15].

**Критика.** Молодой проект (590 commits); bus factor = 1 (Addy Osmani). Нет независимых production-отчётов. Подходит как дополнение к существующему фреймворку, не замена.

---

# Часть 3. Новые и малоизвестные альтернативы

## 3.1. Buildomator (эволюция GSD)

Claude Code plugin, v4.1.0, от jnuyens (прежнее имя — gsd-plugin). «Performance-optimized evolution of GSD»: режет per-turn token overhead ~92%, держит project state в MCP-backed store, auto-resumes через `/compact` [16]. Унаследовал фазовую модель GSD, но с MCP-центричной архитектурой. Был в GitHub Trending (Aug 2026) [17].

## 3.2. specs.md

AI-native framework с pluggable flows. Четыре flow под разные случаи [18]:

- **Ideation** — creative brainstorming: Spark → Flame → Forge (генерация идей через 12 доменов, оценка через multiple lenses, shape top picks в concept briefs).
- **Simple** — только генерация спек: requirements, design, tasks.
- **FIRE** — adaptive execution: 0–2 checkpoint'а по сложности, brownfield-first (auto-detect существующих паттернов, extends rather than rewrites), monorepo support (hierarchical standards + module-specific overrides).
- **AI-DLC** — полная методология: DDD integral, 3 phase-based агента (Master, Inception, Construction, Operations), Mob Elaboration/Mob Construction rituals.

**Позиционирование против конкурентов** [18][19]:

- vs Kiro: «IDE and AI-agnostic… no vendor lock-in» — открытая реализация AWS AI-DLC (Kiro закрыт).
- vs BMAD: 3 phase-based агента вместо 19+ role-based; «want to avoid managing 19 agents».
- vs Spec Kit: pluggable flows, выбор overhead.

**Ограничения.** Community «just born (December 2025)» [19]. VS Code extension для отслеживания прогресса. Нет публичной критики — слишком молод.

## 3.3. Spec Kitty

Community fork, local-first, 1.7K звёзд, 341 branches, 13,737 commits [20]. От community (stijn-dejongh + claude). Ключевые отличия от spec-kit [20]:

- Repo-native mission state, work-package lanes
- Git worktree isolation
- Local dashboard
- Governance commands
- Explicit `next → review → accept → merge` runtime loop

Поддерживаемые агенты: Claude Code, Codex, Cursor, Gemini, GitHub Copilot, OpenCode, Qwen, Windsurf, Kiro, Vibe, Pi, Letta [20]. «Local-first and stores its core artifacts in your repo. Hosted tracker and sync integrations are optional» [20].

## 3.4. Taskmaster AI

25.5K звёзд, 1200+ commits [21]. Позиционирование: «treats AI as a project manager» — парсит PRD в hierarchical, dependency-aware task lists, которые потом скармливаются агентам для исполнения [21].

**Ключевой дифференциатор** — multi-model architecture: три настраиваемых тира моделей — main (core operations), research (fetching свежей web-информации с project context), fallback. Позволяет парить мощную reasoning-модель с быстрой research-моделью и cost-effective fallback [21]. First-class интеграция — Cursor via MCP; также Windsurf [21].

Ограничение: PRD-центричный — спека предполагается существующей; сам PRD не генерирует.

## 3.5. Tessl Registry (частично открытая альтернатива)

Registry — open beta [22]. 10,000+ pre-built specs для open source библиотек: «how to avoid API hallucinations and version mixups» [23]. `npx tessl install` / `npx tessl search`. Snyk partnership: security scoring для каждого skill, установки пиннятся к точным commit-версиям [24].

**Context-as-code:** skills, rules, docs — версионируются, ревьюятся, роллятся с той же строгостью, что и code dependencies. Governance: RBAC, install/publish policies, full audit trail [25]. Evals: измерение фактического impact skill'а — запуск агента на реальных задачах с и без контекста, каждый change с evidence [25].

**Ограничение.** Framework — closed beta; Registry — открытый контент в коммерческой платформе. Vendor-lock риск для governance-слоя.

## 3.6. openspec-schemas (вариации)

**intent-driven-dev/openspec-schemas** [26]: 103 stars, 25 forks, 83 commits. Коллекция кастомных схем для OpenSpec: `intent-driven`, `behavior-driven` и др. Демонстрирует, как кастомизировать OpenSpec под разные стили работы.

**jikkujoyce/openspec-schemas** [27]: 4 stars, 4 commits, anvil schema. Микро-проект; пример вариативности.

Показывают, что OpenSpec-ядро расширяемо схемами без fork'а всего фреймворка [26].

---

# Часть 4. Сравнение по ключевым осям

## 4.1. Кто держит wheel

| Фреймворк | Модель | Последствие |
|---|---|---|
| GSD / Buildomator | **Автономный оркестратор** — агент берёт управление, human approves на checkpoint'ах | Ревью-контроль после факта; senior engineer не может влиять на процесс execution |
| OpenSpec / Spec Kit | Human-in-the-loop — каждый артефакт ревьюится до следующего шага | Контроль сохранён, но скорость упирается в человеческое ревью |
| Superpowers | Human approval перед кодингом, но execution доверен агенту с behavioral gates | Баланс, но gates инструктивные, не механические |
| Taskmaster AI | AI как project manager, dependency-aware разбиение | Хороши для PRD-уже-есть сценария |

## 4.2. Контекст-модель

| Фреймворк | Подход | Токен-затраты |
|---|---|---|
| GSD | Fresh subagent per task, ~200K-token на каждый | 4:1 overhead к коду [4][10] |
| BMAD | 19 агентов в одном окне | Конкуренция за внимание; «19-agent trap» [7] |
| OpenSpec / Spec Kit / agent-skills | 1 основной агент | Умеренные |
| Superpowers | Subagent dispatch + worktrees | Умеренные, batching для мелких задач [12] |
| Buildomator | MCP-backed state store, auto-resume | ~92% режет per-turn overhead [16] |

## 4.3. Project health (данные Ran Isenberg, апрель 2026 [2])

| Метрика | BMAD | Spec-Kit | OpenSpec |
|---|---|---|---|
| Commits (90 дней) | 458 | 37 | 158 |
| Open issues / close rate | 44 / 94.3% | 533 / 36.8% | 201 / 24.2% |
| PR backlog (open / median age) | 6 / 1 день | 94 / 62 дня | 37 / 30 дней |
| Bus factor | 2 | 2 | **1** |

## 4.4. Скорость и стоимость (Ran Isenberg [2])

| | BMAD Full | BMAD Quick | Spec-Kit | OpenSpec |
|---|---|---|---|---|
| Planning time | 2 дня | 5 часов | 4 часа | 3 часа |
| Implementation time | 4 дня | 1.5 дня | 1 день | 1 день |
| Planning cost | $50 | $30 | $30 | $25 |
| Implementation cost | $150 | $55 | $45 | $70 |
| Итоговый score (13 dimensions) | 3.65 | 3.74 | 2.77 | **4.00** |

---

# Часть 5. Рекомендации по выбору

| Ситуация | Рекомендация | Обоснование |
|---|---|---|
| Brownfield, инкрементальные изменения | **OpenSpec** | Дельта-спеки, минимальный friction [2][3][4] |
| Greenfield, чёткие требования, распределённая команда | **Spec Kit** | Constitution как shared contract, branch-per-spec для параллельности [4][5] |
| Compliance, audit, multi-team enterprise | **BMAD (Quick Flow)** | Process multiplier, audit trail; Quick Flow снижает overhead [1][2][6] |
| Claude Code-first, нужен автономный оркестратор | **Buildomator** | Наследник GSD, решает token overhead [16] |
| Behavioral discipline (TDD, review),不喜欢 artifact-heavy | **Superpowers** | Skills вместо тяжёлых артефактов; масштабирование по типу задачи [11][12] |
| Lightweight lifecycle-обвязка для существующего стека | **agent-skills** | 24 skills, 70+ агентов, минимальная ceremony [14] |
| Monorepo, multi-stack, нужен выбор overhead | **specs.md** | FIRE flow, hierarchical standards, module overrides [18] |
| PRD уже есть, нужно разбиение на задачи | **Taskmaster AI** | Dependency-aware, multi-model [21] |
| Spec-герметизация с worktree-изоляцией | **Spec Kitty** | Local-first, mission state, explicit runtime loop [20] |
| Repository готовых specs для библиотек | **Tessl Registry** | 10K+ pre-built specs, Snyk scoring [23][24] |

---

# Часть 6. Открытые вопросы для дальнейшей проверки

1. **Buildomator** — заявленный ~92% token overhead reduction требует независимого подтверждения; MCP-backed state store — новая архитектура без публичной критики.
2. **specs.md** — слишком молод (Dec 2025), нет production-отчётов и негативного опыта; AWS AI-DLC методология — источник, но реализация независимая.
3. **Spec Kitty** — 13,737 commits за короткое время говорит об интенсивной разработке, но fork-модель может наследовать проблемы spec-kit; явной критики нет.
4. **Taskmaster AI** — только упоминания в сравнительных статьях; нет найденных production-постмортемов.
5. **GSD archived** — миграционный путь для существующих пользователей не документирован; Buildomator заявлен как эволюция, но не официальный преемник.

---

# Источники

[1] Torres Bermon W. S. «Spec Kit vs BMAD vs OpenSpec: Choosing an SDD Framework in 2026». dev.to/willtorber (2026-04-23)
[2] Eretz Kdosha I. «I Tested Three Spec-Driven AI Tools. Here's My Honest Take». ranthebuilder.cloud/blog/i-tested-three-spec-driven-ai-tools (2026-04-13)
[3] Davenport J. «OpenSpec Explained: Repo-Native Spec-Driven Development». codemyspec.com/blog/openspec-explained (2026-06-03)
[4] Ortega E. «Spec-Driven Development in Practice: GitHub Spec Kit, OpenSpec, and GSD Compared». somniosoftware.com/blog (2026-05-21)
[5] Riedl K. «GitHub Spec Kit Review: Does It Make Vibe Coding Production-Ready?». wavect.io/blog/github-spec-kit-production-guide (2026-08-14, reviewed 2026-09-02)
[6] «Understanding BMAD-METHOD (SDD)». easyspecs.ai/blog/understanding-bmad-method (2026-09-04)
[7] «The 19-Agent Trap». paddo.dev (2026-01-07) — найден через сниппет поисковой выдачи
[8] gsd-build/get-shit-done. github.com/gsd-build/get-shit-done — archived 2026-06-26
[9] Norton V. «I tried to fork GSD, or: it's for vibe coders, not real devs». dev.to/vtnorton (2026-06-15)
[10] Hendry K. «Comparing SDD Frameworks: spec-kit vs OpenSpec vs get-shit-done». dabase.com/blog/2026/sdd-framework-comparison (2026-05-18)
[11] obra/superpowers. github.com/obra/superpowers — 293K звёзд, v6.4.2 (2026-09-25)
[12] «Superpowers Skills Framework». rywalker.com/research/superpowers-skills-framework (verified 2026-09-15)
[13] «Get Shit Done: A meta-prompting, context engineering». news.ycombinator.com/item?id=47417804
[14] addyosmani/agent-skills. github.com/addyosmani/agent-skills — 99.8K звёзд, 590 commits (2026-09-26)
[15] «How it compares — agent-skills». skills.addy.ie
[16] jnuyens/gsd-plugin (Buildomator). github.com/jnuyens/gsd-plugin — v4.1.0 (2026-09-21)
[17] buildomator/buildomator — Trendshift (GitHub trending, Aug 2026)
[18] «specs.md: Introduction». specs.md
[19] «specs.md vs BMAD-Method». specs.md/compare/vs-bmad
[20] spec-kitty/spec-kitty. github.com/spec-kitty/spec-kitty — 1.7K звёзд, 341 branches (2026-09-29)
[21] Hightower R. «GSD vs Spec Kit vs OpenSpec vs Taskmaster AI: Where SDD tools diverge». medium.com/@richardhightower — 404 на момент проверки; данные из поискового сниппета
[22] «Tessl launches spec-driven framework and registry». tessl.io/blog (2025-09-23)
[23] Maple S. «Tessl launches spec-driven development tools». tessl.io/blog/tessl-launches-spec-driven-framework-and-registry
[24] «Securing the Agent Skills Registry: How Snyk and Tessl». snyk.io/blog/snyk-tessl-partnership (2026-03-17)
[25] «Tessl Docs: What is Tessl?». docs.tessl.io (2026-09-13)
[26] intent-driven-dev/openspec-schemas. github.com/intent-driven-dev/openspec-schemas — 103 stars, 83 commits
[27] jikkujoyce/openspec-schemas. github.com/jikkujoyce/openspec-schemas — 4 stars, 4 commits

---

# Связанные документы

- `openspec-sdd-process-criticism.md` — универсальные принципы, феноменология SDD (A. Шапиро), критика OpenSpec
- `openspec-first-response-materials.md` — (если существует) материалы первой итерации
