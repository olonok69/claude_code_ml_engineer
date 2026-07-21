# Claude Code — Technical implementation guide (course in three parts)

> Copy-paste reference for building each piece. It complements [`GUIA_PRESENTACION_EN.md`](./GUIA_PRESENTACION_EN.md)
> (the narrative thread) with the **how**. All the runnable artifacts are in [`ejemplos/`](./ejemplos/);
> [`docs/`](./docs/) is reference material from a real installation.

> English version of [`GUIA_TECNICA.md`](./GUIA_TECNICA.md).

## Table of contents

**Part 1 — Claude Code**

1. [Installation and CLI](#1-installation-and-cli)
2. [Memory: CLAUDE.md, hierarchy and auto-memory](#2-memory)
3. [Settings and permissions](#3-settings-and-permissions)
4. [Sessions across surfaces](#4-sessions)
5. [Context window](#5-context-window)
6. [Prompt caching](#6-prompt-caching)
7. [MCP](#7-mcp)
8. [Slash commands, skills and plugins](#8-slash-commands-skills-and-plugins)
9. [Subagents and Agent Teams](#9-subagents-and-agent-teams)
10. [Hooks](#10-hooks)
11. [Automation: headless, CI, scheduling, SDK](#11-automation)

**Part 2 — The methodology**

12. [The workflow and the real example](#12-methodology)
13. [The tools: CodeGraph, Serena, GSD](#13-the-methods-tools)
14. [Transferring the methodology (starter-kit / Copilot)](#14-transferring-the-methodology)
15. [Machine sync](#15-machine-sync)

**Part 3 — The ticket knowledge graph (graphify)**

16. [Ticket knowledge graph](#16-ticket-knowledge-graph)

---

# PART 1 — Claude Code

## 1. Installation and CLI

```bash
# Install (pick one)
curl -fsSL https://claude.ai/install.sh | bash          # macOS/Linux/WSL (auto-update)
brew install --cask claude-code                          # Homebrew (brew upgrade to update)
winget install Anthropic.ClaudeCode                      # Windows

# Start
cd your-project && claude

# Headless (one prompt, stdout)
claude -p "summarize the changes on this branch"

# Useful flags
claude --teleport            # bring a web/mobile session to the terminal
claude --continue            # continue the latest session
claude -p "…" --output-format json   # structured output for scripts
```
Commands inside the session: `/help`, `/mcp`, `/plugin`, `/schedule`, `/loop`, `/desktop`, `/config`,
`/context`, `/compact`, `/clear`, `/rewind`, `/agents`.
See the full CLI reference in the official docs (`/en/cli-reference`).

---

## 2. Memory

### `CLAUDE.md` hierarchy (combined by precedence)
```
~/.claude/CLAUDE.md          # user-global (all your projects)
<repo>/CLAUDE.md             # repo root (shared, versioned)
<repo>/<subdir>/CLAUDE.md    # loaded when entering that subfolder
<repo>/CLAUDE.local.md       # personal, NOT versioned
```
The `@path/file` syntax inside a CLAUDE.md imports another doc when it loads
(example: [`ejemplos/context/CLAUDE.import-example.md`](./ejemplos/context/CLAUDE.import-example.md)).

### Two-tier pattern (see [`ejemplos/claude-md/`](./ejemplos/claude-md/))
- **Tier 1** = the always-loaded `CLAUDE.md`: orientation + one-line pointers. Small.
- **Tier 2** = files under `data/changes/` (`STATUS.md`, `PLAYBOOK.md`, `SHARP_EDGES.md`,
  `CONVENTIONS.md`, `<TICKET>/<TICKET>.md`) that are read on demand.
- **Write-once rule:** each fact lives in a single canonical ledger; the core carries the pointer, not the copy.

### Auto-memory
Claude persists learnings (build commands, debugging clues) across sessions automatically. It doesn't
require you to write anything; it accumulates in the project's memory store (the first ~200 lines are
loaded at startup — it also counts against the context, see §5).

---

## 3. Settings and permissions

`.claude/settings.json` (shared) and `.claude/settings.local.json` (personal). The key block is
`permissions`, a **specific allowlist** (no wildcards):

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
Recommended posture: concrete rules (exact invocations), not `Bash(*)`. The human owns external
actions (push/PR/deploy) → those do not go in `allow`.

### Where tools "live" — and the four layers that govern them

The built-in tools (`Read`, `Edit`, `Bash`, `Grep`, `Glob`, `Task`, `WebFetch`, `WebSearch`…) **are
compiled into the binary** and are sent as schemas with every request (the `Tools` level of the caching
prefix, §6). There is no editable tools folder: tools can only be *added* via **MCP** (`mcp__<server>__<tool>`)
or via plugins. What you manage is not the tools but the **access**, in four layers:

1. **Permissions** — the `permissions` block above (+ the `/permissions` command in session). Precedence:
   managed enterprise policy → CLI flags → `settings.local.json` → the project's `settings.json` →
   `~/.claude/settings.json`. A built-in can also be *vetoed*: `deny: ["WebSearch"]` disables it.
2. **CLI flags** — `--allowedTools` / `--disallowedTools` per invocation (typical in headless/CI);
   in the Agent SDK, `options.allowedTools`.
3. **Hooks** — a `PreToolUse` with `exit 2` vetoes based on the *content* of the `tool_input` (§10), which
   the static allowlist cannot do.
4. **Per agent** — the `tools:` frontmatter of a custom subagent restricts what that agent inherits (§9).

> MCP tools use *deferred* loading: a lightweight index (~120 tokens) goes into the context and the full
> schema is loaded when the tool is used (§5). Summary rule: **built-ins ship with the binary and MCP tools
> with your servers; you don't edit tools — you edit permissions.**

---

## 4. Sessions

| I need… | Tool |
|---|---|
| Continue a local session from my phone | **Remote Control** (`/en/remote-control`) |
| Start on web/mobile and bring it to the terminal | `claude --teleport` |
| Move from the terminal to Desktop (visual diffs) | `/desktop` (see caveat below) |
| Push external events (Telegram/Discord/webhooks) into a session | **Channels** |
| Bug-to-PR path from Slack | **Slack** integration (`@Claude`) |

The same engine and the same `CLAUDE.md`/settings/MCP work across all of them.

> ⚠️ **`/desktop` caveat (platform):** only available in the **macOS and Windows** CLI with a
> Claude subscription (not with an API key, nor on Bedrock/Vertex/Foundry). If you run the CLI **inside WSL**,
> Claude Code treats it as **Linux** and the command **is not offered** — even if the Desktop app is
> installed on Windows, because the handoff does not cross the WSL↔Windows boundary. Alternative: open the
> project directly in the Desktop app (*Code* tab). `claude --teleport` and Remote Control **do** work
> from WSL. (Related note: `claude mcp add-from-claude-desktop` does operate on macOS and WSL.)

---

## 5. Context window

Full reference: [`ejemplos/context/`](./ejemplos/context/). The numbers and commands:

**What the session loads before your first prompt:** system prompt ~4,200 tokens · auto-memory ~680
(first 200 lines / 25 KB) · environment ~280 · MCP tool index ~120 in *deferred* mode (each tool's full
schema is loaded when it's used) · your `CLAUDE.md` hierarchy. Window: 200K tokens on current
models (1M in beta via API).

```text
/context                      # per-block usage breakdown — measure before optimizing
/compact focus on the API changes and the modified files
/clear                        # full reset between unrelated tasks
/rewind                       # (Esc+Esc) checkpoints: conversation, code, or both
```

- Auto-compact kicks in near the limit; it's **lossy** → better to run a manual, early `/compact <focus>`.
- `/rewind` restores **only Claude's edits** (not Bash/external changes — it doesn't replace git).
- MCP: every server adds context → disable the ones the project doesn't use (`.claude/settings.json`).
- Noisy research → subagents (§9): the noise dies outside; the summary comes back.
- CLAUDE.md: rule from the official docs — *if you can delete it without Claude getting things wrong, delete it*.

---

## 6. Prompt caching

Reference and runnable demo: [`ejemplos/prompt-caching/`](./ejemplos/prompt-caching/)
([`cache_demo.py`](./ejemplos/prompt-caching/cache_demo.py)).

**Mechanics (API):** a **contiguous prefix** is cached up to a `cache_control` breakpoint; strict
hierarchy `Tools → System → Messages` (a change invalidates its level and the ones after it).

| | Write | Read |
|---|---|---|
| TTL 5 min (default) | 1.25× input | **0.1×** input |
| TTL 1 h (`"ttl": "1h"`) | 2× input | **0.1×** input |

```python
system=[{ "type": "text", "text": STABLE_INSTRUCTIONS,
          "cache_control": {"type": "ephemeral"} }]   # breakpoint AT THE END of the stable part
messages=[{"role": "user", "content": query}]          # the variable part, AFTER (outside the cache)
```

Diagnostics in `response.usage`: `cache_creation_input_tokens` / `cache_read_input_tokens`.
Minimum cacheable ~1,024 tokens (4,096 on Haiku); max. 4 explicit breakpoints.

**In Claude Code** caching is automatic (system + tools + history = stable prefix). What you
control: don't edit `CLAUDE.md`/settings mid-session (it invalidates the cache), few MCP servers (stable
tools block), and knowing that `/compact` rewrites the history (breaks the message cache once).

**TTL in Claude Code:** by default **1 h with a subscription** (included in the plan) and **5 min with an API
key**/Bedrock/Vertex. It's changed via env var (shell or the `env` block of `settings.json`):
`ENABLE_PROMPT_CACHING_1H=1` (1h with API key) · `FORCE_PROMPT_CACHING_5M=1` (force 5 min) ·
`DISABLE_PROMPT_CACHING=1` (turn it off; also per model `DISABLE_PROMPT_CACHING_SONNET/_OPUS/_HAIKU`).
Every read renews the window → with a subscription, pauses of up to 1 h between turns still hit the cache.
Docs: `code.claude.com/docs/en/prompt-caching`.

---

## 7. MCP

See [`ejemplos/mcp/.mcp.json`](./ejemplos/mcp/.mcp.json). Scopes: **local** (`settings.local.json`),
**project** (versioned `.mcp.json`), **user** (`~/.claude.json`).

```bash
# stdio (local process)
claude mcp add serena -- uvx --from git+https://github.com/oraios/serena serena start-mcp-server
# remote HTTP
claude mcp add --transport http context7 https://mcp.context7.com/mcp
claude mcp list
```
```jsonc
// .mcp.json — secret via environment variable, NEVER hardcoded
{ "mcpServers": { "supabase": {
    "command": "npx", "args": ["-y", "@supabase/mcp-server-supabase@latest"],
    "env": { "SUPABASE_ACCESS_TOKEN": "${SUPABASE_ACCESS_TOKEN}" } } } }
```
Tools appear as `mcp__<server>__<tool>` and are allowed/denied in the allowlist.

> **The config gives the capability; the CLAUDE.md gives the judgment.** MCP servers are **not** installed in
> the `CLAUDE.md` — that file is only prompt, not configuration. They are installed in the scopes above (or
> brought in by a plugin). But installing Serena only makes `mcp__serena__find_symbol` *exist*; getting the
> agent to **reach for it unprompted** is the CLAUDE.md's job (global or per-repo) with a *trigger map*: "Serena
> BEFORE reading whole files; `find_referencing_symbols` ALWAYS before a rename". It's the tool-precedence
> rule from [`metodologia/herramientas.md`](./ejemplos/metodologia/herramientas.md) — the config
> turns "I don't have the tool" into "I have it"; the CLAUDE.md turns "I have it" into "it gets used in the
> right order". (Mind the §5 trade-off: that trigger map is loaded in every session — keep it stable and
> pointer-based so it caches well.)

---

## 8. Slash commands, skills and plugins

**Slash command** — `.claude/commands/audit.md`:
```markdown
---
description: Audits dependencies and verifies tests
---
Run `npm audit`, then `npm audit fix`, then the tests. Summarize the result.
```
Invoked with `/audit`. See [`ejemplos/skills-plugins/`](./ejemplos/skills-plugins/).

**Skill** — `.claude/skills/<n>/SKILL.md` with `name` + `description` frontmatter (the `description` guides
auto-selection). It can carry scripts/templates in its folder.

**Plugins:**
```bash
/plugin marketplace add <owner/repo>
/plugin install <plugin>
/plugin                 # manage
```

### The difference, summarized

| | **Slash command** | **Skill** | **Plugin** |
|---|---|---|---|
| **What it is** | Saved prompt | Repeatable capability with instructions + assets | Distributable package |
| **File / location** | `.claude/commands/<n>.md` (or `~/.claude/commands`) | `.claude/skills/<n>/SKILL.md` + folder with scripts/templates/refs | Installed in `~/.claude/plugins` from a marketplace |
| **Invocation** | Manual: `/<n>` (you trigger it) | **Model-invoked**: Claude picks it via its `description` | Installs its contents; not invoked as such |
| **Packages** | One prompt (`$ARGUMENTS`) | Instructions + code/templates/references | skills + commands + agents + MCP + hooks |
| **Distribution** | Copy the `.md` | Copy the folder, or inside a plugin | `/plugin marketplace add <owner/repo>` → `/plugin install <x>` |

Mnemonic rule: **command = you fire it** · **skill = Claude decides** (via the description) ·
**plugin = the delivery vehicle** (versioned) for commands, skills, agents, MCP and hooks. Real examples
of plugins installed this way: `serena`, `context7`, `playwright`, and GSD (which brings dozens of `gsd-*` skills).
More detail and examples in [`ejemplos/skills-plugins/`](./ejemplos/skills-plugins/).

---

## 9. Subagents and Agent Teams

Full reference + diagram: [`ejemplos/subagents/`](./ejemplos/subagents/).

**Built-ins (`Task` tool):** `Explore` (read-only), `Plan`, `general-purpose`. Launch them in parallel for
independent work; only the summary comes back to your session.

**Custom** — `.claude/agents/<name>.md` (project, versioned) or `~/.claude/agents/` (user);
`/agents` lists them:
```yaml
---
name: security-reviewer
description: Reviews code for vulnerabilities. Use it after changes to auth or deps.
tools: Read, Grep, Glob, Bash      # per-agent allowlist (omit = all)
model: opus                         # optional override
---
You are a senior security engineer. Report findings with file:line and severity…
```
Real examples: [`security-reviewer`](./ejemplos/subagents/.claude/agents/security-reviewer.md) ·
[`refactor-scout`](./ejemplos/subagents/.claude/agents/refactor-scout.md) (encodes the
CodeGraph→Serena rule from Part 2). **Gotcha:** the subagent does not inherit your conversation — context
goes in the launch prompt. They run in the background by default.

**Agent Teams (experimental):**
```jsonc
// ~/.claude/settings.json
{ "env": { "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1" },
  "teammateMode": "in-process" }    // or "auto" | "tmux" | "iterm2"
```
Lead + teammates (each one a **full session**), shared task list (`~/.claude/tasks/<team>/`),
inboxes for direct messaging. You request it in natural language (*"set up a team with one architect and two
implementers; require plan approval"*); the roles reuse your custom subagents. Limitations: no
`/resume` in-process, one team per session, no nesting; split-panes require tmux/iTerm2. Cost: each
teammate is a session — for side-quests use subagents.

---

## 10. Hooks

Everything in [`ejemplos/hooks/`](./ejemplos/hooks/). Config in `.claude/settings.json`:

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

**Contract:** payload via stdin · `exit 0` allows · **`exit 2` blocks** and returns `stderr` to Claude.
Pre → `tool_input` (intent); Post → `tool_response` (result + `structuredPatch`). Real payloads:
[`pre-log.json`](./ejemplos/hooks/pre-log.json), [`post-log.json`](./ejemplos/hooks/post-log.json).

**Blocking pattern (JS):**
```js
if (payload.tool_input?.file_path?.includes(".env")) {
  console.error("Blocked: do not read .env");
  process.exit(2);   // <-- veto
}
process.exit(0);
```

Available events: `PreToolUse`, `PostToolUse`, `UserPromptSubmit`, `SessionStart`, `Stop`,
`Notification`. Portable distribution: `settings.example.json` with a `$PWD` token + `init-claude.js` that
replaces it with `process.cwd()` in `npm run setup`.

---

## 11. Automation

See [`ejemplos/automation/`](./ejemplos/automation/).

**Headless / piping:**
```bash
tail -200 app.log | claude -p "flag any anomalies"
git diff main --name-only | claude -p "review for security"
```

**CI (GitHub Actions):** see [`github-action-claude.yml`](./ejemplos/automation/github-action-claude.yml).
It installs Claude, exports `ANTHROPIC_API_KEY` (secret), and uses `claude -p` on the PR diff.

**Scheduling:** `Routines`/`/schedule` (Anthropic infra, triggerable via API/GitHub) · Desktop
scheduled tasks (local) · `/loop` (in-session polling).

**Agent SDK** (`@anthropic-ai/claude-agent-sdk`, formerly `@anthropic-ai/claude-code`):
```ts
import { query } from "@anthropic-ai/claude-agent-sdk";
for await (const m of query({ prompt: "…", options: { allowedTools: ["Edit"] } })) {
  if (m.type === "result") console.log(m.result);
}
```
Full example: [`sdk.ts`](./ejemplos/automation/sdk.ts). The `query_hook.js` is an SDK inside a hook.
The same §6 caching rules apply to the SDK: the stable part goes first.

---

# PART 2 — The methodology

## 12. Methodology

All the deep material (11-stage workflow, real end-to-end example, tool-precedence) is in
[`ejemplos/metodologia/`](./ejemplos/metodologia/). Summary:

### The real workflow (see [`metodologia/WORKFLOW.md`](./ejemplos/metodologia/WORKFLOW.md))
Agent = disciplined collaborator; autonomy is earned per-decision. 11 stages chained by **deterministic
gates**: orient (history+status) → inbound triage against the **output contract** → regression vs
pre-existing → investigate with a **deterministic oracle** (before the paid LLM call) → plan+agreement →
TDD RED→GREEN → verify (unit+scoped+regression+contract via the *wrapper* AND inside the deployed image)
→ document → **sanitize** (added lines)
→ handoff (the human does push/PR/deploy) → automated review + persist.
Diagram: [`metodologia/flow.png`](./ejemplos/metodologia/flow.png) (source `flow.mmd`, render
`render_flow.py`). Concrete case from start to finish:
[`metodologia/EJEMPLO_REAL.md`](./ejemplos/metodologia/EJEMPLO_REAL.md).

> **The outbound gate is three checks** (not just "the tests pass"): (1) reproduce at the **real output
> stage** — the *wrapper* that rebuilds the contract, not an internal `extract()` function; (2) the local JSON
> matches the contract; (3) verify it **inside the deployed image** (download/build the runtime image,
> mount the `src`, re-run). Green tests are not proof of what gets deployed.

### Tool-precedence (see [`metodologia/herramientas.md`](./ejemplos/metodologia/herramientas.md))
The `CLAUDE.md` doesn't just say *what* to do, but **with which tool and in what order** (cheap→expensive,
deterministic→probabilistic):
```
Orient       -> /kg (ticket knowledge graph) · STATUS.md/ledgers · git · gh   (no inference)
Navigate     -> CodeGraph codegraph_explore: source+paths+blast radius+coverage (1 call; treat it as ALREADY read)
Refactor-chk -> Serena find_referencing_symbols (disambiguates by class)  MANDATORY before renaming/deleting
Diagnose     -> deterministic oracle (parser/validator/_diag_*.py)  (no inference, reproducible)
Environment  -> AWS CLI (CloudWatch, lambda get-function, SQS/DLQ)   (read-only)
Contract     -> Playwright / F12 against the output endpoint
Deployed     -> Docker: repro inside the runtime image (real stage = wrapper); green tests != what ships
Only at the end -> the LLM call, to VERIFY the fix (not to diagnose)
```

---

## 13. The method's tools

### CodeGraph ([`ejemplos/codegraph/`](./ejemplos/codegraph/)) — local code intelligence
Tree-sitter index → SQLite in `.codegraph/` (no API keys). Returns symbols + call paths +
blast radius + **test-coverage flags**. Benchmarks: 58% fewer tool calls, 22% faster.
```bash
codegraph init        # creates .codegraph/ and builds the index   codegraph sync   # incremental after editing
codegraph explore "<symbol|question>"       # source + paths + blast radius, in 1 round-trip
codegraph impact|callers|node <symbol>      # blast radius / callers / 1 symbol + trail
codegraph install --target=claude --location=global   # writes the MCP config (--location: global|local, NOT user)
codegraph serve --path <repo> --mcp          # MCP server; --path sets the DEFAULT project
```
It's the **first** navigation tool (before grep/Read); treat the source it prints as **already read** (don't
re-open that file). The MCP server **has no default project** unless you set `--path`: do it and
`codegraph_explore` won't need `projectPath`; pass it only to query **another** indexed repo (we already indexed
`monolith` and `frontend`). On WSL2 `/mnt` the watcher can miss changes → `codegraph sync` after editing.

### Serena ([`ejemplos/serena/`](./ejemplos/serena/)) — semantic navigation via LSP
```bash
claude mcp add serena -- uvx --from git+https://github.com/oraios/serena serena start-mcp-server
```
Key tools: `find_symbol` (with `body=true`), `get_symbols_overview`, `search_for_pattern`, and above all
**`find_referencing_symbols`** — the **precise** check before renaming/deleting: it disambiguates
same-named methods by class, where CodeGraph's flat `impact` mixes them up. It complements CodeGraph, it
doesn't replace it. The [`refactor-scout`](./ejemplos/subagents/.claude/agents/refactor-scout.md) subagent
packages the CodeGraph→Serena→grep order as a procedure.

### GSD ([`ejemplos/gsd/`](./ejemplos/gsd/)) — the method turned into tooling
Phase-based cycle with versioned state in `.planning/` and specialized subagents:
```
/gsd-new-project  -> PROJECT.md + ROADMAP.md
/gsd-plan-phase   -> PLAN.md   (+ gsd-plan-checker gate, goal-backward)
/gsd-execute-phase-> execution in waves, atomic commits (gsd-executor)
/gsd-verify-work  -> VERIFICATION.md (gsd-verifier: verifies the GOAL, not just the tasks)
/gsd-progress     # situational command: what's next now
```
Subagents: `gsd-planner`, `gsd-plan-checker`, `gsd-executor`, `gsd-code-reviewer`, `gsd-verifier`,
`gsd-phase-researcher` — custom subagents (§9) distributed as a plugin (§8). Real CodeGraph+GSD setup
in an installation: [`docs/SETUP_CODEGRAPH_GSD.md`](./docs/SETUP_CODEGRAPH_GSD.md).

> **Honesty — do we use it here?** **No.** GSD is installed and embodies the same discipline, but **this
> project does not run GSD**: it uses the 11-stage workflow + `data/changes/` (`STATUS.md`, `<TICKET>/<TICKET>.md`,
> `PLAYBOOK.md`, `SHARP_EDGES.md`…), **more refined and tuned** for per-ticket fixes on a service in
> production. GSD makes more sense in a **multi-component greenfield** (designing an entire application with
> a roadmap → phases). Here it is the method **productized**, not our daily tool.

---

## 14. Transferring the methodology

Real material: [`docs/ai-agents-code-methodology/`](./docs/ai-agents-code-methodology/) —
[`COPILOT_ADAPTATION.md`](./docs/ai-agents-code-methodology/COPILOT_ADAPTATION.md) (the adaptation guide),
[`TRANSFER_AND_BOOTSTRAP.md`](./docs/ai-agents-code-methodology/TRANSFER_AND_BOOTSTRAP.md) (packaging and
bootstrapping), [`templates/`](./docs/ai-agents-code-methodology/templates/) (templates) and
[`scripts/bootstrap-new-repo.ps1.txt`](./docs/ai-agents-code-methodology/scripts/bootstrap-new-repo.ps1.txt).

**What travels unchanged:** plan→agreement→implement · verify against the consumer's contract · solve
the general class · durable trail · the human owns everything external.

**What gets re-mapped:** contract (HTTP/DB/event/artifact), tracker (Jira/Boards/Issues), test pyramid,
deployed runtime, sanitization rules.

**Bootstrap in the target repo:**
```powershell
Expand-Archive ai-agent-methodology-package.zip -DestinationPath data/changes
Rename-Item …/scripts/bootstrap-new-repo.ps1.txt bootstrap-new-repo.ps1
pwsh data/changes/ai-agent-methodology/scripts/bootstrap-new-repo.ps1
# creates: STATUS.md · FOLLOWUPS.md · SHARP_EDGES.md · handover and QA templates
```
(The script travels as `.ps1.txt` to dodge email active-content blocking.)

**Fallback without a ticket knowledge graph** (80% of the value, minimal setup): newest-first `STATUS.md` +
per-ticket folders · lexical search by symptom/symbol/contract field · commit history (file
overlap) as a lightweight substitute for the graph · a short "danger zones" section.

**First-day checklist:** fill in `STATUS.md` · 3-5 invariants in `SHARP_EDGES.md` · define the
output contract · scoped test commands · one complete issue with RED→GREEN + contract verification.

---

## 15. Machine sync

Real (sanitized) procedure that applies the same principles to an ops task
(see [`metodologia/machine-sync.md`](./ejemplos/metodologia/machine-sync.md);
runbooks from the real installation in [`docs/synchro/`](./docs/synchro/)). **Asymmetric:**

```bash
# OUTBOUND (main -> laptop): FULL COPY. -h dereferences the .aws symlink (critical);
# venvs/node_modules/caches are excluded; .gnupg is skipped if it doesn't exist.
WS=$(ls -d /mnt/*/ILS 2>/dev/null | head -1)          # DERIVE the root, don't assume it
tar -czhf ~/ils-migration-$(date +%Y%m%d).tar.gz \
  --exclude='*/node_modules' --exclude='*/.codegraph' --exclude='*/.venv' --exclude='*/__pycache__' --exclude='*.pyc' \
  -C "$(dirname "$WS")" "$(basename "$WS")" \
  -C /home/$USER .claude .aws .ssh
# USB: WSL does not auto-mount a USB plugged in after boot -> sudo mount -t drvfs F: /mnt/f ; copy, sync,
# and verify byte for byte (stat -c %s of source and destination match) before ejecting. The bundle grows (~1.5 GB).
# On the target: bash data/machine-sync/target-setup.sh  -> reinstalls the CodeGraph CLI, updates GSD if it's
# behind, fixes the MCP --path to the laptop's real root, and rebuilds the index (codegraph init).

# INBOUND (laptop -> main): DELTA ONLY. The code is already on GitHub.
git fetch origin                                      # the only network op (read-only)
cp data/changes/STATUS.md data/changes/STATUS.md.mainbak   # backup FIRST
tar -xzf "$TARBALL" -C "$REPO"                         # only the gitignored docs under data/
diff data/changes/STATUS.md.mainbak data/changes/STATUS.md # additions only? keep. own edits? STOP
```

**Two gaps, two idempotent subcommands** (the workspace carries a `/kg` graph — §16): on a new laptop,
`kg_refresh.sh bootstrap` installs the tooling that doesn't travel in the bundle and pins the interpreter; and
since memory (`~/.claude`) does **not** travel in the delta, `snapshot-memory` parks it under `data/` (so it
travels) and `restore-memory` merges it back with a backup on the main machine, before `/kg-refresh`. Single
entry point for the laptop's agent: `LAPTOP_START_HERE.md` (restore → `bootstrap` → carry on as usual → send
the delta). The graph is a **derived** artifact: it never travels back; it's rebuilt wherever the corpus is.

Guardrails (the landing is driven **by an agent**, with an `INSTRUCTIONS.md` written *for* it): only
non-destructive actions (rename, don't delete; never two move ops at once on a Windows mount); no
git writes to remote (no push/merge/PR); STOP and ask when in doubt; the AWS CLI binary does
**not** travel in the bundle (reinstall on the target + `aws sso login`) — same for the CodeGraph CLI and the
`.codegraph/` index, which `target-setup.sh` restores. The human owns external
actions; the agent prepares and reports with evidence (file counts, PR statuses).

---

# PART 3 — The ticket knowledge graph (graphify)

## 16. Ticket knowledge graph

**Technology: `graphify` — not CodeGraph.** CodeGraph is only the analogy (same role, different domain): if
CodeGraph indexes the *code*, this graph indexes the **project's memory** — per-ticket writeups, "sharp
edges", runbooks, memory notes. All the real material is in
[`docs/knowledge-graph/`](./docs/knowledge-graph/): [`design.md`](./docs/knowledge-graph/design.md) (the
Phase 1 design, a spike with a keep/extend/replace decision), scripts, tests, manifest and the real output.
Additional narrative summary: [`docs/KNOWLEDGE_GRAPH.md`](./docs/KNOWLEDGE_GRAPH.md).

### The pieces (commands created in Claude Code)

| Piece | What it is |
|---|---|
| `/kg` (skill) | Query: `explain` / `path` / `find` — deterministic, **no LLM** |
| `/kg-refresh` (skill) | Rebuilds the graph: `prepare` → `/graphify` → `finalize` |
| [`kg_query.sh`](./docs/knowledge-graph/kg_query.sh) | Wrapper around `graphify explain`/`path` over `output/graph.json` + `find` (discover node names); resolves interpreter and graph path, cleans warnings |
| [`kg_refresh.sh`](./docs/knowledge-graph/kg_refresh.sh) | Deterministic bookends: `prepare` / `finalize` / `bootstrap` / `snapshot-memory` / `restore-memory` |
| [`build_manifest.py`](./docs/knowledge-graph/build_manifest.py) / [`stage_corpus.py`](./docs/knowledge-graph/stage_corpus.py) | Enumerate and stage the corpus with provenance-preserving names (`sst-5468__sst-5468.md`, `hub__STATUS.md`, `memory__x.md`) |
| `test_kg_corpus.py` · `test_kg_query.py` · `test_kg_refresh.py` | The bookends are **tested** — the pipeline is infrastructure, not a one-off |
| [`manifest.txt`](./docs/knowledge-graph/manifest.txt) | The explicit, diffable corpus (~116 files, ~196k words) |

**Is `/kg` a command or a skill? A skill** — even though it's invoked as `/kg` (skills are also triggered
by name with `/`, so the syntax doesn't distinguish them). What makes it a skill: it carries **assets** (the shell
wrappers), it has a **`description`** so Claude auto-selects it at the orient stage without you
typing it, and `/kg-refresh` **orchestrates a step of the model itself** (`/graphify`) — a slash command is just
a saved prompt. The definitions (`SKILL.md`) live **at user level, outside the repo**:
`~/.claude/skills/kg/`, `~/.claude/skills/kg-refresh/` and `~/.claude/skills/graphify/` (graphify is
also a skill). Deliberate location: (1) **confidentiality** — nothing of the KG lives in committable paths;
(2) **scope** — user-level makes it available in any session on the machine, consistent with the fact that the
graph also indexes memory from `~/.claude`. And since `~/.claude` travels in the machine-sync outbound
tarball (§15), the skills reach the laptop with the full copy; the (derived) graph is
rebuilt there with `bootstrap` + `/kg-refresh`.

### Building and querying

```bash
# build / refresh (the only step with an LLM is /graphify, with parallel subagents)
kg_refresh.sh prepare        # manifest -> stage _corpus/ -> copy to a scratch OUTSIDE the repo
/graphify <scratch>          # node/edge extraction + clustering -> HTML/JSON/report
kg_refresh.sh finalize       # copy artifacts to output/ + leak-check (nothing outside data/)

# query (zero LLM: kg_query.sh reads output/graph.json directly)
/kg <ticket|topic>           # a node's neighbors    (graphify explain)  <- the most common use
/kg <A> <B>                  # shortest path A<->B (graphify path)
/kg find <substr>            # discover a node's exact name
```

**Gotcha that holds the pipeline together:** `graphify` honors `.gitignore` and all of `data/` is ignored →
running the detector in place finds 0 files; the corpus is staged in a scratch outside the repo and the artifacts
are copied back. **That's why `/kg-refresh` is a skill and not a script:** the semantic step is a Claude
step; the bookends are deterministic.

### The real output (see [`output/`](./docs/knowledge-graph/output/))

- [`graph.html`](./docs/knowledge-graph/output/graph.html) — **interactive vis-network** visualization:
  node search, info panel, community filter. The screenshot for the deck is regenerated with
  [`presentacion/capture_kg_graph.py`](./presentacion/capture_kg_graph.py) → `presentacion/kg_graph.png`.
- `graph.json` — NetworkX node-link; **typed** edges (`relation`) with `confidence`
  (`EXTRACTED`/`INFERRED` + score). This is what `kg_query.sh` reads.
- [`GRAPH_REPORT.md`](./docs/knowledge-graph/output/GRAPH_REPORT.md) — the audit report:
  **507 nodes · 672 edges · 35 communities**; **92% `EXTRACTED`** · 7% `INFERRED` (mean confidence 0.7);
  god-nodes (the structural tickets, free onboarding) and "surprising connections" (twin lessons
  no one had connected by hand). The communities map to real danger zones
  ("Letter-End & Run-in Titles", "Title Detection Failures", "PDF Extractor Cascade"…).

### Hook-in and lifecycle

Hooked into the **history-first** rule of the `CLAUDE.md` (stage 1, Orient): run `/kg <ticket|topic>`
*before* grepping `data/changes/`; one call surfaces the related tickets + the danger zone
to read (it points to *what to read*, it doesn't replace it). Honesty: the real gain is **recall in dense
zones**; `EXTRACTED` = reliable, `INFERRED` = a lead to verify. In the real installation everything lives under
gitignored `data/` (the nodes carry internal names → internal; sharing outside = a separate sanitization pass).
It is a **derived** artifact: it never travels between machines; it's rebuilt wherever the corpus is (§15, with
`bootstrap` / `snapshot-memory` / `restore-memory` closing the loop).

> **Cost — honest, and why it pays off.** "No LLM at query time" is **not** "free": the expensive reasoning
> is paid **once** when building the graph (`/kg-refresh`, with subagents); each `/kg` is then a deterministic
> algorithm over `graph.json` → **zero inference**, with the only cost being that Claude reads a short output
> (like a `grep`) — a **smaller, targeted** cost, not zero. The cost of building (graph, oracles, deterministic
> skills) is **amortized**: it's an investment → no inference per query, **deterministic and reproducible**
> answers (better outcome), expensive reasoning replaced by cheap lookup → **time and money saved**
> per task. Paid once, collected on every use.
