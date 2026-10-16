---
name: atlassian
description: Read Jira issues/links/comments/XML and Confluence pages (search, read, diff a local file against a page) via the REST token. Read-only. Use when a ticket's live status, links or comments are needed, to export a ticket XML, or to compare a local doc with its Confluence page.
---

# /atlassian — read-only Jira + Confluence

Tool: `data/changes/tools/atlassian/atl.py` in the project repo (course copy:
`ejemplos/metodologia/tools/atlassian/`). Python 3.10+, **standard library only**. Credentials:
`~/.config/<org>/jira.env` (chmod 600; `ATLASSIAN_ENV_FILE` overrides the path).
**GET only — the tool cannot write.** Jira writes (create, edit, transition, comment) stay with the
user; a Confluence page update is a separate, explicitly confirmed action (see Hard rule 1).

```bash
T=data/changes/tools/atlassian/atl.py
python3 $T jira issue PROJ-123              # type, status, summary, assignee, links
python3 $T jira search 'project = PROJ AND assignee = currentUser() AND statusCategory != Done'
python3 $T jira links PROJ-123
python3 $T jira comments PROJ-123 --last 3
python3 $T jira xml PROJ-123 --out data/changes/proj-123/
python3 $T confluence search 'title ~ "authoring" AND type = page'
python3 $T confluence page <PAGE_ID> --body
python3 $T confluence diff <local .md/.html> <PAGE_ID>
```

Exit codes: 0 ok · 2 credentials missing/invalid · 3 HTTP error · 4 not found.
`--json` gives raw JSON — use it only inside a script; in conversation use the compact default to save context.

## Setup (once per machine, by the person — never by the agent)

```
JIRA_BASE_URL=https://<your-site>.atlassian.net
JIRA_EMAIL=<your Atlassian login email>
JIRA_API_TOKEN=<your own token from id.atlassian.com → Security → API tokens>
```

Write it in your own terminal, `chmod 600` it, and never paste the token into a chat or a file under
`data/`. The same token reads Confluence. Check: `python3 $T jira issue PROJ-123` → exit 0 works, exit 2
means the file is missing or wrong.

## Hard rules

1. **Read-only.** `atl.py` has exactly one network function and it sends GET; adding a write is a code
   change, not a flag (a test asserts it).
   - Creating, editing, transitioning or commenting on Jira issues is the **user's** job. Draft the
     text; the user posts it.
   - Updating an existing Confluence page goes through `confluence_write.py`, and only when the user
     explicitly asks for **that** page: `pull` → `plan` (backs up the live body, prints the visible-text
     diff and a confirmation token) → the user reads the diff and says OK → `apply --confirm <token>`.
     Apply refuses if the token, the body file or the live page version changed since the plan, and
     reads the page back afterwards. One page per confirmation. No create/delete/move path exists.
2. **Never print, paste or log the token**, nor the contents of `jira.env`.
3. **Cite tickets by key** in outward text, never local file paths.

A ticket status table can be refreshed from Jira + GitHub by a separate script at `/day start` (step 3b
of the `day` skill): the publisher writes it, every other machine gets a report-only summary.
