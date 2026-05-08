# Illustration Main Process

## Purpose

This document defines the main illustration workflow for this workspace.
The workflow is theory-first:

`load stage theories -> derive decision rules -> execute step -> produce output -> run gate check`

Do not execute a step blindly. Before each step, review the theory blocks mapped to that step and extract concrete decision rules.

## Current Theory Storage Model

- Primary unit: individual theory blocks
- Secondary mapping: process-step linkage

Current mapped theory:

- `references/theory-01-intent.md` -> `STEP 1: INTENT`
- `references/theory-02-composition-silhouette.md` -> `STEP 2: SILHOUETTE & COMPOSITION`, `STEP 2.1: PERSPECTIVE RIG`
- `references/theory-02b-balance-cog.md` -> `STEP 2: SILHOUETTE & COMPOSITION`
- `references/theory-02c-anatomy-structure-gate.md` -> `STEP 2.3: ANATOMY STRUCTURE GATE`, `STEP 2.7: ANATOMY-ON-OBJECT RELATIONSHIP CHECK`
- `references/theory-02d-geometric-blockout.md` -> `STEP 2.3: ANATOMY STRUCTURE GATE`, `STEP 2.8: 3D BLOCKOUT / MODELING CONTRACT`, `STEP 2.9: IMAGE TRANSLATION LOCK`
- `references/theory-02e-object-density-human-priority.md` -> `STEP 2.2: OBJECT INVENTORY`, `STEP 2.3: ANATOMY STRUCTURE GATE`, `STEP 2.8: 3D BLOCKOUT / MODELING CONTRACT`, `STEP 2.9: IMAGE TRANSLATION LOCK`
- `references/theory-02f-structural-scale-capacity-verdict.md` -> `STEP 2.1: PERSPECTIVE RIG`, `STEP 2.3: ANATOMY STRUCTURE GATE`, `STEP 2.8: 3D BLOCKOUT / MODELING CONTRACT`, `STEP 2.9: IMAGE TRANSLATION LOCK`, `STEP 4: FACE`, `STEP 5: LINE & SHAPE`, `STEP 8: FINAL CHECK`
- `references/theory-02g-occlusion-layer-separation.md` -> `STEP 2.2: OBJECT INVENTORY`, `STEP 2.3: ANATOMY STRUCTURE GATE`, `STEP 2.6: OBJECT RELATIONSHIP CHECK`, `STEP 2.8: 3D BLOCKOUT / MODELING CONTRACT`, `STEP 2.9: IMAGE TRANSLATION LOCK`, `STEP 5: LINE & SHAPE`, `STEP 8: FINAL CHECK`
- `references/theory-02h-object-distortion-command-verdict.md` -> `STEP 2.1: PERSPECTIVE RIG`, `STEP 2.2: OBJECT INVENTORY`, `STEP 2.6: OBJECT RELATIONSHIP CHECK`, `STEP 2.8: 3D BLOCKOUT / MODELING CONTRACT`, `STEP 2.9: IMAGE TRANSLATION LOCK`, `STEP 8: FINAL CHECK`
- `references/theory-02i-all-humanoids-anatomy-perspective-scale.md` -> `STEP 2.1: PERSPECTIVE RIG`, `STEP 2.2: OBJECT INVENTORY`, `STEP 2.3: ANATOMY STRUCTURE GATE`, `STEP 2.8: 3D BLOCKOUT / MODELING CONTRACT`, `STEP 2.9: IMAGE TRANSLATION LOCK`, `STEP 8: FINAL CHECK`
- `references/theory-02j-camera-class-scale-gate.md` -> `STEP 2: SILHOUETTE & COMPOSITION`, `STEP 2.1: PERSPECTIVE RIG`, `STEP 2.8: 3D BLOCKOUT / MODELING CONTRACT`, `STEP 2.9: IMAGE TRANSLATION LOCK`, `STEP 8: FINAL CHECK`
- `references/theory-03-lighting-value.md` -> `STEP 3: VALUE DESIGN`
- `references/theory-04-face-eyes.md` -> `STEP 4: FACE`
- `references/theory-04a-face-emotion-patterns.md` -> `STEP 4: FACE`
- `references/theory-05-line-shape.md` -> `STEP 5: LINE & SHAPE`
- `references/theory-05a-hands-fingers.md` -> `STEP 5: LINE & SHAPE`
- `references/theory-06-color-palette-point.md` -> `STEP 6: COLOR & ACCENT`
- `references/theory-07-texture-density.md` -> `STEP 7: TEXTURE`
- `references/theory-08-final-check-correction.md` -> `STEP 8: FINAL CHECK`
- `references/theory-08a-final-prompt-compiler-aesthetic-recovery.md` -> `STEP 8: FINAL PROMPT COMPILER / AESTHETIC RECOVERY`

This means theories are not stored only as step summaries. They are kept as distinct theory units and then attached to one or more process steps.

## Global knowledge

Read these references when needed:

- `references/domain_context.md` for user-specific workflow expectations
- `references/style-guide.md` for the workspace art direction

## Review responsibility overlay

- In `SPEC`, the system must produce a complete staged plan with explicit reasoning hooks, then let validation / pipeline checks judge structure and completeness.
- In `CRITIQUE`, the user's success/failure judgment is primary whenever it is provided.
- The system's role in `CRITIQUE` is diagnostic:
  - explain what supports the user's read
  - explain what conflicts with the user's read
  - suggest the smallest useful next change
- The system may disagree, but it must label that disagreement as analysis, not as an override of the user's verdict.


## PIVA Lifecycle Overlay

Render-bound SPEC runs use `references/pipeline-plan-implement-verify-audit.md` as the outer lifecycle. The Step 0-8 process is the IMPLEMENT body, not the whole workflow.

1. PLAN: capture user commands, non-negotiables, object/anatomy/scale witnesses, intake route, and previous failures before Step 1.
2. IMPLEMENT: execute Step 0-8 while mapping object research and style rules into prompt locks and verdict triggers.
3. VERIFY: pre-image proof that object distortion, protagonist/object scale, object-research transfer, style target, and prompt conflicts are resolved.
4. AUDIT: pre-image command audit plus post-image visual audit plan and rerender triggers.
5. PRE-IMAGE HANDOFF: allowed only when PLAN/IMPLEMENT/VERIFY/AUDIT gates pass and `PRE_IMAGE_HANDOFF_READY: yes`.
6. POST-IMAGE ACCEPTANCE: `POST_IMAGE_VISUAL_VERDICT_*` is required only after a generated image exists and `POST_IMAGE_VERDICT_REQUIRED: yes`.

## Process Overview

0. `STEP 0: ROUTE GATE`
0A. `STEP 0A: EXISTING IMAGE DEVELOPMENT INTAKE`
0B. `STEP 0B: PROMPT-ONLY INTAKE`
1. `STEP 1: INTENT`
2. `STEP 2: SILHOUETTE & COMPOSITION`
2.1 `STEP 2.1: PERSPECTIVE RIG`
2.2 `STEP 2.2: OBJECT INVENTORY FROM PERSPECTIVE`
2.2M `STEP 2.2M: MERGE GATE / NORMALIZED SCENE GRAPH`
2.3 `STEP 2.3: ANATOMY STRUCTURE GATE`
2.4 `STEP 2.4: OBJECT KNOWLEDGE QUERY PLAN`
2.5 `STEP 2.5: OBJECT RESEARCH HANDOFF`
2.6 `STEP 2.6: OBJECT RELATIONSHIP CHECK`
2.7 `STEP 2.7: ANATOMY-ON-OBJECT RELATIONSHIP CHECK`
2.8 `STEP 2.8: 3D BLOCKOUT / MODELING CONTRACT`
2.9 `STEP 2.9: IMAGE TRANSLATION LOCK`
3. `STEP 3: VALUE DESIGN`
4. `STEP 4: FACE`
5. `STEP 5: LINE & SHAPE`
6. `STEP 6: COLOR & ACCENT`
7. `STEP 7: TEXTURE`
8. `STEP 8: FINAL CHECK`

## Standard Step Format

Each step should be executed in the following order:

1. `THEORY`
2. `DECISION RULE`
3. `EXECUTION`
4. `OUTPUT`
5. `CHECK / GATE`

If the gate fails, revise the same step before moving forward.

## STEP 0: ROUTE GATE

### Decision Rule

Before Step 1, choose exactly one active intake branch:

- `image_development`: the user provides, references, or implicitly continues an already-generated/source image.
- `prompt_only`: the user asks for a first-generation image from text/prompt/spec only.

The inactive branch must be `not_applicable`. Existing/previous image verdicts belong to Step 0A, not to `POST_IMAGE_VISUAL_VERDICT_*`. Post-image verdict fields are reserved for accepting/rejecting an image generated after the current spec handoff.

### Execution

1. Set `INPUT_ROUTE`.
2. Set `EXISTING_IMAGE_INPUT` and `PROMPT_ONLY_GENERATION` as opposites.
3. Fill only the active branch:
   - Step 0A for existing/source image development.
   - Step 0B for prompt-only first generation.
4. Record the inactive branch as `not_applicable`.
5. Continue to Step 1 and Step 2.2, then merge both possible inputs at Step 2.2M.

### Output

- `input_route`
- `route_reason`
- `existing_image_input`
- `prompt_only_generation`
- `active_intake_branch`
- `inactive_branch_policy`

### Check / Gate

- exactly one branch is active
- source/previous image verdicts are not required for prompt-only generation
- post-image verdict fields are not required before first image generation
- route fields agree with `SOURCE_IMAGE_UPGRADE`
- image-development route states whether the source pixels/control reference can actually condition generation; if not, the run is labeled `prompt_only_fallback` or blocked rather than claiming true image development

## STEP 0A: EXISTING IMAGE DEVELOPMENT INTAKE

### Decision Rule

Use this branch only when the current request develops an already-generated/source image. Diagnose that image before turning it into the common scene graph.

### Execution

1. Identify the source/previous image reference.
2. State whether source pixels/control references can actually be supplied to image generation. If not, mark the generation path as descriptive reinterpretation / prompt-only fallback.
3. Summarize the image verdict: scale, hand/finger topology, object distortion, command compliance, style, and focal read.
4. List concrete source-image objects.
5. Split them into preserve / change / remove.
6. Map visible failures to likely causes and prevention rules.
7. Send the resulting object and preservation locks into Step 1, Step 2.2, and Step 2.2M.

### Output

- `source_image_reference`
- `previous_image_visual_verdict_summary`
- `source_image_objects_present`
- `preserve_objects`
- `change_objects`
- `remove_objects`
- `failure_cause_map`
- `previous_image_lessons`
- `route_a_output_to_step_1_2_2`

### Check / Gate

- the source image's concrete objects are named before object research
- preserve/change/remove intent is explicit
- failure lessons are prompt-actionable
- `POST_IMAGE_VISUAL_VERDICT_*` is not used as the source-image verdict
- if actual conditioning is unavailable, later prompts are framed as reinterpretation from observed facts rather than source-conditioned edit promises

## STEP 0B: PROMPT-ONLY INTAKE

### Decision Rule

Use this branch only when no existing image is being developed. Build candidates and assumptions from text without requiring source-image or post-image evidence.

### Execution

1. Extract explicit prompt objects.
2. Infer environment, perspective, anatomy, and scale candidates.
3. Record assumptions made without asking.
4. Mark unknowns that must be resolved by Step 2.4/2.5 or removed/abstracted.
5. Send the prompt-derived candidates into Step 1, Step 2.2, and Step 2.2M.

### Output

- `prompt_object_candidates`
- `prompt_implied_environment`
- `prompt_implied_anatomy`
- `prompt_ambiguity_assumptions`
- `route_b_output_to_step_1_2_2`

### Check / Gate

- no source-image verdict is required
- assumptions are explicit rather than silently invented
- unknown objects are routed to research/triage
- the branch produces enough material for Step 1 and Step 2.2

## STEP 1: INTENT

### Theory

- `references/theory-01-intent.md`

### Decision Rule

Before execution, define:

- time or lighting
- environment
- subject role
- current action
- primary emotion axis (1-2 emotions)
- audience feeling

The intent sentence must be concrete and imageable.
Reject vague wording such as "pretty", "cool", or "nice" if it does not describe scene meaning.

### Execution

Input example:

- mood: `cold, dangerous smile`
- scene: `gothic portrait, neon laboratory background`

Procedure:

1. Answer the 5 intent questions internally:
   - when is this scene
   - where is this scene
   - what is the character doing
   - what 1-2 emotions dominate
   - what should the viewer feel first
2. Generate one intent line using a stable sentence pattern.
3. Tag the sentence into:
   - `environment`
   - `time_or_lighting`
   - `role`
   - `action`
   - `emotion_axis`
   - `audience_feeling`
4. Store these tags for Steps 2, 3, and 4.

### Output

- `scene_intent_sentence`
- `environment`
- `time_or_lighting`
- `role`
- `action`
- `emotion_axis`
- `audience_feeling`

### Check / Gate

All conditions must pass:

- the subject is identifiable
- where / when / what is visible in the sentence
- the emotion axis is narrowed to 1-2 emotions
- the audience feeling is explicit
- the sentence contains concrete nouns or verbs

If any condition fails, rewrite Step 1 before continuing.

## STEP 2: SILHOUETTE & COMPOSITION

### Theory

- `references/theory-02-composition-silhouette.md`
- `references/theory-02b-balance-cog.md` for grounded standing / leaning balance checks

### Decision Rule

- determine first read / focal placement
- determine composition type from intent:
  - rule of thirds
  - center / symmetry
  - asymmetry / diagonal tilt
- determine dominant black-mass placement
- determine negative-space ratio
- determine gaze-flow direction and return path
- determine whether visible hands are focal, support, or safely abstract
- determine whether individual finger-chain / prop grip logic needs explicit research
- when the pose is grounded, determine:
  - support leg
  - balance line
  - body-mass fall over the foot base
  - counter-balance between shoulders and pelvis
- when the scene is full-body, standing, braced, leaning, or uses stylized/exaggerated proportions:
  - make the support logic explicit in the written output
  - do not leave balance as an unstated intuition

### Execution

1. Read the Step 1 intent output.
2. Decide the focal point.
3. Classify the emotion as stable vs tense.
4. Generate `3-5` small grayscale thumbnails.
5. In each thumbnail, block only:
   - character position
   - large black mass
   - major leading lines
6. Choose the thumbnail that best matches the scene intent.
7. Build the silhouette blocking from that choice.
8. If the pose is standing, braced, or leaning:
   - mark head, torso, pelvis, and foot anchors
   - estimate the body-mass center
   - drop a balance line toward the support foot or foot base
   - adjust feet, torso tilt, or pelvis tilt until the pose reads as physically supportable
9. List visible hands and classify them as:
   - not visible
   - visible but safely simplified
   - visible and research-critical
10. If hands are visible, write:
    - palm / silhouette read
   - individual thumb / index / middle / ring / little finger-chain read
   - per-hand detail budget: focal/support/background role, minimum reduced-size readability, and nearby detail to reduce first
   - finger-topology fail conditions: fused claw, black lump, melted glove, decorative noise, blood/cloth smear, or unreadable scribble
11. If the scene contains structurally uncertain props, signage, vehicles, machinery, architecture, source-image objects, or visible hands/fingers that are focal / expressive / foreshortened / gripping:
   - list them explicitly before Step 2.5
   - do not continue to Step 3 on guesswork alone
12. If the scene shows a meaningful amount of human figure information beyond a close face crop, route the pose through Step 2.3 before Step 2.5 so age band, sex classification, limb-chain logic, and hand-submodule logic are locked.
13. Add shard, ribbon, or hair flow only after the large masses, hand read, and pose balance read clearly.

Example directional setup when the intent calls for pressure and danger:

- place character at `center-right`
- place a large black mass behind head and shoulders
- flow hair and ribbons in an `S-curve` toward `bottom-left`
- add sharp triangular shards around the character

### Output

- thumbnail set
- chosen composition type
- character position
- camera angle
- visible hands and poses
- black-mass map
- negative-space balance
- flow-direction map
- hand silhouette note
- individual finger-chain note
- hand detail budget
- finger-topology chain lock
- finger-topology fail conditions
- supporting-leg note
- balance-line note
- shoulder/pelvis tilt note

### Check / Gate

- silhouette readable at thumbnail size
- focal area is not swallowed by background
- head / body / arm / prop shapes remain separable
- if hands are visible, the hand silhouette and each finger chain are readable enough that they do not collapse into mitten shapes or fused groups
- hand existence alone does not pass; each visible hand needs readable palm/thumb/finger topology or an explicit overlap/contact cue
- shard flow supports the face instead of competing with it
- gaze stays inside the frame instead of escaping outward
- for grounded poses, the mass reads as supported by the chosen foot or base
- for grounded poses, instability reads intentional rather than anatomically broken
- for full-body or exaggerated grounded poses, the written support notes explain the pose well enough that another artist could reconstruct the balancing logic

## STEP 2.1: PERSPECTIVE RIG

### Theory

- `references/theory-02-composition-silhouette.md`
- `references/theory-02f-structural-scale-capacity-verdict.md` for scale-anchor judgment, capacity anchors, and verdict handoff
- `references/theory-02h-object-distortion-command-verdict.md` for protagonist-to-object scale parity and all-object distortion bans
- `references/theory-02i-all-humanoids-anatomy-perspective-scale.md` for comparing the protagonist against every visible human/humanoid/humanoid monster by perspective depth plane

### Decision Rule

Before listing dense background objects, lock the camera and perspective system:

- camera position and view height
- horizon line
- vanishing point count / placement
- primary depth axis
- support planes and contact planes
- vertical plane locks
- scale anchor objects
- scale-anchor candidate judgment: list possible anchors first, select a baseline, rank anchors by reliability/depth plane, and define ratio tests
- functional-size tests: adult-to-door, head-to-window, body-to-vehicle, roof-to-passenger-cabin, prop-to-hand, parapet-to-body
- irreversible structure registry: every named object/anatomy instance that may not be omitted, fused, absorbed, resized, warped, bent, melted, or reinterpreted
- hero/object scale relationship check: how the protagonist compares with visible humans, vehicles, doors, windows, props, architecture, creatures, and repeated modules
- perspective fail conditions

### Output

- `camera_position`
- `horizon_line`
- `vanishing_points`
- `primary_depth_axis`
- `support_planes`
- `vertical_plane_locks`
- `scale_anchor_objects`
- `scale_anchor_candidates`
- `scale_baseline_selection`
- `scale_anchor_ranking`
- `scale_ratio_judgment_method`
- `near_plane_anchor_check`
- `depth_plane_scale_transfer`
- `functional_size_tests`
- `scale_anchor_fail_conditions`
- `scale_anchor_verdict_handoff`
- `hero_object_scale_relationship_check`
- `irreversible_structure_registry`
- `contact_planes`
- `perspective_fail_conditions`

### Check / Gate

- the main support plane is named
- the primary depth axis is explicit
- objects that must share perspective are named together
- scale anchors are visible or intentionally implied
- the selected baseline explains why it is more reliable than decorative distant objects
- functional-size tests prove that doors, vehicles, windows, props, and architecture remain usable at human scale
- protagonist scale is compared against object witnesses; visible humans/passengers must read as the same species/adult scale unless depth-plane transfer explains the screen-size difference
- every visible human, humanoid object, and humanoid monster has a depth plane and anatomy classification before scale can pass
- Step 2.1 writes a protagonist/background-humanoid comparison table: protagonist row plus one row per passenger, crowd member, driver, humanoid object, or humanoid monster with depth plane, expected head/body ratio after perspective transfer, comparison witness, and fail trigger
- the verdict handoff names exactly what must fail after generation if scale or separation drifts
- later detail cannot contradict the rig

## STEP 2.2: OBJECT INVENTORY FROM PERSPECTIVE

### Theory

- `references/theory-02-composition-silhouette.md`
- `references/theory-02e-object-density-human-priority.md`
- `references/theory-02g-occlusion-layer-separation.md` for identifying occluder masses before they absorb protected chains
- `references/theory-02h-object-distortion-command-verdict.md` for listing object distortion risks before style or correction passes

### Decision Rule

List objects by perspective plane and role instead of collapsing them into generic texture or atmosphere.

Required categories:

- source-image objects when present
- primary retained objects
- structurally clear objects
- structurally uncertain objects
- foreground frame objects
- support-plane objects
- left / right vertical-plane objects
- overhead-plane objects
- background-depth objects
- effect objects
- text / glyph objects
- unknown-object triage
- occluder-mass inventory: cloak, hood, hair, smoke, blood, glow, wings, creature bodies, black costume texture, background density, or other masses that could absorb protected anatomy/props
- object-density edge-case trigger check:
  - if the scene has a human figure plus many vehicles, architecture, creatures, props, signs, particles, blood, smoke, crowds, or dense background systems, mark the edge case active
  - when active, record which non-human details may be reduced before anatomy is sacrificed

Unknown objects must be resolved by asking, researching, removing, replacing with a known object, intentionally abstracting with a declared function, or stopping the render-bound flow. Do not fake them as random pattern/noise.

### Check / Gate

- every structurally important object has a plane or role
- unknown objects have an action, not a decorative excuse
- text / signage is either researchable or intentionally abstracted as glyph blocks
- source-image upgrades list original-image objects before object research
- every visible human/humanoid/humanoid monster candidate is listed in `VISIBLE_HUMANOID_OBJECT_CANDIDATES` and transferred to Step 2.3 unless explicitly non-anatomical/symbolic
- background passengers/crowds are not allowed to remain only scale witnesses, silhouettes, texture, or crowd noise; they become secondary anatomy objects with a depth-plane scale relation
- high-risk occluder masses are named before value, style, or prompt writing

## STEP 2.2M: MERGE GATE / NORMALIZED SCENE GRAPH

### Decision Rule

Step 2.2M is the single join point for the two Step 0 intake branches. After this point, downstream steps must read one canonical graph rather than branching separately for source-image development and prompt-only generation.

### Execution

1. Confirm `MERGED_FROM_ROUTE` matches `INPUT_ROUTE`.
2. Merge Step 0A or Step 0B outputs with Step 1 intent, Step 2 composition, Step 2.1 perspective, and Step 2.2 object inventory.
3. Produce one object registry by perspective plane.
4. Produce one anatomy candidate registry that transfers all visible/implied humans, humanoids, monsters, hands, and pose-relevant body parts into Step 2.3.
5. Preserve route-specific obligations:
   - image-development runs keep source preservation/change/remove locks.
   - prompt-only runs keep assumptions and unknown-object triage locks.
6. Summarize all object-research triggers before Step 2.4.

### Output

- `merged_from_route`
- `scene_intent_lock`
- `composition_lock`
- `perspective_lock`
- `object_registry_by_plane`
- `anatomy_candidate_registry`
- `source_preservation_lock`
- `prompt_only_assumption_lock`
- `object_research_trigger_summary`
- `merge_conflicts`

### Check / Gate

- there is exactly one canonical object/anatomy graph
- branch-specific evidence has been normalized, not carried forward as competing rules
- source preservation locks and prompt-only assumptions are both placed in explicit fields
- Step 2.3 can proceed without needing to know which Step 0 branch was active except through the normalized fields

## STEP 2.3: ANATOMY STRUCTURE GATE

### Theory

- `references/theory-02c-anatomy-structure-gate.md`
- `references/theory-02d-geometric-blockout.md` for primitive anatomy construction
- `references/theory-02f-structural-scale-capacity-verdict.md` for shape-quality preservation of face, limbs, and lower body
- `references/theory-02g-occlusion-layer-separation.md` for protected-chain visibility under cloak/hair/effect/background overlap
- `references/theory-02i-all-humanoids-anatomy-perspective-scale.md` for registering all visible humans/passengers/crowds/humanoid monsters as anatomy objects

### Decision Rule

- decide whether anatomy gating is required before Step 2.5
- default to anatomy gating when any of the following are true:
  - the scene is full-body, half-body, thigh-up, seated, leaning, jumping, lunging, or twisting
  - arms, shoulders, ribcage, pelvis, legs, or hands materially affect the read
  - the scene uses visible hands that are focal, expressive, foreshortened, or gripping
  - the request implies age-coded or sex-coded body language
  - a human figure appears inside an object-density edge case
- lock:
  - one age-band body base
  - one sex-classification overlay
  - one current default body-type baseline
  - one hand anatomy submodule relationship
- keep hands subordinate to the body decision:
  - hand size must agree with the chosen age band
  - wrist / elbow / shoulder logic must agree with the chosen body structure
  - prop grips must agree with both the hand module and the arm chain
- construct the body as primitive volumes before trusting detail:
  - head sphere / box
  - ribcage box or barrel
  - pelvis box
  - limb cylinder chains
  - sphere joints
  - palm blocks, thumb wedges, and individual thumb / index / middle / ring / little finger cylinders
  - foot wedges aligned to the support plane
- lock lower-body silhouette quality before costume detail:
  - separate thigh, knee, shin, ankle, and boot/foot read
  - left/right leg separation
  - pants/armor/skirt may style the leg but cannot absorb it into black texture or decorative noise
- treat preservation as identity + shape quality + scale relation + relationship; existence alone is not enough
- list every visible human/humanoid/humanoid monster in the anatomy inventory; background people/passengers/crowds are anatomy scale objects, not texture
- write `HUMANOID_ANATOMY_TRANSFER_TABLE` from each Step 2.2 candidate to an anatomy object id, primary/secondary/background role, visible landmarks, allowed simplification, and no-texture-only status
- compare protagonist scale against each secondary human/humanoid using the shared perspective/depth map and the Step 2.1 comparison table
- write a protected-chain visibility table for every visible/partial arm, leg, hand, and prop chain: layer owner, depth relation, required landmarks, separation cue, and occlusion budget

### Execution

1. Read the Step 1 intent and Step 2 composition outputs.
2. Decide whether anatomy gating is required for this scene.
3. If anatomy gating is required, choose:
   - `age_band`
   - `sex_classification`
   - `body_type_baseline`
   - `body_anatomy_base_card`
   - `sex_overlay_card`
   - `hand_anatomy_submodule_card`
4. Write the stylization level explicitly:
   - realistic leaning
   - anime simplified
   - stylized elegant
   - or another concrete mode
5. Lock the body with notes for:
   - head-to-body ratio
   - ribcage to pelvis relation
   - shoulder width
   - hip width
   - arm-chain logic
   - leg-chain logic
   - hand-size relation
   - foot-size relation
6. Reduce the body to a primitive blockout:
   - state the head primitive
   - state the ribcage primitive
   - state the pelvis primitive
   - state the limb cylinder chain
   - state the joint sphere map
   - state hand / foot primitives
   - state primitive anatomy fail conditions
7. If the user request implies a “beautiful / handsome / pretty” default body but no detailed body-type taxonomy, keep the baseline broad and note that the current system uses a beautified default rather than a fine-grained subtype.
8. If anatomy gating is not required, explicitly note why the scene is safe to keep outside the full anatomy stack.

### Output

- anatomy gate required
- age band
- sex classification
- body-type baseline
- body anatomy base card
- sex overlay card
- hand anatomy submodule card
- stylization level
- head-to-body ratio
- ribcage-pelvis relation
- shoulder width note
- hip width note
- limb proportion note
- elbow-wrist chain note
- hip-knee-ankle chain note
- hand size relative note
- foot size relative note
- lower body silhouette lock
- protected anatomy chain visibility
- hand detail budget
- finger topology chain lock
- finger topology fail conditions
- anatomy primitive blockout
- head primitive
- ribcage primitive
- pelvis primitive
- limb cylinder chain
- joint sphere map
- hand / foot primitives
- anatomy primitive fail conditions
- anatomy research decision note

### Check / Gate

- age band is explicit when anatomy gating is required
- sex classification is explicit when anatomy gating is required
- body-type baseline is explicit even if the system is still using one broad beautified default
- ribcage, pelvis, and limb-chain logic are concrete enough that another artist could rebuild the pose skeleton
- anatomy primitives are named before clothing, face, hair, fur, effects, or line detail are trusted
- pants, armor, cloak, shadow, or black costume texture cannot replace the lower-body thigh/knee/shin/ankle silhouette
- protected arm/leg/hand chains must be traceable by visible landmarks rather than guessed from the pose
- the primitive stack explains the torso / pelvis / limb connection before silhouette styling is allowed
- if hands are visible, the hand module is clearly subordinate to the chosen body structure rather than guessed independently
- if object-density edge-case is active, anatomy priority is explicit and non-human density reductions are named
- if anatomy gating is skipped, the written note explains why the scene can safely avoid a full body-structure pass

## STEP 2.4: OBJECT KNOWLEDGE QUERY PLAN

### Theory

- external skill planning surface: `object-research-skill`

### Decision Rule

Before handoff, convert the object inventory into research lanes. Do not let anatomy, vehicles, hard-surface background, weapons, effects, and text compete in one flat list.

Use lanes such as:

- anatomy
- core scale anchors
- container capacity / occupancy scale anchors for trams, trains, buses, cars, elevators, rooms, corridors, interiors, cabins, or other human-containing objects
- hard-surface background / architecture
- weapon / prop
- effects / text

### Output

- research lanes
- local card lookup plan
- existing matched cards
- missing or weak cards
- research-required objects
- query terms
- confidence by object
- draw-ready locks needed
- container capacity research needed
- user checkpoint B object direction

### Check / Gate

- weak cards are named instead of marked “none” by default
- every critical object has a lane
- query terms are specific enough to retrieve or build cards
- the user is asked when an unknown object requires a material branch, naming decision, or removal / replacement decision

## STEP 2.5: OBJECT RESEARCH HANDOFF

### Theory

- external skill handoff: `object-research-skill`

### Decision Rule

Hand off when the scene needs specific background objects, props, machinery, furniture, architectural structures, scale anchors, vehicles, container/occupancy objects, weapons, signage/text policy, age-band anatomy cards, sex overlays, or visible hand/finger structures whose believable form is not already clear.

Default to handoff when any of the following are true:

- the scene includes signage, vehicles, container/occupancy objects, weapons, machinery, or architecture that must read believably
- the source image already contains objects whose structure or material needs confirmation
- Step 2.3 anatomy gating is required for the human figure
- the scene includes visible hands or fingers that are focal, close-up, expressive, foreshortened, or gripping a prop / weapon / cigarette / pipe / accessory
- the Step 2.2 notes include structurally uncertain objects
- the spec depends on environment storytelling that would become vague without concrete object form

Before handoff, define:

- scene intent
- scene type
- required objects
- research lanes used
- style mode
- priority
- unknown-object resolution policy
- container capacity/occupancy questions when any object contains humans: how many adults, what entry/exit scale, what XYZ volume, what repeated modules, what internal volume cues, and how each composite subcheck passes

### Execution

1. Use Step 2.4 lanes as the handoff packet.
2. Query the local object library first.
3. Return matched cards by lane.
4. Research or create missing/weak cards when structure matters.
5. For container objects, return capacity research, dimensions/module count, XYZ volume, human-scale anchors, and compact prompt locks that prevent toy/protagonist-sized reads.
6. For every human-enterable object, return a composite verdict with entry fit, XYZ volume, capacity class, occupant anchor, module repetition, and final human-enterable scale verdict. Entry height alone is only a local subcheck.
7. Return per-object draw locks, scale/perspective locks, relationship notes, and generation prompt locks.
8. If unknown objects remain, ask / research / remove / replace / intentionally abstract with declared function / stop. Do not fake them as random detail.

### Output

- object research request packet
- returned object cards by lane
- missing or weak cards by lane
- unknown-object resolution
- draw-ready locks
- container capacity research, when relevant
- container dimension research, when relevant
- human-enterable composite scale table, when relevant
- entry fit / XYZ volume / capacity class / occupant anchor / module repetition checks, when relevant
- human-enterable scale verdict, when relevant
- container human-scale anchors, when relevant
- container prompt locks, when relevant
- generation prompt locks

### Check / Gate

- every structurally important object is either already understood or backed by a card / declared abstraction
- every anatomy-gated human figure has a body base + sex overlay, and a hand submodule when hands matter
- every visible focal hand is either already understood or backed by a reusable hand/finger card
- unresolved object ambiguity does not remain in critical background or prop forms
- object research returns locks that can be checked in Steps 2.6-2.9
- container objects return occupancy/capacity, XYZ volume, repeated-module, occupant-anchor, and composite pass/fail locks before the scene can pass to 3D blockout

## STEP 2.6: OBJECT RELATIONSHIP CHECK

### Theory

- external skill output from `object-research-skill`
- `references/theory-02g-occlusion-layer-separation.md` for occlusion layer graphs and separation cue planning
- `references/theory-02h-object-distortion-command-verdict.md` for all-object distortion locks and local-correction side-effect checks

### Decision Rule

Check how objects interact before styling them. Correct-looking isolated objects can still fail if scale, occlusion, contact, collision, layer ownership, distortion, axis continuity, or material/light relationships contradict each other. Corrections for hands, style, cloak, blood, or effects must not bend, melt, shrink, enlarge, or replace neighboring objects.

### Output

- scale relation table
- occlusion order
- occlusion layer graph
- protected chain exposure rules
- separation cue plan
- finger occlusion separation rule
- contact and support
- collision check
- material / light interaction
- rigid object geometry locks
- all object distortion lock
- text rendering policy

### Check / Gate

- human / vehicle / creature / architecture scales are mutually believable
- every named object has a distortion fail condition: no bent, warped, melted, resized, fused, or texture-replaced form unless explicitly requested
- occlusion order is explicit enough for image generation
- occluder masses may overlap but cannot own protected anatomy/prop silhouettes
- finger gaps and palm/thumb silhouettes get their own separation cue; reduce cloak/blood/armor/background detail before sacrificing hand topology
- every high-risk overlap has a concrete rim/negative-space/value/color/cast-shadow/contour/mask separation cue
- supports attach to supports: feet to planes, trams to rails, signs to walls, cables to anchors
- swords, rails, windows, signage panels, and vehicles do not melt into effects or texture
- text/signage policy prevents fake typography when exact text cannot be guaranteed

## STEP 2.7: ANATOMY-ON-OBJECT RELATIONSHIP CHECK

### Theory

- `references/theory-02c-anatomy-structure-gate.md`
- external object-research output

### Decision Rule

Place anatomy on top of the object relationship map. The body is not solved until it contacts, grips, balances on, or avoids the surrounding objects believably.

### Output

- body support logic
- anatomy structure apply note
- hand / prop relation
- hand structure apply note
- foot / object relation
- torso action relation
- anatomy-object fail conditions

### Check / Gate

- body mass follows a support or airborne arc
- hands originate from arm chains and grip props with thumb opposition / pressure logic
- feet match support surface scale and perspective
- ribcage, pelvis, and shoulders remain connected under action and clothing
- fail conditions are explicit enough to reject bad generations

## STEP 2.8: 3D BLOCKOUT / MODELING CONTRACT

### Theory

- `references/theory-02d-geometric-blockout.md`
- `references/theory-02f-structural-scale-capacity-verdict.md` for absolute scale ladders, vehicle capacity, and non-sacrifice structure locks
- `references/theory-02g-occlusion-layer-separation.md` for instance mask separation and protected-chain mask review
- `references/theory-02h-object-distortion-command-verdict.md` for object distortion blockout checks and hero/object scale parity

### Decision Rule

Before image translation, express the scene as simple 3D primitives. Real 3D software is optional for spec-only work, but Blender evidence is mandatory for render-bound runs under the project hard-route. The blockout proves camera, support, contact, scale, and major silhouette; it does not automatically become the final aesthetic authority.

For full-body, humanoid, creature, architecture, rooftop, street, vehicle, weapon, or large perspective scenes, Step 2.8 must bind the environment blockout and anatomy blockout into one perspective and scale system before any detail stage may proceed.

For painterly, editorial, anime, symbolic, or mood-first outputs, use Blender as a loose structural guide for edge treatment, mood, value grouping, and detail compression by default. The guide is not loose for solved camera/support/contact/scale relationships, perspective size relationships, anatomy scale logic, protected-chain landmarks, or separate object/anatomy instance ownership. Painterly compression, dark massing, partial occlusion, and softened rigid edges are allowed only inside the declared occlusion budget and only when protected chains remain traceable. Use a stricter guide when the user needs technical/mechanical/product/orthographic precision.

Do not use hieratic or symbolic body-size distortion to show power in ordinary commercial illustration. Authority should come from staging, camera placement, throne elevation, value grouping, costume, gaze, gesture, and detail hierarchy, while adult body scale and perspective remain believable unless the user explicitly requests mythic/symbolic scale.

The construction order is:

1. perspective rig
2. environment primitive blockout
3. anatomy primitive blockout
4. shared perspective grid
5. meter / human-scale lock
6. support, contact, footprint, and module-size checks
7. container/capacity scale checks for vehicles: entry fit, XYZ width/height/length/depth volume, intended capacity class, occupant anchors, repeated door/window bays, and how many adult bodies the compartment reads as able to contain
8. scale-proxy dummy pass for scale-critical human-enterable scenes: place a temporary adult dummy/mannequin beside the baseline door/window/occupant landmark, project its height to the protagonist footpoint, then hide/delete the dummy while retaining the measurement trace
9. irreversible structure invariants: identity, shape quality, scale relation, and relationship for named anatomy/objects
10. humanoid scale-parity blockout check: protagonist, passengers/background humans, humanoids, and humanoid monsters stay on one perspective scale grid; fail miniature/doll/giant/background-texture reads
11. object distortion blockout check: named objects keep axis, silhouette, functional geometry, and scale relation before detail
12. instance mask separation: protected chains and occluders get separate mask/layer ownership before style
13. visual guide composite: combine clay/solid, lineart/wire or mask, depth/normal inset, perspective lines, scale witnesses, scale-proxy trace, protagonist footpoint, support plane, and contact/cut/grip markers into one user-reviewable image
14. user visual-guide checkpoint: collect feedback on the composite, revise if needed, and block Step 2.9+ image handoff until approval
15. structural invariant vs painterly freedom split
16. detail-after-blockout lock

### Output

- primitive blocks
- environment primitive blockout
- shared perspective grid
- meter scale lock
- absolute scale ladder
- object/anatomy scale invariants
- humanoid scale parity blockout check
- object distortion blockout check
- irreversible structure invariants
- anatomy to architecture scale check
- window to head size check
- parapet to body height check
- door/vehicle functional scale check
- passenger capacity scale check
- XYZ volume blockout check
- capacity class blockout check
- module repetition blockout check
- human-enterable composite blockout verdict
- scale proxy dummy blockout placement/check/removal policy
- scale proxy trace overlay and protagonist projection verdict
- footprint on support plane check
- detail after blockout lock
- instance mask separation plan
- protected chain mask review
- camera blockout
- depth layer order
- contact points
- scale check
- perspective check
- visual guide composite path
- visual guide composite source passes and overlays
- scale composite hard lock for scale-critical scenes
- user visual-guide feedback / approval status
- optional 3D reference plan
- structural invariants to preserve
- painterly freedoms allowed
- structure over painterly lock
- no structural sacrifice rule
- Blender guide strength
- user checkpoint C visual-guide composite direction

### Check / Gate

- major objects can be rebuilt from boxes, cylinders, wedges, slabs, tubes, and planes
- contact points and depth layers are explicit
- scale and perspective are checked before rendering language is added
- anatomy and environment primitives share one perspective grid
- architectural modules, parapets, railings, vehicles, or fixtures keep human scale when figures are present
- trams/trains/buses are judged by full passenger cabin/capacity and XYZ volume, not only the roof patch under the character or a single door-height comparison
- human-enterable objects fail if any composite subcheck fails: entry fit, XYZ volume, capacity class, occupant anchor, or module repetition
- protagonist-to-background-humanoid scale is checked against every visible passenger/crowd member/driver/humanoid monster, not just against doors/windows
- every registered object/anatomy item survives as a separate structural instance with identity, shape quality, axis continuity, scale relation, and relationship
- protagonist-to-object scale is checked against visible humans/passengers and functional object modules before image translation
- mask/blockout review proves protected chains remain separate from cloak, hair, effects, background, and other occluders
- render-bound handoff has a visual guide composite that translates perspective/blockout math into an actual reference image; prose-only scale/camera locks cannot pass
- for scale-critical scenes, the approved composite is binding for scale: protagonist/object size, door/passenger/container ratios, footpoints, and screen occupancy follow the composite overlays even if style/action/beauty wording conflicts
- user feedback on the composite is recorded and applied; `PRE_IMAGE_HANDOFF_READY` stays `no` until the composite is approved
- scale-critical scenes prove protagonist size with a temporary adult dummy/mannequin beside a reliable door/window/occupant baseline, then remove that dummy before composite/final art while preserving the measurement trace
- detail is explicitly blocked from overriding support/contact/scale and named non-negotiable relationships
- painterly compression is explicitly allowed or disallowed rather than left implicit
- user direction is requested when blockout choices materially branch

## STEP 2.9: IMAGE TRANSLATION LOCK

### Theory

- `references/theory-08-final-check-correction.md`
- `references/theory-02d-geometric-blockout.md` for detail-after-blockout priority
- `references/theory-02f-structural-scale-capacity-verdict.md` for tiered prompt budget and fail-first verdict criteria
- `references/theory-02g-occlusion-layer-separation.md` for prompt-level occlusion solutions
- `references/theory-02h-object-distortion-command-verdict.md` for prompt-level no-distortion and command-audit locks

### Decision Rule

Translate the structural plan into image-generation constraints. Style may enrich the locked structure but cannot replace the named support/contact/scale relationships. Do not flatten the full registry into one exhaustive prompt list: keep the registry in the spec/verdict and compress the final image prompt into a tiered hierarchy.

When the scene has anatomy plus architecture, vehicles, props, or strong perspective, prompt priority must say that primitive blockout, perspective, contact, and scale are solved before face, costume, hair, fur, effects, lighting, color, texture, or decorative detail.

The approved visual guide composite is one strong reference image, not a replacement for earlier evidence. Step 2.9 must carry the full pre-composite evidence stack into the handoff: immutable user commands, source image/conditioning status, object research, Step 2.1 perspective math, scale-proxy dummy projection when used, Blender pass outputs, visibility review, approved composite, and the compiled final prompt. If a runtime can only use the composite or only text, the handoff is not equivalent to the full process. However, for **scale**, the approved composite is a hard visual lock: scale markers, baselines, footpoints, dummy-derived traces, and door/passenger/container ratios win over style or action wording.

The image handoff must state the Blender guide strength:

- `loose guide`: preserve camera, contact, support, scale anchors, perspective size relationships, anatomy scale logic, major silhouettes, protected-chain landmarks, and separate object/anatomy instance ownership; allow painterly compression, partial occlusion, mood-first grouping, and value/detail emphasis only inside the declared occlusion budget and without changing body/object scale to symbolize power.
- `medium guide`: preserve most blockout proportions and placements while allowing limited edge softening and detail integration.
- `strict guide`: preserve blockout geometry closely for product, mechanical, orthographic, or highly technical accuracy.

Default to `loose guide` for painterly/editorial/anime final images unless the user explicitly prioritizes geometric precision over beauty and mood. Loose guide changes only the aesthetic surface; it does not relax scale, support/contact, protected-chain landmarks, occlusion budget, or separate-instance ownership.

Prompt hierarchy is mandatory for dense scenes:

1. Tier 0 macro camera / scale / support / passenger capacity / protagonist-to-secondary-humanoid scale parity.
2. Tier 1 face plane, primary and secondary humanoid anatomy, limb chains, lower-body silhouette, hands/feet.
3. Tier 2 key props, creatures, grips, contact points, and object separations.
4. Tier 3 style, texture, particles, signage, embroidery, blood, glow, and background density.

If tiers conflict, reduce Tier 3 first. Never solve prompt overload by removing or fusing Tier 0-2 structures. For every high-risk overlap, the final prompt must include a visual occlusion solution, not only a prohibition.

### Output

- generation priority order
- non-negotiable locks
- style allowed after structure
- Blender guide strength
- painterly compression allowance
- no hieratic scale distortion lock
- scale over style lock
- prompt attention budget lock
- occlusion translation lock
- all objects/anatomy irreversible lock
- object distortion prompt lock
- prompt finger topology lock
- verdict scale and mixing fails
- verdict irreversible structure fails
- prompt compression rule
- unknown object policy lock
- visual guide composite prompt lock
- image input stack plan
- pre-composite evidence stack lock
- scale proxy trace prompt lock when scale-critical
- scale must follow composite prompt lock when scale-critical
- composite-is-reference-not-sole-authority lock
- user checkpoint D pre-render direction

### Check / Gate

- structure priority is above style density
- the prompt explicitly says detail follows the locked support/contact/scale relationships rather than replacing them
- for object-density edge cases, the prompt explicitly says human anatomy, hands/fingers, feet, grip, and contact survive before background density, particles, blood, costume noise, or creature texture
- for object-density edge cases, the prompt names which non-human clutter can be reduced if it competes with anatomy
- the prompt explicitly says whether Blender is a loose, medium, or strict guide
- painterly compression cannot break named non-negotiables such as grip, support, scale, protected-chain traceability, occlusion budget, object axis/shape continuity, or required object identity
- human figure scale follows perspective and anatomy; power hierarchy is not expressed by making the ruler physically oversized unless the user explicitly requests symbolic scale
- all humans/humanoids/humanoid monsters share the same perspective scale logic; differences must come from actual body size or declared depth/lens transfer, never style/drama/focal importance
- the prompt carries `HUMANOID_SCALE_PARITY_PROMPT_LOCK`: protagonist and background humanoids stay comparable by depth plane; passengers/crowds/humanoid monsters are not miniatures, dolls, giants, or texture
- `VISUAL_GUIDE_COMPOSITE_PROMPT_LOCK` names the approved composite as the structure reference for camera/perspective/scale/support/contact/object placement, while explicitly banning copied clay colors, labels, arrows, or guide text
- `IMAGE_INPUT_STACK_PLAN` states which images are actually supplied to generation: source image, approved visual guide composite, optional clay/lineart/depth/control passes, and each image's role
- `PRE_COMPOSITE_EVIDENCE_STACK_LOCK` and `COMPOSITE_IS_REFERENCE_NOT_SOLE_AUTHORITY` state that the composite is one reference in the source/object/perspective/blockout/final-prompt stack, not the only authority
- scale-critical specs carry `SCALE_PROXY_TRACE_PROMPT_LOCK`: generation follows the hidden dummy's retained height trace/baseline, but the dummy itself is not rendered as a final character
- scale-critical specs carry `SCALE_MUST_FOLLOW_COMPOSITE_PROMPT_LOCK` and Step 8 `SCALE_COMPOSITE_HARD_LOCK_VERDICT_CHECK`: if generated scale drifts from the approved composite, the image fails/rerenders even when the drawing is otherwise attractive
- unknown objects cannot become random pattern/noise
- non-negotiable locks are short enough to survive prompt compression
- the image prompt contains the highest-risk Tier 0-2 visual outcomes, not a flat legalistic inventory
- vehicle scenes carry capacity/cabin/window-door-bay language into the final prompt, not just the spec
- anatomy scenes carry face-plane and lower-body silhouette language into the final prompt before style adjectives
- visible-hand scenes carry per-hand palm/thumb/finger topology language into the final prompt before style/detail adjectives
- high-risk overlaps name the layer solution: occluder behind, protected chain in front, rim/negative-space/value edge, and reducible clutter
- image generation is blocked when user direction is needed for an unresolved object, structural branch, or unapproved visual guide composite
- Step 2.9 writes prompt locks and tier priority, but the final image model receives the Step 8 compiled prompt after aesthetic recovery, not raw Step 2.9 field names

## STEP 3: VALUE DESIGN

### Theory

- `references/theory-03-lighting-value.md`

### Decision Rule

- define the key light:
  - direction
  - intensity / hardness
  - temperature / color character
- limit value groups to `3-5`
- lock the largest contrast around face and eyes
- separate skin values and edges from clothes/background values and edges
- compress outer-frame values so the focal area wins in grayscale

### Execution

1. Read the Step 1 intent and Step 2 composition output.
2. Define the key light.
3. If needed, define fill light and rim light.
4. Choose a value count within `3-5`.
5. Reserve the strongest contrast for face and eyes.
6. Group the background and corners into quieter, lower-priority values.
7. Paint values in grayscale order:
   - large masses
   - middle transitions
   - focal accents
8. Separate materials by value behavior:
   - skin: soft warm-leaning midtone, soft shadow, softer edges
   - clothes/background: cooler rough dark tones, stronger cast shadows, sharper edges
9. Run a grayscale reduction test before moving on.

Example default when the scene calls for high tension:

- use `4` value levels
- skin: soft warm midtone, soft shadow
- clothes/background: cool rough dark tones
- strongest contrast around eyes and face
- darken corners and outer areas

### Output

- lighting plan
- value-count decision
- grayscale value map
- focal contrast zone
- corner / outer-area suppression plan
- material edge plan

### Check / Gate

- light direction and strength are readable
- grayscale focal point holds
- value groups remain controlled instead of muddy
- skin reads separately from costume/background
- outer frame supports center focus
- face / eye region holds the strongest contrast

## STEP 4: FACE

### Theory

- `references/theory-04-face-eyes.md`
- `references/theory-04a-face-emotion-patterns.md`
- `references/theory-02f-structural-scale-capacity-verdict.md` for face shape-quality lock

### Decision Rule

- re-read Step 1 intent and Step 3 lighting before making facial decisions
- separate:
  - surface emotion
  - inner emotion
- extract:
  - main emotion
  - support emotion
- decide emotion intensity:
  - low
  - medium
  - high
- convert emotion into a brow / eyelid / pupil / highlight / mouth pattern set
- use `main 70% + support 30%` blending when the expression is mixed
- eyes are the first-render priority
- face preservation means plane/proportion quality, not just having a face: protect skull/face plane, jaw/chin/cheek width, eye spacing, and intended adult/beautified read
- expression must stay restrained
- expression must feel lived-in: the face should belong to the situation rather than directly describing a role label
- avoid cliché direct acting by default: no villain grin, no wide-eyed power stare, no exaggerated seduction mouth, no obvious authority scowl
- nose and mouth remain understated
- iris, pupil, and highlight design must reinforce focal clarity and agree with the scene light
- controlled asymmetry should be attempted when action, strong emotion, or situational realism would otherwise look too perfect or AI-like

### Execution

1. Re-read Step 1 intent output.
2. Re-read the Step 3 lighting plan.
3. Decide:
   - surface emotion
   - inner emotion
   - main emotion
   - support emotion
   - intensity
4. Select the facial pattern set:
   - eye openness
   - brow angle
   - gaze direction
   - pupil size
   - highlight amount
   - mouth shape and size
5. If mixed emotion is needed, blend the pattern as `main 70% + support 30%`.
6. Add only tiny controlled asymmetry when expression, action, or realism benefits:
   - one brow slightly higher
   - one lid slightly tighter
   - one mouth corner slightly shifted
   - head angle, hair shadow, pipe, hand, or prop interrupts perfect front-facing symmetry
7. Fully render eyes first in this order:
   - iris base
   - 2-3 value steps for depth
   - pupil placement
   - 1-2 main highlights
8. Use crystal-like highlight shapes in the iris.
9. Layer transparent-looking color over the iris structure.
10. Keep brows and mouth controlled rather than exaggerated.
11. Keep the nose small and understated.
12. Check the face at reduced size and make sure the eye area still wins.

### Output

- eye render plan
- surface / inner emotion note
- main / support emotion note
- expression note
- face structure quality lock
- face focal map
- eye-light consistency note
- asymmetry note, if used
- natural acting / anti-direct-expression lock

### Check / Gate

- emotion reads through the eye / brow / mouth combination
- eyes read first at first glance
- the eye region has the highest local detail and strongest focal contrast
- iris / pupil / highlight design matches the scene light
- expression matches the intent sentence without overstatement
- expression reads as a person inhabiting the situation, not a direct symbol for villainy, power, seduction, anger, or authority
- pupil size and highlight amount support the intended emotional intensity
- asymmetry, if present, reads as controlled design rather than a mistake
- small asymmetry has been considered when the face risks looking too perfectly centered, polished, or AI-like
- lower face does not overpower the eyes
- the face does not drift into flattened, dumpling-wide, childlike, or generic doll proportions when the intent calls for an adult stylized heroine

## STEP 5: LINE & SHAPE

### Theory

- `references/theory-05-line-shape.md`
- `references/theory-05a-hands-fingers.md` when hands are visible
- `references/theory-02f-structural-scale-capacity-verdict.md` for limb/lower-body silhouette priority
- `references/theory-02g-occlusion-layer-separation.md` for edge and rim-light plans that keep protected chains traceable

### Decision Rule

- re-read Step 2 silhouette and Step 3 value structure
- if hands are visible, treat them as an anatomy submodule problem under the chosen body structure, not as decorative line noise
- treat legs/pants/boots as silhouette-critical anatomy before costume texture; line weight must separate thigh, knee, shin, ankle, and left/right leg where visible
- split the image into line groups:
  - thin sensitive group
  - thick broken group
- keep line-weight stages within `2-3`
- decide which large planes will be decomposed into:
  - triangles
  - shards
  - ribbons
  - pointed petal forms
- decide where shape alone is enough and where line must reinforce the read
- use shape direction to guide the eye from eyes -> face -> support object
- for visible hands, decide:
  - palm block direction
  - thumb wedge read
  - individual thumb / index / middle / ring / little finger chain direction
  - where overlap or occlusion occurs without fusing fingers into a group

### Execution

1. Re-read the Step 2 silhouette and Step 3 value plan.
2. Assign the thin sensitive line group to:
   - hair
   - hands
   - jawline
   - nose indication
   - eye area
3. Assign the thick broken line group to:
   - clothing folds
   - accessories
   - background structures
   - architecture
   - shard and ribbon outer edges
4. Lock line weights to `2` levels by default, with an optional third accent level only if needed.
5. Decompose large clothing, background, and light planes into:
   - triangles
   - glass-like shard polygons
   - ribbons
   - pointed petal forms
6. Align those forms to the gaze path so the eye moves from the face toward the next supporting element without leaving the frame.
7. If hands are visible:
   - block palm first
   - place thumb second
   - model thumb, index, middle, ring, and little finger as separate chains before costume, prop, blood, or background detail
   - keep finger thickness taper and knuckle cadence readable
   - show pressure / overlap when a prop is being held
8. Decide where broad shapes carry the read without line, especially in larger shadow and light masses.
9. Check the whole image at reduced size and confirm the style reads through line, shape, and hand readability alone.

### Output

- line hierarchy
- line-weight map
- shape-decomposition plan
- gaze-guidance motif map
- hand line priority note
- lower body line priority note
- protected chain edge separation plan
- line-vs-shape role note

### Check / Gate

- sensitive parts use thin line logic while clothing/background use thicker broken logic
- if hands are visible, palm / thumb / individual finger-chain structure reads before tiny wrinkle detail
- if hands are visible, finger lengths and tapers are not uniform
- line weight is not uniform and remains controlled within 2-3 stages
- shape rhythm supports focal flow
- large planes are broken into a coherent shard / ribbon / petal language
- line and shape already communicate the intended style before color
- background roughness does not erase the silhouette
- black costume texture, straps, cloak, or shadow do not absorb leg-chain readability
- line/value edges make protected chains traceable where they cross or approach occluders

## STEP 6: COLOR & ACCENT

### Theory

- `references/theory-06-color-palette-point.md`

### Decision Rule

- re-read Step 1 intent and Step 3 value structure
- choose:
  - 2-3 base colors
  - 1-2 support colors if needed
  - 1-2 accent colors
- keep overall palette narrow and dark
- limit hue-family spread to about `3-4` regions or fewer
- preserve the value hierarchy while recoloring
- assign accent priority:
  - eyes / face first
  - selected hair / accessories second
  - small background lights or signs third
- keep strong accent area roughly under `10-20%` of the canvas
- skin color must avoid glass, porcelain, wax, plastic, or isolated beauty-retouch tones
- skin must receive the scene's shadows and bounce light so the face belongs to the same environment as hair, props, and background

### Execution

1. Re-read Step 1 intent and Step 3 value map.
2. Choose `2-3` dark low-saturation base colors.
3. Choose `1-2` accents from:
   - red
   - teal
   - purple
   - white light
4. Assign color roles:
   - main
   - support
   - accent
5. Recolor the image while preserving the existing value structure.
6. Distribute colors by part:
   - skin stays muted warm gray-beige / warm low-saturation, softer than the environment but still affected by hair shadow, prop shadow, and cool/warm bounce light
   - hair stays near the base palette with selective accent support
   - clothing uses base variations more than accent
   - background stays mostly in base tones
7. Place accent mainly in:
   - eyes / iris / highlights
   - some hair strands, ribbons, or key accessories
   - a few shards or controlled background object lights
8. Reduce or remove accents if the background begins to compete with the face.
9. Check the image at reduced size and confirm color alone still supports focus and mood.

### Output

- palette selection
- accent placement map
- base / support / accent role note
- per-part color distribution note
- non-plastic skin tone lock
- value-preservation note

### Check / Gate

- hue-family count stays controlled
- accent color count stays controlled
- the base tone remains dark and coherent
- value structure remains intact after color
- color emphasis reinforces the focal point
- skin reads alive and scene-integrated rather than porcelain, glass, wax, plastic, or separately retouched
- non-accent areas remain quiet enough
- face / eyes remain the strongest color focus

## STEP 7: TEXTURE

### Theory

- `references/theory-07-texture-density.md`

### Decision Rule

- divide the image into:
  - high density
  - medium density
  - low density
- separate smooth skin from rough costume/background
- skin must be soft but alive, with subtle local value/color variation rather than AI plastic smoothness
- define texture strategy by part:
  - skin
  - clothing / accessories
  - background / fragments
- decide whether a low global grain layer is useful
- decide where local stronger grain or texture is allowed
- decide where labels / symbols / text fragments can appear without competing with the face

### Execution

1. Divide the image into high / medium / low density zones.
2. Keep the face and immediate focal support area as the primary high-density zone.
3. Keep skin relatively smooth with light micro-variation from nose/cheek/forehead planes, eyelid shadow, hair shadow, pipe/prop shadow, and neighboring dark background.
4. Emphasize rougher texture on clothing, accessories, background structures, and fragments.
5. Add a low-intensity global grain layer only if it improves cohesion.
6. Add stronger local texture or noise selectively to:
   - clothing
   - background
   - dark secondary zones
   - fragments / ribbons / debris
7. Mask or reduce heavy texture around the face and eye region, but do not erase all skin variation into a wax/porcelain surface.
8. Add a limited number of labels, symbols, or small text fragments in secondary support zones or edges.
9. Check the image at reduced size and confirm the texture reads as organized density rather than dirt.

### Output

- texture-density map
- rough/smooth separation plan
- secondary symbol placement
- global grain note
- local texture emphasis note
- non-plastic skin surface note

### Check / Gate

- skin remains cleaner than the environment
- skin remains soft but alive, not glassy, porcelain, waxy, airbrushed-doll, or AI-plastic
- face belongs to the same light/shadow environment as hair, pipe/props, clothing, and background
- global grain supports rather than obscures the image
- texture adds atmosphere without masking the face
- density zoning is readable and the focal area stays primary
- labels / symbols support worldbuilding without stealing focus
- corners and outer regions do not become messy noise fields

## STEP 8: FINAL CHECK

### Theory

- `references/theory-08-final-check-correction.md`
- `references/theory-02f-structural-scale-capacity-verdict.md` for fail-first structural verdicts
- `references/theory-02g-occlusion-layer-separation.md` for protected-chain trace verdicts
- `references/theory-08a-final-prompt-compiler-aesthetic-recovery.md` for final prompt compilation and anti-generic aesthetic recovery

### Decision Rule

- re-read Step 1 intent and compare it against the current image
- verify focus in:
  - normal view
  - reduced-size view
  - grayscale view
- verify value structure, color balance, face consistency, and texture density as one aligned system
- run a fail-first structural verdict before aesthetic praise: protagonist-to-object scale, scale/capacity, all-object distortion, object-anatomy mixing, user-command compliance, face/lower-body quality, and irreversible registered structures
- fail hand preservation when a visible hand merely exists but reads as a fused claw, black lump, melted glove, decorative noise, or unreadable scribble
- identify any element that competes with the face
- if output medium matters, verify resolution and color-mode suitability
- when no generated image exists yet, Step 8 is a pre-image spec/prompt final check; leave `POST_IMAGE_VISUAL_VERDICT_*` not_applicable until `POST_IMAGE_VERDICT_REQUIRED: yes`
- before pre-image handoff, compile structural locks and aesthetic recovery into `FINAL_IMAGE_PROMPT_COMPILED`; do not pass schema fields, tier labels, object IDs, or validator/verdict language to the image model
- when a generated image exists, run the post-image visual verdict and set `POST_IMAGE_ACCEPTED` based on the verdict

### Execution

1. Re-read the Step 1 intent sentence.
2. Ask whether the image still communicates that story and feeling.
3. Check the image at reduced size.
4. Check the image in grayscale.
5. Verify:
   - eyes / face still read first
   - visible hands still read as believable hands, not fused mittens or broken claws
   - each visible hand keeps palm block, thumb wedge, and readable separated finger starts/directions/ends or overlap/contact cues
   - vehicle/container scale reads as full human-usable capacity rather than toy/protagonist-sized prop when vehicles are present
   - protagonist scale matches visible passengers, humans, doors, windows, props, architecture, creatures, and repeated object modules after depth-plane transfer
   - every named object keeps its intended silhouette, axis continuity, functional geometry, and material boundary; no object is bent, warped, melted, resized, fused, or texture-replaced by another correction
   - every explicit user command and non-negotiable spec instruction is checked one by one, with pass/fail/needs-revision/not-applicable status
   - face plane and lower-body silhouettes keep their intended quality instead of being flattened or absorbed
   - registered objects/anatomy are not omitted, fused, resized, or converted into texture
   - each protected arm/leg/hand/weapon chain can be traced through visible landmarks without guessing
   - value structure still supports focus
   - color balance is controlled
   - accent colors do not spread too far
   - face and eye expression still match Step 4 / 4A
   - texture and density still support the focal area
6. If needed, make final corrections to:
   - contrast
   - tone balance
   - accent placement
   - face micro-expression
   - texture opacity / masking
7. If the piece has a known delivery medium, check output size / resolution / color suitability.
8. Run the final prompt compiler:
   - `STRUCTURE_LOCK_SUMMARY`: internal high-risk structure summary only.
   - `AESTHETIC_RENDER_BRIEF`: natural visual language restoring face/eye focal, composition pressure, line/value/color/texture, and anti-generic style.
   - `NEGATIVE_PROMPT_LIMITED`: short concrete failure defenses.
   - `FINAL_IMAGE_PROMPT_COMPILED`: the production prompt emitted by the pipeline.
9. Record brief self-feedback and archiving notes.

### Output

- pass/fail review notes
- hero/object scale verdict notes
- all-object distortion verdict notes
- user-command compliance verdict notes
- hand readability and finger-topology verdict notes
- final correction list
- aesthetic recovery check
- structure lock summary
- aesthetic render brief
- limited negative prompt
- final compiled image prompt
- output-medium note, if relevant
- self-feedback note
- archive note

## CRITIQUE output contract

When using this process in `CRITIQUE` mode, report in this order:

1. `User Verdict`
2. `System Read`
   - `intent`
   - `process`
   - `readability`
   - `delivery`
3. `Agreement / Tension`
4. `Next Move`

The user's verdict sets the primary label.
The system diagnostic explains why the result works, fails, or remains unstable across the process steps.

### Check / Gate

All must pass before completion:

- the intended feeling can be explained in one sentence from the image
- eyes are first read
- silhouette has line and edge rhythm
- skin/background separation is clear
- grayscale focal hierarchy remains intact
- scale anchors and capacity anchors pass when present
- human-enterable composite scale verdict passes when present: entry fit, XYZ volume, capacity class, occupant anchor, module repetition, and final composite verdict
- protagonist-to-object scale relationship passes against all available scale witnesses
- protagonist-to-secondary-humanoid scale parity passes for every visible passenger, crowd member, driver, or humanoid monster; fail miniature/doll/giant/background-texture humanoids
- all named objects pass the no-distortion verdict: no unintended bending, warping, melting, resizing, fusing, absorption, or texture replacement
- every explicit user command and non-negotiable instruction has been audited in Step 8
- final prompt compiler passes: no schema/validator jargon, no flat registry dump, aesthetic recovery restored face/eye focal, composition pressure, line/value/color/texture hierarchy, and anti-generic style read
- face and lower-body quality pass, not only existence
- object/anatomy separation and irreversible structure checks pass
- protected-chain trace verdict passes for all visible/partial arms, legs, hands, and weapon chains
- finger-topology verdict passes for every visible hand; hand existence without readable topology fails
- value, color, and texture all support the face
- no competing color/detail/text steals focus from the face
- output settings are appropriate for the sharing medium, if specified

## Expansion Rule

When a new theory is provided:

1. keep it as an individual theory unit
2. map it to one or more steps
3. extract decision rules from theory before execution
4. only compress into step summaries after the theory block is preserved
