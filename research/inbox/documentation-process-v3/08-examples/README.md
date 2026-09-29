# Примеры: от идеи до PR

| Параметр | Значение |
|---|---|
| Дата | 2026-09-29 |
| Статус | Draft |
| Связан с | `02-process-design.md`, `06-repository-structure.md` |

Этот каталог содержит **полные заполненные примеры** инициатив трёх уровней
сложности, демонстрирующие процесс «от идеи до PR» с использованием артефактов
из `06-repository-structure.md`.

---

## Структура примеров

| Пример | Уровень | Что демонстрирует | Источник вдохновения |
|---|---|---|---|
| [01-task-l1/](01-task-l1/) | L1 | Простая задача: Job Story → tasks → PR | [NetPace walkthrough](https://github.com) |
| [02-feature-l2/](02-feature-l2/) | L2 | Фича: PRD → Spec → Tasks → PR | [Spec Kit Quickstart](https://github.github.com/spec-kit/quickstart.html) |
| [03-major-l3/](03-major-l3/) | L3 | Крупная фича: RFC → ADR → Spec → Implementation | [OpenSpec Examples](https://github.com/Fission-AI/OpenSpec/blob/main/docs/examples.md) |

---

## Как использовать эти примеры

1. **Изучение**: прочитать артефакты в порядке пайплайна для понимания потока
2. **Копирование**: использовать как шаблоны для реальных проектов
3. **Валидация**: проверить свои артефакты против этих примеров
4. **Обучение AI-агентов**: добавить в контекст как few-shot examples

---

## Сравнение уровней

| Аспект | L1 (Task) | L2 (Feature) | L3 (Major) |
|---|---|---|---|
| **Артефактов** | 1 (task.md) | 3 (prd, spec, tasks) | 5+ (rfc, adr, spec, design, tasks) |
| **Время на доки** | ~15 мин | ~2-4 часа | ~1-2 дня |
| **AI-агентов** | 1 session | 2-3 sessions | Multiple sessions |
| **Ревью** | Code review | Spec review + code review | RFC review + ADR + spec + code |
| **Риск** | Низкий | Средний | Высокий (архитектурный) |

---

## Каталог примеров

```
08-examples/
├── README.md                     # Этот файл
├── 01-task-l1/
│   ├── README.md                 # Описание примера
│   ├── task-042.md               # L1 задача
│   └── PR_DESCRIPTION.md         # Пример PR description
├── 02-feature-l2/
│   ├── README.md
│   ├── prd-005.md               # PRD
│   ├── spec-012/
│   │   ├── spec.md              # Specification с EARS
│   │   └── tasks.md             # Task breakdown
│   └── PR_DESCRIPTION.md
└── 03-major-l3/
    ├── README.md
    ├── rfc-0031.md              # RFC / Design Doc
    ├── adr-0007.md              # ADR (результат RFC)
    ├── spec-015/
    │   ├── spec.md              # Spec с delta requirements
    │   └── tasks.md
    └── PR_DESCRIPTION.md
```
