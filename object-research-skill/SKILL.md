---
name: object-research-skill
description: Research, normalize, store, and reuse visual object knowledge for illustration backgrounds, props, furniture, machinery, architecture, and visibility-critical anatomy such as age-band body bases, sex overlays, hands, and fingers. Use this skill whenever the user asks to research a background object, build an object card, make props believable, collect visual reference structure, create a reusable object library, save object knowledge for later illustration use, or lock down anatomy / hand construction before rendering. Trigger phrases include "오브젝트 조사해줘", "배경 오브젝트 구조 분석해줘", "이 소품 어떻게 생겼는지 정리해줘", "레퍼런스용 오브젝트 카드 만들어줘", "손 구조 조사해줘", "손가락 파지 정리해줘", "연령대별 인체 구조 정리해줘", "성별 anatomy 정리해줘", "object research", "prop reference", "build an object card", and "background object library". Also trigger when the user names specific environmental props, structures, age-band anatomy needs, sex-coded body reads, or visible hand/finger poses and wants believable form, material, silhouette, grip, or reuse across future scenes without explicitly naming the skill. Prefer this skill over illustrate-skill when the task is object lookup, object research, library update, or scene-recipe building rather than full-scene illustration planning.
---

# Object Research Skill

Use this skill to turn object reference needs into reusable structured knowledge for illustration work.
Keep procedure here. Load schema and domain details from `references/` only when needed.

## Default load order

1. Read `references/domain_context.md`.
2. Read `references/object-card-schema.md`.
3. Read `references/scene-recipe-schema.md` only when a repeatable environment cluster is relevant.

## Modes

Pick one mode explicitly.

- `LOOKUP`: find existing object cards or scene recipes before doing new research
- `RESEARCH`: investigate a missing or weakly-covered object and create/update a card
- `RECIPE`: build or update a reusable scene recipe from multiple object cards

If the user mixes modes, do them in this order:

1. `LOOKUP`
2. `RESEARCH` for gaps
3. `RECIPE` if the environment pattern repeats

## Core workflow

1. Normalize the request into:
   - `scene_intent`
   - `scene_type`
   - `required_objects`
   - `style_mode`
   - `priority`
   - `visible_hand_requirements` when hands / fingers / grips matter
   - `anatomy_requirements` when age band / sex classification / body baseline must be locked
2. Query the local library before browsing.
3. Reuse existing cards when they are sufficient.
4. If a needed card is missing, stale, or too generic, research it.
5. Convert findings into draw-ready structure, not raw notes.
6. Save or update the card in `illustration-library/object_cards/`.
7. If the same environment repeatedly implies a stable object set, create or update a scene recipe in `illustration-library/scene_recipes/`.
8. If this research is serving an `illustrate-skill` Step 2.5 handoff for a render-bound scene, create or update an artifact from `templates/object-research-artifact-template.md` and return its path.
9. For render-bound handoffs, also create an invocation log from `templates/object-research-invocation-log-template.md`, record its path in the artifact field `INVOCATION_LOG_PATH`, and keep it updated, preferably via `python scripts/log_object_research_invocation.py ...`.
10. Return a compact result the calling illustration workflow can immediately apply.
11. For the updated illustrate workflow, organize render-bound results by lane:
   - anatomy
   - core scale anchors
   - hard-surface background / architecture
   - weapon / prop
   - effects / text
12. Unknown or weakly named objects must be resolved by asking, researching, removing, replacing with a known object, intentionally abstracting with a declared function, or stopping the render-bound flow. Do not convert unknowns into random patterns, fake signage, fake machinery, or unidentified texture.

## LOOKUP mode

1. Normalize object names and likely aliases.
2. Search `illustration-library/object_cards/` first.
3. If age-band anatomy, sex classification, hands, or fingers are part of the ask, search anatomy-style cards first instead of treating the figure as a generic body blob.
4. When the ask is a human figure, prefer a layered lookup:
   - age-band body base
   - sex overlay
   - current body-type baseline
   - hand submodule
5. Search `illustration-library/scene_recipes/` if the scene type suggests a reusable environment pattern.
6. Return:
   - matched cards
   - missing objects
   - stale or weak cards that should be refreshed

## RESEARCH mode

1. Start from the object's function in the scene, not from ornament alone.
2. When factual structure matters, use credible sources and clearly separate:
   - observation
   - inference
3. When silhouette or visual breakdown matters, use image/reference search to inspect:
   - front
   - side
   - 3/4 views
   - repeated parts
   - support logic
4. If the object is an age-band body card or sex overlay, also inspect:
   - head-to-body ratio
   - ribcage vs pelvis block relation
   - shoulder vs hip read
   - arm and leg length bias
   - hand and foot scale relative to the chosen age band
   - what remains stable under anime simplification
5. If the object is a hand or finger pose, also inspect:
   - palm vs back-of-hand view
   - thumb base direction
   - finger grouping
   - knuckle rhythm
   - contact / pressure against held props
   - foreshortening overlap order
6. Extract only what improves drawability:
   - silhouette
   - primary forms
   - dimensional envelope
   - thickness logic
   - support logic
   - material behavior
   - angle cues
   - style variation hooks
   - and, for hands, palm block / thumb wedge / finger grouping / taper / contact logic
   - and, for anatomy bases / overlays, age-coded proportion logic and sex-coded silhouette tendencies without turning them into rigid stereotypes
7. Write or update the object card using `references/object-card-schema.md`.
8. Add source notes and confidence.

## RECIPE mode

1. Use this only when multiple cards repeatedly belong to the same environment type.
2. Build a scene recipe using `references/scene-recipe-schema.md`.
3. Store:
   - common object set
   - layout roles
   - density rules
   - focal support roles
   - lighting implications
4. Keep recipes modular. They should reduce repeat research, not hard-code one composition.

## Working rules

- Library lookup comes before web research.
- Save normalized knowledge, not scraped dumps.
- Prefer one object per card.
- Keep cards reusable across scenes.
- Distinguish observed facts from stylistic inference.
- Include aliases so future lookup does not miss the card.
- Treat visible focal hands and finger poses as researchable structure, not as “too organic to card”.
- Treat human figure anatomy as a layered card stack when needed: age-band body base first, sex overlay second, hand submodule third.
- For prop-holding hands, the hand card and the prop card should agree on contact logic.
- For anatomy-driven figure work, the hand card must agree with the chosen body base on hand size, wrist thickness, and arm-chain logic.
- For `illustrate-skill` handoffs tied to final rendering, persist the object-research result in a standalone artifact file before handing control back.
- For `illustrate-skill` handoffs tied to final rendering, persist an invocation log that proves local lookup happened first and points back to the object artifact.
- If the request is really full-scene planning, hand control back to `illustrate-skill` after returning cards or recipes.

## Return shape

Return concise, application-ready outputs:

- `research_lanes`
- `matched_cards_by_lane`
- `new_or_updated_cards`
- `missing_or_weak_cards_by_lane`
- `unknown_object_triage_result`
- `scene_recipe_updates`
- `per_object_draw_locks` for silhouette, structure, anatomy base / overlay logic, hand/finger grouping when relevant, materials, and density
- `scale_perspective_locks`
- `relationship_check_notes`
- `generation_prompt_locks`
- `do_not_fake_policy`
- `artifact_path` when a handoff artifact was created
- `invocation_log_path` when a render-bound handoff log was created
