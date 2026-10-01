# Исследование: AGENTS.md — Руководства, Правила и Фреймворки

## 1. Концепция и Назначение
`AGENTS.md` — это открытый универсальный стандарт (поддерживаемый Agentic AI Foundation) для предоставления контекста и инструкций ИИ-агентам, таким как Cursor, GitHub Copilot, Windsurf, Codex, Devin, Claude Code и другим (https://agents.md/), (https://github.com/FerroxLabs/agents-md).

В отличие от `README.md`, который пишется для людей (история проекта, лицензия, быстрый старт), `AGENTS.md` содержит технические детали, необходимые машине для корректной генерации и модификации кода (https://agents.md/). Он служит единым источником правды, избавляя от необходимости каждый раз вставлять одни и те же системные промпты, и обеспечивает инструментальную независимость (работает везде, в отличие от специфичных `.cursorrules` или `CLAUDE.md`) (https://www.builder.io/blog/agents-md), (https://pub.towardsai.net/your-ai-agent-rules-one-source-of-truth-for-cursor-claude-code-and-every-tool-youll-adopt-next-cd7f1353dbbc).

## 2. Рекомендуемая Структура
Хотя строгих обязательных полей нет (это обычный Markdown), анализ более 2500 файлов и документация Codex выделяют следующие ключевые секции (https://www.augmentcode.com/guides/how-to-build-agents-md), (https://www.morphllm.com/agents-md-guide):

1. **Project Overview (Контекст и роль):** Одно-два предложения, задающие ИИ роль и контекст проекта.
2. **Package Manager & Tooling:** Явное указание пакетного менеджера (например, `pnpm` вместо `npm`) и используемых инструментов.
3. **Build & Test Commands:** Нестандартные команды для сборки, типизации, линтинга и запуска тестов.
4. **Code Style Guidelines:** Архитектурные паттерны, именование, подходы к обработке ошибок.
5. **Security Constraints:** Жесткие запреты (например, "никогда не коммить `.env`", "избегай `eval`").
6. **Commit & PR Rules:** Формат сообщений коммитов (Conventional Commits) и требования к Pull Request.

## 3. Ключевые Фреймворки и Правила (Best Practices)

### A. Progressive Disclosure (Прогрессивное раскрытие)
Это важнейший принцип оптимизации контекстного окна (токенов) (https://www.aihero.dev/a-complete-guide-to-agents-md). Не превращайте корневой `AGENTS.md` в "грязевой шар" из тысяч строк.
- **Правило:** Держите корневой файл максимально коротким. Специфичные правила выносите в отдельные документы и давайте на них ссылки.
- *Пример:* `For TypeScript conventions, see docs/TYPESCRIPT.md`.
- **Польза:** Агент загрузит `TYPESCRIPT.md` только при работе с TypeScript, не засоряя память при других задачах.

### B. Prescriptive vs Descriptive (Предписания против Описаний)
`AGENTS.md` должен быть **прескриптивным** (содержать жесткие правила: что делать и чего избегать) (https://github.com/github/spec-kit/discussions/2476).
- **Правильно:** "Всегда используй `const` вместо `let`. Избегай вложенных тернарных операторов."
- **Неправильно:** Длинные рассуждения о философии проекта (для этого лучше подходит `CLAUDE.md` или обычная документация).

### C. Иерархия и Монорепозитории (Inheritance)
Файлы `AGENTS.md` можно размещать в подпапках (https://agents.md/), (https://www.aihero.dev/a-complete-guide-to-agents-md).
- **Правило приоритета:** ИИ-агент всегда ищет файл, который находится *ближе всего* к редактируемому файлу. Локальный `AGENTS.md` переопределяет или дополняет корневой.
- **Конфликты:** Прямой запрос пользователя в чате всегда имеет наивысший приоритет и переопределяет файл.

## 4. Пример шаблона

```markdown
# Project Context
This is a Next.js 14 e-commerce platform using the App Router.

# Tooling
- Package Manager: pnpm (strict engine)
- Database: PostgreSQL via Prisma ORM

# Commands
- Build: `pnpm build`
- Lint: `pnpm lint`
- Test: `pnpm test`

# Rules
- Always use Server Components by default.
- Extract Client Components to `*.client.tsx` only when interactivity is needed.
- See `docs/STYLING.md` for Tailwind conventions.
```

## 5. Источники и Ссылки

1. [Официальная спецификация AGENTS.md](https://agents.md/) — База стандарта от Agentic AI Foundation.
2. [Drop-in AGENTS.md (FerroxLabs)](https://github.com/FerroxLabs/agents-md) — Реализация открытого кросс-инструментального стандарта.
3. [How to use AGENTS.md (Official FAQ)](https://agents.md/) — Официальные инструкции по иерархии и использованию.
4. [Improve your AI code output with AGENTS.md (Builder.io)](https://www.builder.io/blog/agents-md) — Разбор антипаттернов и TDD-подхода.
5. [One Source of Truth for Your AI Agent Rules (Towards AI)](https://pub.towardsai.net/your-ai-agent-rules-one-source-of-truth-for-cursor-claude-code-and-every-tool-youll-adopt-next-cd7f1353dbbc) — Интеграция с Cursor и Claude.
6. [How to Build Your AGENTS.md (Augment Code)](https://www.augmentcode.com/guides/how-to-build-agents-md) — Анализ 2500+ файлов и выделение 6 ключевых секций.
7. [AGENTS.md Spec: Recommended Sections (Morph)](https://www.morphllm.com/agents-md-guide) — Спецификация и рекомендуемые блоки.
8. [A Complete Guide To AGENTS.md (Matt Pocock / AI Hero)](https://www.aihero.dev/a-complete-guide-to-agents-md) — Гайд по прогрессивному раскрытию и экономии токенов.
9. [Constitution vs AGENTS.md (GitHub Discussion)](https://github.com/github/spec-kit/discussions/2476) — Разница между прескриптивными правилами и описательным контекстом.
