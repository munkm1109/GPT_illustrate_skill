# PLAN_IMPLEMENT_VERIFY_AUDIT_PIPELINE

Summary: This pipeline is the top-level control structure for render-bound `illustrate-skill` SPEC runs. It wraps the Step 0-8 process instead of replacing it: Step 0-8 remain the IMPLEMENT body, while PLAN, VERIFY, and AUDIT become hard gates around it.

## Why this exists

Previous failures showed that a correct-looking field can still fail in the generated image when the instruction is not transferred through every stage. Object research found tram capacity, but the final generation still made the heroine too large compared with visible passengers. Hand topology improved, but that risked distorting the sword hilt. The solution is to track each non-negotiable through a lifecycle:

`PLAN -> IMPLEMENT -> VERIFY -> AUDIT -> PRE-IMAGE HANDOFF -> POST-IMAGE ACCEPTANCE`

No render-bound handoff should happen merely because Step 0-8 are filled. The PIVA gates must prove that requirements were captured, implemented, verified, and audited. `POST_IMAGE_VISUAL_VERDICT_*` is a post-generation acceptance loop, not a prerequisite for the first prompt handoff.

## PLAN gate

Purpose: capture user intent and non-negotiables before drawing decisions.

Required outputs:

- `PIVA_MODE: enabled`
- `PLAN_USER_COMMAND_SOURCE`
- `PLAN_NON_NEGOTIABLES`
- `PLAN_OBJECT_ANATOMY_SCALE_WITNESSES`
- `PLAN_PREVIOUS_FAILURES`
- `PLAN_GATE_STATUS: pass`

Rules:

- Every explicit user command becomes a checklist item.
- Object/anatomy/scale/style requirements are separated before Step 1.
- Human-enterable objects must be planned as composite scale proofs, not a single entry-height comparison.
- Previous failed generations become active constraints, not background memory.
- If the user asks to reuse a previous prompt, record whether “same prompt” means same source scene or byte-identical final image prompt.

## IMPLEMENT gate

Purpose: ensure Step 0-8 implementation carries PLAN requirements forward.

Required outputs:

- `IMPLEMENT_STEP_MAP`
- `IMPLEMENT_OBJECT_RESEARCH_TRANSFER`
- `IMPLEMENT_SCALE_TRANSFER`
- `IMPLEMENT_STYLE_TRANSFER`
- `IMPLEMENT_PROMPT_DRAFT_TRANSFER`
- `IMPLEMENT_GATE_STATUS: pass`

Rules:

- Step 0-8 remain the implementation body.
- Step 0 chooses exactly one intake route (`image_development` or `prompt_only`) before the shared Step 2.2M merge gate.
- Step 2.2M converts branch-specific evidence into one normalized scene/object graph before anatomy, object research, Blender, and prompt locks proceed.
- Object research results must be converted into scale witnesses, prompt locks, verify tests, and audit checks.
- Human-enterable scale transfer must carry entry fit, XYZ volume, capacity class, occupant anchor, module repetition, final composite verdict, and the approved visual guide composite through Step 2.5, Step 2.8, Step 2.9, and Step 8.
- Style wrappers may enrich only after base structure locks pass.
- If a correction protects one element, record what neighboring objects must not break.

## VERIFY gate

Purpose: pre-image checks before handoff.

Required outputs:

- `VERIFY_OBJECT_DISTORTION_TEST`
- `VERIFY_HERO_OBJECT_SCALE_TEST`
- `VERIFY_OBJECT_RESEARCH_TRANSFER_TEST`
- `VERIFY_STYLE_TARGET_TEST`
- `VERIFY_PROMPT_CONFLICT_TEST`
- `VERIFY_GATE_STATUS: pass`

Rules:

- Verify the final prompt, not only the spec.
- Fail if object research facts do not appear as visual prompt locks.
- Fail if a tram/train/bus/room/building passes only because protagonist height is below entry height; the composite human-enterable verdict must also pass XYZ volume, capacity class, occupant anchors, and module repetition.
- Fail if action/drama/camera words can overpower scale or object geometry locks.
- Fail if Redjuice or another style is only a label and not actionable line/plane/material grammar.

## AUDIT gate

Purpose: command compliance and post-image visual accountability.

Required outputs:

- `AUDIT_PRE_IMAGE_COMMAND_AUDIT`
- `AUDIT_PRE_IMAGE_NON_NEGOTIABLE_AUDIT`
- `AUDIT_POST_IMAGE_VISUAL_AUDIT_PLAN`
- `AUDIT_RERENDER_TRIGGERS`
- `AUDIT_GATE_STATUS: pass`
- `IMAGE_HANDOFF_GATE_STATUS: pass`

Rules:

- Pre-image audit must check each user command and each non-negotiable.
- Post-image audit plan must name the visible tests that will be run after generation.
- Rerender triggers are mandatory: no pass can be claimed if scale, object distortion, command compliance, or style fidelity fail.
- For visual tasks, save the post-image verdict JSON under `.omx/state/<scope>/ralph-progress.json` before the next iteration only after an image exists and `POST_IMAGE_VERDICT_REQUIRED: yes`.
- Prompt-only first generation may pass pre-image handoff without `POST_IMAGE_VISUAL_VERDICT_*`; source/previous image diagnostics belong to Step 0A.
- Render-bound first generation may not pass pre-image handoff while `USER_VISUAL_GUIDE_APPROVAL_STATUS` is `pending` or `needs_revision`; the approved `VISUAL_GUIDE_COMPOSITE_PATH` and `IMAGE_INPUT_STACK_PLAN` are part of the pre-image gate, not post-image QA.
- Render-bound first generation also needs an actual image-generation conditioning package: source image + approved visual guide composite + optional clay/lineart/depth inputs. If the runtime cannot attach those images, mark `IMAGE_GEN_STRUCTURE_CONDITIONING_MODE: blocked_text_only` and do not claim true ControlNet-like conditioning.

## Deduplication / single-source lesson

The qe-framework issue about duplicate skill exposure is treated as a structural warning: duplicated rules create noise and drift. In this project:

- theory files hold principles
- the template holds required fields
- the validator enforces fields and gates
- `main-process.md` maps the lifecycle
- derived style wrappers may add style rules but must not duplicate or override base structural gates

If a rule exists in multiple locations, make one location authoritative and reference it from the others.
