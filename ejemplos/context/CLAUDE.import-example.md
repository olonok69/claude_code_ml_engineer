# CLAUDE.md — ejemplo de imports y carga bajo demanda

> Fragmento de ejemplo (sintaxis real) de un CLAUDE.md nivel-1 que usa `@imports` y punteros
> en vez de copiar contenido. Compáralo con el patrón completo en [`../claude-md/CLAUDE.md`](../claude-md/CLAUDE.md).

## Proyecto

API de facturación. Monorepo: `api/` (FastAPI) + `web/` (React). Ver @README.md para el overview
y @package.json para los scripts disponibles.

## Comandos

- Tests: `.venv/bin/pytest tests/ -q` (nunca `pytest` a secas: usa el venv)
- Lint: `npm run lint --workspace=web`

## Reglas

- Antes de renombrar/borrar un símbolo compartido: `codegraph_explore` + Serena
  `find_referencing_symbols` (detalle: una línea aquí, el porqué vive en `data/changes/CONVENTIONS.md`).
- Estado vivo por ticket: `data/changes/STATUS.md` (leer al orientarse, no copiar aquí).

<!--
  Notas sobre la carga:
  - @README.md y @package.json se incorporan al cargar ESTE fichero (import explícito).
  - api/CLAUDE.md y web/CLAUDE.md existen pero solo se cargan cuando Claude entra a esas carpetas.
  - Todo lo demás son punteros de una línea: el agente lo lee bajo demanda con Read.
  - Resultado: nivel 1 pequeño y estable -> menos tokens fijos y mejor prompt caching.
-->
