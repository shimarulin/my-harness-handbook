# Change Proposal Process

## Purpose

This document defines how [ideal-tool-requirements.md](./ideal-tool-requirements.md) changes after its stabilization as the v2.0 baseline (2026-10-02). It implements the change-proposal mechanism referenced in the baseline's Stabilization Note and closes decision 8 of the post-freeze review (2026-10-02).

## Scope: what requires a change proposal

A change proposal (CP) is required **only when normative text changes** — that is, when an FR, NFR, or PG identifier gains, loses, or modifies requirement text or acceptance criteria.

A CP is **not** required for:

- Architectural decisions that realize a requirement without changing its text (mechanism choices, format specifications, module decomposition)
- Additive observability or auditing that no requirement prohibits (e.g., the preemptive-vs-remedial trigger audit added by the Q3 resolution)
- Clarifications recorded in companion documents (architecture document, future-proofing notes) that do not contradict the baseline
- Non-normative prose fixes (typos, wording), which are applied directly with a changelog entry

**Operational test:** *does any acceptance criterion behave differently after this change?* If yes, it is a CP. If no conforming implementation can change pass/fail status, it is not.

This boundary exists so the freeze does not become the bureaucracy the baseline itself warns against (P2, FR-7.4).

## CP format

```
# CP-YYYY-MM-DD-NNN: <Title>

## Motivation
Why the change is needed. What evidence or experience drives it.

## Affected identifiers
- FR-X.Y: <what changes>
- NFR-X: <what changes>
- PG-X: <what changes>

## Proposed change
Exact textual changes: additions / modifications / deletions.
For modifications: before / after.

## Impact on acceptance criteria
For each affected requirement: are ACs added, modified, or removed? How?

## Impact on cross-references
Which other FR/NFR/PG reference the affected identifiers? Do they require updates?

## Alternatives considered
What else was considered, and why it was rejected.

## Review
- Reviewer(s): <name(s)>
- Reviewed: <date>
- Second reviewer (required when NFR-3 is affected): <name or n/a>

## Decision
[Proposed | Accepted | Rejected | Withdrawn] — <date> — <owner>
- If Rejected: reason.
- If Withdrawn: replaced-by (CP id, or none).
- If Accepted: application mode — immediate (annotated) | accumulated (fold revision).
```

## Storage and identity

- CPs live in `docs/research/spec-tools/proposals/` as `CP-YYYY-MM-DD-NNN.md`, versioned as ordinary repository artifacts per FR-6.2
- CP numbers are never reused; a withdrawn CP keeps its number with a `replaced-by` pointer
- A later accepted CP supersedes an earlier one touching the same text; both remain in the register
- Revisions during review are handled via git history

## Ownership and review

- **Approver:** the project maintainer or a designated architecture lead
- **Second reviewer:** required for any CP touching NFR-3 (security/privacy)
- Review sign-off is recorded in the CP's Review section before a decision is entered

## Lifecycle

**Proposed → In Review → Accepted | Rejected → Applied**

- Anyone may author a CP
- In Review: at least one reviewer engaged (two when NFR-3 is affected)
- The decision is recorded with date and owner; rejections record the reason
- Applied according to the application rule below

## Application rule

Two modes:

- **Immediate (annotated).** Permitted only for ambiguity-resolving clarifications and non-normative edits — cases where no conforming implementation can change pass/fail status. The baseline text is updated in place with a trailing annotation `[CP-YYYY-MM-DD-NNN]`.
- **Accumulated (fold revision).** Required for any change that can alter verification behavior, including modifications, deletions, and **additive acceptance criteria**. Accepted CPs are listed in the baseline's revision history as pending and are folded into the next numbered revision (v2.1, v3.0, …) — a rare, deliberate event.

Rationale: cross-references to FR/NFR/PG identifiers must remain stable for readers. Additive growth that tightens verification is semantic churn, not clarification, and belongs to fold revisions.

## Relationship to Open Questions

An open question (currently Q2–Q6 of the baseline) can close in one of three ways:

- **(a) Resolved via CP** — when the resolution changes requirement text
- **(b) Deferred as an architectural decision** — recorded in the architecture document without baseline change
- **(c) Closed with no change** — when discussion concludes the baseline already covers the concern

## Register of deferred design decisions

The following are deliberately routed to the architecture document rather than the baseline (mechanism (b) above):

- **Governance protocol**: single versioned contract with two facets — event schema and rule representation (Q2, Q6, NQ-C); synchronous major versioning
- **Trigger mechanism**: hooks + minimal trigger list + tool-level gates; middleware excluded from the core combo, permitted as an off-by-default plugin under NFR-4 with kill-switch subordination, privacy analysis, and data-handling disclosure (Q3, NQ-A, NQ-K)
- **Secondary trigger metric**: preemptive vs remedial invocation audit — observability-only for v1; target deferred until the FR-3.1 reference corpus yields a baseline (NQ-H)
- **Spec-as-source conditions**: independent verification, generated-artifact marking, round-trip plus a property-test companion derived from the spec (Q4, NQ-D)
- **Spec-tree format**: repo-identifier addressability to avoid a future cross-repo breaking change; link classes broken vs unresolvable (Q5, NQ-E)
- **Rule-injection format**: digest-form governance inheritance, resolution-at-assembly, content-digest cache keys (which subsume FR-5.5 invalidation for configuration inputs) (Q6, NQ-B, NQ-I)
- **Acknowledgment scope**: "project" in FR-1.4 recommended as per-repository (pending confirmation, NQ-F); path-scoped acknowledgment and module-level reset via FR-2.9 override are future CP candidates
- **Arbitration cadence**: re-notification without upper bound for v1; escalation-pending state observable via FR-4.2 (review item 2.3, accepted as-is)

## Status

- Baseline: v2.0, frozen 2026-10-02
- Open CPs: none
- Next fold revision: unscheduled
