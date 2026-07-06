# CodeGraph — grafo de conocimiento del código

Herramienta que indexa tu código en un **grafo SQLite** de símbolos, aristas (llamadas, imports) y
ficheros, expuesto a Claude Code como servidor MCP.
Repo: https://github.com/colbymchenry/codegraph · Docs: https://colbymchenry.github.io/codegraph/

## Qué problema resuelve

El bucle habitual "grep → abrir fichero → seguir el import → volver a grepear" gasta muchísimo
contexto. CodeGraph lo reemplaza por **una llamada**: `codegraph_explore` devuelve el **código fuente
verbatim y numerado** de los símbolos relevantes, **más las rutas de llamada** entre ellos (incluyendo
saltos de dispatch dinámico que grep no puede seguir) y un resumen del *blast radius*.

## Uso

```bash
codegraph init                       # crea el índice .codegraph/ en el repo (decisión del usuario)
codegraph explore "<símbolo o pregunta>"   # desde shell

# Desde Claude Code (MCP), en un repo con .codegraph/:
#   codegraph_explore  ->  fuente + rutas de llamada + blast radius, en un solo round-trip
```

Si no hay carpeta `.codegraph/`, no se usa: indexar es decisión explícita del usuario.

## Cuándo tirar de él antes que de grep/Read

- "¿Quién llama a esta función y qué se rompe si la cambio?" → grafo, no rastreo manual de imports.
- Entender una subsección desconocida → una consulta en vez de leer 6 ficheros enteros.
- Análisis de impacto antes de un refactor.

Es complementario al `code-review-graph`: CodeGraph responde *"qué es y cómo se conecta"*; el otro,
*"qué cambió y con qué riesgo"*.
