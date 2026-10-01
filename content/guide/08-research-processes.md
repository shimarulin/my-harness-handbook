# Глава 8. Исследовательские процессы

Как вести исследования (выбор технологий, ландшафтные обзоры, сравнения, spike) внутри git-репозитория проекта: структура, жизненный цикл, связь с ADR, правила для людей и агентов. Детали — `../content/kb/methods/research-knowledge.md`, `../content/kb/methods/research-tooling.md`.

## 8.1. Какой подход к знаниям выбрать

Вердикт исследования: **гибрид — ADR/RFC для решений + иерархический Markdown-органайзер для заметок + durable context файлы (AGENTS.md, learnings.md) для агентов**. Ключевой принцип: **«предсказуемая структура важнее графа»** — путь к информации вычислим из соглашения без исследования графа ссылок; для агента это проще retrieval и меньше галлюцинаций.

- **Research Compendium** — только для runnable-исследований (spike, PoC, бенчмарки); как основа всей базы знаний избыточен (финальный артефакт, не процесс). → `../content/kb/methods/research-compendium.md`
- **Zettelkasten (чистый)** — для командной разработки не переносится: самоцель, атомарность конфликтует с командной работой, `[[wikilinks]]` ломают toolchain, граф — худший сценарий для machine retrieval.
- **Digital Garden / ADR+RFC / Dendron-Foam / AGENTS.md** — компоненты гибрида, каждый для своей задачи.

## 8.2. Структура research/ и жизненный цикл

Базовая модель (статусы в путях — для малых корпусов S; для M+ — notes/+views/, см. §8.4):

```
research/
├── inbox/                  # черновики, низкий порог входа
├── active/YYYY-MM-DD-<slug>/
│   ├── README.md           # TL;DR, статус, выводы
│   ├── question.md         # вопрос, гипотезы
│   ├── findings/           # по файлу на источник/альтернативу
│   ├── comparison.md       # сравнительная таблица
│   ├── decision.md         # черновик решения → кандидат в ADR
│   └── spike/              # (опц.) runnable код = Research Compendium
├── decided/                # завершённые → ссылка на ADR
├── archive/YYYY/
├── templates/
└── learnings.md            # курсорный файл: накопленные уроки
```

Промоушен: inbox → active (> 3 файлов или > 500 строк); active → decided (decision.md прошёл review); → archive (> 1 года, нет ссылок в активных ADR). Переход в ADR: decision.md → `docs/adr/NNNN-<slug>.md` (MADR) с обратной ссылкой `Research: research/decided/…`.

Правила файлов: ≤ 1000 строк (больше — разбивать); front-matter обязателен (`author: human:/agent:`, created, updated, status, parent); один автор на один findings-файл (параллельная работа без конфликтов); README обновляется атомарно в конце цикла.

## 8.3. Масштабы корпуса и соответствие задаче

S Solo (< 100 файлов): inbox/ + active/ + learnings.md. M Team (100–1000): полная структура с threads/. L Multi-team (> 1000): + archive/, index/. По уровню задачи (соотносится с L0–L4, [глава 5](05-process-at-scale.md)): для L1 достаточно learnings.md + одна заметка в inbox/; для L4 — полный набор с Compendium, RFC, ADR.

## 8.4. Контент стабилен, структура виртуальна (для M+ корпусов)

Архитектура, выведенная из инсайтов о процессе (`../content/kb/principles/content-stays-virtual-structure.md`): файлы **не перемещаются** (`notes/YYYY-MM-DD-<slug>/` навсегда); статус — в **frontmatter**, не в директории; навигация — через **views/** (симлинки, материализация frontmatter) и теги `topics:`; MOC — опционально для аннотированных обзоров. Симлинки — основной механизм навигации (нативная для человека через tree и агента через ls); риски купированы (относительные пути, sync-скрипт, CI verify). Скрипты: `research-status.py` (смена статуса за O(1) токенов), `research-index.py`, `research-link.py` (sync/verify).

## 8.5. Tooling и готовые решения

Принцип: архитектура важнее языка (ядро логики отделено от интерфейса). Dual-mode CLI: интерактив для человека, флаги + `--json` для агента. Гибридная дистрибуция: ядро — внешний пакет, кастомизация — project-local `.research/` (templates/config/hooks/extensions с fallback chain). → `../content/kb/methods/research-tooling.md`

**Готовые решения** (`../content/kb/landscape/spec-kitty-research.md`): research — фаза delivery pipeline, не обязательно отдельная система. **Spec Kitty Research Mission** — evidence-gated research (guard «минимум 3 источника», evidence-log.csv, work packages) — adopt, если процессы укладываются в mission types. **specs.md Ideation Flow** — pre-research brainstorming (Spark → Flame → Forge). Собственная система — только если нужны cross-mission learnings + topic-views как первоклассные механизмы (вариант D: свои скрипты поверх notes/+views/, заимствуя guards и CSV-форматы).

## 8.6. Правила для AI-агентов

Перед началом: прочитай learnings.md; проверь decided/ и active/ по теме; создай inbox/…/notes.md. Во время: шаблоны; один findings-файл = одна альтернатива; `author: "agent:<name>"`; не редактируй чужие файлы. После: обнови learnings.md; промоутни inbox→active; решение → ADR; промоутни в decided/. Контекст по уровню: L1 = learnings.md + релевантный ADR; L2–L3 = + decided/ по теме; L4 = + полный active/ по теме.

---

**Дальше:** [Глава 9. Операционка](09-operations.md) — CI/CD, метрики, обучение, review, жизненный цикл.
