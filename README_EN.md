# Claude Code — A course in three parts (deck + guides)

> English version of [`README.md`](./README.md). English deliverables:
> [`GUIA_PRESENTACION_EN.md`](./GUIA_PRESENTACION_EN.md) (speaker guide),
> [`GUIA_TECNICA_EN.md`](./GUIA_TECNICA_EN.md) (technical reference) and
> [`presentacion/Claude_Code_Presentacion_EN.pptx`](./presentacion/) (the deck, translated in place —
> same slides and images as the Spanish original).

Material for a **course/workshop** on **Claude Code**: a single presentation with **three distinct
parts**, two written guides, and real, runnable examples. Aimed at **developers**.

- **Part 1 — Claude Code:** installation and basic usage · memory, instructions and sessions ·
  **context (context window + prompt caching)** · MCP · plugins, tools and skills · **subagents and
  agent teams** · automation.
- **Part 2 — The methodology (tool-agnostic):** the real 11-stage workflow with gates · the method's
  tools (CodeGraph, Serena, GSD, deterministic oracles) · transferring it to another agent
  (GitHub Copilot) · machine sync.
- **Part 3 — The ticket knowledge graph:** a complete case built with **graphify**: manifest-driven
  corpus, `/kg-refresh` pipeline, zero-LLM `/kg` queries, the real graph visualization
  (507 nodes · 35 communities) and where it hooks into the methodology.

## Contents

| File | What it is |
|---|---|
| [`GUIA_PRESENTACION_EN.md`](./GUIA_PRESENTACION_EN.md) | Speaker guide, in three parts: the narrative per slide block + closing one-liners 🗣️ + links to the code. |
| [`GUIA_TECNICA_EN.md`](./GUIA_TECNICA_EN.md) | Copy-paste implementation reference (configs, commands, code). |
| [`presentacion/Claude_Code_Presentacion_EN.pptx`](./presentacion/) | The deck in English (16:9, 39 slides, with part separators). |
| [`ejemplos/`](./ejemplos/) | Real artifacts, grouped by course section (in Spanish). |
| [`docs/`](./docs/) | **Reference**: documents from a real production installation where the methodology is applied daily. |

## Technology documentation

| Technology | Role in the course | Documentation |
|---|---|---|
| **Claude Code** | The tool (Part 1) | <https://code.claude.com/docs> · [prompt caching](https://code.claude.com/docs/en/prompt-caching) · [sub-agents](https://code.claude.com/docs/en/sub-agents) · [agent teams](https://code.claude.com/docs/en/agent-teams) · [hooks](https://code.claude.com/docs/en/hooks) |
| **MCP** | The connection standard (§04) | <https://modelcontextprotocol.io> |
| **Agent SDK** | Custom automation (§07) | <https://platform.claude.com/docs/en/agent-sdk> |
| **CodeGraph** | The code graph (§09) | <https://colbymchenry.github.io/codegraph/> · [repo](https://github.com/colbymchenry/codegraph) |
| **Serena** | Semantic LSP navigation (§09) | <https://github.com/oraios/serena> |
| **GSD** | The productized method (§09) | <https://github.com/tomascortereal/claude-code-setup> |
| **graphify** | The ticket knowledge graph (Part 3) | <https://graphify.net> · [repo](https://github.com/Graphify-Labs/graphify) |
| **Playwright MCP** | Contract verification (§09) | <https://github.com/microsoft/playwright-mcp> |
| **Context7** | Up-to-date library docs (§09) | <https://context7.com> |
| **tree-sitter** | The parser under CodeGraph | <https://tree-sitter.github.io/tree-sitter/> |

## Regenerating

`presentacion/build_pptx.py` regenerates the 36-slide base deck (Spanish). The current decks include
**3 extra hand-added slides** (custom cover, agent-teams diagram, application architecture) — re-running
the script will overwrite them, so keep a copy or re-apply those slides. The English deck was produced by
in-place translation of the Spanish one (slide 1 and all images untouched).

```bash
pip install python-pptx pillow
python presentacion/build_pptx.py             # -> base 36-slide Spanish deck
python ejemplos/metodologia/render_flow.py    # -> flow.png (11-stage workflow)
python ejemplos/subagents/render_agents.py    # -> agents.png (subagents vs agent teams)
python presentacion/capture_kg_graph.py       # -> kg_graph.png (ticket-graph capture; needs playwright)
```

> Examples derived from a real professional project are **sanitized** (no client names, ticket IDs or
> secrets).
