# Claude Code — Guía de presentación

> Guía narrativa para la charla + vídeo. Está pensada para el/la **ponente**: cada sección mapea a un
> bloque de slides del deck ([`presentacion/`](./presentacion/)) e incluye el hilo a contar, los puntos
> clave y una frase de cierre 🗣️ lista para la diapositiva. Audiencia: **técnica / desarrolladores**.
>
> El detalle de implementación (configs, código copy-paste) está en [`GUIA_TECNICA.md`](./GUIA_TECNICA.md)
> y en [`ejemplos/`](./ejemplos/).

---

## Índice

0. [Qué es Claude Code (encuadre)](#0-qué-es-claude-code)
1. [Instalación y uso básico](#1-instalación-y-uso-básico)
2. [Memoria, instrucciones y sesiones](#2-memoria-instrucciones-y-sesiones)
3. [MCP — conectar tus herramientas](#3-mcp)
4. [Plugins, tools y skills](#4-plugins-tools-y-skills)
5. [Automatización](#5-automatización)
6. [Metodología real: GSD + CodeGraph + agente disciplinado](#6-metodología-real)
7. [Cierre](#7-cierre)

---

## 0. Qué es Claude Code

**Hilo:** Claude Code es un agente de coding que **lee tu codebase, edita ficheros, ejecuta comandos** y
se integra con tus herramientas. No es un autocompletado: entiende el proyecto entero y trabaja a través
de varios ficheros y tools. Y **el mismo motor** corre en terminal, IDE (VS Code/JetBrains), app de
escritorio y navegador — tus `CLAUDE.md`, settings y servers MCP funcionan en todas las superficies.

**Qué puedes hacer con él (los titulares):**
- Automatizar lo tedioso: escribir tests, arreglar lint, resolver conflictos de merge, actualizar deps.
- Construir features y arreglar bugs describiendo en lenguaje natural.
- Crear commits y PRs; revisar código en CI.
- Conectar tus herramientas con MCP; correr en pipelines Unix; programar tareas recurrentes.

🗣️ *"No es un copiloto que sugiere líneas: es un colaborador que planifica, edita en varios ficheros y verifica."*

---

## 1. Instalación y uso básico

**Hilo:** Instalar es una línea. Lo importante es entender los **dos modos** de uso.

**Instalación (elige uno):**
```bash
curl -fsSL https://claude.ai/install.sh | bash     # macOS / Linux / WSL (recomendado, auto-update)
brew install --cask claude-code                     # Homebrew
winget install Anthropic.ClaudeCode                 # Windows
# también: apt / dnf / apk en Linux
```
Luego, en cualquier proyecto:
```bash
cd tu-proyecto
claude            # primera vez te pide login
```

**Los dos modos (la idea que hay que dejar clara):**
- **Interactivo** — abres `claude` y conversas. Aquí vive el **plan mode**: Claude propone un plan antes
  de tocar nada y tú lo apruebas.
- **Headless (`-p`)** — un solo prompt, entra por stdin, sale por stdout. Es lo que lo hace **componible**
  al estilo Unix y automatizable en CI:
  ```bash
  tail -200 app.log | claude -p "avísame si ves anomalías"
  git diff main --name-only | claude -p "revisa estos ficheros por seguridad"
  ```

**Superficies:** terminal, VS Code/Cursor, JetBrains, Desktop (diffs visuales, sesiones en paralelo),
Web (claude.ai/code, tareas largas sin setup local).

🗣️ *"Interactivo para pensar contigo; `-p` para meterlo en una tubería. El mismo Claude, dos formas de invocarlo."*

---

## 2. Memoria, instrucciones y sesiones

**Hilo:** El agente es tan bueno como el contexto que le das — y como lo **gestionas**. Tres piezas:
`CLAUDE.md`, settings, y sesiones que viajan entre dispositivos.

### `CLAUDE.md` — la memoria del proyecto
Un Markdown que Claude lee al inicio de **cada** sesión. Ahí pones estándares de código, decisiones de
arquitectura, comandos y checklists. Se combina por **jerarquía**: global del usuario
(`~/.claude/CLAUDE.md`) → raíz del repo → subcarpetas → `CLAUDE.local.md` personal.

**El error clásico y cómo lo resuelvo — patrón de dos niveles:**
- **Nivel 1 (siempre cargado):** pequeño. Solo orientación + **punteros de una línea**.
- **Nivel 2 (bajo demanda):** el detalle en ficheros que el agente lee solo cuando hace falta.
- Regla *write-once*: cada dato se escribe en un único sitio; el `CLAUDE.md` lleva el puntero, no la copia.
- Resultado real: recortamos el nuestro **~73% sin perder información**. (Ejemplo sanitizado en
  [`ejemplos/claude-md/`](./ejemplos/claude-md/).)

**Auto-memory:** además, Claude guarda solo aprendizajes (comandos de build, pistas de debug) entre
sesiones sin que escribas nada.

### Settings — permisos
`settings.json` controla qué puede hacer el agente con un **allowlist** (`allow`/`deny`/`ask`). Un setup
profesional no usa comodines: usa reglas específicas (p. ej. la invocación exacta de pytest, operaciones
git acotadas, tools `mcp__*` concretas). Es la postura "el humano es dueño de las acciones externas".

### Sesiones que viajan
Las sesiones no están atadas a una superficie: empieza en la web/móvil y tráela al terminal con
`claude --teleport`; sigue desde el móvil con **Remote Control**; pasa una sesión del terminal al
**Desktop** con `/desktop` para revisar diffs.

> ⚠️ **Caveat de plataforma:** `/desktop` solo está disponible en la CLI de **macOS y Windows** (con
> suscripción Claude; no con API key). Si corres la CLI **dentro de WSL**, Claude Code la ve como
> **Linux** y el comando **no aparece** — aunque tengas la app de Desktop instalada en Windows. En ese
> caso, abre el proyecto directamente en la app de Desktop (pestaña *Code*). `--teleport` y Remote
> Control sí funcionan desde WSL.

🗣️ *"El `CLAUDE.md` que se carga siempre debe ser una onboarding de 30 segundos, no un vertedero. Punteros, no copias."*

---

## 3. MCP

**Hilo:** **MCP (Model Context Protocol)** es el estándar abierto para enchufar Claude a datos y
herramientas externas: Drive, Jira, Slack, tu base de datos, un navegador, tu tooling propio. Cada server
expone *tools* que aparecen como `mcp__<server>__<tool>`.

**Los tres scopes (dónde vive la config):**
- **local** → `.claude/settings.local.json` (solo tú, esta máquina).
- **project** → `.mcp.json` en la raíz, **versionado**, compartido con el equipo.
- **user** → `~/.claude.json` (todos tus proyectos).

**Añadir uno:**
```bash
claude mcp add --transport http context7 https://mcp.context7.com/mcp
claude mcp list        # estado
/mcp                   # dentro de la sesión: auth OAuth, tools
```

**Los que uso a diario:** `serena` (navegación semántica de código), `context7` (docs de librerías al
día), `playwright` (verificar la UI en un navegador real), `codegraph` (grafo del código), `supabase`.

**Buenas prácticas:** secretos por variable de entorno (nunca en el JSON versionado); el server disponible
≠ tool permitida (sigues controlando con el allowlist). Config de ejemplo en [`ejemplos/mcp/`](./ejemplos/mcp/).

🗣️ *"MCP convierte a Claude de 'sabe de código' a 'sabe de TU sistema': tus docs, tus tickets, tu navegador."*

---

## 4. Plugins, tools y skills

**Hilo:** Cuatro capas de extensibilidad, de simple a potente.

1. **Tools** — lo que Claude puede *hacer*: `Read/Edit/Write/Bash/Grep/Glob/WebFetch/Task` + las `mcp__*`.
   El acceso se gobierna con el allowlist de permisos.
2. **Slash commands** — un `.md` en `.claude/commands/` = un `/comando`. El cuerpo es el prompt.
   Ejemplo: [`/audit`](./ejemplos/skills-plugins/.claude/commands/audit.md) (npm audit → fix → tests).
3. **Skills** — empaquetan un flujo repetible en `.claude/skills/<n>/SKILL.md` con `description`; Claude
   la **auto-selecciona** por esa descripción. Ejemplo: `deploy-staging`. Frente al slash command (lo
   invocas tú), la skill puede llevar scripts/plantillas y se dispara sola.
4. **Plugins + marketplaces** — agrupan skills + comandos + agentes + MCP + hooks como una unidad
   instalable: `/plugin marketplace add <owner/repo>` → `/plugin install <x>`. Así se distribuye un setup
   entero (GSD instala decenas de skills de golpe).

**Subagentes:** con `Task` lanzas agentes con su propio contexto (`Explore`, `Plan`, `general-purpose`,
o especializados) para paralelizar sin ensuciar tu sesión.

🗣️ *"Slash command = atajo que invocas tú. Skill = capacidad que Claude decide usar. Plugin = las dos, distribuibles."*

---

## 5. Automatización

**Hilo:** Cuatro niveles, del control determinista a la autonomía total. (Aquí es donde el curso de hooks
brilla — todo en [`ejemplos/hooks/`](./ejemplos/hooks/) y [`ejemplos/automation/`](./ejemplos/automation/).)

### a) Hooks — el control determinista
Un hook es un comando de shell que se dispara **antes/después** de una acción del agente. No le *pides*
que formatee: lo **fuerzas**. Contrato:
- Payload por **stdin**; eventos `PreToolUse`/`PostToolUse`/`SessionStart`/`Stop`/…
- **Matcher = regex sobre el nombre de la tool** (`Write|Edit|MultiEdit`, `Read|Grep`, `*`).
- **`exit 0` permite · `exit 2` BLOQUEA** y devuelve stderr a Claude como feedback.
- Pre te da la *intención* (`tool_input`, puedes vetar); Post te da el *resultado* (`tool_response`).

Cinco hooks de ejemplo, todos reales:
- **Seguridad:** bloquear lectura de `.env` (exit 2).
- **Observabilidad:** volcar cada payload a un JSON.
- **Calidad (no bloqueante):** `prettier --write` tras cada edición.
- **Calidad (bloqueante):** type-check; si no compila, corta y Claude lo arregla en el turno.
- **Meta ("IA revisando IA"):** un hook que llama al Agent SDK para detectar código duplicado y vetarlo.

### b) Headless / piping — `claude -p` en cualquier tubería (ver sección 1).

### c) CI/CD — GitHub Actions / GitLab / GitHub Code Review. Revisión de PRs e issues automáticas.
   Ejemplo de workflow en [`ejemplos/automation/github-action-claude.yml`](./ejemplos/automation/github-action-claude.yml).

### d) Tareas programadas:
- **Routines** (`/schedule`) — corren en infra de Anthropic aunque apagues el equipo; disparables por
  API o eventos de GitHub.
- **Desktop scheduled tasks** — en tu máquina, con acceso local.
- **`/loop`** — polling rápido dentro de una sesión.

### e) Agent SDK — para workflows a medida: `query({ prompt, options: { allowedTools } })`.

🗣️ *"Con instrucciones le pides que se porte bien; con un hook lo garantizas. `exit 2` es el 'no' que Claude no puede ignorar."*

---

## 6. Metodología real

**Hilo:** Herramientas sin método = caos rápido. Esta es la parte más valiosa de la charla: **cómo se
trabaja de verdad con Claude Code en un proyecto en producción.** No es un flujo perfecto — es el que
usamos, sujeto a revisión constante. Todo el material está en
[`ejemplos/metodologia/`](./ejemplos/metodologia/) (sanitizado).

### El principio
> **El agente es un colaborador disciplinado, no un autopilot. La autonomía se gana por-decisión, no se
> concede en bloque.** El agente posee investigación, planes, implementación, tests y documentación;
> el humano posee las decisiones go/no-go, el scope y **toda acción externa** (push, PR, deploy).

### El flujo de 11 etapas

![Flujo de trabajo con Claude Code — 11 etapas](./ejemplos/metodologia/flow.png)

Encadenadas por **gates** (los recuadros coral del diagrama); un gate rojo es un STOP = *no escribir código*:

1. **Orientar** — history-first Y status-first (`STATUS.md`/ledgers + `git`/`gh`). #1 causa de retrabajo saltárselo.
2. **Triaje inbound** — ¿el síntoma es real en el **contrato de salida**? Si no → push back, no código.
3. **Regresión vs. pre-existente** — reproducir sobre el estado previo antes de asumir la culpa.
4. **Investigar** — **oráculo determinista** (parser/validador) primero; el LLM se reserva para verificar.
5. **Plan** — proponer opciones + trade-offs; **acuerdo humano** explícito antes de tocar código.
6. **Implementar** — TDD: RED (por el motivo correcto) → GREEN, cambio mínimo.
7. **Verificar** — unit + scoped + regresión + **gate outbound**: reproducir el contrato arreglado en local.
8. **Documentar** — porqué + qué + handover + criterios de aceptación, cada cosa **una vez**.
9. **Sanitizar** — escanear las **líneas añadidas** por nombres/IDs/secretos/atribución del agente.
10. **Handoff** — el humano (o un tool suyo, p. ej. Cursor) hace push/PR/deploy. El agente **nunca**.
11. **Revisión automática + persistir** — triar hallazgos del bot como los de un humano; codificar lecciones.

### Prevalencia de tools — qué usa Claude y cuándo (ver [`metodologia/herramientas.md`](./ejemplos/metodologia/herramientas.md))
El `CLAUDE.md` no solo dice *qué* hacer, sino **con qué tool y en qué orden**. Regla real (actualizada):
*"para 'qué es esto / quién depende / qué toco', un `codegraph_explore` **primero** — fuente + rutas de
llamada + blast radius + flags de cobertura de tests en una sola llamada (trata la fuente que devuelve como
YA leída, no la re-abras); Serena `find_referencing_symbols` para el chequeo **preciso** antes de
renombrar/borrar; grep/Read solo para literales."* Orden barato→caro:

| Etapa | Herramienta |
|---|---|
| Orientar | `STATUS.md`/ledgers · `git` · `gh` (coste 0) |
| Navegar (survey) | **CodeGraph** `codegraph_explore` — fuente + rutas + blast radius + cobertura, en 1 llamada |
| Refactor-check preciso | **Serena** `find_referencing_symbols` — desambigua por clase; **obligatorio** antes de renombrar/borrar |
| Diagnosticar | **Oráculo determinista** (parser, validador, `_diag_*.py`) — coste 0, reproducible |
| Entorno (logs, config) | **AWS CLI** — herramienta de debugging de primera clase |
| Contrato de salida | **Playwright** / F12 sobre el endpoint que ve el consumidor |
| Solo al final | La tirada del **LLM** — para *verificar* el fix, no para diagnosticar |

### Un ejemplo real (ver [`metodologia/EJEMPLO_REAL.md`](./ejemplos/metodologia/EJEMPLO_REAL.md))
Bug: *"un campo sale vacío en la UI pero está en el PDF."* → Orientar (STATUS.md encuentra un
`SHARP_EDGES` que restringe el fix) → confirmar el vacío en el JSON del contrato (Playwright) →
pre-existente, no regresión → Serena+CodeGraph localizan el detector de fin de provisión, y un
`_diag_pdf.py` determinista revela la causa (desbordamiento a 2ª columna) **sin una sola llamada al LLM**
→ plan aprobado → test RED → fix keyed en la *propiedad estructural* (no en el cliente) → regresión
byte-idéntica (prueba no-op) + contrato reproducido en local → documentar → sanitizar → el humano hace el
push. Un review-bot detecta un caso de columna a la izquierda → se añade el test y va al `PLAYBOOK`.

### El tooling que lo encarna
- **GSD** ([`ejemplos/gsd/`](./ejemplos/gsd/)) — el método **hecho tooling**: ciclo *discutir → planificar
  → ejecutar → verificar* con estado en `.planning/` y subagentes (`gsd-planner`, `gsd-plan-checker`,
  `gsd-executor`, `gsd-verifier`…). El gate de plan y la verificación de objetivo son los de la metodología.
- **CodeGraph** ([`ejemplos/codegraph/`](./ejemplos/codegraph/)) — índice tree-sitter→SQLite local; una
  consulta (`codegraph_explore`) devuelve fuente + rutas de llamada + blast radius + **flags de cobertura de
  tests** (58% menos tool calls en sus benchmarks). Es el **primer** tool de navegación; el proyecto por
  defecto se fija con `--path` en la config MCP (o se pasa `projectPath` para otro repo — ya indexamos
  también `monolith` y `frontend`).
- **Serena · Playwright · AWS CLI** — navegación semántica, verificación del contrato, diagnóstico determinista.

### Los mismos principios en ops: sincronizar máquinas (ver [`metodologia/machine-sync.md`](./ejemplos/metodologia/machine-sync.md))
Un runbook real que usamos para mover el workspace entre la máquina principal y el portátil. Demuestra que
la metodología no es solo para código:
- **Sincronización asimétrica:** outbound = **copia completa** (un tarball: workspace + `~/.claude`/`.aws`/
  `.ssh`, con `-h` para dereferenciar symlinks, excluyendo venvs/node_modules); inbound = **solo delta**
  (el código ya está en GitHub → `git fetch`; solo los docs gitignored de `data/`, unos MB, viajan).
- **Memoria durable, bajo demanda:** el runbook **no** vive en el `CLAUDE.md` always-loaded — hay un
  puntero de una línea; se carga solo cuando viajas.
- **El landing lo conduce un agente con guardrails:** el `INSTRUCTIONS.md` del delta está escrito *para un
  agente*; solo no-destructivo (renombrar, no borrar), `git fetch` es la única op de red, backup+`diff` de
  `STATUS.md`, y **STOP y pregunta** si la principal hizo ediciones propias. El humano aprueba; el agente
  no hace push/merge.
- **"Descubre, no asumas":** los comandos **derivan** la raíz del workspace (`ls -d /mnt/*/ILS`), no la
  hardcodean, porque las rutas difieren por máquina.
- **El tooling también se sincroniza:** el índice `.codegraph/` se **excluye** del tarball (es local, con
  rutas absolutas) y se reconstruye en destino; un `target-setup.sh` idempotente reinstala el CLI de
  CodeGraph, actualiza GSD solo si va atrasado y **corrige el `--path` del MCP** a la raíz real del portátil.

🗣️ *"Ninguna etapa dice 'pídele al LLM que lo arregle'. La potencia del modelo se canaliza por gates deterministas; el humano conserva las decisiones."*

---

## 7. Cierre

- Instalar es trivial; el valor está en **cómo** lo usas: contexto lean, permisos guardados, método.
- Las 5 capas: **instalar → memoria/sesiones → MCP → skills/plugins → automatización.**
- El salto de nivel: de "chatear con un asistente" a **un sistema** con hooks que garantizan calidad,
  MCP que conecta tu mundo, y una metodología que trata al agente como colaborador con gates de evidencia.

**Referencias:** documentación oficial <https://code.claude.com/docs> · GSD
<https://github.com/tomascortereal/claude-code-setup> · CodeGraph <https://colbymchenry.github.io/codegraph/>.
