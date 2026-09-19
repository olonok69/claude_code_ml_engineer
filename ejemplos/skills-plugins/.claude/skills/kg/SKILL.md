---
name: kg
description: >-
  History-first ticket knowledge-graph lookup for <your-repo>. Use at
  session start or whenever orienting on a bug/area — before grepping data/changes/.
  Surfaces related prior tickets and danger zones (graphify index).
---

# kg — ticket knowledge graph query

## When to use

- Session start / Orient stage.
- User mentions a ticket id, symptom area, extractor, or “have we seen this before?”.
- Before broad reads under `data/changes/`.

## Procedure

1. Prefer the project query script (no LLM). **Pick the door for the host OS** — the
   PowerShell one is a wrapper that shells into WSL, so it is Windows-only:

```bash
# macOS / Linux / WSL / Git Bash — the script itself
bash data/knowledge-graph/kg_query.sh TCK-1234
bash data/knowledge-graph/kg_query.sh "letter-end"
bash data/knowledge-graph/kg_query.sh TCK-1234 TCK-1234
bash data/knowledge-graph/kg_query.sh find signature
```

```powershell
# Windows only — proxies into WSL:
bash data/knowledge-graph/kg_query.sh TCK-1234        # macOS / Linux / WSL
.\scripts\kg_query.ps1 TCK-1234                        # Windows PowerShell
bash data/knowledge-graph/kg_query.sh find signature   # macOS / Linux / WSL
.\scripts\kg_query.ps1 find signature                  # Windows PowerShell
```

Needs a python that can `import graphify` (`python3 -m pip install graphifyy`). Without it
the script exits with *"graphify package not importable"* — `find` mode still works, it is
pure python3.

2. Read **only** the tickets / danger-zone docs the query points to.
3. Status-first: `git branch -a`, `gh pr list`, skim `data/changes/STATUS.md`.
4. Summarize for the human — **do not start coding**.

## Fallback (no graph / script fails)

1. Search `data/changes/STATUS.md`.
2. Open newest matching `data/changes/<id>/<id>.md`.
3. Skim `data/changes/SHARP_EDGES.md`.
4. `git log --oneline -- <paths>` for file overlap.

State clearly that you used the fallback.

## Output format

```text
KG / history-first
- Query: …
- Related tickets: …
- Danger zones / sharp edges: …
- Live status (branch/PRs): …
- What to read next: …
- Recommendation: (base / constraints / whether to proceed to triage)
```
