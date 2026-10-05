# Форматы данных

## Назначение

Это финальный документ архитектурной фазы. Он владеет физическими форматами и макетом репозитория, на которые ссылаются другие документы: дерево артефактов, разрешение `spec://` и его расширения, распределение идентификаторов, схема журнала событий (несущая требование атомарности, записанное в execution-layers), схемы артефактов управления, форматы триггеров, форматы измерений, профили интеграции harness и фреймворк миграции.

Логические контракты живут там, где были установлены — контракт идентификаторов `spec://` и семантика идентичности сессии в [governance-protocol.md](./governance-protocol.md), объявления владения в [composition.md](./composition.md) — и *не* пересказываются здесь, кроме как в виде физических схем.

## Соблюдаемые проектные ограничения

- **FR-6.2 (repo-native):** каждый постоянный формат — версионированный файл в репозитории; кэш — производное состояние и не несёт семантики (см. ниже).
- **NFR-2 / FR-6.7 (офлайн):** все форматы — простые локальные файлы; разрешение никогда не требует сети.
- **NFR-5 (без daemon, холодный старт):** ничто здесь не требует жадного парсинга при запуске — манифесты, списки и профили читаются по требованию; digests согласно governance-protocol Facet 2.
- **NFR-1:** форматы журнала событий и записей рассчитаны на потоковое чтение в точках вызова, а не на загрузку всего журнала.

## Макет репозитория

Корень инструмента — `.sdd/` (имя каталога, как и имя инструмента, — placeholder согласно composition.md):

```
.sdd/
  config/                        # all configuration (FR-6.2): ceremony defaults,
                                 #   strictness profiles, ownership declaration,
                                 #   integration consent (per-integration files)
  specs/                         # canonical spec tree (the current truth)
  changes/
    <change-id>/                 # active change folders
    archive/<date>-<change-id>/  # archived changes; mission records fold in here
  decisions/<shard>/<id>.md      # decision records (FR-4.4)
  missions/<mission-id>/
    record.md                    # live index from mission start; folded at compaction
                                 #   — post-compaction, a pointer record remains (see below)
  sessions/<shard>/<session-id>.json
  events/
    missions/<mission-id>/log.jsonl
    global/log.jsonl
  corpus/                        # reference corpus: shipped + community cases
  reports/<mission-id>/          # cost reports (FR-5.4)
  cache/                         # content-digest keyed derived state; gitignored
```

**Шардирование:** `<shard>` — двухсимвольный префикс идентификатора (префикс ULID), ограничивающий размеры каталогов. Достаточность при масштабе — известное неизвестное #1. `missions/` намеренно **не** шардируется: каталоги миссий живые, почти пустые после компакции (содержат только pointer record), поэтому их количество растёт медленно и каждый транзиентен — в отличие от append-only деревьев `sessions/` и `decisions/`.

**Кэш:** только производный контент (разрешённые фрагменты правил, скомпилированные digests), ключ — content digest (governance-protocol Facet 2, покрывающий инвалидацию FR-5.5 across all input classes). По умолчанию gitignored: восстановим, и семантика никогда от него не зависит — удовлетворяет FR-6.2 «no tool state outside the repository affects semantics», поскольку попадание в кэш и регенерация неразличимы по поведению.

**Adapter-declared homes:** в композициях режима A/B negotiable классы живут по путям, объявленным адаптером (матрица владения composition); это дерево тогда содержит core-owned хребет (decisions, sessions, events, missions) и любые negotiable классы, которые композиция размещает здесь. Отображение разрешения адаптера (ниже) — мост.

## Распределение идентификаторов

- **mission-id:** repo-local **ULID**, распределяется ядром при создании миссии. Глобальная уникальность приходит из repo-qualified URI: `spec://<repo>/missions/<id>` коллизируется только если два репозитория используют один идентификатор — вне области v1 (single repo), а future-proofing Q5 — именно эта адресуемость.
- **session-id:** согласно NQ-Q — UUIDv7/ULID, непрозрачный, никогда не выводится из (harness, branch, timestamp); шардированный путь как выше.
- **change-id:** repo-local, предпочтительно человекочитаемый slug (появляется в путях и поверхностях обзора); ULID fallback для сгенерированных имён.

## Разрешение `spec://`

### Классы и гранулярность

```
spec://<repo>/<class>/<id>
  classes: requirements | changes | decisions | missions | sessions
```

- `events` **не** класс: записи журнала событий не адресуемы индивидуально; запись миссии — единственная адресуемая единица для активности миссии (governance-protocol v1.2.1).
- Разрешение локальное против дерева артефактов (NFR-2). `<repo>` разрешается в локальный репозиторий в v1; другие значения — **кросс-репозиторные ссылки** — синтаксически валидны, разрешение отложено (Q5).

### Классы ссылок (NQ-E)

| Класс | Значение | Поведение CI |
|---|---|---|
| **broken** | цель не существует (плохой id, удалена без следа) | **fail** (FR-4.6 AC) |
| **unresolvable** | цель существует, но не разрешима в этом контексте (кросс-репозиторная ссылка, другого репозитория нет) | **warn** — graceful degradation; становится *fail* только внутри репозиториев, opting into cross-repo resolution |

Это различие записано сейчас, чтобы будущее кросс-репозиторное расширение не вынудило CP на FR-4.6: в рамках single-repo v1 unresolvable ссылки возникают только из рукописных кросс-репозиторных ссылок, и предупреждение — правильное поведение для них.

### Отображения разрешения адаптера

Адаптеры объявляют, по каждому negotiable классу, который они home, отображение класса `spec://` на физическое расположение:

```yaml
# inside the adapter declaration (composition template #2)
ownership:
  - class: changes
    home: external
    resolve:
      spec://<repo>/changes/<id> → openspec/changes/<id>/
```

Отображение — чистая функция пути (локальная, офлайн, детерминированная). Не-core homes, которые не могут быть выражены как функции пути, не адресуемы и не должны упоминаться core-артефактами.

**Записи миссий при компакции (и при внешней архивации).** `spec://<repo>/missions/<id>` должен разрешаться в течение всей жизни миссии — до и после компакции. Разрешение остаётся чистой функцией пути через **alias file**: компакция складывает запись в `changes/archive/<date>-<id>/mission-record.md` и оставляет pointer record по живому пути (`missions/<id>/record.md` → archive location). Это часть контракта идентификаторов (governance-protocol), а не состояние resolver. Отображения адаптера для mission-bearing классов должны объявлять ту же гарантию для внешних homes — путь после архивации (или pointer mechanism самого внешнего инструмента) — потому что внешние инструменты выполняют собственную архивацию (composition KU #6); отображение, которое не может сохранить идентификатор стабильным через шаг архивации внешнего инструмента, не является валидным отображением.

## Журнал событий

### Схема записи (JSONL)

```json
{
  "type": "review.verdict",
  "session": "spec://<repo>/sessions/<session-id>",
  "ts": "2026-10-02T14:03:11Z",
  "mission": "spec://<repo>/missions/<mission-id>",
  "refs": {
    "requirement": "spec://<repo>/requirements/<id>",
    "change": "spec://<repo>/changes/<id>",
    "decision": "spec://<repo>/decisions/<id>"
  },
  "payload": { }
}
```

- Поля согласно governance-protocol; записи `refs` опциональны по типу, но при наличии должны разрешаться (классы ссылок выше).
- `mission` **nullable**: события в глобальном журнале (обновления протокола, переключения kill-switch) несут `mission: null`; per-mission журналы требуют non-null.
- Полезные нагрузки `projection.gap` дополнительно несут **ссылку на переход** — путь артефакта и идентификаторы diff — согласно контракту жизненного цикла: разрешение выводится во время запроса повторным сопоставлением с текущим набором сигнатур адаптера; тип события `.resolved` не существует.
- Полезные нагрузки `skill.invoked` несут **`invocation_origin: preemptive | remedial | explicit`** (классификация происхождения решения execution-layers: preemptive = hooks/trigger-list; remedial = gate dispatch на любом канале, включая вызовы runner, выполненные непосредственно в ответ на failure payload; explicit = пользовательская команда или независимая от payload конфигурация) и ссылку на навык — делая частоту FR-3.1 и split NQ-H восстановимыми только из журнала.

### Атомарность (помеченное требование из execution-layers)

**Один git commit несёт и изменение артефакта, и добавленную запись события.** Код инструмента ставит запись артефакта и добавление в журнал вместе; commit — транзакция. Per-mission журналы single-writer (изоляция worktree FR-5.3); параллелизм глобального журнала разрешается как обычные git merge. Закоммиченный артефакт без своего события или событие без артефакта — аномалия, которую отмечает проход обнаружения — именно это делает тишину core-event tripwire (принцип потребителя, класс core-emitter).

### Взаимодействие с компакцией (NQ-P)

При архивации `events/missions/<id>/log.jsonl` складывается в `changes/archive/<date>-<id>/mission-record.md`: вердикты, ссылки на решения, записи эскалации, ссылки на сессии сохраняются; детали обзора по циклам отбрасываются. Запись миссии остаётся адресуемой единицей; сырой файл журнала удаляется вместе со свёрткой (он никогда не был адресуемым).

## Схемы артефактов управления

### Записи решений (FR-4.4)

Markdown с front matter:

```markdown
---
id: <ulid>
kind: arbitration | rejection | unknown-resolution | review-outcome | ...
refs: [spec://…, …]
sessions: [<session-id>]
ts: <ISO-8601>
---
<body: the decision, the reasoning, the alternatives>
```

Вердикты арбитража (FR-2.5 Class B) дополнительно записывают обе версии и архивное расположение проигравшей версии (FR-2.3).

### Манифесты сессий (NQ-Q)

JSON согласно контракту governance-protocol (поля фиксированы там: `session_id`, `parent_session_id`, `continues_session_id`, `kind`, `harness`, `agent`, `operator`, repo/branch/worktree, `mission_id`, `task_id`, timestamps, `commit_shas`, `config_digest`, `governance_digest`, `decision_ids`, `review_ids`). Физически: `sessions/<shard>/<session-id>.json`. Опциональное поле подписи, если когда-либо заполнено, проверяется согласно execution-layers Layer 6 — present-but-invalid валит шлюз; absent проходит при non-requiring конфигурации.

### Запись миссии

Markdown, создаётся в начале миссии как живой индекс (указатель на активное изменение, состояние фазы, открытые решения); складывается с деталями событий при компакции. Единственная `spec://`-адресуемая единица для активности миссии.

## Форматы триггеров

### Список триггеров (механизм триггеров 2)

```yaml
- skill: systematic-debugging
  when: [test-failure, tool-error]     # carrier-dependent semantics (v1.0.1):
                                       #   code on the hooks path, natural-language
                                       #   match conditions on the fallback path
  load: skills/systematic-debugging/SKILL.md
  explicit-only: false                 # true for skills with no observable predicate
```

Размещение always-loaded — свойство per-harness, записанное в профиле harness (ниже) — нативная поверхность инструкций каждого harness (системный префикс, rules file, эквивалент).

### Блок инъекции (канал 1 execution-layers)

Компактный структурированный блок, инжектируемый tool-side в контекст следующего хода:

```yaml
gate: <gate-id>
blocked-evidence: <named evidence per the gate's criterion>
producing-skill: <skill>
ref: <event/decision reference>
```

### `run <skill>` (headless-команда)

```
<tool> run <skill> [--mission <id>] [--evidence <ref>]
```

Headless-capable; коды выхода различают успех, unresolved-evidence и gate-reblock (питая границу one-dispatch-per-cycle).

## Форматы измерений

### Референсный корпус (execution-layers Layer 5)

```
.sdd/corpus/                      # project-local only: community-contributed cases
  <case-id>/
    task.md            # the task, ceremony level, expected artifacts
    labels.yaml        # [{skill, applicable, rationale}]
    review.md          # adversarial review record: reviewer (non-author), blind attestation
```

Политика разметки согласно execution-layers v1.0.1: состязательная, не-автор, слепая к runtime-результатам; community cases следуют той же политике.

**Разделение поставки.** **Поставляемый корпус живёт в каталоге установки, а не в `.sdd/`** — это состояние инструмента, а не состояние проекта: решения репозитория не должны мутировать поставляемую ground truth (граница FR-6.2 работает в обе стороны). Поставляемые метки версионируются с версией инструмента и заменяются при обновлении; project-local community cases никогда не трогаются обновлением. Измерительные прогоны агрегируют оба источника и записывают состав корпуса (поставляемая версия + локальные case ids) рядом со score, чтобы результаты оставались интерпретируемыми across upgrades.

### Отчёт о стоимости (FR-5.4)

JSON per mission под `reports/<mission-id>/`: итоги, токены и время по фазам, и itemizations — базовая линия церемонии vs допуск строгого принуждения (FR-1.4), инъекция пакета субагента (FR-3.3), split preemptive/remedial (NQ-H), bridged vs native flows (composition KU #5) и сравнение с текущей базовой линией.

## Профили интеграции harness

Один профиль на поддерживаемый harness (десять FR-6.1: Claude Code, Cursor, GitHub Copilot, Gemini CLI, Codex, OpenCode, Windsurf, Antigravity, Devin CLI, Qwen Code), сам по себе версионированный артефакт:

```yaml
harness: <name>
invocation-grammar: <command form per this harness's native conventions>
hook-surface: <available pre/post-action hooks, or none>
injection-point: <tool-controllable next-turn injection, or none>   # execution-layers KU #1
always-loaded-placement: <native surface for the trigger list>
notes: <grammar variance, limitations>
```

Профили — живая запись для execution-layers KU #1 (достаточность двух каналов) и triggering KU #1 (покрытие хуков); их корректность across внешних версий harness сама является полевыми данными (известное неизвестное #4 ниже). Исследование уже документирует ожидаемую вариативность: та же команда OpenSpec как `/opsx:propose`, `/opsx-propose`, `@opsx-propose` по harness.

## Фреймворк миграции (применённый FR-8.6)

- **Предварительная проверка обновления:** читает текущее дерево, сообщает требуемые миграции до применения чего-либо — включая каждую миграцию с намеренной потерей, помеченную своим предупреждением (что теряется, как сделать резервную копию).
- **Классы:** миграции с потерей данных обратимы с down-migration тестом, гейтящим релиз; add-only миграции идемпотентны по построению; миграции с намеренной потерей несут окно устаревания FR-6.6/PG-1 (удаление происходит как минимум через одну мажорную версию после уведомления).
- **Схема `spec://`:** версионируется с протоколом (синхронные грани, NQ-C); изменения схемы подчиняются тем же классам, как только артефакты появятся в реальной эксплуатации. Предрелизные ревизии макета не несут обязательств миграции (governance-protocol versioning).
- **Adopted formats (режим A):** явно *не* покрыты — гарантии FR-8.6 на них не распространяются (компромисс composition); адаптеры предварительно проверяют и предупреждают.

## Известные неизвестные (требуется полевая верификация)

1. **Достаточность шардирования:** двухсимвольные префиксы при масштабе sessions/decisions; повторное шардирование позже — add-only миграция, но стоимость следует измерять, а не предполагать.
2. **Доступность точки инъекции** по harness — записывается живо в профилях; открытая половина execution-layers KU #1.
3. **Эволюция схемы меток корпуса** при вкладе сообщества — метки и обзоры версионируются, но дрейф между поставляемыми и внесёнными формами кейсов требует полевых данных.
4. **Стабильность профилей:** нативные поверхности harness (грамматика, поведение rules-file) дрейфуют across внешних версий; собственное версионирование профилей должно питаться дисциплиной drift-check (composition adapter template #1).

## Статус

- Финальный документ архитектурной фазы: дерево артефактов, разрешение, идентичность, схема журнала событий с атомарностью, форматы управления/триггеров/измерений, профили harness, фреймворк миграции
- Потребляет: governance-protocol (контракт идентификаторов, идентичность сессии, семантика событий), composition (объявления владения, отображения адаптеров), triggering (форматы, отложенные там), execution-layers (тег атомарности, политика корпуса, поля профилей)
- Соблюдает ограничения NFR 1–5
- Версия 1.0.1: механизм alias/pointer записи миссии (U), требование стабильности отображения адаптера через внешнюю архивацию, разделение поставки корпуса (V), поля схемы `skill.invoked` (W), nullable mission для глобальных событий (X), заметка о шардировании миссий (Y)
- Фаза завершена: архитектурный набор закрыт (README, governance-protocol, composition, triggering, execution-layers, data-formats)
