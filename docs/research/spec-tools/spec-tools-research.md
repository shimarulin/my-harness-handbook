# Spec-Driven Development Tools Research: specs.md, OpenSpec, obra/superpowers, and Spec Kitty

## TL;DR

**specs.md** is an AI-native methodology framework implementing AWS AI-DLC with four pluggable flows (Ideation, Simple, FIRE, AI-DLC), positioned for full-lifecycle complex systems. **OpenSpec** (Fission AI) is a lightweight, brownfield-first change-management CLI that won the independent ranthebuilder.cloud comparison (4.00/5) but is criticized for spec verbosity and parallel-change conflicts. **obra/superpowers** (Jesse Vincent) is not a spec tool in the traditional sense — it is an agentic skills framework that enforces a disciplined engineering workflow (TDD, subagent-driven development) and has the largest community (294k GitHub stars) but persistent criticism for token burn and overkill on simple tasks. **Spec Kitty** (Robert Douglass / Priivacy-ai) is a community fork of GitHub Spec Kit that adds governance, observability, and multi-agent orchestration on top of the spec-driven workflow — it scores highest for parallel feature development (5/5) but lowest for trivial fixes and hotfixes (1-2/5).

The four tools occupy different layers: specs.md and OpenSpec decide *what* gets built, Superpowers controls *how* the agent builds it, and Spec Kitty adds the governance and team-observability layer on top of the spec-driven workflow. The emerging best practice is combining them (e.g., OpenSpec + Superpowers via `superpowers-bridge`, or Spec Kitty's tracker-sync governance around either).

---

## Tool Profiles

### 1. specs.md (fabriqaai)

**Positioning:** AI-native development framework with pluggable flows, implementing AWS AI-DLC as a formal methodology. Targets complex systems requiring full lifecycle traceability.

**Key characteristics:**
- Four flows: Ideation (Spark → Flame → Forge creative brainstorming), Simple (spec generation only), FIRE (adaptive execution with 0-2 checkpoints), AI-DLC (full methodology with DDD and 4 agents)
- Reversed conversation direction: AI initiates and directs conversations, humans validate
- "Bolts" as batched stories with full traceability
- Mob rituals (Mob Elaboration, Mob Construction) for team alignment
- First-class brownfield and monorepo support in FIRE flow
- VS Code extension with visual dashboard
- MIT licensed, ~216 GitHub stars (September 2026), active development

**Real-world usage:** [Reddit user reports 1,700 unique installations](https://www.reddit.com/r/SpecDrivenDevelopment/comments/1tvt2g9/cmu_research_study_on_specdriven_development) and the project describes itself as "alpha, looking for feedback from engineers actually using spec-driven development, not polish-seekers" in its [initial announcement](https://www.reddit.com/r/ClaudeCode/comments/1pxsebr/specsmd_aidlc_implementation_with_vs_code).

**Vendor's positioning vs competitors:** [specs.md's own comparison](https://specs.md/compare/overview) claims it is the only tool implementing a formal AWS methodology (AI-DLC), with DDD as default rather than optional, and the only one with team rituals (Mob Elaboration/Construction). It positions Spec Kit as a "lightweight toolkit vs full methodology," BMAD as targeting the same complexity but with role-based agents instead of phase-based, and OpenSpec as change-centric vs its full lifecycle.

**Criticism and limitations:**
- Very little independent, third-party review exists — most available material is from the vendor's own documentation or announcements
- The project self-describes as alpha-stage, suggesting immaturity
- Complex multi-flow architecture may present a learning curve despite claims of "choose your overhead"
- No large-scale production case studies are publicly available
- The comparison matrix on specs.md is self-published, raising questions about bias

### 2. OpenSpec (Fission AI)

**Positioning:** Lightweight, brownfield-first spec-driven development CLI focused on change management. The most "sane ceremony" according to community feedback.

**Key characteristics:**
- Change-centric: specs written as deltas (ADDED, MODIFIED, REMOVED) rather than full rewrites
- Four-command workflow: `/opsx:explore` → `/opsx:propose` → `/opsx:apply` → `/opsx:archive`
- Active changes live in `openspec/changes/<name>/`, archived specs merge into canonical `openspec/specs/`
- 50KB hard limit on context injected into every request
- 30+ AI assistant support (Claude Code, Cursor, Copilot, Gemini CLI, Codex, Kiro, OpenCode)
- MIT licensed, ~139.7k GitHub stars (September 2026)

**Real-world performance:**
- [Won the independent ranthebuilder.cloud comparison](https://ranthebuilder.cloud/blog/i-tested-three-spec-driven-ai-tools-here-s-my-honest-take) with a score of 4.00/5 vs BMAD (3.65), BMAD Quick (3.74), and Spec-Kit (2.77), praised for: specification quality, parallel development support, time-to-PR, and cost
- [A 4-month longitudinal study with 8 simulated engineers and 40 PRs](https://medium.com/@vinodh.thiagarajan/simulating-a-software-team-to-study-spec-driven-development-using-openspec-5d2195fb2a37) found OpenSpec held up to real-team dynamics: hotfixes on Saturdays, two engineers modifying the same requirement, capability evolution across 10 sprints
- [Vicens Fayos after intensive use](https://www.linkedin.com/posts/vicensfayos_i-have-mixed-feelings-about-openspec-and-activity-7474702776086966272-rNQz): "As an individual contributor, I think it is a powerful tool... However, once you move into a medium-sized team, I start seeing limitations. The biggest one is governance."

**Criticism and limitations:**
- [Spec verbosity](https://www.glukhov.org/ai-devtools/openspec): "The AI generates way more spec than I need" — the most-cited complaint, with agents turning 30-minute features into 800-line specs. The 50KB context limit forces some discipline, but delta specs have no hard limit
- [Parallel-change conflicts](https://www.glukhov.org/ai-devtools/openspec): "Two changes touched the same requirement and one silently dropped the other's scenario" — archiving applies MODIFIED deltas as whole-block replaces keyed by requirement name, creating documented edge cases in parallel workflows
- [No rejected-proposal memory](https://www.glukhov.org/ai-devtools/openspec): `/opsx:archive` has no dedicated status for declined changes, so nothing tells a future proposal that an idea was already investigated and turned down
- [Namespace criticism](https://github.com/Fission-AI/OpenSpec/discussions/1598): "OpenSpec purports itself as being 'simple' and 'minimal' but I argue it's not" — the `/opsx:*` namespace is "awkward, hard to remember"
- [Spec-implementation gap](https://www.glukhov.org/ai-devtools/openspec): "OpenSpec only checks that artifacts exist, not that code honors them" — the `/opsx:verify` command exists to catch this but requires explicit invocation
- [A failed experiment report](https://dev.to/incomplete_developer/openspec-spec-driven-development-failed-my-experiment-instructionsmd-was-simpler-and-faster-3a5d): After 2 hours and significant tokens with GPT-5.3 Codex, the front-end redesign output "looked almost identical to the original." A simpler `Instructions.md` approach was "faster, cheaper, easier to iterate"

### 3. obra/superpowers (Jesse Vincent / Prime Radiant)

**Positioning:** An agentic skills framework and software development methodology. Not a spec-driven tool in the artifact sense — it is a process enforcement layer that controls how agents build, not what they build.

**Key characteristics:**
- ~294k GitHub stars, 26.3k forks, 683 commits — the most popular tool in this category
- Complete methodology: brainstorming → git worktrees → writing plans → subagent-driven development → TDD → code review → finishing branches
- "Iron Law" of TDD: no production code without a failing test first
- Auto-triggered skills based on context (not user-invoked slash commands)
- 14+ composable skills organized by category
- Multi-harness support: Claude Code, Codex, Cursor, Gemini CLI, GitHub Copilot CLI, and others
- MIT licensed, active commercial support via Prime Radiant

**Real-world performance:**
- [A controlled comparison reported by MCP.Directory](https://www.joanmedia.dev/ai-blog/the-honest-tradeoffs-of-superpowers-token-costs-overkill-and-the-alternatives) found runs 9% cheaper with 14% fewer tokens *and better output* on non-trivial tasks — while *simple tasks cost more* with Superpowers
- [First-time user feedback (GitHub issue #655)](https://github.com/obra/superpowers/issues/655): "Overall it was a positive experience" but identified three problems (see criticism below)
- [Community usage reports](https://www.reddit.com/r/ClaudeCode/comments/1sjuq8f/has_anyone_actually_benchmarked_whether): "1000s of hours of using Claude Code without it. I get lazy and don't instruct it as well as I should. This is where superpowers really shines."

**Criticism and limitations:**
- [Token burn](https://www.joanmedia.dev/ai-blog/the-honest-tradeoffs-of-superpowers-token-costs-overkill-and-the-alternatives): "Huge token guzzler"; one user reported it "burned through all my max plan" on straightforward tasks; another that simple fixes "take literally an hour with all the verification"
- [Overkill for capable models](https://www.joanmedia.dev/ai-blog/the-honest-tradeoffs-of-superpowers-token-costs-overkill-and-the-alternatives): Recurring comparison to elaborate `.vimrc` configurations — "these prompt shenanigans are just not worth it" now that current models plan competently when simply asked
- [Rigidity](https://www.joanmedia.dev/ai-blog/the-honest-tradeoffs-of-superpowers-token-costs-overkill-and-the-alternatives): Plans that specify exact files to edit can hurt on exploratory work where the right implementation is discovered, not pre-specified
- [Insufficient questioning during planning (GitHub issue #655)](https://github.com/obra/superpowers/issues/655): "Didn't ask me questions about how testing should be done at any time during planning"
- [Autopilot tendency (GitHub issue #655)](https://github.com/obra/superpowers/issues/655): "Claude Code seems to generally be blazing through on its own without ever stopping to ask me stuff if things aren't going according to plan"
- [No context-clearing guidance (GitHub issue #655)](https://github.com/obra/superpowers/issues/655): "It provides no guidance as to when context can safely be cleared (/clear) between phases"
- [Token-based billing incompatibility (GitHub issue #1940)](https://github.com/obra/superpowers/issues/1940): "In the token-based billing era, using Superpowers for a large amount of work will make cost control very difficult"
- [Confirmatory rather than adversarial review (GitHub issue #1803)](https://github.com/obra/superpowers/issues/1803): "The built-in writing-plans self-review is confirmatory — it checks coverage, types, and placeholders. It does not attempt to break the plan... Claude in 'completion state' produces plans that look correct but contain silent failures"

**Author's active response to criticism:**
- v5.0.6 (March 2026): subagent review loops removed after regression testing showed ~25 minutes of overhead with no measurable quality gain
- v6.0.0 (June 2026): spec-compliance and code-quality reviewers merged, review inputs pre-generated — "up to 50% faster and up to 60% cheaper"
- v6.1.0: always-loaded bootstrap compressed
- As noted by [one analysis](https://www.joanmedia.dev/ai-blog/the-honest-tradeoffs-of-superpowers-token-costs-overkill-and-the-alternatives): "'It's bloated' is a criticism the project actively metabolizes. It is also still true that no amount of optimization makes a design interview free."

---

### 4. Spec Kitty (spec-kitty.ai / Priivacy-ai)

**Positioning:** A community fork of GitHub Spec Kit that extends the spec-driven workflow with governance, observability, and multi-agent orchestration. Created by Robert Douglass (former VP at Platform.sh) after concluding that Spec Kit "didn't work" as-is. Officially described as "not a new center of gravity" — a layer that sits beside existing tools (GitHub, GitLab, Linear, Jira, Slack, Teams, Claude Code, Codex, Cursor, Gemini CLI) rather than replacing them.

**Key characteristics:**
- Community fork of Spec Kit with governance layer: Charter, Doctrine, glossary, work packages, approvals, ADRs, and review loops
- Teamspace: cross-team observability layer showing which missions are active against which projects and builds
- Decision Moments: widens decisions from the CLI into Slack/Teams threads for accountable, consulted, and informed stakeholders
- Tracker integration: Linear and Jira can seed missions and receive status updates, keeping the ticket system authoritative
- Living `kitty-specs` wiki: specs, plans, evidence, review trails, and Decision Moment ADRs as repo-native artifacts
- Mandatory review step on every Work Package, used by some for adversarial model reviews
- Git worktree strategy: v3.1.0 changed from "Worktree per Work Package" to "Worktree per Swim Lane" after the former was called "a mediocre idea" and "instabile" by users
- 11 supported agents (Claude Code, Cursor, Windsurf, Gemini CLI, GitHub Copilot, and others)
- Python-based CLI (pip install), MIT licensed, ~1.7k GitHub stars, 175 forks

**Real-world performance (from cameronsjo/spec-compare independent comparison, 20 SDD tools tracked):**

| Use Case | Score | Reasoning |
|---|---|---|
| Parallel feature development (3 teams, 5 features) | ★★★★★ | "Built-in worktree strategy. Kanban dashboard. Designed for this scenario." |
| Greenfield feature (0→1) | ★★★★ | "Spec-Kit workflow + worktree isolation. Good for larger features." |
| Refactor existing component | ★★★ | "Worktree isolation helps but workflow overhead for medium change." |
| Add REST API endpoint | ★★★ | "Spec-Kit API workflow + worktrees. Overhead may not be needed." |
| Trivial modification (change button color) | ★★ | "Same Spec-Kit issues + worktree overhead excessive for one-line change." |
| Fix production bug | ★★ | "Worktree + spec workflow too slow for emergencies." |
| Emergency hotfix (production down) | ★ | "Worktree setup wastes precious minutes." |

Source: [cameronsjo/spec-compare use-case scoring](https://github.com/cameronsjo/spec-compare/blob/main/docs/use-case-scoring.md)

**Real-world usage and criticism:**

- **Martin Dilger's detailed critique** (author of the upcoming book "Spec Driven"): Tested Spec Kitty with intentionally vague requirements and documented specific failures in a [LinkedIn post](https://www.linkedin.com/posts/martindilger_i-honestly-dont-understand-spec-driven-development-activity-7489568450927869952-nA2Q):
  - "The third question was already about the tech stack. That confused me. I stopped it. Shouldn't we spend some more time understanding the problem first?"
  - "Then it came up with a 'domain model' almost immediately. Structures for a book, a catalog entry, defined before it had any real grasp of the problem."
  - "The requirements covered a few different functionalities, and the questions came back in arbitrary order, jumping between features with no structure."
  - "A business stakeholder on the other end of that conversation would have no idea if they're supposed to answer feature by feature or think about the whole system at once."
  - "We ended up with 46 markdown files after 20 min... Twenty minutes in, you have fifty markdown files. Who is reading all of that? Who is maintaining it?"
  - "Skipping the visual model doesn't remove the complexity. It just removes the thing that was managing it."
  - Final verdict: "The tools aren't the problem. Skipping the digging is."
  - Robert Douglass responded to this criticism acknowledging its validity and proposing integration with Event Modeling via `eventmodelers export --spec-kitty`

- **Repeat-review inefficiency (from the project's own dogfooding, GitHub issue #3925):** "When a WP is rejected and re-reviewed, the second and third reviews re-run the entire acceptance checklist, re-prove facts the first reviewer already established, and re-run the full blast radius... each review pass took 12–22 minutes of wall-clock, most of it re-verifying settled items. By the third pass the marginal signal is close to zero." Source: [spec-kitty issue #3925](https://github.com/spec-kitty/spec-kitty/issues/3925)

- **Positive experiences:**
  - [Reddit user on r/ClaudeCode](https://www.reddit.com/r/ClaudeCode/comments/1qweqjm/claude_code_wrote_the_specs_made_the_plan): "Every Work Package (task) has a mandatory review step in Spec Kitty. I use this to have adversarial model reviews."
  - [Hacker News discussion](https://news.ycombinator.com/item?id=46961910): "Quite amazing how a short interview on an idea can produce full documents of requirements, specs, tasks, etc... definitely an improvement."
  - [Medium reviewer](https://medium.com/@sh19871122/from-vibe-coding-to-spec-driven-development-2b03019e79bf): Positions Spec Kitty as "traceability + Kanban," recommending it for "distributed teams need strong visibility" with "medium" learning curve and "very high" documentation rigor.

**Limitations (from independent comparison):**
- "Adds complexity on top of Spec-Kit"
- "Requires understanding both base Spec-Kit and Spec Kitty extensions"
- "Dashboard overhead may be unnecessary for solo developers on simple projects"
- "Python dependency (pip install) vs. Node-based alternatives"

Source: [cameronsjo/spec-compare spec-kitty profile](https://github.com/cameronsjo/spec-compare/blob/main/docs/tools/spec-kitty.md)

**Comparison with parent (GitHub Spec Kit):** [Spec Kitty's own positioning](https://spec-kitty.ai/blog/spec-kit-alternatives-why-i-built-spec-kitty-instead-of-stopping-at-githubs-toolkit) states: "Like Spec Kit, Spec Kitty is an open-source, local-first CLI... The difference is what the loop does after the spec exists. The mission lives in Git: specs, plans, work packages, acceptance criteria, decision records, review state, and merge status become repo-native artifacts, not ephemeral chat... Governance is the part a toolkit leaves empty."

---

## Cross-Comparison

### specs.md vs OpenSpec

| Aspect | specs.md | OpenSpec |
|---|---|---|
| Primary focus | Full lifecycle (Inception → Operations) | Change management |
| Best for | Complex systems, greenfield + brownfield | Brownfield, incremental changes |
| Philosophy | Complete methodology | Lightweight, change-centric |
| Structure | Intents → Units → Stories | Specs + Changes separation |
| Design integration | DDD as core | Design-agnostic |
| Rituals | Mob Elaboration, Mob Construction | None |
| Learning curve | Moderate | Low |
| VS Code extension | Yes (visual dashboard) | CLI dashboard |
| Maturity | Alpha, 216 stars | Mature, 139.7k stars |
| Independent reviews | Very few | Multiple, including longitudinal study |

Source: [specs.md's own comparison](https://specs.md/compare/vs-openspec)

### Superpowers vs Spec Kit (representative of artifact-centric tools)

| Aspect | Superpowers | Spec Kit |
|---|---|---|
| Core idea | Skills enforce a disciplined dev workflow | Specs are executable; code is generated from specs |
| Primary artifact | The skill (a triggered procedure) | The specification document |
| Trigger model | Auto-triggered based on context | User-invoked slash commands |
| Methodology | Agentic SDLC (brainstorm → design → plan → TDD → review → ship) | Spec-Driven Development (SDD) |
| Best for | Multi-hour autonomous work, parallel subagents, TDD discipline | Greenfield features, spec-to-code traceability |
| Maturity | 294k stars, active releases | 140k stars, 136 releases |

Source: [dev.to comprehensive comparison](https://dev.to/truongpx396/spec-kit-vs-superpowers-a-comprehensive-comparison-practical-guide-to-combining-both-52jj)

### Superpowers vs OpenSpec (process vs artifact)

As [one analysis frames it](https://arceapps.com/blog/superpowers-vs-openspec): "Superpowers is a prescriptive, skill-based methodology that enforces strict engineering practices like Test-Driven Development (TDD). OpenSpec, on the other hand, is an artifact-guided workflow that focuses on creating living documentation before any code is written."

The emerging best practice is [combining them](https://spec-coding.dev/blog/spec-driven-development-tools-openspec-spec-kit-superpowers): "OpenSpec and Spec Kit decide *what* gets built, and Superpowers controls *how* the agent builds it." The `superpowers-bridge` schema exists specifically for this combination, redirecting Superpowers brainstorming output into OpenSpec change folders.

### Comparison with Previously Reviewed Tools

| Dimension | specs.md | OpenSpec | Superpowers | Spec Kitty | GitHub Spec Kit | BMAD | Kiro |
|---|---|---|---|---|---|---|---|
| **Type** | Methodology + Framework | Lightweight Framework | Skills Framework | Community fork with orchestration | Toolkit + Agent Prompts | Multi-agent Framework | Full IDE |
| **Methodology** | AWS AI-DLC (formal) | OpenSpec SDD | Agentic SDLC | Spec Kit SDD + governance | Spec Kit SDD | Agentic Agile | Kiro SDD |
| **Primary focus** | Full lifecycle | Change management | Execution quality | Team governance + observability | Spec-to-code pipeline | Enterprise planning | IDE-integrated development |
| **Agent model** | 3 phase-based agents | AGENTS.md compatible | 14+ auto-triggered skills | 3 phase-based agents | Prompts for 15+ assistants | 19 role-based agents | Built-in + Subagents |
| **Brownfield support** | Yes (FIRE flow) | Excellent (primary focus) | Via git worktrees | Yes | Yes | Yes | Yes |
| **Monorepo support** | Yes (hierarchical standards) | Limited | No built-in | No built-in | No | No | No |
| **Parallel development** | Via Bolts | ★★★ (manual worktrees) | ★★★★★ (subagent-driven) | ★★★★★ (built-in worktrees) | ★★ | ★★ | ★★ |
| **Token efficiency** | Adaptive (FIRE checkpoints) | Good (delta specs, 50KB limit) | Poor on simple tasks, good on complex | Variable | Variable | Poor (21 agents) | Variable |
| **TDD enforcement** | Optional (via bolt types) | None | Mandatory ("Iron Law") | None | None | None | None |
| **Team rituals** | Mob Elaboration, Mob Construction | None | None | Decision Moments (Slack/Teams) | None | None | None |
| **IDE lock-in** | None | None | None | None | None | None | High (Kiro IDE + Claude) |
| **Pricing** | Free (OSS) + API tokens | Free (OSS) + API tokens | Free (OSS) + API tokens | Free (OSS) + API tokens | Free (OSS) + API tokens | Free (OSS) + API tokens | $20-200/mo |
| **GitHub stars** | ~216 | ~139.7k | ~294k | ~1.7k | ~140k | — | — |
| **Independent review quality** | Very limited | Good (longitudinal study exists) | Good (controlled comparisons exist) | Limited (mostly dogfooding) | Good (ranthebuilder comparison) | Good | Limited |

---

## Criticism Patterns Across Tools

### Common themes in SDD criticism

1. **Process overhead tax**: As [Hidde de Smet documents](https://hiddedesmet.com/the-hidden-costs-of-spec-driven-development), spec-driven development adds "planning tax, review bottlenecks, and process overhead" — the question is when full specs are worth it vs. a lighter path

2. **Spec-implementation gap**: [OpenSpec's own documentation acknowledges](https://www.glukhov.org/ai-devtools/openspec): "OpenSpec only checks that artifacts exist, not that code honors them." A schema description in their community catalog puts it plainly: this is a problem across all SDD tools

3. **Spec drift over time**: [Multiple reviewers note](https://www.glukhov.org/ai-devtools/openspec) that specs can drift from implementation, especially in tools without enforcement mechanisms

4. **Double review burden**: [Critical analysis of SDD](https://github.com/cameronsjo/spec-compare/blob/main/docs/critical-analysis.md) notes that reviewing extensive specifications may be less efficient than code review — "verbose markdown is tedious to review" and creates "double review burden (specs + code)"

5. **Waterfall regression risk**: [The same critical analysis](https://github.com/cameronsjo/spec-compare/blob/main/docs/critical-analysis.md) draws parallels to Model-Driven Development (MDD) from the 2000s: "We might end up with the downsides of both MDD and LLMs: Inflexibility and non-determinism"

### Tool-specific criticism profiles

**specs.md:** The primary criticism is simply lack of independent validation. With ~216 GitHub stars and self-described alpha status, there are no longitudinal studies, no controlled comparisons, and no large-scale production case studies publicly available.

**OpenSpec:** The most independently-validated tool, but with specific documented failure modes: spec verbosity, parallel-change conflicts, no rejected-proposal memory, and the fundamental gap between spec existence and code compliance.

**Superpowers:** The most community-scrutinized tool with persistent, substantive criticism that the author actively addresses. The core tension is between discipline (which it delivers) and token/cognitive overhead (which is real).

---

## Recommendations

### When to use each tool

| Situation | Recommended tool | Rationale |
|---|---|---|
| Complex greenfield system, team alignment needed | specs.md (AI-DLC) | Mob rituals, DDD, full lifecycle |
| Brownfield incremental changes, 30+ AI assistants | OpenSpec | Delta specs, minimal ceremony, broadest tool support |
| Agent skips planning/tests, multi-hour feature work | Superpowers | Mandatory TDD, subagent isolation |
| Team needs governed agentic coding + observability | Spec Kitty | Teamspace, Decision Moments, tracker integration |
| Strict phase gates, same process every feature | GitHub Spec Kit | Constitution-driven, converge reporting |
| Enterprise planning with specialized roles | BMAD | 19 role-based agents |
| API-driven architecture | BMAD | Architect Agent creates precise OpenAPI specs |

### Combining tools

The emerging best practice is layering: [use a planning tool (OpenSpec or Spec Kit) for *what* to build, plus Superpowers for *how* to execute](https://spec-coding.dev/blog/spec-driven-development-tools-openspec-spec-kit-superpowers). The `superpowers-bridge` schema for OpenSpec specifically redirects Superpowers brainstorming and planning output into OpenSpec change folders, eliminating duplicate design documents.

---

## Source Index

### specs.md sources
- [specs.md official documentation](https://specs.md)
- [specs.md GitHub repository](https://github.com/fabriqaai/specs.md)
- [specs.md comparison overview](https://specs.md/compare/overview)
- [specs.md vs OpenSpec comparison](https://specs.md/compare/vs-openspec)
- [specs.md FIRE Flow overview](https://specs.md/fire-flow/overview)
- [specs.md Master Agent documentation](https://specs.md/agents/master-agent)
- [specs.md Ideation Skills](https://specs.md/ideation-flow/skills)
- [Reddit announcement - alpha status](https://www.reddit.com/r/ClaudeCode/comments/1pxsebr/specsmd_aidlc_implementation_with_vs_code)
- [Reddit CMU research discussion - installation numbers](https://www.reddit.com/r/SpecDrivenDevelopment/comments/1tvt2g9/cmu_research_study_on_specdriven_development)
- [Spec Kit vs AWS AI-DLC comparison](https://jackiechen.blog/2026/09/02/spec-kit-vs-aws-ai-dlc)

### OpenSpec sources
- [OpenSpec official site](https://openspec.dev)
- [ranthebuilder.cloud - I Tested Three Spec-Driven AI Tools](https://ranthebuilder.cloud/blog/i-tested-three-spec-driven-ai-tools-here-s-my-honest-take)
- [OpenSpec Quickstart and Common Pitfalls (glukhov.org)](https://www.glukhov.org/ai-devtools/openspec)
- [Simulating a Software Team to Study SDD using OpenSpec (Medium)](https://medium.com/@vinodh.thiagarajan/simulating-a-software-team-to-study-spec-driven-development-using-openspec-5d2195fb2a37)
- [OpenSpec Spec-Driven Development Failed My Experiment (dev.to)](https://dev.to/incomplete_developer/openspec-spec-driven-development-failed-my-experiment-instructionsmd-was-simpler-and-faster-3a5d)
- [Vicens Fayos LinkedIn post on OpenSpec limitations](https://www.linkedin.com/posts/vicensfayos_i-have-mixed-feelings-about-openspec-and-activity-7474702776086966272-rNQz)
- [OpenSpec namespace feedback discussion](https://github.com/Fission-AI/OpenSpec/discussions/1598)
- [OpenSpec team workflow documentation](https://github.com/Fission-AI/OpenSpec/blob/main/docs/team-workflow.md)
- [OpenSpec multiple changes integration discussion](https://github.com/Fission-AI/OpenSpec/discussions/737)
- [Spec Kit vs OpenSpec GitHub discussion](https://github.com/github/spec-kit/discussions/1536)
- [OpenSpec Review 2026 (vibecodinghub)](https://vibecodinghub.org/blog/openspec-review)
- [OpenSpec Hacker News discussion](https://news.ycombinator.com/item?id=49734264)
- [OpenSpec Optimizes Chaos, Not Tokens](https://andreadicarlo.dev/blog/openspec-optimizes-chaos)
- [How OpenSpec Actually Works (Medium)](https://apurvsheth.medium.com/how-openspec-actually-works-a-three-phase-workflow-that-keeps-ai-honest-3d4aeb61e9fa)
- [Medium - Spec Driven Development Beyond the Hype](https://medium.com/@mpholoane/spec-driven-development-beyond-the-hype-my-honest-first-impressions-03a7c62d5414)
- [OpenSpec token impact discussion](https://github.com/Fission-AI/OpenSpec/discussions/749)

### Superpowers sources
- [obra/superpowers GitHub repository](https://github.com/obra/superpowers)
- [obra/superpowers-marketplace](https://github.com/obra/superpowers-marketplace)
- [The Honest Tradeoffs of Superpowers (joanmedia.dev)](https://www.joanmedia.dev/ai-blog/the-honest-tradeoffs-of-superpowers-token-costs-overkill-and-the-alternatives)
- [First-time user impressions - GitHub issue #655](https://github.com/obra/superpowers/issues/655)
- [Token-based billing concern - GitHub issue #1940](https://github.com/obra/superpowers/issues/1940)
- [Adversarial review proposal - GitHub issue #1803](https://github.com/obra/superpowers/issues/1803)
- [Reddit - obra/superpowers overkill discussion](https://www.reddit.com/r/ClaudeCode/comments/1uyy7y1/obrasuperpowers_overkill)
- [Reddit - Superpower takes too long and consumes too much token](https://www.reddit.com/r/ClaudeAI/comments/1v49gxt/superpower_takes_too_long_and_consumes_too_much)
- [Reddit - Has anyone actually benchmarked whether superpowers](https://www.reddit.com/r/ClaudeCode/comments/1sjuq8f/has_anyone_actually_benchmarked_whether)
- [Superpowers vs OpenSpec comparison (arceapps.com)](https://arceapps.com/blog/superpowers-vs-openspec)
- [Spec Kit vs Superpowers comprehensive comparison (dev.to)](https://dev.to/truongpx396/spec-kit-vs-superpowers-a-comprehensive-comparison-practical-guide-to-combining-both-52jj)
- [OpenSpec vs Superpowers vs Spec Kit: Compare and Combine (spec-coding.dev)](https://spec-coding.dev/blog/spec-driven-development-tools-openspec-spec-kit-superpowers)
- [Superpowers and Spec Kit: Can They Work Together?](https://imtien.com/software-development/superpowers-vs-spec-kit)
- [OpenSpec vs Superpowers in Claude Code](https://www.heyuan110.com/posts/ai/2026-04-09-claude-code-openspec-superpowers)
- [Superpowers + Claude Code: Full Test & Honest Review (YouTube)](https://www.youtube.com/watch?v=98e8lpOtaWc)
- [Superpowers 6.0 analysis (Towards AI)](https://pub.towardsai.net/superpowers-6-0-unpacked-faster-ai-code-review-and-fewer-tokens-5ab40a6c564c)
- [OpenSpec-Superpowers integration workflow](https://www.heyuan110.com/posts/ai/2026-06-28-openspec-superpowers-workflow)
- [Veath/openspec-spec-driven-superpowers integration](https://github.com/Veath/openspec-spec-driven-superpowers)

### Spec Kitty sources
- [Spec Kitty official site](https://spec-kitty.ai)
- [Spec Kitty GitHub repository (Priivacy-ai)](https://github.com/Priivacy-ai/spec-kitty)
- [Spec Kitty vs GitHub Spec Kit vs AWS Kiro vs GSD (official comparison)](https://spec-kitty.ai/blog/spec-driven-ai-development-for-teams)
- [Spec Kit Alternatives: Why I Built Spec Kitty (official)](https://spec-kitty.ai/blog/spec-kit-alternatives-why-i-built-spec-kitty-instead-of-stopping-at-githubs-toolkit)
- [cameronsjo/spec-compare - Spec Kitty tool profile](https://github.com/cameronsjo/spec-compare/blob/main/docs/tools/spec-kitty.md)
- [cameronsjo/spec-compare - Use case scoring matrix](https://github.com/cameronsjo/spec-compare/blob/main/docs/use-case-scoring.md)
- [cameronsjo/spec-compare - Critical analysis of SDD](https://github.com/cameronsjo/spec-compare/blob/main/docs/critical-analysis.md)
- [Martin Dilger's critique on LinkedIn](https://www.linkedin.com/posts/martindilger_i-honestly-dont-understand-spec-driven-development-activity-7489568450927869952-nA2Q)
- [Repeat-review inefficiency - GitHub issue #3925](https://github.com/spec-kitty/spec-kitty/issues/3925)
- [Spec Kitty 3.1.0 release notes on LinkedIn](https://www.linkedin.com/posts/roberttdouglass_spec-kitty-310-is-by-far-the-most-performant-activity-7447272098114351104-90KW)
- [Worktree per Swim Lane change discussion](https://www.linkedin.com/posts/roberttdouglass_now-thats-the-type-of-pr-i-like-to-see-activity-7446496326655328256-V6lA)
- [Reddit - Claude Code wrote the specs, made the plan (user experience)](https://www.reddit.com/r/ClaudeCode/comments/1qweqjm/claude_code_wrote_the_specs_made_the_plan)
- [Hacker News - spec-kitty as Spec Kit fork](https://news.ycombinator.com/item?id=46961910)
- [Medium - From Vibe Coding to Spec-Driven Development (石涵)](https://medium.com/@sh19871122/from-vibe-coding-to-spec-driven-development-2b03019e79bf)
- [Robert Douglass - Why I Built Spec Kitty (LinkedIn)](https://www.linkedin.com/posts/roberttdouglass_why-i-built-spec-kitty-spec-kitty-activity-7454585140690776064-O9jt)
- [Spec Kitty documentation - SDD context](https://docs.spec-kitty.ai/context/spec-driven.html)
- [Spec Kitty executives page (governance positioning)](https://spec-kitty.ai/executives)

### Cross-tool comparison sources
- [cameronsjo/spec-compare - 20 SDD tools comparison](https://github.com/cameronsjo/spec-compare)
- [Spec-Driven Development Tools Compared (felipefontoura.com)](https://felipefontoura.com/articles/spec-driven-development-tools-compared)
- [Comparing 15 Spec-Driven Development Frameworks (Medium)](https://medium.com/@wasowski.jarek/comparing-15-spec-driven-development-frameworks-sdd-c052df529274)
- [SDD Observatory - Compare frameworks](https://sddobservatory.com/compare)
- [From Vibe Coding to Spec-Driven Development (Medium)](https://medium.com/@sh19871122/from-vibe-coding-to-spec-driven-development-2b03019e79bf)
- [The hidden costs of spec-driven development](https://hiddedesmet.com/the-hidden-costs-of-spec-driven-development)
- [Spec-Driven Development Is the Real AI Coding Bottleneck](https://davidyosuanto.com/en/articles/spec-driven-development)
- [BMAD vs. OpenSpec vs. Spec Kit: A CxO's Field Guide](https://tooltwist.com/insights/spec-driven-frameworks-cxo-guide)
- [Agentic Coding: GSD vs Spec Kit vs OpenSpec vs Taskmaster AI](https://medium.com/@richardhightower/agentic-coding-gsd-vs-spec-kit-vs-openspec-vs-taskmaster-ai-where-sdd-tools-diverge-0414dcb97e46)
- [Spec Driven Development: Beyond the Hype (Medium)](https://medium.com/@mpholoane/spec-driven-development-beyond-the-hype-my-honest-first-impressions-03a7c62d5414)

### General SDD criticism sources
- [Addy Osmani - How to write a good spec for AI agents](https://addyo.substack.com/p/how-to-write-a-good-spec-for-ai-agents)
- [IBM - What is Spec-Driven Development?](https://www.ibm.com/think/topics/spec-driven-development)
- [Spec-driven development: a guide to moving beyond vibe (sparkfabrik)](https://www.sparkfabrik.com/en/blog/spec-driven-development-guide)
- [Spec Kit vs Kiro vs Claude Code SDD Workflows (glukhov.org)](https://www.glukhov.org/ai-devtools/ai-coding-assistants/spec-kit-vs-kiro-vs-claude-code)
- [Reddit - We tried spec-driven development for months](https://www.reddit.com/r/SpecDrivenDevelopment/comments/1vubvmz/we_tried_specdriven_development_for_months_we)

---

*Document compiled: 2026-10-02*
*Research scope: independent reviews, user feedback, criticism, and cross-comparisons for specs.md, OpenSpec, obra/superpowers, and Spec Kitty, with references to previously reviewed tools (GitHub Spec Kit, BMAD, Kiro, GSD, Tessl).*
