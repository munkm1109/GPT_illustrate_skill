# Theory Read Proof Template

Use this template for render-bound `illustrate-skill` runs to record which required theory files were actually read before each step.

Recommended workflow:

1. Copy this file to a working path such as `.omx/runs/<YYYYMMDD>-<scene-slug>-theory-read-proof.md`.
2. Record its path in the parent spec's `THEORY_READ_PROOF_PATH`.
3. Update the file as each stage theory is read, preferably via `python scripts/record_theory_read.py ...`.
4. Do not mark `PROOF_READY: yes` until every required theory file has been logged.

[THEORY_READ_PROOF]

PARENT_SPEC_PATH:
WORKSPACE_STYLE_MODE:
STYLE_GUIDE_REQUIRED: <yes|no>
STEP_1_FILES_READ:
STEP_2_FILES_READ:
STEP_3_FILES_READ:
STEP_4_FILES_READ:
STEP_5_FILES_READ:
STEP_6_FILES_READ:
STEP_7_FILES_READ:
STEP_8_FILES_READ:
STYLE_GUIDE_FILES_READ:
READ_EVENTS:
PROOF_READY: <yes|no>

[/THEORY_READ_PROOF]
