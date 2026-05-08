---
name: reference-copy-skill
description: Analyze a local reference image set and generate or refine a new reference-derived illustration style wrapper skill while preserving the base illustrate-skill unchanged. Use when Codex needs to turn a reference folder into a reusable new style skill, build a derivative 그림체 스킬 from references, update an existing derived style wrapper with more references, or handle an illustrate-skill handoff whose real task is “make me a new style skill from these references.” Trigger phrases include "레퍼런스로 새 스킬 만들어줘", "새 그림체 스킬 만들고 싶어", "reference copy skill", "reference-derived style skill", "reference style skill builder", "style skill builder", "이 폴더 보고 스타일 스킬 생성해줘", "새 일러스트레이트 스킬 파생해줘", and "reference set을 style wrapper로 만들어줘".
---

# Reference Copy Skill

Use this skill to create or refine a **reference-derived illustration wrapper skill** from a local reference set.
Do not replace or fork `illustrate-skill` unless the user explicitly asks for a destructive rewrite.

`reference-style-skill-builder` is the deprecated legacy name for this workflow; absorb those requests here.

## Default load order

1. Read `references/domain_context.md`.
2. Read `references/invocation-routing.md`.
3. Read `references/derived-skill-structure.md`.
4. Read `references/pixel-plane-reference-analysis.md`.
5. Read `references/style-learning-pipeline.md`.
6. Read `references/style-pack-schema.md`.
7. Read `references/reference-analysis-checklist.md`.

## Core rule

This skill builds **reference-derived wrappers** from reusable visual grammar.

Pixel-plane analysis is the official first-pass method for all reference analysis in this workspace. Measure the reference pixels before writing style rules, then translate the measured value / bloom / palette / edge / grid evidence into visual grammar. Do not replace the visual judgment pass; use the pixel-plane report as the evidence floor.

Project default assumption: the user's reference sets are usually **AI-generated style-study outputs**, not original artist source art, unless the user says otherwise. Treat direct source-image imitation risk as lower under that provenance, but still prevent overfitting to a single reference image and still translate the set into repeatable drawing grammar rather than name-based mimicry.

The output should:

- preserve `illustrate-skill` as the base process
- generate a new wrapper under `derived-style-skills/`
- keep style rules local to that derivative
- separate observation, inference, and anti-generic constraints
- extract style as **visual grammar**: composition pressure, value design, face/eye handling, line/shape language, color control, texture density, motifs, and failure patterns
- compile style into production image language through an `AESTHETIC_RENDER_BRIEF`, not raw analysis prose
- declare a `STYLE_APPLICATION_BOUNDARY`: style affects rendering and mood, while base structure, object research, camera, perspective, scale, approved composites, and hard locks remain authoritative

## Modes

Pick one mode explicitly.

- `ANALYZE`: inspect the reference set and extract reusable style rules
- `GENERATE`: create a new derivative wrapper skill from approved analysis
- `REFINE`: improve an existing derived wrapper with new references or stronger routing / anti-drift rules

If the user gives a reference folder and wants the final skill immediately, run:

1. `ANALYZE`
2. `GENERATE`

If a wrapper already exists and the user wants it improved, run:

1. `ANALYZE`
2. `REFINE`

## ANALYZE mode

1. Inspect all provided references or the specified reference folder.
2. Run the pixel-plane reference analysis from `references/pixel-plane-reference-analysis.md`. Use full source resolution by default; if the folder has more than 10 images, measure in batches of 10 and merge the batch JSON reports.
3. Record `PIXEL_PLANE_ANALYSIS_REPORT`, `PIXEL_PLANE_ANALYSIS_JSON`, and `PIXEL_PLANE_VISUAL_GRAMMAR_SYNTHESIS` paths. If measurement is impossible, record why and mark the analysis as provisional rather than silently falling back to captions.
4. Record `AI_REFERENCE_PROVENANCE_NOTE` when the references are user-provided AI outputs or otherwise non-original style studies.
5. Build a `REFERENCE_STYLE_OBSERVATION_MATRIX` aligned to the base illustration steps:
   - intent / mood
   - composition / silhouette / focal pressure
   - value / lighting / mass grouping
   - face / emotion / eye grammar
   - line / shape / edge control
   - color / accents / palette release
   - texture / density / surface treatment
   - motifs
   - anti-drift / do-not patterns
6. Extract `STYLE_GRAMMAR_EXTRACTION` from repeated traits only. Prefer measured pixel-plane evidence, ratios, hierarchy, placement rules, edge behavior, density behavior, and palette logic over image captions.
7. Run `COPY_RISK_FILTER` as an anti-overfit transform: do not copy a single reference composition, pose, costume, exact symbol arrangement, or accidental artifact; preserve reusable grammar.
8. Define `STYLE_APPLICATION_BOUNDARY`: style may bend mood/rendering, but must not override base structure, object research, perspective math, scale hard locks, user-approved visual guide composites, or final scene requirements.
9. Compile an `AESTHETIC_RENDER_BRIEF` for image generation: compact natural visual language, no schema jargon, no validator prose, no field-name leakage.
10. Separate:
   - direct observation
   - inferred preference
   - production rule
   - anti-generic / anti-overfit rule
11. Write:
   - `style-pack.md` draft
   - `reference-index.md`
   - pixel-plane report and visual-grammar synthesis
   - optional deeper analysis notes when line/plane grammar matters

## GENERATE mode

1. Choose a stable slug for the derivative skill.
2. Create a folder under:
   - `derived-style-skills/<slug>/`
3. Generate:
   - `SKILL.md`
   - `references/domain_context.md`
   - `references/style-pack.md`
   - `references/reference-index.md`
   - optional deep analysis files when needed
4. The derivative skill must be a **thin wrapper**:
   - it loads the base illustration process
   - then loads its own style pack
   - then applies style-specific deltas without mutating the base skill
   - then hands final wording to the base final-prompt compiler / aesthetic recovery path
5. Explicitly state:
   - the base process was preserved
   - the derivative is reference-derived from visual grammar
   - the derivative should resist generic model-default drift
   - style cannot override camera, perspective, scale, object, source-image, composite, or handoff locks

## REFINE mode

1. Read the existing derivative skill and its local references.
2. Determine whether the update is:
   - new evidence from references
   - stronger style grammar extraction
   - better aesthetic render brief wording
   - stronger style application boundary
   - stronger anti-generic / anti-overfit rules
   - better trigger / routing behavior
3. Update only the derivative skill and its local references.
4. Leave `illustrate-skill` unchanged unless the user explicitly asks to evolve the base methodology.

## Handoff logic from illustrate-skill

If `illustrate-skill` receives a request whose real task is **“make a new style skill from references”** instead of planning one scene, this skill should be called.

Use this skill when the user wants:

- a new style wrapper generated from a reference folder
- a style pack extracted from multiple reference images
- a derivative illustration skill added under `derived-style-skills/`
- an existing derived wrapper updated with more references

Do **not** use this skill when the user only wants a single image planned in an existing style.

## Working rules

- Preserve the base skill as the stable original method.
- Treat the derivative skill as a wrapper, not a replacement.
- Keep derivative `SKILL.md` short and procedural.
- Put style evidence and analysis into local `references/`.
- Use progressive disclosure:
  - `SKILL.md` = routing + workflow
  - `references/` = style knowledge
- Align all observations to the base step model so the wrapper remains compatible with the original process.
- Never let style-wrapper wording weaken existing `illustrate-skill` structure locks; if style conflicts with approved composite scale or perspective, the structural lock wins.

## Output contract

Return:

- derivative skill path
- style-pack summary
- reference index summary
- style grammar summary
- aesthetic render brief summary
- style application boundary summary
- note describing whether this was:
  - analyze only
  - generate
  - refine
- explicit confirmation that `illustrate-skill` remained preserved
