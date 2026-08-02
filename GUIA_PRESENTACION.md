# Claude Code — Guía de presentación (curso en dos partes)

> Guía narrativa para el curso/workshop. Está pensada para el/la **ponente**: cada sección mapea a un
> bloque de slides del deck ([`presentacion/`](./presentacion/)) e incluye el hilo a contar, los puntos
> clave y una frase de cierre 🗣️ lista para la diapositiva. Audiencia: **técnica / desarrolladores**.
>
> El deck es **una sola presentación** con **tres partes diferenciadas**:
> - **Parte 1 — Claude Code:** la herramienta, de la instalación a los equipos de agentes.
> - **Parte 2 — La metodología:** cómo se trabaja de verdad con un agente en producción. Es **agnóstica
>   de la herramienta** — se demuestra con Claude Code, pero viaja a otros agentes (sección 10).
> - **Parte 3 — El grafo de conocimiento de tickets:** un caso completo construido con **graphify**
>   (no con CodeGraph): pipeline, comandos creados en Claude Code, visualización real y enganche
>   en la metodología.
>
> El detalle de implementación (configs, código copy-paste) está en [`GUIA_TECNICA.md`](./GUIA_TECNICA.md)
> y en [`ejemplos/`](./ejemplos/). La carpeta [`docs/`](./docs/) es material de referencia de una
> instalación real donde se aplica la metodología a diario.

---

## Índice

**Parte 1 — Claude Code**

0. [Qué es Claude Code (encuadre)](#0-qué-es-claude-code)
1. [Instalación y uso básico](#1-instalación-y-uso-básico)
2. [Memoria, instrucciones y sesiones](#2-memoria-instrucciones-y-sesiones)
3. [Contexto: context window y prompt caching](#3-contexto)
4. [MCP — conectar tus herramientas](#4-mcp)
5. [Plugins, tools y skills](#5-plugins-tools-y-skills)
6. [Subagents y Agent Teams](#6-subagents-y-agent-teams)
7. [Automatización](#7-automatización)

**Parte 2 — La metodología (agnóstica)**

8. [La metodología: principio, flujo y ejemplo real](#8-la-metodología)
9. [Las herramientas del método: CodeGraph, Serena, GSD…](#9-las-herramientas-del-método)
10. [Transferir la metodología a otro agente](#10-transferir-la-metodología)
11. [Sincronización de máquinas](#11-sincronización-de-máquinas)

**Parte 3 — El grafo de conocimiento de tickets (graphify)**

12. [El grafo de conocimiento de tickets](#12-el-grafo-de-conocimiento-de-tickets)
13. [Cierre](#13-cierre)

---

# PARTE 1 — Claude Code

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

## 3. Contexto

**Hilo:** Aquí está la sección que explica **por qué** el patrón de dos niveles de la sección anterior no
es manía: el context window es el recurso que gobierna rendimiento **y** coste. Dos mitades: gestionarlo
(context window) y no pagarlo dos veces (prompt caching). Material: [`ejemplos/context/`](./ejemplos/context/)
y [`ejemplos/prompt-caching/`](./ejemplos/prompt-caching/).

### 3a. Context window — el recurso que gobierna todo

**Qué lo llena antes de que escribas nada:** system prompt (~4.2k tokens), auto-memory (~680), entorno
(~280), el índice de tools MCP, y tu `CLAUDE.md`. Después: conversación, ficheros leídos, output de
comandos. La ventana es de 200K tokens (1M en beta vía API), pero el rendimiento **degrada antes de
llenarla** — contexto con ruido = peores decisiones.

**Los mandos:**
- `/context` — visualiza el uso, bloque a bloque. Mide antes de optimizar.
- `/compact [instrucciones]` — compacta guiando qué sobrevive (*"céntrate en los cambios de la API"*).
  El auto-compact salta solo cerca del límite; anticiparse con foco es mejor (la compactación es lossy).
- `/clear` — reset entre tareas no relacionadas. Contexto fresco > resumen de ruido.
- `/rewind` (Esc+Esc) — checkpoints: restaura conversación, código o ambos; condensa tramos.

**Higiene que aplicamos de verdad:** CLAUDE.md mínimo (dos niveles); `@imports` y CLAUDE.md de subcarpeta
que cargan bajo demanda; desactivar servers MCP que no usas; investigar en **subagentes** (sección 6) para
que el ruido no viva en tu sesión; lecturas con puntería en vez de "entiende todo el auth".

### 3b. Prompt caching — no pagar el mismo contexto dos veces

**El mecanismo:** cada turno reenvía TODO el contexto. La API cachea el **prefijo estable** (orden
estricto: `Tools → System → Messages`): escribir cache cuesta 1.25× (2× a 1h de TTL), **leerlo cuesta
0.1×**. Una sesión de 50 turnos relee el prefijo 50 veces a precio de saldo.

**En Claude Code no configuras nada** — lo aplica solo. El **TTL por defecto depende de la
autenticación**: **1 h con suscripción** (incluido en el plan) · **5 min con API key**/Bedrock/Vertex; se
puede cambiar por env var (`ENABLE_PROMPT_CACHING_1H`, `FORCE_PROMPT_CACHING_5M`,
`DISABLE_PROMPT_CACHING`). Como cada lectura renueva la ventana, con suscripción una pausa de hasta 1 h
entre turnos sigue acertando cache. Y tus decisiones determinan si acierta:
- CLAUDE.md pequeño y **estable** → prefijo que nunca cambia → hits.
- Editar CLAUDE.md/settings a mitad de sesión → invalida el cache desde ahí.
- Muchos MCP → bloque de tools grande y cambiante → escrituras caras.
- `/compact` reescribe historial → rompe el cache de mensajes una vez, y sigue.

Demo ejecutable con la API (ver los contadores `cache_read_input_tokens`):
[`ejemplos/prompt-caching/cache_demo.py`](./ejemplos/prompt-caching/cache_demo.py).

**El puente que une 3a y 3b (y adelanta la Parte 2):** contexto lean y estable **rinde mejor y cuesta
menos a la vez**. Y la "prevalencia de tools" de la metodología (CodeGraph antes que leer ficheros) es,
en el fondo, política de contexto: máxima señal por token.

🗣️ *"El context window es tu presupuesto y el prompt caching tu descuento: lean y estable gana en los dos."*

---

## 4. MCP

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
≠ tool permitida (sigues controlando con el allowlist); y — enlaza con la sección 3 — **cada server suma
contexto**: desactiva los que el proyecto no use. Config de ejemplo en [`ejemplos/mcp/`](./ejemplos/mcp/).

**La distinción que hay que dejar clara:** los servers **no se instalan en el `CLAUDE.md`** — ese fichero
es prompt, no configuración. La config (estos tres scopes, o un plugin) da la **capacidad**; el CLAUDE.md
da el **criterio** — el *trigger map* que hace que el agente tire de la tool correcta sin que se lo pidas
("Serena antes de leer ficheros enteros"). Instalar convierte "no tengo la tool" en "la tengo"; el
CLAUDE.md convierte "la tengo" en "se usa en el orden correcto" (es la prevalencia de la Parte 2).

🗣️ *"MCP convierte a Claude de 'sabe de código' a 'sabe de TU sistema': tus docs, tus tickets, tu navegador."*

---

## 5. Plugins, tools y skills

**Hilo:** Cuatro capas de extensibilidad, de simple a potente.

1. **Tools** — lo que Claude puede *hacer*: `Read/Edit/Write/Bash/Grep/Glob/WebFetch/Task` + las `mcp__*`.
   Las built-in van **compiladas en el binario** (no hay carpeta de tools que editar; se envían como
   schemas en cada request); solo MCP y plugins *añaden* tools. Lo que gestionas es el **acceso**:
   allowlist de permisos (que también puede vetar una built-in), flags `--allowedTools`/`--disallowedTools`,
   hooks `PreToolUse` como veto por contenido, y el frontmatter `tools:` de cada subagente.
2. **Slash commands** — un `.md` en `.claude/commands/` = un `/comando`. El cuerpo es el prompt.
   Ejemplo: [`/audit`](./ejemplos/skills-plugins/.claude/commands/audit.md) (npm audit → fix → tests).
3. **Skills** — empaquetan un flujo repetible en `.claude/skills/<n>/SKILL.md` con `description`; Claude
   la **auto-selecciona** por esa descripción. Ejemplo: `deploy-staging`. Frente al slash command (lo
   invocas tú), la skill puede llevar scripts/plantillas y se dispara sola.
4. **Plugins + marketplaces** — agrupan skills + comandos + agentes + MCP + hooks como una unidad
   instalable: `/plugin marketplace add <owner/repo>` → `/plugin install <x>`. Así se distribuye un setup
   entero (GSD instala decenas de skills de golpe).

### Slash command vs. skill vs. plugin — la diferencia en una tabla

| | **Slash command** | **Skill** | **Plugin** |
|---|---|---|---|
| **Qué es** | Un prompt guardado | Una capacidad repetible con instrucciones + ficheros de apoyo | Un paquete distribuible |
| **Dónde vive** | `.claude/commands/<n>.md` | `.claude/skills/<n>/SKILL.md` (+ scripts/plantillas en la carpeta) | Se instala en `~/.claude/plugins` desde un marketplace |
| **Cómo se invoca** | **Tú**, escribiendo `/<n>` | **Claude la auto-selecciona** por su `description` | No se "invoca": instala lo de dentro |
| **Qué empaqueta** | Solo el prompt (acepta `$ARGUMENTS`) | Instrucciones + código/plantillas/referencias | skills + comandos + agentes + MCP + hooks |
| **Alcance** | Un flujo corto | Un flujo con assets | Un setup entero |
| **Distribución** | Copiar el fichero | Copiar la carpeta (o vía un plugin) | `/plugin install` (GSD, serena, context7… son plugins) |

La idea en una frase: el **slash command lo disparas tú**; la **skill la decide Claude** (por su
descripción); el **plugin es el vehículo de reparto** de ambas cosas —y de agentes, MCP y hooks— versionado.

🗣️ *"Slash command = atajo que invocas tú. Skill = capacidad que Claude decide usar. Plugin = las dos, distribuibles."*

---

## 6. Subagents y Agent Teams

**Hilo:** La quinta capa de extensibilidad merece sección propia: no extender *qué sabe hacer* Claude,
sino **cuántos Claudes trabajan y cómo se coordinan**. Tres escalones: subagentes built-in → subagentes
custom → agent teams. Todo el material (incl. el diagrama) en [`ejemplos/subagents/`](./ejemplos/subagents/).

### 6a. Subagentes (tool `Task`) — aislar contexto

Claude lanza **subagentes** con su propio context window: la investigación sucia sucede "fuera" y a tu
sesión vuelve **solo el resumen**. Built-ins: `Explore` (read-only), `Plan`, `general-purpose`. Es el
mecanismo de higiene de contexto de la sección 3 — y se pueden lanzar **en paralelo** para trabajo
independiente.

### 6b. Subagentes custom — `.claude/agents/*.md`

Un Markdown con frontmatter (`name`, `description`, `tools`, `model`) + system prompt propio. La
`description` guía la auto-selección (como en las skills); `tools` es un allowlist por agente; `/agents`
los lista. Scopes: usuario (`~/.claude/agents/`) o proyecto (versionado). Dos ejemplos reales:
- [`security-reviewer`](./ejemplos/subagents/.claude/agents/security-reviewer.md) — revisor con tools read-only.
- [`refactor-scout`](./ejemplos/subagents/.claude/agents/refactor-scout.md) — codifica la regla
  CodeGraph→Serena de la metodología (Parte 2) como procedimiento de agente.

**El gotcha que hay que contar:** el subagente **no hereda tu conversación** — el contexto necesario va
en el prompt de lanzamiento.

### 6c. Agent Teams (experimental) — coordinar sesiones

Un **team** = un lead + teammates, cada uno una **sesión completa** de Claude Code, con **task list
compartida** (`~/.claude/tasks/<team>/`) y **mensajería directa** entre teammates (inboxes) — pueden
debatir hallazgos, no solo reportar hacia arriba. Se activa con `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`;
display in-process o split-panes (tmux/iTerm2). Los roles pueden reutilizar tus subagentes custom.

**Cuándo cada uno (la diapositiva de decisión):**

| | Subagente | Agent team |
|---|---|---|
| Contexto | Aislado; devuelve un resumen | Cada teammate = sesión completa |
| Comunicación | Solo resultado → principal | Task list + mensajes entre teammates |
| Coste | Bajo | Alto (N sesiones) |
| Úsalo para | Side-quests: investigar, explorar, verificar | Paralelismo real: revisión multi-capa, hipótesis en competencia |

Reglas prácticas: 3–5 teammates; **particionar ficheros** (cada teammate dueño de los suyos); contexto
completo en el prompt de arranque. Limitaciones hoy: sin `/resume` in-process, un team por sesión, sin
teams anidados.

**Puente a la Parte 2:** GSD (sección 9) empaqueta exactamente esto — `gsd-planner`, `gsd-executor`,
`gsd-verifier` son subagentes custom distribuidos como plugin (para proyectos multi-fase; **este proyecto
usa el flujo `data/changes/`, no GSD** — ver la aclaración en la sección 9).

🗣️ *"Subagente para que el ruido muera fuera de tu sesión; team para que varios Claudes debatan. El coste no es el mismo."*

---

## 7. Automatización

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

# PARTE 2 — La metodología (agnóstica de la herramienta)

## 8. La metodología

**Hilo:** Herramientas sin método = caos rápido. Esta es la parte más valiosa del curso: **cómo se
trabaja de verdad con un agente de coding en un proyecto en producción.** No es un flujo perfecto — es el
que usamos, sujeto a revisión constante. Y es **agnóstico**: se demuestra con Claude Code, pero la
disciplina viaja (sección 10). Todo el material está en
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
7. **Verificar** — unit + scoped + regresión + **gate outbound** (tres checks): reproducir el contrato en la
   **etapa real de salida** (el *wrapper* que reconstruye la salida, no una función interna), que el JSON
   local case, y verificarlo **dentro de la imagen desplegada** — los tests en verde no prueban lo que se envía.
8. **Documentar** — porqué + qué + handover + criterios de aceptación, cada cosa **una vez**.
9. **Sanitizar** — escanear las **líneas añadidas** por nombres/IDs/secretos/atribución del agente.
10. **Handoff** — el humano (o un tool suyo, p. ej. Cursor) hace push/PR/deploy. El agente **nunca**.
11. **Revisión automática + persistir** — triar hallazgos del bot como los de un humano; codificar lecciones.

> **¿Dónde está el coste? El agente es el orquestador — y es donde vive la inferencia.** Ninguna etapa es
> "gratis": las **herramientas** (`/kg`, `git`, parsers, `pytest`, `grep`) dan **hechos sin inferencia**, pero
> el agente **lee** esos hechos, **razona** y **decide** — y eso cuesta. El método no elimina el coste, lo
> **concentra**: barato en 1–3 y 9 (leer hechos + decidir), **caro en 5–6–7** (plan, código, verify), donde el
> modelo *piensa y crea*. Tabla coste-por-etapa: [`metodologia/WORKFLOW.md`](./ejemplos/metodologia/WORKFLOW.md).

### Un ejemplo real (ver [`metodologia/EJEMPLO_REAL.md`](./ejemplos/metodologia/EJEMPLO_REAL.md))
Bug: *"un campo sale vacío en la UI pero está en el PDF."* → Orientar (STATUS.md encuentra un
`SHARP_EDGES` que restringe el fix) → confirmar el vacío en el JSON del contrato (Playwright) →
pre-existente, no regresión → Serena+CodeGraph localizan el detector de fin de provisión, y un
`_diag_pdf.py` determinista revela la causa (desbordamiento a 2ª columna) **sin una sola llamada al LLM**
→ plan aprobado → test RED → fix keyed en la *propiedad estructural* (no en el cliente) → regresión
byte-idéntica (prueba no-op) + contrato reproducido en local (vía *wrapper*) y **dentro de la imagen
desplegada** → documentar → sanitizar → el humano hace el push. Un review-bot detecta un caso de columna a la izquierda → se añade el test y va al `PLAYBOOK`.

🗣️ *"El agente orquesta y es donde vive la inferencia; lo caro se concentra en plan/código/verify, no en buscar."*

---

## 9. Las herramientas del método

**Hilo:** El flujo dice *qué* hacer; esta sección dice **con qué tool y en qué orden** — y qué hace cada
una. La regla vive en el `CLAUDE.md` del proyecto: no basta con "tener MCP instalado", el agente debe
tirar de la tool correcta **automáticamente**. Detalle:
[`metodologia/herramientas.md`](./ejemplos/metodologia/herramientas.md).

### La prevalencia: barato → caro, determinista → probabilístico

Regla real (actualizada): *"para 'qué es esto / quién depende / qué toco', un `codegraph_explore`
**primero** — fuente + rutas de llamada + blast radius + flags de cobertura de tests en una sola llamada
(trata la fuente que devuelve como YA leída, no la re-abras); Serena `find_referencing_symbols` para el
chequeo **preciso** antes de renombrar/borrar; grep/Read solo para literales."*

| Etapa del flujo | Herramienta |
|---|---|
| Orientar (1) | `/kg` (grafo de tickets — **graphify**, Parte 3) · `STATUS.md`/ledgers · `git` · `gh` (sin inferencia) |
| Navegar / investigar (4) | **CodeGraph** `codegraph_explore` — fuente + rutas + blast radius + cobertura, en 1 llamada |
| Refactor-check preciso (4-6) | **Serena** `find_referencing_symbols` — desambigua por clase; **obligatorio** antes de renombrar/borrar |
| Diagnosticar (4) | **Oráculo determinista** (parser, validador, `_diag_*.py`) — sin inferencia, reproducible |
| Entorno: logs, config (4) | **AWS CLI** — herramienta de debugging de primera clase (read-only) |
| Contrato de salida (2, 7) | **Playwright** / F12 sobre el endpoint que ve el consumidor |
| Verificar lo desplegado (7) | **Docker** — repro dentro de la imagen del runtime; los tests en verde ≠ lo enviado |
| Solo al final (7) | La tirada del **LLM** — para *verificar* el fix, no para diagnosticar |

> **"Sin inferencia" ≠ "gratis".** Estas etapas no disparan la **tirada del modelo** (el recurso caro y no
> determinista), pero Claude sí lee su output — un coste **menor y dirigido**, como el de un `grep`, no cero.
> El razonamiento caro se paga **una vez** al construir el grafo / el oráculo y se **amortiza** en cada uso
> (el ROI: sin inferencia por consulta, resultados deterministas y reproducibles, ahorro de tiempo y dinero).

### Qué es cada herramienta (una frase cada una, luego slide propia para las tres grandes)

- **CodeGraph** ([`ejemplos/codegraph/`](./ejemplos/codegraph/)) — índice tree-sitter→SQLite **local, sin
  API keys**; una consulta (`codegraph_explore`) devuelve fuente + rutas de llamada + blast radius +
  **flags de cobertura de tests** (58% menos tool calls en sus benchmarks). Es el **primer** tool de
  navegación; el proyecto por defecto se fija con `--path` en la config MCP (o se pasa `projectPath` para
  otro repo — ya indexamos también `monolith` y `frontend`). Fases: **investigar/navegar**.
- **Serena** ([`ejemplos/serena/`](./ejemplos/serena/)) — navegación **semántica vía LSP**: símbolos, no
  texto. `find_referencing_symbols` desambigua métodos homónimos por clase — el chequeo **preciso** que el
  `impact` plano de CodeGraph no da. Complementarios, no rivales. Fases: **investigar → implementar**
  (pre-rename/borrado).
- **GSD** ([`ejemplos/gsd/`](./ejemplos/gsd/)) — el método **hecho tooling**: ciclo *discutir → planificar
  → ejecutar → verificar* con estado en `.planning/` y subagentes (`gsd-planner`, `gsd-plan-checker`,
  `gsd-executor`, `gsd-verifier`…), que automatizan las fases **plan (5) → implementar (6) → verificar (7)**.
  **Honestidad — este proyecto NO usa GSD:** corre el flujo de 11 etapas + `data/changes/`, **más depurado y
  enfocado** a nuestro trabajo (fixes por ticket sobre un servicio en producción). GSD tiene más sentido en
  **otro tipo de proyecto** —un *greenfield* multi-componente (diseñar una aplicación entera, roadmap → fases)—;
  aquí lo mostramos como la misma disciplina **productizada** y como ejemplo vivo de la Parte 1 (subagentes
  custom + skills como plugin).
- **Playwright** — reproduce el síntoma donde lo ve el consumidor (fases **triaje y gate outbound**).
- **Context7** — docs de librerías al día, en vez del corte de entrenamiento (fase **investigar**).
- **Oráculos deterministas propios** (`_diag_*.py`) — la respuesta barata y reproducible antes de gastar
  la tirada del LLM (fase **investigar**). **No son skills ni tools MCP:** son **código suelto** que el agente
  teclea y corre con Bash, gitignored bajo `data/changes/<ticket>/` (frente a `/kg`/Serena/CodeGraph, que sí
  son capacidades registradas). Detalle: [`metodologia/herramientas.md`](./ejemplos/metodologia/herramientas.md).

🗣️ *"La inversión clásica — tirar del modelo para diagnosticar — es justo lo que este orden evita: el modelo verifica; los oráculos diagnostican."*

---

## 10. Transferir la metodología

**Hilo:** La prueba de que la Parte 2 es **agnóstica**: el método está empaquetado como un *starter-kit*
y transferido de verdad a **GitHub Copilot** en otro repo. Material real:
[`docs/ai-agents-code-methodology/`](./docs/ai-agents-code-methodology/) (guía de adaptación, plantillas,
bootstrap).

### Qué viaja sin cambios (las 5 reglas que hay que conservar)
1. Plan → acuerdo → implementar.
2. Verificar en el **contrato visible por el consumidor**, no en funciones internas.
3. Resolver la **clase general** del problema, no un input de muestra.
4. Rastro durable de decisiones (porqué, qué cambió, cómo se verificó).
5. El humano posee las acciones externas irreversibles (merge, deploy, comunicación).

### Qué se re-mapea por repo
El **contrato** (payload HTTP / fila de DB / evento / artefacto), el **tracker** (Jira/Azure
Boards/Issues), la **pirámide de tests**, el **runtime** desplegado (container/VM/serverless), y las
reglas de **sanitización** locales.

### Qué se sustituye (las tools son fungibles; la disciplina no)
Serena/CodeGraph/`/kg` son *implementaciones*. Sin grafo de tickets hay un **fallback determinista
documentado**: `STATUS.md` newest-first + carpetas por ticket + búsqueda léxica por síntoma + historia de
commits como sustituto ligero del grafo + una sección de "danger zones". El 80% del valor con setup mínimo.

### El kit (ver [`TRANSFER_AND_BOOTSTRAP.md`](./docs/ai-agents-code-methodology/TRANSFER_AND_BOOTSTRAP.md))
Plantillas de `STATUS`/`SHARP_EDGES`/`HANDOVER`/`QA_ACCEPTANCE`/working-agreement + un script
`bootstrap-new-repo.ps1` que crea la estructura en el repo destino. El modelo operativo con Copilot es el
mismo flujo con gates: cargar orientación → triaje en el contrato → probes deterministas → plan gate →
TDD gate → outbound gate → handover. Checklist de primer día: rellenar `STATUS.md`, 3-5 invariantes
iniciales, definir el contrato, comandos de test scoped, y **un issue completo con RED → GREEN + contrato**.

🗣️ *"Si solo conservas cinco reglas, conserva esas cinco. Las tools se sustituyen; la disciplina viaja."*

---

## 11. Sincronización de máquinas

**Hilo:** Los mismos principios de la metodología aplicados a **ops**: mover el workspace entre la máquina
principal y el portátil con un runbook real (ver
[`metodologia/machine-sync.md`](./ejemplos/metodologia/machine-sync.md)). Demuestra que la metodología no
es solo para código:

- **Sincronización asimétrica:** outbound = **copia completa** (un tarball: workspace + `~/.claude`/`.aws`/
  `.ssh`, con `-h` para dereferenciar symlinks, excluyendo venvs/node_modules); inbound = **solo delta**
  (el código ya está en GitHub → `git fetch`; solo los docs gitignored de `data/`, unos MB, viajan).
- **Copiar al USB tiene gotchas reales:** WSL no auto-monta un USB conectado tras arrancar
  (`sudo mount -t drvfs F: /mnt/f`); y la copia se **verifica byte a byte** (`stat -c %s` en origen y destino
  coinciden) antes de expulsar — evidencia, no "parece que cabe". El bundle **crece** (~0.9→~1.5 GB); el USB
  al alza.
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
- **Bring-up y memoria, con subcomandos idempotentes:** en un portátil nuevo, `kg_refresh.sh bootstrap`
  instala lo que no va en el bundle y verifica `/kg`; y como la memoria (`~/.claude`) **no** viaja en el delta,
  `snapshot-memory` la parquea bajo `data/` para que viaje y `restore-memory` la fusiona de vuelta (con backup)
  antes de `/kg-refresh`. Un `LAPTOP_START_HERE.md` es el punto de entrada único para el agente del portátil.

🗣️ *"La metodología no es solo para código: memoria durable, guardrails y 'el humano hace lo externo' también en ops."*

---

# PARTE 3 — El grafo de conocimiento de tickets (graphify)

## 12. El grafo de conocimiento de tickets

**Hilo:** Un caso completo, de la idea al tooling en producción. Si CodeGraph indexa el *código*, este
grafo indexa la **memoria del proyecto** — writeups por ticket, "sharp edges", runbooks, notas de memoria —
y responde *"¿qué se rompió antes cerca de aquí?"* en una llamada, **sin LLM**. La tecnología que lo
construye es **graphify** (no CodeGraph — CodeGraph es solo la *analogía*: mismo rol, otro dominio, otra
herramienta). Todo el material real está en [`docs/knowledge-graph/`](./docs/knowledge-graph/): diseño,
scripts, tests, manifest y la salida real ([`output/graph.html`](./docs/knowledge-graph/output/graph.html)).

### 12a. El problema y el diseño (ver [`docs/knowledge-graph/design.md`](./docs/knowledge-graph/design.md))

En un repo con **~540 ficheros** de writeups, un bug "nuevo" casi siempre tiene contexto previo que
restringe el fix: un invariante, un ticket que arregló algo parecido, una regresión documentada.
Encontrarlo a mano = recordar que existe + grep. El grafo lo hace **explícito y consultable**.

- **Corpus curado, no un glob:** un [`manifest.txt`](./docs/knowledge-graph/manifest.txt) **diffeable**
  enumera exactamente qué entra (~116 ficheros, ~196k palabras): writeups `sst-*` (con fallback
  determinista para carpetas sin doc primario), hubs (`STATUS`, `SHARP_EDGES`, `PLAYBOOK`…), estado de
  extractores, runbooks de ops y la memoria de `~/.claude`.
- **Exclusiones duras:** binarios, handovers que repiten el ticket, QA repetitivo y — crítico — las
  **copias stale** de un tarball de viaje (`payload/`): incluirlas crearía nodos duplicados/conflictivos.
  *Densidad sin conocimiento nuevo = ruido.*
- **Fase 1 fue un spike con decisión al final** (keep/extend/replace): validar si `graphify`
  off-the-shelf bastaba antes de invertir en extracción custom. Bastó — y se quedó.

### 12b. El pipeline y los comandos creados en Claude Code

Dos **skills** (`/kg`, `/kg-refresh`) + dos **scripts** deterministas
([`kg_query.sh`](./docs/knowledge-graph/kg_query.sh), [`kg_refresh.sh`](./docs/knowledge-graph/kg_refresh.sh))
+ dos utilidades de corpus (`build_manifest.py`, `stage_corpus.py`) + **tests** (`test_kg_*.py`):

```
kg_refresh.sh prepare   # build_manifest -> stage _corpus/ (nombres con provenance:
                        #   sst-5468__sst-5468.md, hub__STATUS.md, memory__x.md)
                        #   -> copiar a un SCRATCH FUERA del repo
/graphify <scratch>     # el único paso con LLM (subagentes en paralelo): extracción
                        #   de nodos/aristas + clustering -> HTML/JSON/reporte
kg_refresh.sh finalize  # copiar artefactos a output/ + leak-check (nada fuera de data/)
```

- **El gotcha que lo sostiene:** `graphify` respeta `.gitignore` y todo `data/` lo está → correr el
  detector in situ encuentra **0 ficheros**. Por eso el corpus se monta en un scratch fuera del repo.
- **Por eso `/kg-refresh` es un skill y no un script:** el paso semántico (`/graphify`) es un paso de
  Claude; los bookends (`prepare`/`finalize`) son deterministas y testeados.
- **¿Comando o skill? Skill, aunque se invoque con `/`:** lleva assets (los wrappers), tiene `description`
  para que Claude la auto-seleccione al orientar, y orquesta un paso del modelo. Las `SKILL.md` viven **a
  nivel de usuario** (`~/.claude/skills/kg/`, `kg-refresh/`, `graphify/`), fuera del repo — por
  confidencialidad (nada del KG en rutas committeables) y por alcance (disponible en toda la máquina).
  Viajan entre máquinas dentro del tarball de `~/.claude` (sección 11).
- Subcomandos extra para el viaje entre máquinas: `bootstrap` (portátil nuevo), `snapshot-memory` /
  `restore-memory` (la memoria no viaja en el delta — se parquea bajo `data/` y se fusiona de vuelta).

### 12c. La salida real (ver [`output/GRAPH_REPORT.md`](./docs/knowledge-graph/output/GRAPH_REPORT.md) y la slide con la visualización)

El grafo real del proyecto (capturado de `output/graph.html`, un vis-network interactivo con búsqueda,
panel de nodo y filtro por comunidad):

- **507 nodos · 672 aristas · 35 comunidades** sobre 116 ficheros (~196k palabras).
- **92% de aristas `EXTRACTED`** (citas literales, fiables) · 7% `INFERRED` (similitud semántica,
  confianza media 0.7 — pistas a verificar, no hechos).
- Las **comunidades mapean a zonas de peligro reales**: "Letter-End & Run-in Titles", "Title Detection
  Failures", "Comment-Memo Boundaries", "PDF Extractor Cascade"… — exactamente los clústers que un
  ingeniero senior tiene en la cabeza.
- Los **god-nodes** (nodos más conectados) son los tickets estructurales del proyecto — el top-10 del
  reporte es una lista de onboarding gratis.
- El reporte incluye **"surprising connections"**: pares de lecciones semánticamente gemelas que nadie
  había conectado a mano.

### 12d. Cómo se usa y dónde se engancha

```bash
/kg <ticket|tema>     # vecinos de un nodo   (graphify explain)  ← el uso más común
/kg <A> <B>           # camino más corto A<->B (graphify path)
/kg find <substr>     # descubrir el nombre exacto de un nodo
/kg-refresh           # reconstruir tras nuevos tickets (barato, re-runnable)
```

Matching difuso: `SST-1234`, `get_letter_end`, `"letter-end"` resuelven. **Determinista, sin LLM en la
consulta**: `kg_query.sh` lee `output/graph.json` directamente. Ejemplo real: para un fix de
fin-de-carta, `/kg get_letter_end` devuelve al instante la zona de peligro completa — los 5-6 tickets que
comparten ese código.

> **"Sin LLM en la consulta" no es "gratis" — es coste menor y amortizado.** La inferencia cara (la extracción
> con subagentes) se paga **una sola vez** en `/kg-refresh`; cada `/kg` es luego un algoritmo determinista
> sobre `graph.json` → **cero inferencia**. El único coste es que Claude lee un output pequeño (como un `grep`):
> menor y dirigido, no cero. Así, construir el grafo es una **inversión** que se amortiza: sin inferencia por
> consulta, resultados **deterministas y reproducibles** (mejor resultado), y ahorro de tiempo y dinero por
> tarea. 🗣️ *"El grafo no es un gasto: razonar una vez, recuperar mil."*

**Dónde se engancha:** en la **etapa 1 (Orientar)** de la metodología — la regla *history-first* del
`CLAUDE.md` dice **corre `/kg <ticket|tema>` antes de hacer grep** en `data/changes/`. El grafo apunta a
*qué leer*, no lo sustituye. Y es un **artefacto derivado**: nunca viaja entre máquinas; se reconstruye
donde esté el corpus (sección 11). Confidencialidad: los nodos llevan nombres internos → el árbol
completo vive bajo `data/` gitignored; compartirlo fuera exigiría una pasada de sanitización aparte.

🗣️ *"Un paso semántico en el build, cero LLM en la consulta. El grafo es el mapa; el agente, el guía."*

---

## 13. Cierre

**Parte 1 — la herramienta:** instalar es trivial; el valor está en **cómo** lo usas. Las capas:
**instalar → memoria/sesiones → contexto & caching → MCP → skills/plugins → subagents/teams →
automatización.** El context window es el presupuesto; hooks y permisos son las garantías.

**Parte 2 — el método:** un agente potente sin método es caos rápido. El flujo de 11 etapas canaliza la
potencia por **gates deterministas**; las tools (CodeGraph, Serena, los oráculos) encarnan la prevalencia
barato→caro — con GSD como la versión **productizada** del método —; y la disciplina **viaja** — a otro
repo, a otro agente, incluso a ops.

**Parte 3 — el grafo de tickets:** el caso completo que une las dos partes — skills y subagentes de
Claude Code (Parte 1) al servicio del paso *history-first* de la metodología (Parte 2), construido con
**graphify**: 507 nodos, 672 aristas, 35 comunidades que mapean a zonas de peligro reales.

**El salto de nivel:** de "chatear con un asistente" a **un sistema**: hooks que garantizan calidad, MCP
que conecta tu mundo, subagentes que escalan el trabajo, y una metodología que trata al agente como
colaborador con gates de evidencia.

**Referencias:** documentación oficial <https://code.claude.com/docs> · GSD
<https://github.com/tomascortereal/claude-code-setup> · CodeGraph <https://colbymchenry.github.io/codegraph/> ·
Serena <https://github.com/oraios/serena>.
