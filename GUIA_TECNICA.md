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
| Pasar del terminal al Desktop (diffs visuales) | `/desktop` |
| Empujar eventos externos (Telegram/Discord/webhooks) a una sesión | **Channels** |
| Ruta de bug desde Slack a un PR | integración **Slack** (`@Claude`) |

El mismo motor y los mismos `CLAUDE.md`/settings/MCP funcionan en todas.

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

**Metodología** (ver `GUIA_PRESENTACION.md` §6): agente = colaborador disciplinado; gates de evidencia
("sin prueba local no está hecho"), oráculo determinista antes de la tirada de pago, solución genérica
con prueba no-op, gate de sanitización, "variación del LLM = último recurso".

**GSD** ([`ejemplos/gsd/`](./ejemplos/gsd/)) — ciclo por fases con estado en `.planning/`:
```
/gsd-new-project → /gsd-plan-phase → /gsd-execute-phase → /gsd-verify-work
/gsd-progress    # dónde estás y qué toca
```

**CodeGraph** ([`ejemplos/codegraph/`](./ejemplos/codegraph/)) — grafo SQLite del código:
```bash
codegraph init                       # crea .codegraph/
codegraph explore "<símbolo|pregunta>"   # fuente + rutas de llamada + blast radius, en 1 round-trip
```
Úsalo antes que grep/Read para impacto, callers y navegación en repos grandes.
