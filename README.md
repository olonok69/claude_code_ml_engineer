# Claude Code — Curso en tres partes (presentación + guías)

> **English version:** [`README_EN.md`](./README_EN.md) · [`GUIA_PRESENTACION_EN.md`](./GUIA_PRESENTACION_EN.md) ·
> [`GUIA_TECNICA_EN.md`](./GUIA_TECNICA_EN.md) · `presentacion/Claude_Code_Presentacion_EN.pptx`.

Material para un **curso/workshop** sobre **Claude Code**: una única presentación (`.pptx`) con **tres
partes diferenciadas** y dos guías escritas, con ejemplos reales y ejecutables. En español, orientado a
**desarrolladores**.

- **Parte 1 — Claude Code:** instalación y uso básico · memoria, instrucciones y sesiones · **contexto
  (context window + prompt caching)** · MCP · plugins, tools y skills · **subagents y agent teams** ·
  automatización.
- **Parte 2 — La metodología (agnóstica de la herramienta):** el flujo real de 11 etapas con gates ·
  las herramientas del método (CodeGraph, Serena, GSD, oráculos) · la transferencia a otro agente
  (GitHub Copilot) · la sincronización de máquinas.
- **Parte 3 — El grafo de conocimiento de tickets:** un caso completo construido con **graphify**:
  corpus con manifest, pipeline `/kg-refresh`, consulta `/kg` sin LLM, la visualización real del grafo
  (507 nodos · 35 comunidades) y su enganche en la metodología.

## Contenido

| Archivo | Qué es |
|---|---|
| [`GUIA_PRESENTACION.md`](./GUIA_PRESENTACION.md) | Guía narrativa para el/la ponente, en dos partes: hilo a contar por slide + frases de cierre 🗣️ + links al código. |
| [`GUIA_TECNICA.md`](./GUIA_TECNICA.md) | Referencia de implementación copy-paste (configs, comandos, código), en las mismas dos partes. |
| [`presentacion/Claude_Code_Presentacion.pptx`](./presentacion/) | El deck (16:9, 39 slides — 36 generadas + portada, diagrama de teams y arquitectura añadidas a mano; versión EN: Claude_Code_Presentacion_EN.pptx). |
| [`presentacion/build_pptx.py`](./presentacion/build_pptx.py) | Generador del deck (regenerable). |
| [`ejemplos/`](./ejemplos/) | Artefactos reales, agrupados por sección del curso. |
| [`docs/`](./docs/) | **Referencia**: documentos de una instalación real donde se aplica la metodología a diario (knowledge graph, adaptación a Copilot, runbooks de sync, setup de CodeGraph+GSD). |

## Ejemplos (por sección del curso)

**Parte 1:**
- [`ejemplos/claude-md/`](./ejemplos/claude-md/) — el patrón de CLAUDE.md de dos niveles (§02).
- [`ejemplos/context/`](./ejemplos/context/) — gestión del context window: anatomía, comandos, higiene (§03).
- [`ejemplos/prompt-caching/`](./ejemplos/prompt-caching/) — cómo funciona el caching + demo ejecutable `cache_demo.py` (§03).
- [`ejemplos/mcp/`](./ejemplos/mcp/) — `.mcp.json` con scopes y secretos por entorno (§04).
- [`ejemplos/skills-plugins/`](./ejemplos/skills-plugins/) — un slash command y una skill (§05).
- [`ejemplos/subagents/`](./ejemplos/subagents/) — subagentes custom (`.claude/agents/`), agent teams y el diagrama subagente-vs-team (§06).
- [`ejemplos/hooks/`](./ejemplos/hooks/) — 5 hooks reales (seguridad, observabilidad, formato, type-check, "IA revisando IA") + payloads (§07).
- [`ejemplos/automation/`](./ejemplos/automation/) — GitHub Action, Agent SDK, scheduling (§07).

**Parte 2:**
- [`ejemplos/metodologia/`](./ejemplos/metodologia/) — **el flujo real de 11 etapas, un ejemplo concreto de principio a fin, la prevalencia de tools** (Serena/CodeGraph/Playwright/AWS/Docker/oráculo determinista), el **gate outbound de tres checks** (contrato vía *wrapper* + verificación en la **imagen desplegada**), el **runbook de ops** (sincronizar el workspace entre máquinas) y el diagrama del flujo (§08, §11).
- [`ejemplos/gsd/`](./ejemplos/gsd/) · [`ejemplos/codegraph/`](./ejemplos/codegraph/) · [`ejemplos/serena/`](./ejemplos/serena/) — las herramientas del método, en profundidad (§09).
- [`docs/ai-agents-code-methodology/`](./docs/ai-agents-code-methodology/) — el starter-kit portable + adaptación a GitHub Copilot (§10).
- [`docs/synchro/`](./docs/synchro/) — runbooks reales de sincronización entre máquinas (§11).

**Parte 3:**
- [`docs/knowledge-graph/`](./docs/knowledge-graph/) — el grafo de conocimiento de tickets, construido con **graphify**: diseño (`design.md`), scripts (`kg_query.sh`, `kg_refresh.sh`, `build_manifest.py`, `stage_corpus.py`), tests, `manifest.txt` y la **salida real** (`output/graph.html` interactivo + `GRAPH_REPORT.md`) (§12).
- [`docs/KNOWLEDGE_GRAPH.md`](./docs/KNOWLEDGE_GRAPH.md) — el resumen narrativo del mismo sistema.
- [`presentacion/kg_graph.png`](./presentacion/kg_graph.png) — la captura del grafo usada en el deck (regenerable con `capture_kg_graph.py`).

## Regenerar el deck y los diagramas

```bash
pip install python-pptx pillow
python presentacion/build_pptx.py             # -> presentacion/Claude_Code_Presentacion.pptx
python ejemplos/metodologia/render_flow.py    # -> flow.png (flujo de 11 etapas)
python ejemplos/subagents/render_agents.py    # -> agents.png (subagentes vs agent teams)
python presentacion/capture_kg_graph.py       # -> kg_graph.png (captura del grafo de tickets; requiere playwright)
```

## Documentación de las tecnologías

| Tecnología | Qué es en el curso | Documentación |
|---|---|---|
| **Claude Code** | La herramienta (Parte 1) | <https://code.claude.com/docs> · [prompt caching](https://code.claude.com/docs/en/prompt-caching) · [sub-agents](https://code.claude.com/docs/en/sub-agents) · [agent teams](https://code.claude.com/docs/en/agent-teams) · [hooks](https://code.claude.com/docs/en/hooks) |
| **MCP** | El estándar de conexión (§04) | <https://modelcontextprotocol.io> |
| **Agent SDK** | Automatización a medida (§07) | <https://platform.claude.com/docs/en/agent-sdk> |
| **CodeGraph** | Grafo del código (§09) | <https://colbymchenry.github.io/codegraph/> · [repo](https://github.com/colbymchenry/codegraph) |
| **Serena** | Navegación semántica LSP (§09) | <https://github.com/oraios/serena> |
| **GSD** | El método productizado (§09) | <https://github.com/tomascortereal/claude-code-setup> |
| **graphify** | El grafo de tickets (Parte 3) | <https://graphify.net> · [repo](https://github.com/Graphify-Labs/graphify) |
| **Playwright MCP** | Verificación del contrato (§09) | <https://github.com/microsoft/playwright-mcp> |
| **Context7** | Docs de librerías al día (§09) | <https://context7.com> |
| **tree-sitter** | El parser bajo CodeGraph | <https://tree-sitter.github.io/tree-sitter/> |

## Fuentes

Documentación oficial <https://code.claude.com/docs> · curso de hooks de Anthropic · GSD
<https://github.com/tomascortereal/claude-code-setup> · CodeGraph <https://colbymchenry.github.io/codegraph/> ·
Serena <https://github.com/oraios/serena> · graphify <https://graphify.net>.

> Los ejemplos derivados de un proyecto profesional real están **sanitizados** (sin nombres de cliente,
> IDs de ticket ni secretos).
