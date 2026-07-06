# GSD — "Get Stuff Done"

Setup de Claude Code para **gestión de proyectos por fases**, instalado como plugin.
Repo: https://github.com/tomascortereal/claude-code-setup

## La idea

En vez de "chatear" con el agente, GSD impone un **ciclo de vida** con estado persistente en
`.planning/`. Cada fase pasa por: **discutir → planificar → ejecutar → verificar**, con artefactos
versionados (`ROADMAP.md`, `PLAN.md`, `VERIFICATION.md`) y commits atómicos.

## Comandos que más uso

| Comando | Para qué |
|---|---|
| `/gsd-new-project` | Inicializa el proyecto con contexto profundo → `PROJECT.md`. |
| `/gsd-progress` | Comando "situacional": dice en qué punto estás y qué toca. |
| `/gsd-discuss-phase` | Recoge contexto de la fase con preguntas adaptativas. |
| `/gsd-plan-phase` | Crea un `PLAN.md` detallado con verificación. |
| `/gsd-execute-phase` | Ejecuta los planes con paralelización por olas (waves). |
| `/gsd-verify-work` | Valida lo construido contra criterios (UAT conversacional). |
| `/gsd-autonomous` | Corre todas las fases restantes de forma autónoma. |

## Por qué encaja con la metodología

GSD es la **encarnación en tooling** de la idea "el agente es un colaborador disciplinado, no un
autopilot": separa planificar de ejecutar, exige verificación, y deja un rastro durable. Trae además
una batería de **subagentes especializados** (`gsd-planner`, `gsd-executor`, `gsd-code-reviewer`,
`gsd-verifier`…) que se orquestan solos.

> Nota: GSD instala **muchas** skills (`gsd-*`). Empieza por `/gsd-help` y `/gsd-progress`.
