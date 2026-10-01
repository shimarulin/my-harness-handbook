---
id: research-note-20261002-000000001
type: research-note
status: active
created: 2026-10-02
updated: 2026-10-02
topics: [sdd-tools, specs-md, spec-kitty, artifacts, integration]
author: agent:omp
---

# Research: артефакты specs.md и spec-kitty для нашего репозитория

## Вопрос

Какие артефакты создают specs.md и spec-kitty при работе в репозитории, как они интегрируются с нашей трёхслойной структурой (`content/`, `docs/`, `tools/process-framework/`), и что можно adopt/adapt без конфликтов?

## Критерии

- Совместимость с нашей структурой (нет конфликтов путей)
- Совместимость с нашим frontmatter (обязателен во всех слоях)
- Ценность артефактов для research и планирования
- Стоимость интеграции (adopt / adapt / build)

## Метод

Два параллельных research-агента (task), веб-поиск + чтение GitHub README, docs, source code. Синтез — этот документ.

## Статус

- ✅ specs.md — исследовано (agent: SpecsMdResearch)
- ✅ spec-kitty — исследовано (agent: SpecKittyResearch)
- 🔄 Синтез и сравнение — этот документ
