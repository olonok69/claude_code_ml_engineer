# Claude Code — Presentación y guía técnica

Material para una charla + vídeo sobre **Claude Code**: una presentación (`.pptx`) y dos guías escritas,
con ejemplos reales y ejecutables. En español, orientado a **desarrolladores**.

Cubre las cinco secciones pedidas — **instalación y uso básico · memoria, instrucciones y sesiones · MCP ·
plugins, tools y skills · automatización** — más la **metodología real** de trabajo (GSD + CodeGraph +
agente disciplinado).

## Contenido

| Archivo | Qué es |
|---|---|
| [`GUIA_PRESENTACION.md`](./GUIA_PRESENTACION.md) | Guía narrativa para el/la ponente: hilo a contar por slide + frases de cierre 🗣️. |
| [`GUIA_TECNICA.md`](./GUIA_TECNICA.md) | Referencia de implementación copy-paste (configs, comandos, código). |
| [`presentacion/Claude_Code_Presentacion.pptx`](./presentacion/) | El deck (16:9, 14 slides). |
| [`presentacion/build_pptx.py`](./presentacion/build_pptx.py) | Generador del deck (regenerable). |
| [`ejemplos/`](./ejemplos/) | Artefactos reales: hooks, CLAUDE.md, MCP, skills, GSD, CodeGraph, automatización. |
| [`docs/DISENO.md`](./docs/DISENO.md) | Documento de diseño / decisiones. |

## Ejemplos

- [`ejemplos/hooks/`](./ejemplos/hooks/) — 5 hooks reales (seguridad, observabilidad, formato, type-check, "IA revisando IA") + payloads.
- [`ejemplos/claude-md/`](./ejemplos/claude-md/) — el patrón de CLAUDE.md de dos niveles.
- [`ejemplos/mcp/`](./ejemplos/mcp/) — `.mcp.json` con scopes y secretos por entorno.
- [`ejemplos/skills-plugins/`](./ejemplos/skills-plugins/) — un slash command y una skill.
- [`ejemplos/automation/`](./ejemplos/automation/) — GitHub Action, Agent SDK, scheduling.
- [`ejemplos/gsd/`](./ejemplos/gsd/) · [`ejemplos/codegraph/`](./ejemplos/codegraph/) — las dos herramientas de metodología.

## Regenerar el deck

```bash
pip install python-pptx
python presentacion/build_pptx.py     # -> presentacion/Claude_Code_Presentacion.pptx
```

## Fuentes

Documentación oficial <https://code.claude.com/docs> · curso de hooks de Anthropic · GSD
<https://github.com/tomascortereal/claude-code-setup> · CodeGraph <https://colbymchenry.github.io/codegraph/>.

> Los ejemplos derivados de un proyecto profesional real están **sanitizados** (sin nombres de cliente,
> IDs de ticket ni secretos).
