---
name: methodology-plan
description: >-
  Fill the methodology planning template after inbound triage and cheap
  investigation. Use in Plan mode before writing production code.
---

# methodology-plan

## When to use

- After orient, inbound triage, provenance, cheap root-cause probe.
- Before any production implementation.
- User asks for a plan, options, or “should we fix this?”.

## Rules

1. Stay in **Plan** posture: propose, do not implement.
2. Prefer evidence already gathered (contract sample, oracle output, KG hits).
3. Record rejected options, not only the chosen one.
4. Contract = **`get-sl-upload-status` JSON** unless the human says otherwise.

## Template (fill completely)

```text
Issue: <SST-NNNN> - <short title>

1) Contract confirmation
- Consumer-visible contract: get-sl-upload-status JSON (Provision UI)
- Symptom reproduced there: <yes/no + evidence path under data/changes/…/qa_review_N/>

2) Provenance
- Reproduced on pre-change baseline: <yes/no>
- Classification: <regression | pre-existing>

3) Root cause hypothesis
- Deterministic probe used: <_diag_ / parser / schema>
- Result: <what proved the hypothesis>

4) Fix shape (general-case)
- Structural class addressed: <class>
- Why not instance-specific: <one sentence>
- Options considered (incl. rejected): <bullets>
- Contract rule: <comply | revise | record> + case tag if applicable

5) Verification plan
- RED test: <test id>
- Scoped suite: <pytest command>
- Regression suite: <pytest -q / variant battery>
- Contract output repro: <wrapper / last writer>
- Deployed-image check: <how>

6) Outputs before human gate
- data/changes/<TICKET>/<TICKET>.md update
- qa_acceptance_criteria.md
- STATUS.md row (append)
- Next-actions note (push/PR/deploy — human only)
```

## Exit

Stop and ask for explicit human agreement. Only after agreement, implement with TDD.
