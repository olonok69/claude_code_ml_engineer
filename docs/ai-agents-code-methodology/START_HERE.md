# AI Agent Methodology Pack - Start Here

Use this folder as a portable starter kit for a different repository and machine.

## Goal

Set up a reliable GitHub Copilot agent workflow with:

1. Clear guardrails.
2. Reproducible triage and verification.
3. Lightweight but durable documentation.

## Fast path (15-30 minutes)

1. Copy this whole folder to the new repository under:
   - `data/changes/ai-agent-methodology`
2. Read in order:
   - `README.md`
   - `TECHNICAL.md`
   - `COPILOT_ADAPTATION.md`
   - `TRANSFER_AND_BOOTSTRAP.md`
3. Rename and run the bootstrap script in the new repo root:
   - PowerShell:

```powershell
Rename-Item data/changes/ai-agent-methodology/scripts/bootstrap-new-repo.ps1.txt bootstrap-new-repo.ps1
pwsh data/changes/ai-agent-methodology/scripts/bootstrap-new-repo.ps1
```
4. Fill templates created under `data/changes/` in the new repo.
5. Start the first issue using the planning template from `COPILOT_ADAPTATION.md`.

## What this pack gives you

1. Methodology overview and technical mechanics.
2. Copilot-specific adaptation rules.
3. Transfer and initialization instructions.
4. Ready-to-fill templates for status, sharp edges, handover, and QA checks.
5. Optional script to scaffold docs in a new repo.

## Non-negotiable rules

1. Plan -> agree -> implement.
2. Verify at output contract level.
3. Keep fixes generic (class-level, not one example only).
4. Keep a durable change trail.
5. Human owns external actions (merge, deploy, external comms).
