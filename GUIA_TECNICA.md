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
  `CONVENTIONS.md`, `<TICKET>/<TICKET>.md`) que se leen bajo demanda.
- **Regla write-once:** cada dato en un único ledger canónico; el core lleva el puntero, no la copia.

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

> **El gate outbound son tres checks** (no solo "los tests pasan"): (1) reproducir en la **etapa real de
> salida** —el *wrapper* que reconstruye el contrato, no una función interna `extract()`—; (2) el JSON local
> casa con el contrato; (3) verificarlo **dentro de la imagen desplegada** (descargar/construir la imagen del
> runtime, montar el `src`, re-correr). Los tests en verde no son prueba de lo que se despliega.

### Prevalencia de tools (ver [`metodologia/herramientas.md`](./ejemplos/metodologia/herramientas.md))
El `CLAUDE.md` no solo dice *qué* hacer, sino **con qué tool y en qué orden** (barato→caro,
determinista→probabilístico):
```
Orientar     -> /kg (grafo de tickets) · STATUS.md/ledgers · git · gh   (coste 0)
Navegar      -> CodeGraph codegraph_explore: fuente+rutas+blast radius+cobertura (1 llamada; trátala como YA leída)
Refactor-chk -> Serena find_referencing_symbols (desambigua por clase)  OBLIGATORIO antes de renombrar/borrar
Diagnosticar -> oráculo determinista (parser/validador/_diag_*.py)  (coste 0, reproducible)
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
delta). El grafo es un artefacto **derivado**: nunca viaja de vuelta; se reconstruye donde esté el corpus.

Guardrails (el landing lo conduce **un agente**, con un `INSTRUCTIONS.md` escrito *para* él): solo
no-destructivo (renombrar, no borrar; nunca dos ops de movimiento a la vez en un mount Windows); sin
escrituras git a remoto (nada de push/merge/PR); STOP y preguntar ante ambigüedad; el binario del AWS CLI
**no** va en el bundle (reinstalar en destino + `aws sso login`) — igual el CLI de CodeGraph y el índice
`.codegraph/`, que repone `target-setup.sh`. El humano es dueño de las acciones
externas; el agente prepara y reporta con evidencia (conteos de ficheros, estados de PR).

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
Es un artefacto **derivado**: nunca viaja entre máquinas; se reconstruye donde esté el corpus (§15, con
`bootstrap` / `snapshot-memory` / `restore-memory` cerrando el círculo).
