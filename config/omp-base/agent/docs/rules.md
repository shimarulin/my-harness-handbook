Нормальная отправная точка — RULES.md именно для этого и сделан: sticky, always-apply, грузится в каждой сессии без условий【turn0fetch1】. Но сама формулировка ослабит эффект. Три практических замечания:

**Что стоит подкрутить в тексте**

1. Нет имён инструментов. Правило говорит «use Context7 MCP», но не называет тулы. Для модели гораздо надёжнее увидеть в правиле `mcp__context7_resolve-library-id` и `mcp__context7_get-library-docs` — те имена, что реально видны в `/tools`.
2. Нет границы, когда НЕ вызывать. Без исключений правило будет стрелять на каждую строку кода, включая внутренние модули и стандартную библиотеку — лишние вызовы, лишний контекст, лишние траты API-ключа.
3. Нет fallback. Если Context7 не нашёл библиотеку или отдал пустой ответ, модель должна сказать об этом явно, а не выдумать API из головы — молча подставить «правдоподобное» имя функции как раз тот риск, который вы хотите убрать.
4. «without me having to explicitly ask» — полезная мысль, но лучше сказать позитивно: «вызывай как обычный шаг задачи, не спрашивая разрешения». Модель это воспринимает надёжнее, чем отрицательную формулировку.

**Улучшенная версия `~/.omp/agent/RULES.md`**

```markdown
## Library documentation (Context7)

When the task involves a third-party library, framework, SDK, external API, or
service configuration — code generation, setup, integration, debugging, or
upgrades — automatically call Context7 before writing or modifying code:

1. `mcp__context7_resolve-library-id` to resolve the library name.
2. `mcp__context7_get-library-docs` with the resolved ID and the topic.

Run these as a normal step of the task; do not ask permission and do not wait
for an explicit request.

Skip Context7 for: code in this repository, relative imports, the standard
library, and tools/libraries explicitly provided in AGENTS.md.

If Context7 returns no match or the docs are incomplete, say so explicitly and
fall back to repository code or official upstream docs — do not invent APIs
from memory.
```

Это тот же смысл, что у вашего варианта, но с именами тулов, границей и fallback. Пользовательский `~/.omp/agent/RULES.md` действует во всех проектах; если в конкретном репозитории нужны более узкие правила — кладёте `<repo>/.omp/RULES.md`, оба файла применяются одновременно, не перезаписывают друг друга【turn0fetch1】.

**Проверка после сохранения**

- Новая сессия (`/new`) — RULES.md читается при старте, в текущей не подхватится.
- `/extensions` → Rules — файл должен быть в списке как включённый, путь `~/.omp/agent/RULES.md`, без пометки shadowed.
- `/mcp list` → `context7` подключён, `/tools` показывает оба `mcp__context7_*`.
- Тестовый запрос без слова-триггера: «настрой middleware в Next.js с JWT-редиректом». Агент должен сам дернуть `resolve-library-id` → `get-library-docs` до написания кода.

**Про ожидания**

RULES.md — инструкция, а не принуждение: модель может изредка проигнорировать её, особенно если задача длинная или правило конкурирует с другим контекстом. Для первой итерации этого достаточно. Если заметите, что Context7 пропускается чаще, чем хотелось бы, — накатываете сверху TTSR-страховку из прошлого шага, она гарантированно обрывает «глухой» edit с внешним импортом.
