## Library documentation (Context7)

When the task involves a third-party library, framework, SDK, external API, or
service configuration — code generation, setup, integration, debugging, or
upgrades — automatically call Context7 before writing or modifying code:

1. `mcp__context7_resolve-library-id` to resolve the library name.
2. `mcp__context7_get-library-docs` with the resolved ID and the topic.

Run these as a normal step of the task; do not ask permission and do not wait
for an explicit request.

Skip Context7 for: code in this repository, relative imports, the standard
library, and tools/libraries explicitly provided in AGENTS.md.

If Context7 returns no match or the docs are incomplete, say so explicitly and
fall back to repository code or official upstream docs — do not invent APIs
from memory.
