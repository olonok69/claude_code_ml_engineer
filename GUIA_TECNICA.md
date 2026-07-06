# Claude Code — Guía técnica de implementación

> Referencia copy-paste para montar cada pieza. Complementa a [`GUIA_PRESENTACION.md`](./GUIA_PRESENTACION.md)
> (el hilo narrativo) con el **cómo**. Todos los artefactos ejecutables están en [`ejemplos/`](./ejemplos/).

## Índice

1. [Instalación y CLI](#1-instalación-y-cli)
2. [Memoria: CLAUDE.md, jerarquía y auto-memory](#2-memoria)
3. [Settings y permisos](#3-settings-y-permisos)
4. [Sesiones entre superficies](#4-sesiones)
5. [MCP](#5-mcp)
6. [Slash commands, skills y plugins](#6-slash-commands-skills-y-plugins)
7. [Hooks](#7-hooks)
8. [Automatización: headless, CI, scheduling, SDK](#8-automatización)
9. [Metodología, GSD y CodeGraph](#9-metodología-gsd-y-codegraph)

---

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
Comandos dentro de la sesión: `/help`, `/mcp`, `/plugin`, `/schedule`, `/loop`, `/desktop`, `/config`.
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

### Patrón de dos niveles (ver [`ejemplos/claude-md/`](./ejemplos/claude-md/))
- **Nivel 1** = el `CLAUDE.md` siempre cargado: orientación + punteros de una línea. Pequeño.
- **Nivel 2** = ficheros bajo `data/changes/` (`STATUS.md`, `PLAYBOOK.md`, `SHARP_EDGES.md`,
  `CONVENTIONS.md`, `<TICKET>/<TICKET>.md`) que se leen bajo demanda.
- **Regla write-once:** cada dato en un único ledger canónico; el core lleva el puntero, no la copia.

### Auto-memory
Claude persiste aprendizajes (comandos de build, pistas de debug) entre sesiones automáticamente. No
requiere que escribas nada; se acumula en el store de memoria del proyecto.

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

## 5. MCP

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

## 6. Slash commands, skills y plugins

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

**Subagentes** (tool `Task`): `Explore` (read-only), `Plan`, `general-purpose`, o especializados.
Lánzalos en paralelo para trabajo independiente.

---

## 7. Hooks

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

## 8. Automatización

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

---

## 9. Metodología, GSD y CodeGraph

Todo el material profundo (flujo de 11 etapas, ejemplo real end-to-end, prevalencia de tools) está en
[`ejemplos/metodologia/`](./ejemplos/metodologia/). Resumen:

### Metodología — el flujo real (ver [`metodologia/WORKFLOW.md`](./ejemplos/metodologia/WORKFLOW.md))
Agente = colaborador disciplinado; la autonomía se gana por-decisión. 11 etapas encadenadas por **gates
deterministas**: orientar (history+status) → triaje inbound en el **contrato de salida** → regresión vs
pre-existente → investigar con **oráculo determinista** (antes de la tirada de pago) → plan+acuerdo →
TDD RED→GREEN → verificar (unit+scoped+regresión+contrato) → documentar → **sanitizar** (líneas añadidas)
→ handoff (el humano hace push/PR/deploy) → revisión automática + persistir.
Caso concreto de principio a fin: [`metodologia/EJEMPLO_REAL.md`](./ejemplos/metodologia/EJEMPLO_REAL.md).

### Prevalencia de tools (ver [`metodologia/herramientas.md`](./ejemplos/metodologia/herramientas.md))
El `CLAUDE.md` no solo dice *qué* hacer, sino **con qué tool y en qué orden** (barato→caro,
determinista→probabilístico):
```
Orientar     -> STATUS.md/ledgers · git · gh                        (coste 0)
Navegar      -> CodeGraph codegraph_explore: fuente+rutas+blast radius+cobertura (1 llamada; trátala como YA leída)
Refactor-chk -> Serena find_referencing_symbols (desambigua por clase)  OBLIGATORIO antes de renombrar/borrar
Diagnosticar -> oráculo determinista (parser/validador/_diag_*.py)  (coste 0, reproducible)
Entorno      -> AWS CLI (CloudWatch, lambda get-function, SQS/DLQ)   (read-only)
Contrato     -> Playwright / F12 sobre el endpoint de salida
Solo al final-> la tirada del LLM, para VERIFICAR el fix (no para diagnosticar)
```

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
`gsd-phase-researcher`.

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
Complementa a Serena: `find_referencing_symbols` sigue siendo el chequeo **preciso** antes de renombrar/borrar
(CodeGraph `impact` mezcla métodos homónimos; Serena los desambigua por clase).

### Runbook de ops: sincronizar el workspace entre máquinas (ver [`metodologia/machine-sync.md`](./ejemplos/metodologia/machine-sync.md))
Procedimiento real (sanitizado) que aplica los mismos principios a una tarea de ops. **Asimétrico:**

```bash
# OUTBOUND (principal -> portátil): COPIA COMPLETA. -h dereferencia el symlink de .aws (crítico);
# se excluyen venvs/node_modules/caches; se omite .gnupg si no existe.
WS=$(ls -d /mnt/*/ILS 2>/dev/null | head -1)          # DERIVAR la raíz, no asumir
tar -czhf ~/ils-migration-$(date +%Y%m%d).tar.gz \
  --exclude='*/node_modules' --exclude='*/.codegraph' --exclude='*/.venv' --exclude='*/__pycache__' --exclude='*.pyc' \
  -C "$(dirname "$WS")" "$(basename "$WS")" \
  -C /home/$USER .claude .aws .ssh
# En destino: bash data/machine-sync/target-setup.sh  -> reinstala el CLI de CodeGraph, actualiza GSD si va
# atrasado, corrige el --path del MCP a la raíz real del portátil, y reconstruye el índice (codegraph init).

# INBOUND (portátil -> principal): SOLO DELTA. El código ya está en GitHub.
git fetch origin                                      # única op de red (read-only)
cp data/changes/STATUS.md data/changes/STATUS.md.mainbak   # backup ANTES
tar -xzf "$TARBALL" -C "$REPO"                         # solo los docs gitignored de data/
diff data/changes/STATUS.md.mainbak data/changes/STATUS.md # ¿solo adiciones? quedarse. ¿ediciones propias? STOP
```

Guardrails (el landing lo conduce **un agente**, con un `INSTRUCTIONS.md` escrito *para* él): solo
no-destructivo (renombrar, no borrar; nunca dos ops de movimiento a la vez en un mount Windows); sin
escrituras git a remoto (nada de push/merge/PR); STOP y preguntar ante ambigüedad; el binario del AWS CLI
**no** va en el bundle (reinstalar en destino + `aws sso login`) — igual el CLI de CodeGraph y el índice
`.codegraph/`, que repone `target-setup.sh`. El humano es dueño de las acciones
externas; el agente prepara y reporta con evidencia (conteos de ficheros, estados de PR).
