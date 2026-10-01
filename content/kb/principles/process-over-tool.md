# Принцип: процесс важнее инструмента; инструмент — заменяемая реализация

| Параметр | Значение |
|---|---|
| Статус | draft |
| Обновлено | 2026-09-30 |

## Что это

Процесс проектируется владельцем, а не принимается «из коробки»: «Design the experience you want, not the one the tool ships. Decide the workflow steps, artifacts, formats, and review gates your org needs. The tool implements that experience but it doesn't define it» (Ran Isenberg, 2026-04-13). Любой SDD-фреймворк — заготовка, а не готовый процесс; настройка под себя обязательна. Инструмент должен быть заменяем без разрушения процесса и привычек команды.

## Ключевые концепции

### Начинай с методологии, не с инструмента

Порядок: принципы → формат артефактов (стандартный, открытый) → процесс и роли → выбор инструмента как реализации. Обоснование из корпуса: идеального фреймворка нет — у каждого подтверждённые реальным опытом фундаментальные проблемы; 90k звёзд не спасают от проблем дизайна (случай Spec Kit). «Сообщество важнее звёзд». Framework shopping как анти-паттерн: четыре недели реального использования на реальных тикетах научат быстрее, чем сравнение фреймворков.

### Оборачивание в собственную абстракцию

- Свои команды вместо команд инструмента: `my-company-sdd start feature TICKET-123` вместо `openspec create-feature TICKET-123` — разработчики учат команды компании, а не инструмента; при смене инструмента привычки не ломаются.
- Обернуть установку/настройку (контроль того, что установлено и enforced across repos).
- Спроектировать свой workflow: шаги, артефакты, форматы, review gates.
- Документировать процесс отдельно от инструмента (PROCESS.md); инструмент — лишь реализация.
- Артефакты в стандартных форматах: Markdown для текстов, YAML/JSON для структур; никаких проприетарных форматов.

Снижение зависимости через формы: инварианты в типах, контракты в тестах, решения в ADR (см. `cheapest-form.md`).

### Комбинирование вместо серебряной пули

Вердикт-комбинация практиков (d1): **OpenSpec** — планирование/фиксация требований (гибок, итерации); **Superpowers** — принудительное исполнение (TDD, subagent review); **Open SWE** — асинхронное делегирование механической реализации; **cc-thingz** — hooks и детерминированные проверки. Superpowers силён в принуждении, но предполагает frozen requirements; OpenSpec гибок в планировании, но слаб в принуждении — практики комбинируют.

### Место артефактов определяет доступность процесса (кейс Talk Think Do)

UK-компания: внедрение OpenSpec Q4 2025 → 84% AI-authored code в Q1 2026 → полный отказ через два месяца. Причина организационная, не инструментальная: «The repository is the wrong workspace for the work that happens before code… Specs in the repository coupled the planning process to a tool optimised for engineering, and that does not work for a multi-disciplinary team». Discovery/refinement/scope/stakeholder alignment идут upstream от репозитория с участием BA, delivery managers, QA leads, клиента; спеки в репо скрывали движение scope/cost против estimate (semi-agile: оценки на story, бюджеты на epic). Замена: планирование в Claude Team, governance в Azure DevOps work items, свой delivery plugin + MCP; «дисциплина планирования и change-подход OpenSpec — genuinely good, и мы её сохранили. Изменилось место, где живут артефакты».

### Таксономия vendor-lock (4 формы)

| Форма | Пример |
|---|---|
| Лицензионный | Kiro («AWS Content» license — не open source) |
| Знаниевый | Tessl (10,000+ specs в закрытом registry) |
| Экосистемный | Antigravity (Google Cloud only), частично AI-DLC (AWS) |
| Форматный | Проприетарные форматы данных без экспорта |

Чек-лист оценки фреймворка (7 пунктов): лицензия MIT/Apache/BSD; весь код доступен и форкабелен; нет обязательных облачных сервисов; основные возможности бесплатны; открытый формат данных; данные экспортируемы; активное сообщество (не bus factor = 1).

Красные флаги: лицензия «AWS Content» и аналоги; ключевая функциональность в закрытом реестре; требование конкретных облачных сервисов; платный доступ к сообществу/документации; проприетарный формат без экспорта.

### План миграции и переоценка

Иметь план Б: знать экспорт данных, понимать потери при переходе, регулярно проверять возможность отката; форк при необходимости; альтернативный инструмент в запасе. Пространство меняется быстро — регулярно переоценивать выбор («то, что работало вчера, может не работать завтра»). Thoughtworks Technology Radar (апрель 2026): OpenSpec в категории Assess с предупреждением — следить за развитием нативных возможностей агентов и переоценивать необходимость SDD-инструментов.

Осторожность с форком: «for a public tool that re-opinionates the flow, a fork is the worst quadrant» (Vitor Norton: 250 форков GSD, ни одного успешного divergent lite).

## Сильные и слабые стороны

Сильные: процесс переживает инструменты; vendor-exit становится тестируемым свойством; привычки команды стабильны при смене tooling.

Слабые / риски: собственная абстракция — дополнительный слой поддержки; риск переизобретения («roll your own»: 4 custom slash-команды + AGENTS.md дают ~80% функциональности, остальные 20% — presets, дельта-маркеры, handoffs — приходится достраивать); обёртка скрывает эволюцию инструмента (пропускаются улучшения upstream).

## Источники

- Eretz Kdosha I. (Ran Isenberg): https://ranthebuilder.cloud/blog/i-tested-three-spec-driven-ai-tools-here-s-my-honest-take/
- Talk Think Do, «Why we've moved away from OpenSpec»: https://talkthinkdo.com/ai-velocity-report/moving-away-from-openspec/ (2026-06-01)
- Norton V., «I tried to fork GSD»: https://dev.to/vtnorton (2026-06-15)
- Thoughtworks Radar, OpenSpec: https://www.thoughtworks.com/zh-cn/radar/tools/openspec (апрель 2026)
- Kiro license: https://kiro.dev/license/; Tessl registry: https://tessl.io/blog/tessl-launches-spec-driven-framework-and-registry
- Входные материалы inbox: `documentation-process-criticism/q1/sdd-frameworks-analysis.md`, `documentation-process-criticism/d1/openspec-sdd-criticism-and-principles.md`, `documentation-process-criticism/g1/openspec-sdd-process-criticism.md`
