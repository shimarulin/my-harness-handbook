# Data Formats

## Purpose

This is the final document of the architecture phase. It owns the physical formats and the repository layout that the other documents reference: the artifact tree, `spec://` resolution and its extensions, identity allocation, the event-log schema (carrying the atomicity requirement recorded in execution-layers), governance artifact schemas, triggering formats, measurement formats, harness integration profiles, and the migration framework.

Logical contracts live where they were settled — the `spec://` identifier contract and the session-identity semantics in [governance-protocol.md](./governance-protocol.md), ownership declarations in [composition.md](./composition.md) — and are *not* restated here except as physical schemas.

## Design constraints honored

- **FR-6.2 (repo-native):** every persistent format is a versioned file in the repository; the cache is derived state and carries no semantics (see below).
- **NFR-2 / FR-6.7 (offline):** all formats are plain local files; resolution never requires network.
- **NFR-5 (no daemon, cold start):** nothing here requires eager parsing at startup — manifests, lists, and profiles are read on demand; digests per governance-protocol Facet 2.
- **NFR-1:** event-log and record formats are sized for streaming reads at invocation points, not whole-log loads.

## Repository layout

The tool root is `.sdd/` (directory name, like the tool name, is a placeholder per composition.md):

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

**Sharding:** `<shard>` is a two-character prefix of the identifier (ULID prefix), bounding directory sizes. Adequacy at scale is known unknown #1. `missions/` is deliberately **not** sharded: mission directories are living, near-empty after compaction (they hold only the pointer record), so their count grows slowly and each is transient — unlike the append-only `sessions/` and `decisions/` trees.

**Cache:** derived content only (resolved rule fragments, compiled digests), keyed by content digest (governance-protocol Facet 2, covering FR-5.5 invalidation across all input classes). It is gitignored by default: recoverable, and semantics never depend on it — satisfying FR-6.2's "no tool state outside the repository affects semantics," since a cache hit and a regeneration are indistinguishable in behavior.

**Adapter-declared homes:** in Mode A/B compositions, negotiable classes live at adapter-declared paths (composition ownership matrix); this tree then holds the core-owned spine (decisions, sessions, events, missions) and whatever negotiable classes the composition homes here. The adapter's resolution mapping (below) is the bridge.

## Identity allocation

- **mission-id:** repo-local **ULID**, allocated by the core at mission creation. Global uniqueness comes from the repo-qualified URI: `spec://<repo>/missions/<id>` collides only if two repositories share an identifier — outside v1 scope (single repo), and the Q5 future-proofing is precisely this addressability.
- **session-id:** per NQ-Q — UUIDv7/ULID, opaque, never derived from (harness, branch, timestamp); sharded path as above.
- **change-id:** repo-local, human-readable slug preferred (it appears in paths and review surfaces); ULID fallback for generated names.

## `spec://` resolution

### Classes and granularity

```
spec://<repo>/<class>/<id>
  classes: requirements | changes | decisions | missions | sessions
```

- `events` is **not** a class: event-log records are not individually addressable; the mission record is the sole addressable unit for mission-scoped activity (governance-protocol v1.2.1).
- Resolution is local against the artifact tree (NFR-2). `<repo>` resolves to the local repository in v1; other values are **cross-repo references** — syntactically valid, resolution deferred (Q5).

### Link classes (NQ-E)

| Class | Meaning | CI behavior |
|---|---|---|
| **broken** | the target does not exist (bad id, deleted without trace) | **fail** (FR-4.6 AC) |
| **unresolvable** | the target exists but is not resolvable in this context (cross-repo reference, other repo absent) | **warn** — graceful degradation; becomes *fail* only inside repos that opt into cross-repo resolution |

This distinction is recorded now so that a future cross-repo extension does not force a CP on FR-4.6: within v1's single-repo scope, unresolvable links arise only from hand-written cross-repo references, and warning is the correct behavior for them.

### Adapter resolution mappings

Adapters declare, per negotiable class they home, the mapping from `spec://` class to physical location:

```yaml
# inside the adapter declaration (composition template #2)
ownership:
  - class: changes
    home: external
    resolve:
      spec://<repo>/changes/<id> → openspec/changes/<id>/
```

The mapping is a pure path function (local, offline, deterministic). Non-core homes that cannot be expressed as path functions are not addressable and must not be referenced by core artifacts.

**Mission records under compaction (and under external archiving).** `spec://<repo>/missions/<id>` must resolve for the mission's entire lifetime — before and after compaction. Resolution stays a pure path function via an **alias file**: compaction folds the record into `changes/archive/<date>-<id>/mission-record.md` and leaves a pointer record at the live path (`missions/<id>/record.md` → archive location). This is part of the identifier contract (governance-protocol), not resolver state. Adapter mappings for mission-bearing classes must declare the same guarantee for external homes — the post-archiving path (or a pointer mechanism of the external tool's own) — because external tools perform their own archiving (composition KU #6); a mapping that cannot keep the identifier stable across the external tool's archive step is not a valid mapping.

## Event log

### Record schema (JSONL)

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

- Fields per governance-protocol; `refs` entries are optional per type but, when present, must resolve (link classes above).
- `mission` is **null-able**: events in the global log (protocol upgrades, kill-switch toggles) carry `mission: null`; per-mission logs require it non-null.
- `projection.gap` payloads additionally carry the **transition reference** — artifact path and diff identifiers — per the lifecycle contract: resolution is derived at query time by re-matching against the adapter's current signature set; no `.resolved` event type exists.
- `skill.invoked` payloads carry **`invocation_origin: preemptive | remedial | explicit`** (the decision-origin classification of execution-layers: preemptive = hooks/trigger-list; remedial = gate dispatch on either channel, including runner invocations performed directly in response to a failure payload; explicit = user command or payload-independent configuration) and the skill reference — making the FR-3.1 rate and the NQ-H split reconstructible from the log alone.

### Atomicity (the tagged requirement from execution-layers)

**One git commit carries both the artifact change and the appended event record.** Tool code stages the artifact write and the log append together; the commit is the transaction. Per-mission logs are single-writer (FR-5.3 worktree isolation); global-log concurrency resolves as ordinary git merges. A committed artifact without its event, or an event without its artifact, is an anomaly the detection pass flags — this is what makes core-event silence a tripwire (consumer principle, core-emitter class).

### Compaction interplay (NQ-P)

On archive, `events/missions/<id>/log.jsonl` folds into `changes/archive/<date>-<id>/mission-record.md`: verdicts, decision references, escalation records, session references retained; per-cycle review detail dropped. The mission record remains the addressable unit; the raw log file is removed with the fold (it was never addressable).

## Governance artifact schemas

### Decision records (FR-4.4)

Markdown with front matter:

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

Arbitration verdicts (FR-2.5 Class B) additionally record both versions and the losing version's archive location (FR-2.3).

### Session manifests (NQ-Q)

JSON per the governance-protocol contract (fields fixed there: `session_id`, `parent_session_id`, `continues_session_id`, `kind`, `harness`, `agent`, `operator`, repo/branch/worktree, `mission_id`, `task_id`, timestamps, `commit_shas`, `config_digest`, `governance_digest`, `decision_ids`, `review_ids`). Physical: `sessions/<shard>/<session-id>.json`. The optional signature field, if ever populated, is checked per execution-layers Layer 6 — present-but-invalid fails the gate; absent passes under non-requiring configuration.

### Mission record

Markdown, created at mission start as the live index (pointer to active change, phase state, open decisions); folded with event detail at compaction. The only `spec://`-addressable unit for mission activity.

## Triggering formats

### Trigger list (triggering mechanism 2)

```yaml
- skill: systematic-debugging
  when: [test-failure, tool-error]     # carrier-dependent semantics (v1.0.1):
                                       #   code on the hooks path, natural-language
                                       #   match conditions on the fallback path
  load: skills/systematic-debugging/SKILL.md
  explicit-only: false                 # true for skills with no observable predicate
```

Always-loaded placement is a per-harness property recorded in the harness profile (below) — the native instruction surface of each harness (system prefix, rules file, equivalent).

### Injection block (execution-layers channel 1)

A compact structured block injected tool-side into next-turn context:

```yaml
gate: <gate-id>
blocked-evidence: <named evidence per the gate's criterion>
producing-skill: <skill>
ref: <event/decision reference>
```

### `run <skill>` (headless command)

```
<tool> run <skill> [--mission <id>] [--evidence <ref>]
```

Headless-capable; exit codes distinguish success, unresolved-evidence, and gate-reblock (feeding the one-dispatch-per-cycle bound).

## Measurement formats

### Reference corpus (execution-layers Layer 5)

```
.sdd/corpus/                      # project-local only: community-contributed cases
  <case-id>/
    task.md            # the task, ceremony level, expected artifacts
    labels.yaml        # [{skill, applicable, rationale}]
    review.md          # adversarial review record: reviewer (non-author), blind attestation
```

Labeling policy per execution-layers v1.0.1: adversarial, non-author, blind-to-runtime-results; community cases follow the same policy.

**Shipping split.** The **shipped corpus lives in the install directory, not `.sdd/`** — it is tool state, not project state: repository decisions must not mutate shipped ground truth (the FR-6.2 boundary runs both ways). Shipped labels version with the tool version and are replaced on upgrade; project-local community cases are never touched by an upgrade. Measurement runs aggregate both sources and record the corpus composition (shipped version + local case ids) alongside the score, so results stay interpretable across upgrades.

### Cost report (FR-5.4)

JSON per mission under `reports/<mission-id>/`: totals, per-phase tokens and time, and the itemizations — ceremony baseline vs. strict-enforcement allowance (FR-1.4), subagent package injection (FR-3.3), preemptive/remedial split (NQ-H), bridged vs. native flows (composition KU #5), and the running-baseline comparison.

## Harness integration profiles

One profile per supported harness (the FR-6.1 ten: Claude Code, Cursor, GitHub Copilot, Gemini CLI, Codex, OpenCode, Windsurf, Antigravity, Devin CLI, Qwen Code), itself a versioned artifact:

```yaml
harness: <name>
invocation-grammar: <command form per this harness's native conventions>
hook-surface: <available pre/post-action hooks, or none>
injection-point: <tool-controllable next-turn injection, or none>   # execution-layers KU #1
always-loaded-placement: <native surface for the trigger list>
notes: <grammar variance, limitations>
```

Profiles are the living record for execution-layers KU #1 (two-channel sufficiency) and triggering KU #1 (hook coverage); their correctness across external harness versions is itself field data (known unknown #4 below). The research already documents the variance to expect: the same OpenSpec command as `/opsx:propose`, `/opsx-propose`, `@opsx-propose` per harness.

## Migration framework (FR-8.6 applied)

- **Pre-upgrade check:** reads the current tree, reports required migrations before applying anything — including every intentional-loss migration flagged with its warning (what is lost, how to back up).
- **Classes:** data-losing migrations are reversible with a down-migration test gating release; add-only migrations are idempotent by construction; intentional-loss migrations carry the FR-6.6/PG-1 deprecation window (removal lands at least one major version after the notice).
- **`spec://` scheme:** versioned with the protocol (synchronous facets, NQ-C); scheme changes are subject to the same classes once artifacts exist in the wild. Pre-release, layout revisions carry no migration obligation (governance-protocol versioning).
- **Adopted formats (Mode A):** explicitly *not* covered — FR-8.6 guarantees do not extend to them (composition trade-off); adapters pre-check and warn.

## Known unknowns (field verification required)

1. **Sharding adequacy:** two-character prefixes at sessions/decisions scale; re-sharding later is an add-only migration, but the cost should be measured, not assumed.
2. **Injection-point availability** per harness — recorded live in the profiles; the open half of execution-layers KU #1.
3. **Corpus label schema evolution** under community contribution — labels and reviews are versioned, but drift between shipped and contributed case shapes needs field data.
4. **Profile stability:** harness native surfaces (grammar, rules-file behavior) drift across external versions; the profiles' own versioning must be fed by the drift-check discipline (composition adapter template #1).

## Status

- Final document of the architecture phase: artifact tree, resolution, identity, event-log schema with atomicity, governance/triggering/measurement formats, harness profiles, migration framework
- Consumes: governance-protocol (identifier contract, session identity, event semantics), composition (ownership declarations, adapter mappings), triggering (formats deferred there), execution-layers (atomicity tag, corpus policy, profile fields)
- Honors NFR constraints 1–5
- Version 1.0.1: mission-record alias/pointer mechanism (U), adapter mapping stability requirement across external archiving, corpus shipping split (V), `skill.invoked` schema fields (W), null-able mission for global events (X), mission sharding note (Y)
- Phase complete: architecture set closed (README, governance-protocol, composition, triggering, execution-layers, data-formats)
