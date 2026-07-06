# CodeGraph — inteligencia de código local

Herramienta *local-first* que indexa tu código con **tree-sitter** en un **grafo SQLite** de símbolos,
aristas y ficheros, y lo expone a Claude Code como servidor MCP.
Repo: https://github.com/colbymchenry/codegraph · Docs: https://colbymchenry.github.io/codegraph/

## Qué indexa (determinista, del AST — no resumido por un LLM)

- **Símbolos:** funciones, clases, métodos, tipos, rutas, componentes.
- **Aristas:** llamadas, imports, herencia, referencias, relaciones de framework.
- **Ficheros:** estructura + búsqueda full-text.

Todo vive en `.codegraph/` (una base SQLite local). **Sin servicios externos ni API keys.**

## Qué problema resuelve

El bucle habitual "grep → abrir fichero → seguir el import → volver a grepear" gasta muchísimo contexto.
CodeGraph lo reemplaza por **una consulta**: `codegraph_explore` devuelve el **código fuente verbatim y
numerado** de los símbolos relevantes, **más las rutas de llamada** entre ellos (incluidos saltos de
dispatch dinámico que grep no puede seguir) y un resumen del **blast radius** (qué se rompería al cambiar).

Según sus benchmarks, dar acceso a CodeGraph a un agente produjo **58% menos tool calls**, **22% más
rápido** y prácticamente eliminó las lecturas de fichero.

## CLI

```bash
codegraph init        # crea el índice .codegraph/ en el repo (decisión explícita del usuario)
codegraph index       # (re)indexa
codegraph watch       # re-indexa en vivo al cambiar ficheros
codegraph explore "<símbolo o pregunta>"   # fuente + rutas de llamada + blast radius, en 1 round-trip
codegraph mcp         # arranca el servidor MCP para Claude Code
codegraph serve       # interfaz de servidor
```
Desde Claude Code (MCP), en un repo con `.codegraph/`: la tool **`codegraph_explore`** hace lo mismo en un
solo round-trip. Se le pasa `projectPath` para consultar un repo concreto (útil en un monorepo o con
varios repos en el workspace). Si no hay `.codegraph/`, no se usa: indexar es decisión del usuario.

## CodeGraph vs. Serena vs. grep — cuándo cada uno

| Pregunta | Herramienta |
|---|---|
| "Dame la fuente de este símbolo y sus callers, y qué se rompe si lo cambio" | **CodeGraph** `explore` (fuente + rutas + blast radius en 1 llamada) |
| "Overview de símbolos de este fichero" / "cuerpo de esta función" | **Serena** `get_symbols_overview` / `find_symbol` |
| "¿Quién referencia este helper?" antes de un rename | **Serena** `find_referencing_symbols` (o CodeGraph para el blast radius) |
| Búsqueda textual simple de una cadena | grep/`search_for_pattern` |

En el flujo real (ver [`../metodologia/EJEMPLO_REAL.md`](../metodologia/EJEMPLO_REAL.md)), CodeGraph y
Serena entran en la **etapa 4 (investigar)**: navegar ficheros de 5k líneas por símbolos y rutas de
llamada, no leyéndolos enteros. Es complementario a `code-review-graph` (que responde *"qué cambió y con
qué riesgo"*): CodeGraph responde *"qué es y cómo se conecta"*.
