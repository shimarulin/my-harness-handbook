---
status: "draft"
topics: "superpowers, ai-agents, claude-code, criticism, research"
author: "human"
created: "2026-10-01T00:00:00+03:00"
updated: "2026-10-01T00:00:00+03:00"
---

# Criticism of Superpowers (obra/superpowers)

Systematic collection of criticisms, limitations, and negative feedback found in public sources about the Superpowers plugin for AI coding agents.

**Project:** https://github.com/obra/superpowers
**Author:** Jesse Vincent (obra), Prime Radiant
**Stars (as of 2026-09-30):** ~293k

---

## 1. Session Misbehavior (Officially Acknowledged)

Superpowers' own README acknowledges that sessions can misbehave in several ways, leading to the creation of a special diagnostic skill:

> "Sometimes a session misbehaves: a skill fires when it shouldn't, stays silent when it should, or the agent ignores its plan, repeats work, or burns more tokens than you'd expect."

This led to the creation of the `diagnosing-superpowers` skill:
> "Ask your coding agent to 'figure out what went wrong with superpowers in this session' and it will invoke the **diagnosing-superpowers** skill. The skill reads the session transcript, reports what happened with line-level evidence, and, if you want, packages a scrubbed bundle for a bug report."

**Source:** [Superpowers README, "When Something Goes Wrong" section](https://github.com/obra/superpowers#when-something-goes-wrong)

**Implication:** The existence of a built-in diagnostic tool for sessions that "misbehave" is an implicit acknowledgment that these problems occur frequently enough to warrant dedicated tooling.

---

## 2. Overly Strict Reviewers (Fixed in Later Versions)

The RELEASE-NOTES.md for Superpowers reveals that early versions had a calibration problem with code reviewers:

> "Raised the bar for blocking issues — both spec and plan reviewer prompts now include a 'Calibration' section: only flag issues that would cause real problems"

**Source:** [Superpowers RELEASE-NOTES.md](https://github.com/obra/superpowers/blob/main/RELEASE-NOTES.md)

**Problem identified:** Reviewers were flagging non-critical issues as blocking, preventing progress. The fix was to add explicit calibration instructions to only flag issues that "would cause real problems."

**Implication:** Mandatory review workflows can be counterproductive when reviewers lack proper calibration, blocking on stylistic or minor issues rather than genuine problems.

---

## 3. Cannot Handle Environment Debugging

A detailed technical review identifies environment debugging as a key limitation:

> "The Superpowers plugin has two main limitations: it can't handle environment debugging (platform-specific issues that aren't plannable in advance) [and ...]"

**Source:** [The Superpowers Plugin for Claude Code: The Structured — builder.io](https://www.builder.io/blog/superpowers-plugin-for-claude-code)

**Implication:** Superpowers' methodology (brainstorm → plan → implement) assumes work can be planned in advance. Platform-specific issues (e.g., Docker networking quirks, OS-specific paths, hardware dependencies) cannot be anticipated in a plan and fall outside Superpowers' workflow.

---

## 4. Not Suitable for All Work Styles

From the Hacker News discussion of Superpowers 6:

> "It works very well for the way that I work (interactively and iteratively, not 'one-shot'), and it helps me to better work in less time."

This implies that Superpowers is optimized for interactive, iterative workflows and may not suit "one-shot" or batch-style work patterns.

**Source:** [Superpowers 6 — Hacker News discussion](https://news.ycombinator.com/item?id=superpowers6)

Also from the same discussion:

> "IMO Superpowers isn't the ideal solution because it too lacks flexibility, but including the 'plan sketch' stage is sure an improvement."

**Source:** [Hacker News comment on Superpowers 6](https://news.ycombinator.com/item?id=superpowers6)

**Implication:** Even supporters acknowledge a fundamental tension between structured methodology and flexibility. The rigid workflow may not accommodate all types of tasks or working preferences.

---

## 5. Only Covers Software Development Domain

Evan Schwartz's positive review ("rave review") ends with an important observation about domain limitations:

> "I have friends who are academic researchers. Every time they tell me about issues they've run into trying to use Claude or other AI tools, I've immediately thought that they could use an equivalent structured workflow plugin that adapts a Superpowers-style workflow to non-programming domains. Just a thought for the Prime Radiant folks or others who are building agent-focused dev tools."

**Source:** [A Rave Review of Superpowers (for Claude Code) — emschwartz.me](https://emschwartz.me/a-rave-review-of-superpowers-for-claude-code/)

**Implication:** Superpowers is explicitly designed for software development workflows. Research, academic work, documentation, and other domains require different structured approaches that Superpowers does not provide. (This is a gap that Spec Kitty's `research` mission type and specs.md's `Ideation Flow` attempt to fill.)

---

## 6. Skills Can Be "Too Vague" or "Too Rigid"

From a DataCamp technical review of the Superpowers architecture:

> "Skills that are too vague get ignored and skills that are too rigid usually don't work on edge cases. Skills that overlap with existing ones [cause conflicts]..."

**Source:** [Claude Code Superpowers: Structured AI Development — DataCamp](https://www.datacamp.com/blog/claude-code-superpowers)

**Implication:** There's a fundamental tension in skill design. Superpowers must balance between being specific enough to trigger correctly and general enough to handle edge cases. This is a non-trivial design challenge that affects reliability.

---

## 7. Claude Skills System Described as "Janky"

A LinkedIn post about the broader Claude Skills ecosystem (which Superpowers builds upon):

> "Claude just dropped 'Skills' and they're janky AF. That's exactly why you should care. Tanmay Jain and I spent hours trying to break this thing."

**Source:** [Claude Skills: The Good, the Bad, and the Ugly — LinkedIn](https://www.linkedin.com/pulse/claude-skills-good-bad-ugly-david-quan)

**Implication:** The underlying Skills mechanism that Superpowers depends on is still evolving and has known reliability issues. Superpowers inherits these platform-level limitations.

---

## 8. Multi-Page Plan Problem (Partially Addressed)

Evan Schwartz describes the problem with stock Claude Code's Plan mode that Superpowers partially addresses:

> "In Plan mode, Claude would write up a giant plan document and ask for feedback. It's hard to review a multi-page plan. Making matters worse, if you give it feedback, it would respond with a whole new version of the multi-page plan. That's not a productive way to plan out a project or feature."

While Superpowers addresses this through its staged approach (plan sketch → design doc), this criticism highlights that plan review remains challenging even with structure.

**Source:** [A Rave Review of Superpowers (for Claude Code) — emschwartz.me](https://emschwartz.me/a-rave-review-of-superpowers-for-claude-code/)

---

## 9. TDD Enforcement May Be Too Strict

Superpowers' `test-driven-development` skill "deletes code written before tests." While this enforces discipline, it may be too aggressive for:

- Legacy code exploration
- Prototyping/spike work
- Debugging sessions where code-first is more natural
- Non-testable infrastructure work

**Source:** [Superpowers README, Skills Library section](https://github.com/obra/superpowers#skills-library)

> "**test-driven-development** - RED-GREEN-REFACTOR cycle (includes testing anti-patterns reference)"

The "mandatory workflows, not suggestions" philosophy means users cannot easily opt out of TDD for cases where it doesn't apply.

---

## 10. Token Burn from Subagent Orchestration

The README mentions that agents may "burn more tokens than you'd expect" as one of the problems requiring diagnosis. The `subagent-driven-development` approach (fresh subagent per task) is thorough but expensive:

> "It's not uncommon for your agent to work autonomously for a couple hours at a time without deviating from the plan you put together."

**Source:** [Superpowers README, "How it works" section](https://github.com/obra/superpowers#how-it-works)

**Implication:** The thoroughness of subagent-per-task with review-after-each comes at a cost. For small tasks, the overhead of spawning subagents and reviewing each step may exceed the value.

---

## Summary of Limitations

| # | Limitation | Severity | Source |
|---|---|---|---|
| 1 | Sessions can misbehave (skills fire/silent incorrectly) | High (acknowledged by project) | [GitHub README](https://github.com/obra/superpowers#when-something-goes-wrong) |
| 2 | Reviewers were too strict (fixed via calibration) | Medium (fixed) | [RELEASE-NOTES.md](https://github.com/obra/superpowers/blob/main/RELEASE-NOTES.md) |
| 3 | Cannot handle environment debugging | High (structural) | [builder.io](https://www.builder.io/blog/superpowers-plugin-for-claude-code) |
| 4 | Lacks flexibility for all work styles | Medium | [Hacker News](https://news.ycombinator.com/item?id=superpowers6) |
| 5 | Only covers software dev domain | High (by design) | [emschwartz.me](https://emschwartz.me/a-rave-review-of-superpowers-for-claude-code/) |
| 6 | Skills can be too vague or too rigid | Medium (design challenge) | [DataCamp](https://www.datacamp.com/blog/claude-code-superpowers) |
| 7 | Underlying Skills system described as "janky" | Medium (platform-level) | [LinkedIn](https://www.linkedin.com/pulse/claude-skills-good-bad-ugly-david-quan) |
| 8 | Multi-page plan review remains hard | Low (partially addressed) | [emschwartz.me](https://emschwartz.me/a-rave-review-of-superpowers-for-claude-code/) |
| 9 | TDD enforcement may be too strict for some cases | Medium (philosophical) | [GitHub README](https://github.com/obra/superpowers#skills-library) |
| 10 | Token burn from subagent orchestration | Medium (cost) | [GitHub README](https://github.com/obra/superpowers#how-it-works) |

---

## Open Questions

1. How does Superpowers compare to Spec Kitty's `research` mission type for non-software-development work?
2. What is the actual token overhead of `subagent-driven-development` vs. `executing-plans`?
3. How often do sessions actually "misbehave" in practice?
4. Are there forks or extensions that address the domain limitation (research, documentation, etc.)?

---

## Related Research

- [Spec Kitty Research Mission](https://github.com/spec-kitty/spec-kitty/blob/main/docs/guides/how-to/scenarios/research-mission-example.md) — addresses limitation #5
- [specs.md Ideation Flow](https://specs.md/ideation-flow/overview) — addresses limitation #5 for ideation
- [GitHub Spec Kit](https://github.com/github/spec-kit) — alternative with different approach

---

## Metadata

**Search queries used:**
- "superpowers obra criticism problems issues reddit hackernews"
- "superpowers claude code TDD criticism overhead tokens"
- "superpowers plugin review problems limitations"
- "superpowers claude code criticism reddit r/ClaudeAI"
- "superpowers \"diagnosing-superpowers\" session misbehaves"

**Search date:** 2026-10-01
**Coverage:** Public web search; GitHub repository (README, RELEASE-NOTES); blog posts; social media discussions
**Limitations:** Could not access full HN thread for Superpowers 6; some sources returned partial content; Reddit search rate-limited
