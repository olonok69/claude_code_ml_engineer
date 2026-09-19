---
name: day
description: Start-of-day and end-of-day routine for the shared ticket record — role-aware pull, orientation briefing, end-of-day push, KG refresh request, and publisher-baton handover for travel. Use at the START of any working session on the repo that owns the shared record, at the END before stopping, and whenever asked "who has pulled/pushed recently" or "hand the publisher role to another machine".
trigger: /day
---

# /day

Packages the two moments the shared record depends on and that are otherwise forgotten:
**prepare the machine at the start**, **publish the work at the end**. Role-aware — a
contributor and the publisher do different things, and the machine states which it is.

```
/day start     # pull the team's latest, then a short orientation briefing
/day end       # publish today's work, and flag the KG if the corpus moved
/day status    # who pulled/pushed recently, across machines; who holds the KG baton
/day baton     # hand the publisher role to another machine (travel, leave, handover)
```

Default with no argument: `start` if no `pull --go` was recorded for this machine today,
otherwise `status`.

> **Why this is a skill and not just a doc.** The rule "pull at the start, push at the
> end" sat in `OPERATIONS.md` for months and was not being followed on the publisher
> machine — nothing recorded a sync, so nothing could show the drift. Documentation
> cannot enforce a habit; a callable routine can.

---

## Step 1 — locate the repo and read this machine's role

Walk up from the cwd for the sync scripts, then read the identity card. **Do this before
any bucket write or KG action** — the role decides what is allowed.

```bash
S3=""
d="$PWD"
while [ "$d" != "/" ]; do
  if [ -f "$d/data/changes/s3-sync/data-pull.sh" ]; then S3="$d/data/changes/s3-sync"; break; fi
  d="$(dirname "$d")"
done
if [ -z "$S3" ]; then echo "No shared-record sync in this repo."; fi
echo "S3=$S3"
grep -E '^- \*\*(Machine|Role|S3 target)' "$S3/IDENTITY.md" 2>/dev/null
```

If `IDENTITY.md` is missing or its generated date is old, regenerate it — it is what
agents read to learn their role, and a stale card once named a profile that had been
deleted:

```bash
(cd "$S3" && ./identity.sh --write)
```

If `S3` is empty, tell the user this repo has no shared record and STOP.

---

## Step 2 — branch on the requested action

### `/day start`

1. **⚠️ FIRST check for unpublished local work — a pull can overwrite it.**

   `aws s3 sync` transfers whenever the **size differs**, not only when the remote is
   newer. So a pull overwrites a locally-edited file with the bucket's older copy, and a
   file renamed locally is re-created under its old name. Measured 2026-09-16: a pull at
   that moment would have clobbered 20+ files edited earlier the same day.

   ```bash
   (cd "$S3" && ./data-push.sh --root changes)   # dry run: anything listed is local-only work

   `--root changes` limits the sweep to the only root that moves day to day (measured 212s → 123s:
   a trim, not an order of magnitude). Fine for this check; use the full sweep when publishing.

   ```

   - **Nothing listed** → the previous session ended properly; go to step 2.
   - **Something listed** → that is unpublished work from a previous session. Say what it
     is and offer to publish it first (`./data-push.sh --go`). Do **not** pull past it
     without the user's explicit go-ahead.

   This is why the day *ends* with a push: a properly-closed day makes the next morning's
   pull risk-free. The check exists for the days that were not closed properly.

2. **Pull.** Never `--delete`. The script now protects you, but you must READ what it says.

   ```bash
   (cd "$S3" && ./data-pull.sh --go)
   ```

   Before applying anything it dry-runs, **snapshots every local file the pull would
   replace** into `data/_prepull/<timestamp>/`, and lists them. Two outcomes to act on:

   - **"⚠️ N existing local file(s) will be REPLACED"** — read that list aloud to the user.
     Shared hub files (`STATUS.md`, `FOLLOWUPS.md`, `SHARP_EDGES.md`, `TEST_MAP.md`,
     `_PENDING_*.md`) appearing there means a colleague's copy is landing on top of yours,
     and **each side may hold content the other lacks — that needs a merge, not a winner.**
     Diff the snapshot against the new file before doing anything else:
     `diff data/_prepull/<ts>/changes/STATUS.md data/changes/STATUS.md`
     To undo the whole pull: `cp -a data/_prepull/<ts>/. data/`
   - **Exit code 3, "CASE-COLLIDING FILES"** — two bucket objects differ only in
     capitalisation and map to one file on this machine. **Stop.** The pull would pick a
     winner at random. Delete the wrong-cased key in the bucket first; canonical casing for
     ticket docs is lowercase `sst-NNNN.md`.

   ⚠️ If this fails on credentials, **re-login before drawing any conclusion** — an
   expired cached token reports as a permission error and has produced wrong findings
   here more than once:
   `aws sso logout && aws sso login`

3. **Show what changed and who else is active.**

   ```bash
   (cd "$S3" && ./activity.sh)
   ```

4. **Orient — history-first AND status-first.** Read, in this order:
   - the newest `data/changes/_PENDING_*.md` (the resume point),
   - `data/changes/STATUS.md` rows for the area in play,
   - `git fetch --all --prune` then `git status -sb` (the written record does not know
     about today's branches), and `gh pr list` if PRs are in play.
   - the **`kg` skill** for prior art before designing anything — not a grep of
     `data/changes/`.

5. **If this machine is the PUBLISHER**, also:

   ```bash
   (cd "$S3" && ./publisher.sh status)                       # do we still hold the baton?
   bash "$(dirname "$S3")/../knowledge-graph/kg_refresh.sh" queue   # any refresh requests pending?
   ```

   Report pending requests; do **not** start a refresh unasked — it is ~100 naming
   judgements and a full hour, and a half-named graph passes no gate.

6. **Brief the user in a few lines**: what the pull brought in, who else has been active,
   the resume point, and anything the queue or baton says. Then stop and take direction —
   `/day start` prepares the machine, it does not pick the work.

### `/day end`

1. **Make sure today's thinking is written down** before it is published: the ticket doc
   (`data/changes/<ticket>/`), a `STATUS.md` row, any follow-up in `FOLLOWUPS.md`. If a
   piece of work has no written record, say so and offer to write it — an unpublished
   day is indistinguishable from a day that did not happen.

2. **Preview the push and read the file list out loud.** This is the sanitisation moment:
   secrets, keys, anything that should not enter the shared record. Keys live outside
   `data/`; scripts saved under `data/` carry placeholders.

   ```bash
   (cd "$S3" && ./data-push.sh)
   ```

3. **Publish.** Never `--delete` unless the user explicitly asks and this machine is the
   publisher.

   ```bash
   (cd "$S3" && ./data-push.sh --go)
   ```

   A contributor push that says it **skipped `knowledge-graph/`** is correct behaviour,
   not an error — only `refresh_queue/` goes up from a contributor.

   ⛔ **If the push exits 4 — "REFUSED: shared hub file(s) changed in the bucket"** — a teammate
   wrote one of those files after this machine last synced, and our copy differs. `aws s3 sync`
   has no merge, so pushing would replace theirs. **Read the named files out to the user, diff each
   against the bucket copy, and merge.** Do NOT pass `--allow-clobber` on your own initiative — it
   is for "the user has confirmed ours supersedes theirs", nothing less.

   ```bash
   (cd "$S3" && source ./config.env && \
     aws s3 cp "s3://$BUCKET/$PREFIX/changes/STATUS.md" - --profile "$PROFILE" | diff - ../STATUS.md)
   ```

   Measured 2026-09-18: a push four minutes after a colleague closed his day destroyed his entire
   `STATUS.md` section AND his activity ledger — and nothing on this machine looked wrong
   afterwards, so it went a full day unnoticed. The guard does not fire when our copy is
   byte-identical to the bucket's, so a file we just pulled is never a collision.


4. **If ticket docs were added or materially changed, flag the graph** (this is the
   contributor loop, and the publisher should file one too so the reason is recorded):

   ```bash
   bash "$(dirname "$S3")/../knowledge-graph/kg_refresh.sh" request "<what changed, and why it matters>"
   (cd "$S3" && ./data-push.sh --go)
   ```

5. **Confirm the record landed**: `(cd "$S3" && ./activity.sh)` should now show this
   machine's push as minutes old.

### `/day status`

```bash
(cd "$S3" && ./activity.sh)          # last pull/push per machine
(cd "$S3" && ./activity.sh --log)    # the full event stream
(cd "$S3" && ./publisher.sh status)  # who may rebuild and publish the KG
```

Report it plainly. ⚠️ The ledger reports what was *recorded*: a machine that has never
run the instrumented scripts shows nothing, and absence of a record is **not** evidence
of no activity.

### `/day baton` — moving the publisher role (travel, leave, handover)

The KG publisher is a single machine because `aws s3 sync` is last-writer-wins with no
merge: two publishers silently destroy each other's hand-authored community names. The
baton is an advisory lock kept **in the bucket**, so either machine can check it rather
than both having to remember.

```bash
(cd "$S3" && ./publisher.sh status)              # who holds it
(cd "$S3" && ./publisher.sh release)             # outgoing machine hands it back
(cd "$S3" && ./publisher.sh claim "why")         # incoming machine takes it
```

**Order matters — release before claim.** The receiving machine must also set
`MACHINE_ROLE="publisher"` in its `config.env` and re-run `./identity.sh --write`, or its
agent will keep reading "CONTRIBUTOR" and decline the work it now owns.

⚠️ `claim --force` exists for a machine that is provably idle (lost, off, wiped). It is
the one command here that can cause the damage the baton prevents — confirm with the
user before using it, every time.

For a trip, the full procedure (what to copy, what **not** to run on the travelling
machine, and how to land the delta on return) is `s3-sync/TRAVEL_HANDOVER.md` and
`data/machine-sync/RUNBOOK.md`. Two standing rules from it: the travelling machine does
**not** run `data-pull.sh`, and it does **not** run `/kg-refresh`.

---

## Rules that hold in every branch

- **Never `--delete`** from this skill. It is publisher-only, deliberate, and only right
  after a fresh pull.
- **Never push `knowledge-graph/` from a contributor.** The tool enforces it; do not work
  around it.
- **Re-login before diagnosing an access error.** The error describes the cached token,
  not the entitlement.
- **The human owns outward actions** — this skill syncs the shared record; it does not
  push branches, open PRs, deploy, or message anyone.
