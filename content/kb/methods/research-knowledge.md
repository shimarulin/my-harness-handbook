# Исследовательские процессы и управление знаниями в разработке

| Параметр | Значение |
|---|---|
| Статус | draft |
| Обновлено | 2026-09-30 |

## Что это

Модель ведения исследований (выбор технологий, ландшафтные обзоры, сравнения, spike) внутри git-репозитория проекта: структура `research/`, жизненный цикл артефактов, шаблоны, связь с ADR, правила для людей и AI-агентов. Вердикт исходного исследования: **гибрид — ADR/RFC для решений + иерархический Markdown-органайзер для заметок + durable context файлы (AGENTS.md, learnings.md) для агентов**; Research Compendium — только для runnable-исследований; чистый Zettelkasten для командной разработки не переносится.

Ключевой принцип: **«предсказуемая структура важнее графа»** — путь к информации вычислим из соглашения без исследования графа ссылок. Для AI-агента: иерархия → проще retrieval → меньше галлюцинаций.

## Сравнение подходов к управлению знаниями

| Подход | Для человека | Для AI-агента | Git-native | Подходит для |
|---|---|---|---|---|
| **Research Compendium** | Высокая воспроизводимость | Хорошо (если Docker) | Да | Runnable spikes, бенчмарки, PoC |
| **Zettelkasten (чистый)** | Личная рефлексия, плох для команд | Плохо: нестандартные links, слабая структура | Частично | Личные дневники |
| **Digital Garden** | Заметки эволюционируют публично | Средне | Да (Markdown) | Ландшафтные обзоры |
| **ADR + RFC** | Явные решения с контекстом | Отлично: предсказуемая структура | Да | Решения, выбор технологий |
| **Dendron / Foam (иерархия)** | Nested структура как в IDE | Хорошо: предсказуемая схема | Да | Большой корпус заметок |
| **AGENTS.md / durable context** | Минимально (не для человека) | Отлично: интерфейс агента | Да | Правила, конвенции, «память» |
| **Agile Spike + findings** | Timeboxed, результат — документ | Средне | Да | Точечные исследования перед фичей |

Критика Zettelkasten (4 пункта): самоцель вместо инструмента; атомарность конфликтует с командной работой; `[[wikilinks]]` нестандартны и ломают toolchain (mdBook, Hugo, CI); граф из тысяч атомарных заметок — худший сценарий для machine retrieval.

Ограничения Research Compendium: ориентация на финальный артефакт, а не процесс; дисциплина окружения (Docker/Make) — overhead; не решает навигацию между десятками исследований (см. `research-compendium.md`).

## Структура research/ и жизненный цикл

Исходная модель (статусы в путях — впоследствии заменена моделью notes/+views/, см. `../principles/content-stays-virtual-structure.md`; здесь зафиксирована как работающая альтернатива для малых корпусов):

```
research/
├── inbox/                  # Черновики, низкий порог входа
│   └── YYYY-MM-DD-<slug>/notes.md
├── active/                 # Активные исследования
│   └── YYYY-MM-DD-<slug>/
│       ├── README.md       # TL;DR, статус, выводы
│       ├── question.md     # исходный вопрос, гипотезы
│       ├── findings/       # по файлу на источник/альтернативу
│       ├── threads/        # под-направления (при разрастании)
│       ├── comparison.md   # сравнительная таблица
│       ├── decision.md     # черновик решения → кандидат в ADR
│       └── spike/          # (опционально) runnable код = Research Compendium
├── decided/                # Завершённые → ссылка на ADR
├── archive/YYYY/           # Архив по годам
├── templates/
└── learnings.md            # Курсорный файл: накопленные уроки
```

Правила промоушена: inbox → active при > 3 файлов или > 500 строк; active → decided при decision.md, прошедшем review; → archive/YYYY/ при возрасте > 1 года и отсутствии ссылок в активных ADR. Переход в ADR: decision.md → `docs/adr/NNNN-<slug>.md` (MADR) с обратной ссылкой `Research: research/decided/YYYY-MM-DD-<slug>/`.

## Правила файлов и параллельной работы

1. Максимальный размер файла ~1000 строк — больше → разбивать.
2. Front-matter обязателен (findings/, threads/): `author` (`human:<name>` / `agent:<name>`), `created`, `updated`, `status` (draft|review|final), `parent`.
3. Один автор на один findings-файл — параллельная работа в разных файлах, merge-конфликтов нет.
4. README.md — единственный файл, который обновляют все (атомарно в конце цикла).

## Шаблоны

**question.md**: `--- author, created, status: draft ---` → `# Research: <тема>` → Вопрос → Контекст (требования-ссылки, ограничения) → Критерии сравнения → Известные альтернативы (чекбоксы) → Связанные ресурсы.

**findings-note.md**: frontmatter (author/created/updated/status/parent) → `# <Название>` → Источник (URL) → Ключевые характеристики → Pros → Cons → Чего не хватает → Соответствие критериям (таблица ✅/⚠️/❌) → Вывод (подходит / не подходит / требует исследования).

**comparison.md**: `# Сравнение: A vs B vs …` → таблица критериев → Чего не хватает → Вывод (предварительный).

**learnings.md** (курсорный, по месяцам): `## 2026-09` → `- **Выбор ORM:** SQLAlchemy > Peewee для async, из-за зрелости экосистемы. Смотри ADR-014.`

## Масштабы корпуса (S/M/L)

| Уровень | Корпус | Структура |
|---|---|---|
| **S** Solo | < 100 файлов, 1–2 человека | inbox/ + active/ + learnings.md |
| **M** Team | 100–1000 файлов, 3–10 человек | Полная структура с threads/ |
| **L** Multi-team | > 1000 файлов | + archive/, index/ (автоиндексы) |

Деградация: S ⊂ M ⊂ L; переход = добавление директорий, не реорганизация. Принцип соответствия уровню задачи (G5): для L1 достаточно learnings.md + одна заметка в inbox/; для L4 — полный набор с Research Compendium, RFC, ADR.

## Правила для AI-агентов (AGENTS.md, Research KB Rules)

- **Перед началом**: прочитай learnings.md; проверь research/decided/ и active/ по теме; создай inbox/YYYY-MM-DD-<slug>/notes.md.
- **Во время**: шаблоны; один findings-файл = одна альтернатива; `author: "agent:<name>"`; не редактируй чужие файлы; README обновляй в конце сессии.
- **После завершения**: обнови learnings.md; промоутни inbox→active; решение → ADR (MADR); промоутни в decided/.
- **Чтение для контекста**: L1 = learnings.md + релевантный ADR; L2–L3 = + research/decided/ по теме; L4 = + полный research/active/ по теме.

## Матрица выбора по сценариям

| Сценарий | Подход |
|---|---|
| Выбор библиотеки/фреймворка | Research Compendium (если бенчмарк) + comparison.md + ADR |
| Ландшафтный обзор | Digital Garden: `research/active/<slug>/landscape.md` |
| Architecture spike (PoC) | Research Compendium: код + Docker + findings |
| Быстрое исследование (L1–L2) | Lightweight: inbox/<дата>-<slug> → промоут в active/ |
| Решение уровня платформы (L4) | RFC + Compendium (если код) + ADR + learnings.md |
| Накопление уроков | research/learnings.md |
| Контекст для AI-агентов | AGENTS.md + ссылки на learnings.md, ADR, spec |

## От чего воздержаться на старте

Полноценный Zettelkasten с wiki-links (команда > 1 человека); Research Compendium для каждого исследования; тяжёлые PKM-инструменты как обязательная зависимость (Obsidian — личный выбор, не зависимость процесса). «Ритуалы вместо инструментов»: система работает, когда проста и встроена в workflow (Git, PR, code review).

## Источники

- Входные материалы inbox: `research-and-notes/research-process.md` (строки 1–629)
- Инструменты: Foam (https://github.com/foambubble/foam), Dendron (https://github.com/dendronhq/dendron), Repomix (https://github.com/yamadashy/repomix), MkDocs Material (https://squidfunk.github.io/mkdocs-material/)
- Связанные KB: `research-compendium.md`, `research-tooling.md`, `../principles/content-stays-virtual-structure.md`, `../landscape/spec-kitty-research.md`
