# Версионирование и жизненный цикл артефактов

| Параметр | Значение |
|---|---|
| Статус | draft |
| Обновлено | 2026-09-30 |

## Что это

Управление жизненным циклом артефактов документации: принятые решения (ADR/RFC) иммутабельны и меняются только через supersession; живые спецификации эволюционируют через формальный amendment process; deprecation и archive имеют явные workflow; версионирование — Git-based с semver для документации.

## Принципы

1. **Immutable Record** — принятые решения **никогда не редактируются**; изменения через supersession; история сохраняется для audit и обучения.
2. **Living Documentation** — спецификации обновляются по мере развития; код и документация эволюционируют вместе (в одном PR).
3. **Explicit Status** — каждый артефакт имеет явный статус в metadata; автоматическая проверка в CI.
4. **Traceability** — supersession-ссылки, amendment logs, cross-references обновляются при supersession.

## Три типа артефактов

| Тип | Lifecycle | Изменение после approval |
|---|---|---|
| **1. Immutable Decisions** (ADR, RFC) | Draft → In Review → Changes Requested → Approved → Superseded (↘ Blocked/Discarded/Rejected) | ❌ Только supersede |
| **2. Living Specifications** (Requirements, Approach, Tasks) | Draft → In Review → Approved → Active → Deprecated → Archived | ⚠️ Через amendment process |
| **3. Product Artifacts** (PRD) | Draft → In Review → Approved → Frozen → Archived | ❌ После freeze — нет |

## Supersession (immutable)

Три шага, **оба файла одним коммитом**:

1. Новый ADR (Status: Proposed; секция `## Supersedes [ADR-0007]`; контекст «Since ADR-0007…»; drivers; options; outcome).
2. Старый ADR: Status `Superseded by [ADR-0015](./adr-0015-*.md)`; Supersession Date; Supersession Reason; оригинальный контент сохранён («preserved for historical record»).
3. Commit: `docs(adr): supersede ADR-0007 with ADR-0015 …`.

CI: `validate_supersessions.py` — superseding ADR существует; старый содержит «Superseded by».

## Amendment (living)

Четыре шага:

1. **Propose Amendment** (шаблон): Current Requirement → Proposed Change → Justification → Impact Analysis (code/tests/docs/risk) → Approval Required (Tech Lead / PM / QA чекбоксы).
2. **Review**: checklist (justification sound, impact analyzed, no breaking changes, stakeholders notified, tests updated).
3. **Apply**: branch `amend/req-exp-020-v2.1` → bump version (v2.0 → v2.1) + amendment log entry (Changed / From / To / Reason / Approved by / Related ADR) → commit `docs(spec): amend REQ-EXP-020 …`.
4. **Update Related Artifacts**: approach.md секция с пометками Previous / Updated / How (ссылка на ADR).

Заголовок living spec: `Status: Active`, `Version: 2.1`, `Last amended: <date>`, `Amendment history: v1.0 … v2.0 … v2.1 …`.

## Deprecation и Archive

Deprecation workflow: announce (**3–6 months notice**) → migration guide → monitor usage → reach out to lagging consumers → sunset (старые endpoints возвращают **410 Gone**) → archive. Deprecation Notice: Status, Deprecation Date, **Sunset Date**, Replacement, Migration Guide, What Changed, Why, Action Required. Мониторинг: `monitor_deprecations.py` — алерт за 30 дней до sunset (Slack/email).

Archive triggers: feature retired; ADR/RFC superseded (keep, mark); major version bump (archive v1); project completed; team dissolution (historical repo). Структура: `docs/archive/{README.md (index), v1/YYYY-QN/<feature>/, deprecated/<feature>/}`. Правило: **«Archived documentation is read-only and not maintained»**.

## Версионирование

- **Git-based (рекомендуется)**: docs версионируются с кодом; tags = release versions, branches = parallel development.
- **Semver для документации**: MAJOR — breaking changes (API spec, process, terminology); MINOR — новые артефакты/секции/паттерны; PATCH — исправления, уточнения, примеры. Пример: `v1.1.0 → v2.0.0: Migrated from MADR 3.0 to MADR 4.0`.
- **Hybrid (enterprise)**: Git — source of truth; Docusaurus/MkDocs versioning — presentation (`/docs/1.2.0/intro`); авто-синхронизация через CI.
- Commit conventions: `docs(spec):`, `docs(adr):`; tagging: `git tag -a v1.2.0 -m "Release v1.2.0: …"`.

## Анти-паттерны

1. **Silent Edits to Approved Documents** — всегда supersession, никогда правка approved ADR.
2. **Orphaned Documents** — каждый документ имеет metadata header (status, version, date).
3. **Inconsistent Status** — enforce через linters и CI.
4. **No Amendment Process** — amendment log + approval.
5. **Broken Supersession Links** — автоматическая проверка в CI.
6. **Eternal Drafts** — **time-box draft phase 30 дней, затем auto-archive**.

## Источники

- Входные материалы inbox: `documentation-process-v2/versioning-lifecycle/README.md`
- Связанные KB: `docs-cicd.md` (CI-валидация), `review-collaboration.md` (approval процессов), `adr.md` (форматы и supersession в форматах)
