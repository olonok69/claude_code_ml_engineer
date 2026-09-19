# Claude Code — Guía técnica de implementación (curso en dos partes)

> Referencia copy-paste para montar cada pieza. Complementa a [`GUIA_PRESENTACION.md`](./GUIA_PRESENTACION.md)
> (el hilo narrativo) con el **cómo**. Todos los artefactos ejecutables están en [`ejemplos/`](./ejemplos/);
> [`docs/`](./docs/) es referencia de una instalación real.

## Índice

**Parte 1 — Claude Code**

1. [Instalación y CLI](#1-instalación-y-cli)
2. [Memoria: CLAUDE.md, jerarquía y auto-memory](#2-memoria)
3. [Settings y permisos](#3-settings-y-permisos)
4. [Sesiones entre superficies](#4-sesiones)
5. [Context window](#5-context-window)
6. [Prompt caching](#6-prompt-caching)
7. [MCP](#7-mcp)
8. [Slash commands, skills y plugins](#8-slash-commands-skills-y-plugins)
9. [Subagents y Agent Teams](#9-subagents-y-agent-teams)
10. [Hooks](#10-hooks)
11. [Automatización: headless, CI, scheduling, SDK](#11-automatización)

**Parte 2 — La metodología**

12. [El flujo y el ejemplo real](#12-metodología)
13. [Las herramientas: CodeGraph, Serena, GSD](#13-herramientas-del-método)
14. [Transferir la metodología (starter-kit / Copilot)](#14-transferir-la-metodología)
15. [Sincronización de máquinas](#15-sincronización-de-máquinas)

**Parte 3 — El grafo de conocimiento de tickets (graphify)**

16. [Grafo de conocimiento de tickets](#16-grafo-de-conocimiento-de-tickets)

---

# PARTE 1 — Claude Code

## 1. Instalación y CLI

```bash
# Instalar (elige uno)
curl -fsSL https://claude.ai/install.sh | bash          # macOS/Linux/WSL (auto-update)
brew install --cask claude-code                          # Homebrew (brew upgrade para actualizar)
winget install Anthropic.ClaudeCode                      # Windows

# Arrancar
cd tu-proyecto && claude

# Headless (un prompt, stdout)
claude -p "resume los cambios de esta rama"

# Flags útiles
claude --teleport            # traer una sesión web/móvil al terminal
claude --continue            # continuar la última sesión
claude -p "…" --output-format json   # salida estructurada para scripts
```
Comandos dentro de la sesión: `/help`, `/mcp`, `/plugin`, `/schedule`, `/loop`, `/desktop`, `/config`,
`/context`, `/compact`, `/clear`, `/rewind`, `/agents`.
Ver la referencia completa de CLI en la doc oficial (`/en/cli-reference`).

---

## 2. Memoria

### Jerarquía de `CLAUDE.md` (se combinan por precedencia)
```
~/.claude/CLAUDE.md          # global del usuario (todos tus proyectos)
<repo>/CLAUDE.md             # raíz del repo (compartido, versionado)
<repo>/<subdir>/CLAUDE.md    # se carga al entrar en esa subcarpeta
<repo>/CLAUDE.local.md       # personal, NO versionado
```
Sintaxis `@ruta/fichero` dentro de un CLAUDE.md importa otro doc al cargarlo
(ejemplo: [`ejemplos/context/CLAUDE.import-example.md`](./ejemplos/context/CLAUDE.import-example.md)).

### Patrón de dos niveles (ver [`ejemplos/claude-md/`](./ejemplos/claude-md/))
- **Nivel 1** = el `CLAUDE.md` siempre cargado: orientación + punteros de una línea. Pequeño.
- **Nivel 2** = ficheros bajo `data/changes/` (`STATUS.md`, `PLAYBOOK.md`, `SHARP_EDGES.md`,
  `TEST_MAP.md`, `CONVENTIONS.md`, `TICKETS.md`, `FOLLOWUPS.md`, `<TICKET>/<TICKET>.md`) que se leen
  bajo demanda.
- **Regla write-once:** cada dato en un único ledger canónico; el core lleva el puntero, no la copia.
- **Nivel 0 (machine-local):** `IDENTITY.md` — qué máquina es esta y qué rol tiene (`publisher` /
  `contributor`) en el registro compartido (§15B). Gitignored, nunca sincronizado: es el único fichero
  que **no** debe ser igual en todas partes.

> **El índice también se queda obsoleto.** Sacar contenido del fichero always-loaded a un fichero
> bajo demanda **no lo actualiza** — hereda la obsolescencia del original y encima *parece* recién
> escrito. Caso real: una lista de 28 entradas ticket→test se movió a `TEST_MAP.md` y el check de
> verificación afirmaba "el fichero tiene 28 entradas". Tenía exactamente 28 — y 28 era el número
> equivocado: en `tests/` había **80** ficheros y la lista se había parado ~40 tickets antes. El
> recuento no podía fallar porque se derivaba de la misma fuente obsoleta que estaba comprobando.
> Verifica una lista movida **contra lo que describe** (el filesystem, el código), nunca contra su
> propia versión anterior.

### Auto-memory
Claude persiste aprendizajes (comandos de build, pistas de debug) entre sesiones automáticamente. No
requiere que escribas nada; se acumula en el store de memoria del proyecto (las primeras ~200 líneas se
cargan al inicio — también cuenta contra el contexto, ver §5).

---

## 3. Settings y permisos

`.claude/settings.json` (compartido) y `.claude/settings.local.json` (personal). El bloque clave es
`permissions`, un **allowlist específico** (no comodines):

```json
{
  "permissions": {
    "allow": [
      "Bash(.venv/bin/pytest tests/ -q)",
      "Bash(git status)",
      "Bash(git diff:*)",
      "mcp__serena__find_symbol",
      "mcp__playwright__browser_navigate",
      "WebSearch",
      "WebFetch"
    ],
    "deny": [],
    "ask": []
  }
}
```
Postura recomendada: reglas concretas (invocaciones exactas), no `Bash(*)`. El humano es dueño de las
acciones externas (push/PR/deploy) → esas no van en `allow`.

### Dónde "viven" las tools — y las cuatro capas que las gobiernan

Las tools built-in (`Read`, `Edit`, `Bash`, `Grep`, `Glob`, `Task`, `WebFetch`, `WebSearch`…) **van
compiladas en el binario** y se envían como schemas en cada request (el nivel `Tools` del prefijo de
caching, §6). No hay carpeta de tools editable: solo se *añaden* tools vía **MCP** (`mcp__<server>__<tool>`)
o vía plugins. Lo que se gestiona no son las tools sino el **acceso**, en cuatro capas:

1. **Permisos** — el bloque `permissions` de arriba (+ el comando `/permissions` en sesión). Precedencia:
   política gestionada de empresa → flags de CLI → `settings.local.json` → `settings.json` del proyecto →
   `~/.claude/settings.json`. Una built-in también se puede *vetar*: `deny: ["WebSearch"]` la desactiva.
2. **Flags de CLI** — `--allowedTools` / `--disallowedTools` por invocación (típico en headless/CI);
   en el Agent SDK, `options.allowedTools`.
3. **Hooks** — un `PreToolUse` con `exit 2` veta por *contenido* del `tool_input` (§10), cosa que el
   allowlist estático no puede.
4. **Por agente** — el frontmatter `tools:` de un subagente custom restringe lo que ese agente hereda (§9).

> Las tools MCP usan carga *deferred*: al contexto va un índice ligero (~120 tokens) y el schema completo
> se carga al usar la tool (§5). Regla-resumen: **las built-in vienen con el binario y las MCP con tus
> servers; tú no editas tools — editas permisos.**

---

## 4. Sesiones

| Necesito… | Herramienta |
|---|---|
| Continuar una sesión local desde el móvil | **Remote Control** (`/en/remote-control`) |
| Empezar en web/móvil y traerla al terminal | `claude --teleport` |
| Pasar del terminal al Desktop (diffs visuales) | `/desktop` (ver caveat abajo) |
| Empujar eventos externos (Telegram/Discord/webhooks) a una sesión | **Channels** |
| Ruta de bug desde Slack a un PR | integración **Slack** (`@Claude`) |

El mismo motor y los mismos `CLAUDE.md`/settings/MCP funcionan en todas.

> ⚠️ **Caveat de `/desktop` (plataforma):** solo está disponible en la CLI de **macOS y Windows** con
> suscripción Claude (no con API key, ni en Bedrock/Vertex/Foundry). Si ejecutas la CLI **dentro de WSL**,
> Claude Code la trata como **Linux** y el comando **no se ofrece** — aunque la app de Desktop esté
> instalada en Windows, porque el handoff no cruza la frontera WSL↔Windows. Alternativa: abre el proyecto
> directamente en la app de Desktop (pestaña *Code*). `claude --teleport` y Remote Control **sí** funcionan
> desde WSL. (Nota relacionada: `claude mcp add-from-claude-desktop` sí opera en macOS y WSL.)

---

## 5. Context window

Referencia completa: [`ejemplos/context/`](./ejemplos/context/). Los números y comandos:

**Qué carga la sesión antes de tu primer prompt:** system prompt ~4.200 tokens · auto-memory ~680
(primeras 200 líneas / 25 KB) · entorno ~280 · índice de tools MCP ~120 en modo *deferred* (el schema
completo de cada tool se carga al usarla) · tu jerarquía de `CLAUDE.md`. Ventana: 200K tokens en los
modelos actuales (1M en beta vía API).

```text
/context                      # desglose de uso por bloque — mide antes de optimizar
/compact céntrate en los cambios de la API y los ficheros modificados
/clear                        # reset total entre tareas no relacionadas
/rewind                       # (Esc+Esc) checkpoints: conversación, código o ambos
```

- Auto-compact salta cerca del límite; es **lossy** → mejor `/compact <foco>` manual y anticipado.
- `/rewind` restaura **solo ediciones de Claude** (no cambios de Bash/externos — no sustituye a git).
- MCP: cada server suma contexto → desactiva los que el proyecto no use (`.claude/settings.json`).
- Investigación ruidosa → subagentes (§9): el ruido muere fuera; vuelve el resumen.
- CLAUDE.md: regla de la doc oficial — *si puedes borrarlo sin que Claude se equivoque, bórralo*.

---

## 6. Prompt caching

Referencia y demo ejecutable: [`ejemplos/prompt-caching/`](./ejemplos/prompt-caching/)
([`cache_demo.py`](./ejemplos/prompt-caching/cache_demo.py)).

**Mecánica (API):** se cachea un **prefijo contiguo** hasta un breakpoint `cache_control`; jerarquía
estricta `Tools → System → Messages` (un cambio invalida su nivel y los siguientes).

| | Escritura | Lectura |
|---|---|---|
| TTL 5 min (defecto) | 1.25× input | **0.1×** input |
| TTL 1 h (`"ttl": "1h"`) | 2× input | **0.1×** input |

```python
system=[{ "type": "text", "text": STABLE_INSTRUCTIONS,
          "cache_control": {"type": "ephemeral"} }]   # breakpoint AL FINAL de lo estable
messages=[{"role": "user", "content": query}]          # lo variable, DESPUÉS (fuera del cache)
```

Diagnóstico en `response.usage`: `cache_creation_input_tokens` / `cache_read_input_tokens`.
Mínimo cacheable ~1.024 tokens (4.096 en Haiku); máx. 4 breakpoints explícitos.

**En Claude Code** el caching es automático (system + tools + historial = prefijo estable). Lo que tú
controlas: no editar `CLAUDE.md`/settings a mitad de sesión (invalida el cache), pocos MCP (bloque de
tools estable), y saber que `/compact` reescribe el historial (rompe el cache de mensajes una vez).

**TTL en Claude Code:** por defecto **1 h con suscripción** (incluido en el plan) y **5 min con API
key**/Bedrock/Vertex. Se cambia por env var (shell o bloque `env` de `settings.json`):
`ENABLE_PROMPT_CACHING_1H=1` (1h con API key) · `FORCE_PROMPT_CACHING_5M=1` (forzar 5 min) ·
`DISABLE_PROMPT_CACHING=1` (apagarlo; también por modelo `DISABLE_PROMPT_CACHING_SONNET/_OPUS/_HAIKU`).
Cada lectura renueva la ventana → con suscripción, pausas de hasta 1 h entre turnos siguen acertando.
Doc: `code.claude.com/docs/en/prompt-caching`.

---

## 7. MCP

Ver [`ejemplos/mcp/.mcp.json`](./ejemplos/mcp/.mcp.json). Scopes: **local** (`settings.local.json`),
**project** (`.mcp.json` versionado), **user** (`~/.claude.json`).

```bash
# stdio (proceso local)
claude mcp add serena -- uvx --from git+https://github.com/oraios/serena serena start-mcp-server
# HTTP remoto
claude mcp add --transport http context7 https://mcp.context7.com/mcp
claude mcp list
```
```jsonc
// .mcp.json — secreto por variable de entorno, NUNCA hardcodeado
{ "mcpServers": { "supabase": {
    "command": "npx", "args": ["-y", "@supabase/mcp-server-supabase@latest"],
    "env": { "SUPABASE_ACCESS_TOKEN": "${SUPABASE_ACCESS_TOKEN}" } } } }
```
Las tools aparecen como `mcp__<server>__<tool>` y se permiten/deniegan en el allowlist.

> **La config da la capacidad; el CLAUDE.md da el criterio.** Los MCP servers **no** se instalan en el
> `CLAUDE.md` — ese fichero es solo prompt, no configuración. Se instalan en los scopes de arriba (o los
> trae un plugin). Pero instalar Serena solo hace que *exista* `mcp__serena__find_symbol`; que el agente
> **tire de ella sin pedirlo** lo consigue el CLAUDE.md (global o de repo) con un *trigger map*: "Serena
> ANTES de leer ficheros enteros; `find_referencing_symbols` SIEMPRE antes de un rename". Es la regla de
> prevalencia de [`metodologia/herramientas.md`](./ejemplos/metodologia/herramientas.md) — la config
> convierte "no tengo la tool" en "la tengo"; el CLAUDE.md convierte "la tengo" en "se usa en el orden
> correcto". (Ojo al trade-off de §5: ese trigger map se carga en cada sesión — mantenlo estable y con
> punteros para que cachee bien.)

---

## 8. Slash commands, skills y plugins

**Slash command** — `.claude/commands/audit.md`:
```markdown
---
description: Audita dependencias y verifica tests
---
Ejecuta `npm audit`, luego `npm audit fix`, luego los tests. Resume el resultado.
```
Se invoca con `/audit`. Ver [`ejemplos/skills-plugins/`](./ejemplos/skills-plugins/).

**Skill** — `.claude/skills/<n>/SKILL.md` con frontmatter `name` + `description` (la `description` guía la
auto-selección). Puede llevar scripts/plantillas en su carpeta.

**Plugins:**
```bash
/plugin marketplace add <owner/repo>
/plugin install <plugin>
/plugin                 # gestionar
```

### La diferencia, resumida

| | **Slash command** | **Skill** | **Plugin** |
|---|---|---|---|
| **Qué es** | Prompt guardado | Capacidad repetible con instrucciones + assets | Paquete distribuible |
| **Fichero / ubicación** | `.claude/commands/<n>.md` (o `~/.claude/commands`) | `.claude/skills/<n>/SKILL.md` + carpeta con scripts/plantillas/refs | Instalado en `~/.claude/plugins` desde un marketplace |
| **Invocación** | Manual: `/<n>` (la haces tú) | **Model-invoked**: Claude la elige por su `description` | Instala su contenido; no se invoca como tal |
| **Empaqueta** | Un prompt (`$ARGUMENTS`) | Instrucciones + código/plantillas/referencias | skills + commands + agents + MCP + hooks |
| **Distribución** | Copiar el `.md` | Copiar la carpeta, o dentro de un plugin | `/plugin marketplace add <owner/repo>` → `/plugin install <x>` |

Regla mnemotécnica: **command = lo disparas tú** · **skill = lo decide Claude** (por la descripción) ·
**plugin = el vehículo de reparto** (versionado) de comandos, skills, agentes, MCP y hooks. Ejemplos reales
de plugins instalados así: `serena`, `context7`, `playwright`, y GSD (que trae decenas de skills `gsd-*`).
Más detalle y ejemplos en [`ejemplos/skills-plugins/`](./ejemplos/skills-plugins/).

⚠️ **La razón más fuerte para hacer una skill no es la comodidad: es que se cumpla.** Una regla que solo vive en un runbook se degrada en silencio, y nadie ve la degradación. La skill `day` de esa carpeta existe porque "pull al empezar, push al terminar" estuvo en nuestro documento de operaciones **meses sin cumplirse**; empaquetarla como rutina invocable la ejecuta y además deja el rastro que hace visible el incumplimiento. Ver §15B.

---

## 9. Subagents y Agent Teams

Referencia completa + diagrama: [`ejemplos/subagents/`](./ejemplos/subagents/).

**Built-ins (tool `Task`):** `Explore` (read-only), `Plan`, `general-purpose`. Lánzalos en paralelo para
trabajo independiente; a tu sesión vuelve solo el resumen.

**Custom** — `.claude/agents/<nombre>.md` (proyecto, versionado) o `~/.claude/agents/` (usuario);
`/agents` los lista:
```yaml
---
name: security-reviewer
description: Revisa código en busca de vulnerabilidades. Úsalo tras cambios en auth o deps.
tools: Read, Grep, Glob, Bash      # allowlist por agente (omitir = todos)
model: opus                         # override opcional
---
Eres un ingeniero de seguridad senior. Reporta hallazgos con fichero:línea y severidad…
```
Ejemplos reales: [`security-reviewer`](./ejemplos/subagents/.claude/agents/security-reviewer.md) ·
[`refactor-scout`](./ejemplos/subagents/.claude/agents/refactor-scout.md) (codifica la regla
CodeGraph→Serena de la Parte 2). **Gotcha:** el subagente no hereda tu conversación — contexto en el
prompt de lanzamiento. Corren en background por defecto.

**Agent Teams (experimental):**
```jsonc
// ~/.claude/settings.json
{ "env": { "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1" },
  "teammateMode": "in-process" }    // o "auto" | "tmux" | "iterm2"
```
Lead + teammates (cada uno una **sesión completa**), task list compartida (`~/.claude/tasks/<team>/`),
inboxes para mensajería directa. Se pide en lenguaje natural (*"monta un equipo con un architect y dos
implementers; exige aprobación de plan"*); los roles reutilizan tus subagentes custom. Limitaciones: sin
`/resume` in-process, un team por sesión, sin anidar; split-panes requiere tmux/iTerm2. Coste: cada
teammate es una sesión — para side-quests usa subagentes.

---

## 10. Hooks

Todo en [`ejemplos/hooks/`](./ejemplos/hooks/). Config en `.claude/settings.json`:

```json
{ "hooks": {
  "PreToolUse": [
    { "matcher": "Read|Grep", "hooks": [{ "type": "command", "command": "node ./hooks/read_hook.js" }] },
    { "matcher": "Write|Edit|MultiEdit", "hooks": [{ "type": "command", "command": "node ./hooks/query_hook.js", "timeout": 300 }] }
  ],
  "PostToolUse": [
    { "matcher": "Write|Edit|MultiEdit", "hooks": [
      { "type": "command", "command": "node ./hooks/format_hook.js" },
      { "type": "command", "command": "node ./hooks/tsc.js" } ] }
  ] } }
```

**Contrato:** payload por stdin · `exit 0` permite · **`exit 2` bloquea** y devuelve `stderr` a Claude.
Pre → `tool_input` (intención); Post → `tool_response` (resultado + `structuredPatch`). Payloads reales:
[`pre-log.json`](./ejemplos/hooks/pre-log.json), [`post-log.json`](./ejemplos/hooks/post-log.json).

**Patrón de bloqueo (JS):**
```js
if (payload.tool_input?.file_path?.includes(".env")) {
  console.error("Bloqueado: no leas .env");
  process.exit(2);   // <-- veto
}
process.exit(0);
```

Eventos disponibles: `PreToolUse`, `PostToolUse`, `UserPromptSubmit`, `SessionStart`, `Stop`,
`Notification`. Distribución portable: `settings.example.json` con token `$PWD` + `init-claude.js` que lo
sustituye por `process.cwd()` en `npm run setup`.

---

## 11. Automatización

Ver [`ejemplos/automation/`](./ejemplos/automation/).

**Headless / piping:**
```bash
tail -200 app.log | claude -p "avísame de anomalías"
git diff main --name-only | claude -p "revisa por seguridad"
```

**CI (GitHub Actions):** ver [`github-action-claude.yml`](./ejemplos/automation/github-action-claude.yml).
Instala Claude, exporta `ANTHROPIC_API_KEY` (secreto), y usa `claude -p` sobre el diff del PR.

**Scheduling:** `Routines`/`/schedule` (infra de Anthropic, disparable por API/GitHub) · Desktop
scheduled tasks (local) · `/loop` (polling en sesión).

**Agent SDK** (`@anthropic-ai/claude-agent-sdk`, antes `@anthropic-ai/claude-code`):
```ts
import { query } from "@anthropic-ai/claude-agent-sdk";
for await (const m of query({ prompt: "…", options: { allowedTools: ["Edit"] } })) {
  if (m.type === "result") console.log(m.result);
}
```
Ejemplo completo: [`sdk.ts`](./ejemplos/automation/sdk.ts). El `query_hook.js` es un SDK dentro de un hook.
Al SDK le aplican las mismas reglas de caching de §6: lo estable primero.

---

# PARTE 2 — La metodología

## 12. Metodología

Todo el material profundo (flujo de 11 etapas, ejemplo real end-to-end, prevalencia de tools) está en
[`ejemplos/metodologia/`](./ejemplos/metodologia/). Resumen:

### El flujo real (ver [`metodologia/WORKFLOW.md`](./ejemplos/metodologia/WORKFLOW.md))
Agente = colaborador disciplinado; la autonomía se gana por-decisión. 11 etapas encadenadas por **gates
deterministas**: orientar (history+status) → triaje inbound en el **contrato de salida** → regresión vs
pre-existente → investigar con **oráculo determinista** (antes de la tirada de pago) → plan+acuerdo →
TDD RED→GREEN → verificar (unit+scoped+regresión+contrato vía *wrapper* Y dentro de la imagen desplegada)
→ documentar → **sanitizar** (líneas añadidas)
→ handoff (el humano hace push/PR/deploy) → revisión automática + persistir.
Diagrama: [`metodologia/flow.png`](./ejemplos/metodologia/flow.png) (fuente `flow.mmd`, render
`render_flow.py`). Caso concreto de principio a fin:
[`metodologia/EJEMPLO_REAL.md`](./ejemplos/metodologia/EJEMPLO_REAL.md).

> **El gate outbound son CINCO checks** (no solo "los tests pasan"):
> **(0) validar el instrumento de medida antes de fiarte de él** — todo `_diag_*`/`_sweep_*` que informe una
> decisión de envío se corre primero contra un **caso de respuesta conocida**, y ese resultado se anota junto
> al hallazgo; nunca envuelvas la medición en tu propio `try/except → return False`;
> (1) reproducir en la **etapa real de salida** —el *wrapper* que reconstruye el contrato, no una función
> interna `extract()`—; (2) el JSON local casa con el contrato, y **se verifica sobre la LISTA de miembros,
> nunca sobre un total**; (3) verificarlo **dentro de la imagen desplegada** (descargar/construir la imagen del
> runtime, montar el `src`, re-correr); (4) **mirar la salida** renderizada con los ojos antes del PR — para
> cambios de geometría/highlight, artefactos **antes/después obligatorios**.
> Los tests en verde no son prueba de lo que se despliega.

> **Cinco formas de que un gate verde no pruebe nada** — las cinco nos han mordido:
> **Instrumento roto.** Saltarse el constructor para probar un predicado barato deja sin asignar todo atributo
> que no pensaste en poner; si el método lo lee y tiene su propio `try/except`, el error se traga y vuelve como
> un `False` plausible. El sondeo entonces reporta un "no" uniforme y confiado para **todos** los casos. Canario
> con respuesta conocida, siempre.
> **Total que cuadra.** Un recuento que coincide con lo esperado **no** es un test que pasa: un elemento de más
> y uno de menos se cancelan. Afirma sobre **títulos/ids**, no sobre `len(...)`; y donde el fix tiene dirección
> conocida, mide un **delta** contra baseline (ganados/perdidos), no dos totales. Cuanto más cerca cae un
> número del esperado, **más** sospechoso, no menos.
> **Gate que no podía fallar.** Si el corpus de referencia no contiene ningún ejemplo positivo de la forma que
> acabas de tocar, la pasada limpia demuestra **no-regresión y nada más**. Dilo explícitamente y nombra qué
> sostiene entonces la evidencia de corrección. (Caso real: un detector que dispara en **0 de 190** documentos
> del corpus — `fires=0` se lee idéntico si el código es correcto o si está completamente roto.)
> **Canario que nunca aplicó la perturbación real.** El instrumento puede estar impecable y aun así no probar
> nada, porque lo que le hace al dato **no es lo que hace producción**. Caso real: el test sintético renombró
> los *contenedores* y movió un 4% de los elementos, recuperó el **100%** del mapeo y se dio por "verificado";
> la reconstrucción real cambió algo que el test nunca tocó —los **identificadores de los propios elementos**,
> el 88% de ellos— y la recuperación cayó por debajo del **1%**. Antes de fiarte de un canario en verde, di en
> una frase *qué le hace producción a este dato* y comprueba que el canario hace lo mismo. Si no puedes, el
> gate está **sin probar**: "pasó el test que supe construir" no es "el riesgo está retirado".
> **Gate estructural leído como semántico.** Comprobar que todo está presente, es único y engancha bien no dice
> **nada** sobre si es *correcto*. Caso real: una migración dio parte limpio —todos los grupos casados, ninguno
> perdido, cero huérfanos— mientras el **56%** de los nombres heredados no describía aquello a lo que estaban
> pegados, porque el emparejamiento cayó a un proxy superficial. Un nombre equivocado es **peor** que uno
> ausente: el ausente pregunta, el equivocado responde mal y manda al siguiente al sitio incorrecto. Cuando la
> corrección de un valor es cuestión de **significado**, ningún check automático la retira: programa la lectura
> humana y dilo en la descripción del gate.

> **El contrato de salida es un documento vivo.** Cuando un cambio altera lo que se emite, consulta la regla que
> lo gobierna **antes** de diseñar el fix y haz exactamente una de tres cosas: **cumplirla**, **revisarla** como
> parte del mismo cambio, o **registrar** por qué queda fuera de su alcance. Las tres son válidas; **el silencio
> no**. Revisar es normal: que un fix correcto destape que una regla acordada estaba mal es *cómo mejora* el
> contrato. Dos notas prácticas: cita la regla por **identificador estable** (nunca por ruta de fichero — las
> rutas locales no resuelven para quien lo lee en un ticket), y no lo conviertas en un gate de CI: la decisión
> es de **tres valores** y un check binario bloquearía justamente el resultado correcto de "revisar la regla".

> **¿De dónde sale el número "esperado"?** "El otro entorno devuelve X" es evidencia **sobre ese entorno**,
> nunca una especificación — y si ese entorno corre el mismo camino de código que estás arreglando, casarlo
> reproduce el bug. Deriva el objetivo de la estructura del documento y del contrato, y dilo claramente cuando
> la expectativa del ticket esté mal (caso real: el ticket decía 12; la respuesta correcta era 13).

### Prevalencia de tools (ver [`metodologia/herramientas.md`](./ejemplos/metodologia/herramientas.md))
El `CLAUDE.md` no solo dice *qué* hacer, sino **con qué tool y en qué orden** (barato→caro,
determinista→probabilístico):
```
Orientar     -> /kg (grafo de tickets) · STATUS.md/ledgers · git · gh   (sin inferencia)
Navegar      -> CodeGraph codegraph_explore: fuente+rutas+blast radius+cobertura (1 llamada; trátala como YA leída)
Refactor-chk -> Serena find_referencing_symbols (desambigua por clase)  OBLIGATORIO antes de renombrar/borrar
Diagnosticar -> oráculo determinista (parser/validador/_diag_*.py)  (sin inferencia, reproducible)
Entorno      -> AWS CLI (CloudWatch, lambda get-function, SQS/DLQ)   (read-only)
Contrato     -> Playwright / F12 sobre el endpoint de salida
Desplegado   -> Docker: repro dentro de la imagen del runtime (etapa real = wrapper); tests verdes != lo enviado
Solo al final-> la tirada del LLM, para VERIFICAR el fix (no para diagnosticar)
```

---

## 13. Herramientas del método

### CodeGraph ([`ejemplos/codegraph/`](./ejemplos/codegraph/)) — inteligencia de código local
Índice tree-sitter → SQLite en `.codegraph/` (sin API keys). Devuelve símbolos + rutas de llamada +
blast radius + **flags de cobertura de tests**. Benchmarks: 58% menos tool calls, 22% más rápido.
```bash
codegraph init        # crea .codegraph/ y construye el índice   codegraph sync   # incremental tras editar
codegraph explore "<símbolo|pregunta>"       # fuente + rutas + blast radius, en 1 round-trip
codegraph impact|callers|node <símbolo>      # blast radius / callers / 1 símbolo + trail
codegraph install --target=claude --location=global   # escribe la config MCP (--location: global|local, NO user)
codegraph serve --path <repo> --mcp          # server MCP; --path fija el proyecto POR DEFECTO
```
Es el **primer** tool de navegación (antes que grep/Read); trata la fuente que imprime como **ya leída** (no
re-abras ese fichero). El MCP **no tiene proyecto por defecto** salvo que fijes `--path`: hazlo y
`codegraph_explore` no necesita `projectPath`; pásalo solo para consultar **otro** repo indexado (ya indexamos
`monolith` y `frontend`). En WSL2 `/mnt` el watcher puede perder cambios → `codegraph sync` tras editar.

### Serena ([`ejemplos/serena/`](./ejemplos/serena/)) — navegación semántica vía LSP
```bash
claude mcp add serena -- uvx --from git+https://github.com/oraios/serena serena start-mcp-server
```
Tools clave: `find_symbol` (con `body=true`), `get_symbols_overview`, `search_for_pattern`, y sobre todo
**`find_referencing_symbols`** — el chequeo **preciso** antes de renombrar/borrar: desambigua métodos
homónimos por clase, donde el `impact` plano de CodeGraph los mezcla. Complementa a CodeGraph, no lo
sustituye. El subagente [`refactor-scout`](./ejemplos/subagents/.claude/agents/refactor-scout.md)
empaqueta el orden CodeGraph→Serena→grep como procedimiento.

### GSD ([`ejemplos/gsd/`](./ejemplos/gsd/)) — el método hecho tooling
Ciclo por fases con estado versionado en `.planning/` y subagentes especializados:
```
/gsd-new-project  -> PROJECT.md + ROADMAP.md
/gsd-plan-phase   -> PLAN.md   (+ gate gsd-plan-checker, goal-backward)
/gsd-execute-phase-> ejecución en olas, commits atómicos (gsd-executor)
/gsd-verify-work  -> VERIFICATION.md (gsd-verifier: verifica el OBJETIVO, no solo las tareas)
/gsd-progress     # comando situacional: qué toca ahora
```
Subagentes: `gsd-planner`, `gsd-plan-checker`, `gsd-executor`, `gsd-code-reviewer`, `gsd-verifier`,
`gsd-phase-researcher` — subagentes custom (§9) distribuidos como plugin (§8). Setup real de CodeGraph+GSD
en una instalación: [`docs/SETUP_CODEGRAPH_GSD.md`](./docs/SETUP_CODEGRAPH_GSD.md).

> **Honestidad — ¿lo usamos aquí?** **No.** GSD está instalado y encarna la misma disciplina, pero **este
> proyecto no corre GSD**: usa el flujo de 11 etapas + `data/changes/` (`STATUS.md`, `<TICKET>/<TICKET>.md`,
> `PLAYBOOK.md`, `SHARP_EDGES.md`…), **más depurado y afinado** a fixes por ticket sobre un servicio en
> producción. GSD tiene más sentido en un **greenfield multi-componente** (diseñar una aplicación entera con
> roadmap → fases). Aquí es el método **productizado**, no nuestra herramienta diaria.

---

## 14. Transferir la metodología

Material real: [`docs/ai-agents-code-methodology/`](./docs/ai-agents-code-methodology/) —
[`COPILOT_ADAPTATION.md`](./docs/ai-agents-code-methodology/COPILOT_ADAPTATION.md) (la guía de adaptación),
[`TRANSFER_AND_BOOTSTRAP.md`](./docs/ai-agents-code-methodology/TRANSFER_AND_BOOTSTRAP.md) (empaquetar y
arrancar), [`templates/`](./docs/ai-agents-code-methodology/templates/) (plantillas) y
[`scripts/bootstrap-new-repo.ps1.txt`](./docs/ai-agents-code-methodology/scripts/bootstrap-new-repo.ps1.txt).

**Qué viaja sin cambios:** plan→acuerdo→implementar · verificar en el contrato del consumidor · resolver
la clase general · rastro durable · el humano posee lo externo.

**Qué se re-mapea:** contrato (HTTP/DB/evento/artefacto), tracker (Jira/Boards/Issues), pirámide de tests,
runtime desplegado, reglas de sanitización.

**Bootstrap en el repo destino:**
```powershell
Expand-Archive ai-agent-methodology-package.zip -DestinationPath data/changes
Rename-Item …/scripts/bootstrap-new-repo.ps1.txt bootstrap-new-repo.ps1
pwsh data/changes/ai-agent-methodology/scripts/bootstrap-new-repo.ps1
# crea: STATUS.md · FOLLOWUPS.md · SHARP_EDGES.md · plantillas de handover y QA
```
(El script viaja como `.ps1.txt` para esquivar los bloqueos de contenido activo del correo.)

**Fallback sin grafo de tickets** (80% del valor, setup mínimo): `STATUS.md` newest-first + carpetas por
ticket · búsqueda léxica por síntoma/símbolo/campo del contrato · historia de commits (solapamiento de
ficheros) como sustituto ligero del grafo · sección corta de "danger zones".

**Checklist de primer día:** rellenar `STATUS.md` · 3-5 invariantes en `SHARP_EDGES.md` · definir el
contrato de salida · comandos de test scoped · un issue completo con RED→GREEN + verificación de contrato.

---

## 15. Sincronización de máquinas

Dos mecanismos, y **no** compiten: **(A)** tarball+USB para el *bring-up completo* de una
máquina, y **(B)** almacenamiento compartido (S3) para el *registro de ingeniería del día a
día*. (B) es el cambio reciente y es lo que se usa a diario; (A) sigue siendo el camino
cuando hay que levantar una máquina desde cero.

### A. Bring-up completo: tarball + USB (asimétrico)

Procedimiento real (sanitizado) que aplica los mismos principios a una tarea de ops
(ver [`metodologia/machine-sync.md`](./ejemplos/metodologia/machine-sync.md);
runbooks de la instalación real en [`docs/synchro/`](./docs/synchro/)). **Asimétrico:**

```bash
# OUTBOUND (principal -> portátil): COPIA COMPLETA. -h dereferencia el symlink de .aws (crítico);
# se excluyen venvs/node_modules/caches; se omite .gnupg si no existe.
WS=$(ls -d /mnt/*/ILS 2>/dev/null | head -1)          # DERIVAR la raíz, no asumir
tar -czhf ~/ils-migration-$(date +%Y%m%d).tar.gz \
  --exclude='*/node_modules' --exclude='*/.codegraph' --exclude='*/.venv' --exclude='*/__pycache__' --exclude='*.pyc' \
  -C "$(dirname "$WS")" "$(basename "$WS")" \
  -C /home/$USER .claude .aws .ssh
# USB: WSL no auto-monta un USB conectado tras arrancar -> sudo mount -t drvfs F: /mnt/f ; copiar, sync,
# y verificar byte a byte (stat -c %s origen destino coinciden) antes de expulsar. El bundle crece (~1.5 GB).
# En destino: bash data/machine-sync/target-setup.sh  -> reinstala el CLI de CodeGraph, actualiza GSD si va
# atrasado, corrige el --path del MCP a la raíz real del portátil, y reconstruye el índice (codegraph init).

# INBOUND (portátil -> principal): SOLO DELTA. El código ya está en GitHub.
git fetch origin                                      # única op de red (read-only)
cp data/changes/STATUS.md data/changes/STATUS.md.mainbak   # backup ANTES
tar -xzf "$TARBALL" -C "$REPO"                         # solo los docs gitignored de data/
diff data/changes/STATUS.md.mainbak data/changes/STATUS.md # ¿solo adiciones? quedarse. ¿ediciones propias? STOP
```

**Dos huecos, dos subcomandos idempotentes** (el workspace lleva un grafo `/kg` — §16): en un portátil
nuevo, `kg_refresh.sh bootstrap` instala el tooling que no va en el bundle y fija el intérprete; y como la
memoria (`~/.claude`) **no** viaja en el delta, `snapshot-memory` la parquea bajo `data/` (para que viaje) y
`restore-memory` la fusiona de vuelta con backup en la principal, antes de `/kg-refresh`. Punto de entrada
único para el agente del portátil: `LAPTOP_START_HERE.md` (restaurar → `bootstrap` → seguir igual → mandar
delta). El **grafo construido** no viaja de vuelta: se reconstruye donde esté el corpus. ⚠️ Pero el
overlay de nombres curados **sí viaja, y en ambos sentidos** — está escrito a mano dentro del árbol
generado y no lo regenera nada. Es la corrección de §16: *"derivado" es propiedad del fichero, no de la
carpeta.*

Guardrails (el landing lo conduce **un agente**, con un `INSTRUCTIONS.md` escrito *para* él): solo
no-destructivo (renombrar, no borrar; nunca dos ops de movimiento a la vez en un mount Windows); sin
escrituras git a remoto (nada de push/merge/PR); STOP y preguntar ante ambigüedad; el binario del AWS CLI
**no** va en el bundle (reinstalar en destino + `aws sso login`) — igual el CLI de CodeGraph y el índice
`.codegraph/`, que repone `target-setup.sh`. El humano es dueño de las acciones
externas; el agente prepara y reporta con evidencia (conteos de ficheros, estados de PR).

### B. El registro compartido: `data/` sobre S3

El tarball resuelve **transporte**, no **compartir**. Con una tercera máquina y una segunda
persona aparecen tres costes: el registro es gitignored → **no se puede enlazar** desde un
ticket/PR; moverse degenera en empaquetarlo todo; y cada compañero acaba con **su propio
índice privado** de la misma historia. Runbook completo:
[`docs/synchro/s3-sync/README.md`](./docs/synchro/s3-sync/README.md).

```bash
# Dry-run es el DEFAULT: no se transfiere nada hasta --go
./data-pull.sh            # preview  ->  ./data-pull.sh --go
./data-push.sh            # preview  ->  ./data-push.sh --go
./mount-data.sh           # vista compartida en vivo, SOLO LECTURA (~/s3-<name>-data)
./validate.sh             # una máquina no está lista hasta que imprime MACHINE READY
```

| Regla | Por qué |
|---|---|
| Alcance **por fases**, cada una revisada | Empezó estrecho (`changes/**/*.md` + grafo) y se ensanchó en cuatro fases hasta el árbol completo, binarios de cliente incluidos — **con la firma del dueño en cada salto**. Ensanchar es fácil; retraer, no. ⚠️ **Cada ampliación es un evento de seguridad**: escanea antes, y **canaria el escáner primero** (un escaneo de 1.141 ficheros dio limpio *y el canario con un secreto plantado también* — un nombre se parseó como opción y abortó el lote en silencio; arreglado, encontró 15 ficheros con URLs firmadas). Y después **reconcilia**: un informe de transferencia limpio solo dice *"lo que me pediste enviar, lo envié"*, nunca *"lo que existe está"*. |
| **Escribe por sync, lee por mount de solo lectura** | El almacenamiento de objetos no tiene locking ni rename atómico: un mount escribible corrompe y se descubre semanas después. |
| Dry-run por defecto; `--delete` es opt-in aparte | Un espejo exacto desde una vista local vieja **borra** lo que un compañero acaba de empujar. |
| Docs = fuente de verdad; el grafo es **derivado** | Los ficheros por ticket casi nunca chocan; el grafo generado es el único punto real de contención → reconstruir en local (`/kg-refresh`) o **un solo publisher**. |
| ⚠️⚠️ **La recuperación CADUCA — y cada uno responde de su trabajo** | El versionado se describe siempre como "la red de seguridad", punto. Es media verdad: casi siempre lleva una regla de ciclo de vida que **expira las versiones no actuales a los 30 días**. Una sobrescritura es recuperable **30 días y solo si alguien se da cuenta**; nadie audita los ficheros de nadie. Dilo literal en el onboarding: *baja antes de editar, sube lo que cambiaste, y si desaparece algo tuyo, dilo dentro del mes o se ha ido.* |
| **Los ledgers compartidos son de solo-append** | `STATUS.md`, `TICKETS.md`, `FOLLOWUPS.md`… Last-writer-wins sin merge: **reescribir uno borra en silencio la línea de otra persona**, sin conflicto ni error. Añade filas, no reestructures las ajenas. Detectarlo es barato: una línea presente en local y ausente en la copia entrante es borrado deliberado o pisotón → un chequeo en el `pull` que avise casi no tiene falsos positivos. Es la **visibilidad** que el versionado no da: hace la pérdida *recuperable*, no *advertida*. ⚠️⚠️ **Construimos ese chequeo exacto y aun así perdimos trabajo** — ver la fila siguiente. |
| **En divergencia manda el almacén compartido** | *"Yo lo tengo en local"* deja de ser argumento en cuanto la versión de otro es la publicada. Acuérdalo **antes**: el instinto va al revés, porque tu copia es la que ves. |
| ⚠️⚠️ **Protege las DOS direcciones — el `pull` te pisa a ti, el `push` pisa a tu compañero** | El chequeo en el `pull` de la fila anterior es el que todo el mundo construye, porque protege a quien lo ejecuta. Es **la mitad del problema**. Medido: dos máquinas editaron el ledger de estado la misma tarde; el segundo `push` reemplazó el primero entero — **11 líneas perdidas, sin conflicto, sin error, y nada en la máquina que empujó parecía mal después.** Pasó un día sin que nadie lo viera. Un `pull` puede avisarte *a ti*; un `push` destruye evidencia en **una máquina que tú nunca miras**. Protege también el `push`: antes de subir un fichero compartido, comprueba si la copia publicada se movió desde tu última sincronización, y **rechaza** — no avises: un aviso dentro de un preview de 60 líneas es exactamente lo que se pasa por alto. |
| ⚠️ **Un fichero por máquina necesita EXACTAMENTE un escritor, forzado en la herramienta** | Partir un ledger compartido en un fichero por máquina elimina la contención *por diseño* — y la herramienta puede romperlo igual. La nuestra subía el fichero de **todas** las máquinas, incluida su copia permanentemente vieja de la de otro, revirtiendo en silencio el registro de esa persona. **El primer síntoma no fue un fichero corrupto: fue una conclusión equivocada sobre una persona** — con su registro borrado, el panel decía que nunca había cerrado su día. Sí lo había cerrado. Antes de concluir que un compañero se saltó un paso del proceso, comprueba si tu propia herramienta se comió la evidencia. |
| ⚠️ **Un guardia que grita en falso el primer día enseña a la gente a saltárselo** | Nuestro guardia de `push` comparaba solo marcas de tiempo, y habría rechazado el primerísimo `push` de un compañero —sobre ficheros que acababa de bajar y tenía byte a byte— porque su log aún no registraba ningún `pull` real (script viejo, primer día en la máquina: ambos habituales). Ahora hace la pregunta que importa: *¿esta subida cambiaría realmente el objeto publicado?* **La tasa de falsos positivos de un guardia es una propiedad de seguridad, no un detalle de usabilidad**: cada rechazo espurio gasta credibilidad, y el override que la gente aprende a usar es justo el que provoca el incidente. Publica la vía de escape *y* la razón para no usarla. |

**Lo específico de agentes — la máquina tiene rol.** En cuanto el mismo registro es
alcanzable desde varias máquinas con permisos distintos, la sesión debe saber **dónde está y
qué puede hacer** *antes* de actuar; si no, una máquina *contributor* republicará el grafo
compartido —lo único que no debe hacer— y lo reportará como trabajo hecho. Cada máquina
declara `MACHINE_NAME`/`MACHINE_ROLE` en su `config.env`, `identity.sh --write` genera un
`IDENTITY.md` **machine-local** (con checks en vivo: cuenta autenticada, bucket alcanzable,
mount presente) y el `CLAUDE.md` **apunta a él**, así que toda sesión lee su rol primero.
`IDENTITY.md` es el único fichero que **no** debe ser igual en todas partes: gitignored,
nunca sincronizado, nunca empaquetado.

**Y el hábito necesita un mecanismo, no un párrafo.** Todo lo anterior son *reglas*, y las reglas en
un runbook se degradan en silencio. Las nuestras lo hicieron: "pull al empezar, push al terminar"
estuvo en el documento de operaciones **durante meses sin cumplirse**, justo en la máquina que
publicaba. Nada registraba una sincronización, así que nada podía mostrar la deriva — el
incumplimiento era invisible incluso para quien lo incumplía.

La solución fue empaquetar los dos momentos de los que depende el registro compartido en una rutina
invocable — `day start` (preparar la máquina y dar el parte) y `day end` (escribirlo, publicarlo,
confirmar que llegó) — y hacerla **consciente del rol**, leyendo la tarjeta de identidad de la
máquina antes de tocar nada. Hay un ejemplo completo en
[`ejemplos/skills-plugins/.claude/skills/day/SKILL.md`](./ejemplos/skills-plugins/.claude/skills/day/SKILL.md), y los scripts que orquesta —genericizados pero reales— están en
[`ejemplos/metodologia/s3-sync/`](./ejemplos/metodologia/s3-sync/). Empieza por `config.env.example`: ese fichero es donde vive el diseño, y genericizar los once scripts para este curso cambió **una línea en un fichero**, porque todo lo específico del entorno ya estaba en la config.

Léela por la forma, no por los comandos. Cada paso peligroso está detrás de una pregunta que
responde antes — *¿hay trabajo local sin publicar?, ¿qué ficheros va a sobrescribir este pull?,
¿puede esta máquina publicar el artefacto derivado?* — y donde la respuesta es ambigua **se detiene y
pregunta** en vez de elegir. Una rutina que resuelve sola el caso ambiguo es justo la que acaba
destruyendo el trabajo de otro. El beneficio secundario es el rastro: en cuanto la rutina registra
cada sincronización, *"¿cuándo sincronizó esta máquina por última vez?"* pasa a ser contestable para
todas las máquinas — y ese registro es lo que hizo detectables los dos fallos anteriores.

> **Antes del primer push compartido:** limpiar credenciales incrustadas en los docs. No es
> hipotético — las notas de investigación capturan URLs firmadas y tokens **a propósito**,
> como evidencia de un bug, y son exactamente las cadenas que no quieres en almacenamiento
> compartido. Pasar el escáner de sanitización sobre **todo** el registro, no sobre un diff.

> ⚠️⚠️ **Un rol que solo existe en la documentación es código sin probar.** Escribimos el rol
> `contributor`, lo revisamos y lo enseñamos durante semanas. La primera vez que alguien lo
> ejecutó de verdad, no funcionaba: el guard del testigo bloqueaba el sync **entero**, así que
> un contributor no podía ni subir sus propias carpetas de ticket. Arreglarlo destapó tres
> fallos más, cada uno detrás del anterior — (1) la cola de peticiones vivía *dentro* de la
> carpeta protegida, así que las peticiones no salían nunca de la máquina, en silencio;
> (2) marcar una petición como consumida movía el fichero **solo en local**, y un sync sin
> borrado dejaba el original en el almacén, así que el siguiente pull lo resucitaba en todas
> las máquinas; (3) la copia del propio solicitante no la borra ningún pull, así que las
> peticiones consumidas se volvían a subir para siempre y se leían como pendientes. Ninguno
> era visible leyendo el código.
>
> **De ahí salen dos reglas.** Primera: **antes de proteger una ruta, enumera qué más vive
> debajo** — los datos de coordinación y los publicados comparten padre mucho más a menudo de
> lo que nadie pretende. Segunda: **"baja antes de editar" es un consejo peligroso si tienes
> trabajo sin subir**: ese mismo "el pull no borra" sobrescribe tu cambio local con la copia
> vieja del almacén y resucita ficheros que borraste a propósito. Haz el pull en dry-run y lee
> qué pretende sobrescribir.
>
> **La práctica que caza todo esto es barata: simula el rol antes de dar de alta a nadie en
> él.** Una identidad de máquina distinta y un árbol local vacío ejercitan los scripts reales
> sin riesgo — una ejecución que acierte por error no sube nada. Ese cambio convirtió cuatro
> fallos latentes en una tarde de trabajo en vez de en la primera semana de alguien nuevo.

> ⚠️⚠️ **Un guardia de seguridad puede desactivar en silencio el instrumento que prueba el hábito.**
> Añadimos un snapshot previo al `pull` para hacerlo reversible —un guardia genuinamente bueno— y
> este instalaba su propio `trap ... EXIT` para limpiar un temporal. Bash mantiene **un solo** trap
> EXIT, así que reemplazó al que escribía el log de sincronización. El bloque del snapshot solo
> corre en la ruta real (`--go`), de modo que **los dry-run siguieron registrando y todos los `pull`
> reales quedaron sin registrar durante dos días**, mientras la columna "último pull" seguía llena y
> perfectamente plausible.
>
> Dos cosas generalizan. Primero, **pregunta qué más reclama el mismo recurso de ranura única** al
> añadir un guardia: el trap EXIT, `$?`, un contexto `set -e`. Segundo, **la ruta real y la ruta de
> ensayo son código distinto, y solo una se ejercita a la ligera** — un instrumento que funciona en
> dry-run no está probado.
>
> El aislamiento también merece copiarse: una línea marcador añadida al log sobrevivió a un `pull`
> real **byte a byte**, lo que descartó *"se escribió y luego se sobrescribió"* y probó *"nunca se
> escribió"*. Un conteo de líneas no habría distinguido ambas. Cuando dos hipótesis predicen el
> mismo número resumen, busca la observación que las separa.

> ⚠️ **Mide una optimización antes de citarla.** Restringir el barrido al único directorio que
> cambia a diario se predijo como pasar el chequeo "de dos minutos a segundos". Medido:
> **212s → 123s, un 40%** — la mayor parte del coste estaba *dentro* de ese directorio. Una
> optimización citada de intuición se convierte en dato documentado con un solo copy-paste, y de ahí
> pasa al onboarding. Mídela una vez, escribe el número y ponle fecha.

> **Presupuesta el juicio que cuesta un rebuild, no solo el cómputo.** Cuando un artefacto
> compartido lleva etiquetas escritas a mano sobre una estructura generada, mide cuántas
> sobreviven a un rebuild antes de dar por hecho que nombrar es un coste único. Las nuestras
> aguantaron un **48%** en un rebuild y un **37%** en el siguiente — sobre identificadores
> fijados a propósito para que fueran estables. El pinning arregló la deduplicación *dentro*
> de una ejecución y no hizo nada por la continuidad *entre* ejecuciones. Reetiquetar es un
> coste recurrente de cada refresh; un artefacto a medio etiquetar no pasa ningún gate y no
> le sirve a nadie.

---

# PARTE 3 — El grafo de conocimiento de tickets (graphify)

## 16. Grafo de conocimiento de tickets

**Tecnología: `graphify` — no CodeGraph.** CodeGraph es solo la analogía (mismo rol, otro dominio): si
CodeGraph indexa el *código*, este grafo indexa la **memoria del proyecto** — writeups por ticket, "sharp
edges", runbooks, notas de memoria. Todo el material real está en
[`docs/knowledge-graph/`](./docs/knowledge-graph/): [`design.md`](./docs/knowledge-graph/design.md) (diseño
de la Fase 1, un spike con decisión keep/extend/replace), scripts, tests, manifest y la salida real.
Resumen narrativo adicional: [`docs/KNOWLEDGE_GRAPH.md`](./docs/KNOWLEDGE_GRAPH.md).

### Las piezas (comandos creados en Claude Code)

| Pieza | Qué es |
|---|---|
| `/kg` (skill) | Consulta: `explain` / `path` / `find` — determinista, **sin LLM** |
| `/kg-refresh` (skill) | Reconstruye el grafo: `prepare` → `/graphify` → `finalize` |
| [`kg_query.sh`](./docs/knowledge-graph/kg_query.sh) | Envoltorio de `graphify explain`/`path` sobre `output/graph.json` + `find` (descubrir nombres de nodo); resuelve intérprete y ruta del grafo, limpia warnings |
| [`kg_refresh.sh`](./docs/knowledge-graph/kg_refresh.sh) | Bookends deterministas: `prepare` / `finalize` / `bootstrap` / `snapshot-memory` / `restore-memory` |
| [`build_manifest.py`](./docs/knowledge-graph/build_manifest.py) / [`stage_corpus.py`](./docs/knowledge-graph/stage_corpus.py) | Enumeran y montan el corpus con nombres provenance-preserving (`sst-5468__sst-5468.md`, `hub__STATUS.md`, `memory__x.md`) |
| `test_kg_corpus.py` · `test_kg_query.py` · `test_kg_refresh.py` | Los bookends están **testeados** — el pipeline es infraestructura, no un one-off |
| [`manifest.txt`](./docs/knowledge-graph/manifest.txt) | El corpus explícito y diffeable (~116 ficheros, ~196k palabras) |

**¿`/kg` es un comando o una skill? Skill** — aunque se invoque como `/kg` (las skills también se disparan
por nombre con `/`, así que la sintaxis no distingue). Lo que lo hace skill: lleva **assets** (los shell
wrappers), tiene **`description`** para que Claude la auto-seleccione en la etapa de orientar sin que la
escribas, y `/kg-refresh` **orquesta un paso del propio modelo** (`/graphify`) — un slash command es solo
un prompt guardado. Las definiciones (`SKILL.md`) viven **a nivel de usuario, fuera del repo**:
`~/.claude/skills/kg/`, `~/.claude/skills/kg-refresh/` y `~/.claude/skills/graphify/` (graphify también es
una skill). Ubicación deliberada: (1) **confidencialidad** — nada del KG vive en rutas committeables;
(2) **alcance** — user-level la hace disponible en cualquier sesión de la máquina, coherente con que el
grafo indexa también memoria de `~/.claude`. Y como `~/.claude` viaja en el tarball outbound del
machine-sync (§15), las skills llegan al portátil con la copia completa; el grafo (derivado) se
reconstruye allí con `bootstrap` + `/kg-refresh`.

### Construir y consultar

```bash
# construir / refrescar (el único paso con LLM es /graphify, con subagentes en paralelo)
kg_refresh.sh prepare        # manifest -> stage _corpus/ -> copiar a un scratch FUERA del repo
/graphify <scratch>          # extracción de nodos/aristas + clustering -> HTML/JSON/reporte
kg_refresh.sh finalize       # copiar artefactos a output/ + leak-check (nada fuera de data/)

# consultar (cero LLM: kg_query.sh lee output/graph.json directamente)
/kg <ticket|tema>            # vecinos de un nodo    (graphify explain)  <- el uso más común
/kg <A> <B>                  # camino más corto A<->B (graphify path)
/kg find <substr>            # descubrir el nombre exacto de un nodo
```

**Gotcha que sostiene el pipeline:** `graphify` respeta `.gitignore` y todo `data/` lo está → correr el
detector in situ encuentra 0 ficheros; el corpus se monta en un scratch fuera del repo y los artefactos
se copian de vuelta. **Por eso `/kg-refresh` es un skill y no un script:** el paso semántico es un paso
de Claude; los bookends son deterministas.

### La salida real (ver [`output/`](./docs/knowledge-graph/output/))

- [`graph.html`](./docs/knowledge-graph/output/graph.html) — visualización **vis-network interactiva**:
  búsqueda de nodos, panel de info, filtro por comunidad. La captura para el deck se regenera con
  [`presentacion/capture_kg_graph.py`](./presentacion/capture_kg_graph.py) → `presentacion/kg_graph.png`.
- `graph.json` — NetworkX node-link; aristas **tipadas** (`relation`) con `confidence`
  (`EXTRACTED`/`INFERRED` + score). Es lo que lee `kg_query.sh`.
- [`GRAPH_REPORT.md`](./docs/knowledge-graph/output/GRAPH_REPORT.md) — el informe de auditoría:
  **507 nodos · 672 aristas · 35 comunidades**; **92% `EXTRACTED`** · 7% `INFERRED` (confianza media 0.7);
  god-nodes (los tickets estructurales, onboarding gratis) y "surprising connections" (lecciones gemelas
  que nadie había conectado a mano). Las comunidades mapean a zonas de peligro reales
  ("Letter-End & Run-in Titles", "Title Detection Failures", "PDF Extractor Cascade"…).

### Enganche y ciclo de vida

Enganchado a la regla **history-first** del `CLAUDE.md` (etapa 1, Orientar): corre `/kg <ticket|tema>`
*antes* de hacer grep en `data/changes/`; una llamada saca los tickets relacionados + la zona de peligro
a leer (apunta a *qué leer*, no lo sustituye). Honestidad: la ganancia real es **recall en zonas densas**;
`EXTRACTED` = fiable, `INFERRED` = pista a verificar. En la instalación real todo vive bajo `data/`
gitignored (los nodos llevan nombres internos → interno; compartir fuera = pasada de sanitización aparte).
Es un artefacto **derivado**: se reconstruye donde esté el corpus (§15, con `bootstrap` /
`snapshot-memory` / `restore-memory` cerrando el círculo).

> ⚠️ **Corrección: "derivado" es una propiedad del fichero, no de la carpeta.** Esta guía decía que el
> grafo "nunca viaja entre máquinas" porque se reconstruye. Eso vale **solo mientras reconstruir sea sin
> pérdida**, y dejó de serlo: dentro del árbol generado vive un fichero **escrito a mano** — los nombres
> curados de cada comunidad — que no lo regenera nada. Al reconstruir, los identificadores internos del
> grafo se derivan de cero, así que los nombres dejan de enganchar: medido en una reconstrucción real,
> **sobrevivió menos del 1%**, y aun corrigiendo la causa de fondo solo ~38%. Rehacerlos es una hora de
> criterio, no un comando. Clasifica **por fichero**: *fuente*, *derivado*, y **"escrito a mano pero
> dentro del árbol derivado"** — el tercero se trata como fuente: viaja siempre.
>
> Y como el overlay de nombres solo tiene sentido contra el grafo exacto del que salió, mientras que
> `aws s3 sync` compara **cada objeto por separado**, una máquina puede acabar con grafo nuevo y nombres
> viejos. Eso no da error: da **nombres pegados a la comunidad equivocada**. Se sella el overlay con una
> **huella del grafo** contra el que se construyó y el chequeo de salud falla en ruidoso si no coinciden.
> Un sync fichero-a-fichero no sabe expresar atomicidad; la comprobación tiene que vivir en el dato.

> **Coste — honesto, y por qué compensa.** "Sin LLM en la consulta" **no** es "gratis": el razonamiento caro
> se paga **una vez** al construir el grafo (`/kg-refresh`, con subagentes); cada `/kg` es luego un algoritmo
> determinista sobre `graph.json` → **cero inferencia**, con el único coste de que Claude lee un output corto
> (como un `grep`) — coste **menor y dirigido**, no cero. El coste de construir (grafo, oráculos, skills
> deterministas) se **amortiza**: es inversión → sin inferencia por consulta, respuestas **deterministas y
> reproducibles** (mejor resultado), razonamiento caro sustituido por lookup barato → **ahorro de tiempo y
> dinero** por tarea. Se paga una vez, se cobra en cada uso.
