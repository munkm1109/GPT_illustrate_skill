---
name: illustrate-skill
description: >-
  Plan, specify, critique, and extend illustration work with a theory-first SOP:
  intent, composition, value, face, line, color, texture, and final check. Use
  this skill whenever the user asks to design an illustration, break a scene into
  staged art decisions, apply drawing theory before execution, refine an
  illustration workflow, or add theory blocks. Trigger phrases include "일러스트
  그려줘", "그림 구도 잡아줘", "이론 기반으로 일러스트 설계해줘", "장면 의도부터
  정리해줘", "이 그림 프로세스로 분석해줘", "구도랑 명암 구조 짜줘",
  "illustration workflow", "gothic portrait composition". Also trigger when the
  user provides mood/scene keywords, theory blocks, or reference-driven art
  direction and wants a staged illustration spec. Prefer this skill over imagegen
  when the user needs theory-driven planning, critique, workflow design, or
  stage-by-stage reasoning before image generation. Prefer it over
  object-research-skill for full-scene planning rather than isolated lookup.
---

# Illustrate Skill

Use this skill as a theory-first SOP folder for illustration planning and critique.
Keep procedure in this file. Load domain knowledge from `references/` only when needed.

Legacy per-image specs under `.omx/archive/` are historical records only. Do not
search, cite, migrate, or reuse archived specs during normal image work unless
the user explicitly names an archived path or asks for legacy-run inspection.

## Default load order

1. Read `references/domain_context.md`.
2. Read `references/main-process.md`.
3. Read `references/pipeline-plan-implement-verify-audit.md` for render-bound SPEC runs.
4. Read `references/theory-02j-camera-class-scale-gate.md` whenever the user sets a camera class or the scene is scale-critical.
5. Read `references/theory-08a-final-prompt-compiler-aesthetic-recovery.md` before any pre-image handoff.
6. Read only the theory files needed for the active step.
7. Read `references/style-guide.md` when the task needs the workspace reference style.
8. If background, prop, age-band anatomy, sex-classification anatomy, or visible hand/finger knowledge is insufficient after Step 2 / Step 2.3 blocking, load `object-research-skill` and follow its SOP before resuming this workflow.

## Modes

Pick one mode explicitly.

- `SPEC`: turn user intent or keywords into a staged illustration spec
- `CRITIQUE`: review an existing illustration, prompt, or plan against the staged process
- `EXTEND`: add or rewrite theory blocks and update the process mapping

If the user mixes modes, do the blocking mode first:

- missing scene definition -> `SPEC`
- existing image or plan review -> `CRITIQUE`
- skill structure or theory library changes -> `EXTEND`

If the user's real task is **creating a new style-specific wrapper skill from reference images/folders**, do not continue as normal `SPEC`.
Hand off to `reference-copy-skill` first.

## SPEC mode

1. Capture the user's scene, mood, constraints, and deliverable.
2. For any SPEC run that is intended to reach final rendering or image generation, start from `templates/illustrate-spec-template.md` and write into a working spec artifact before Step 1. Use a path such as `.omx/runs/<timestamp>-<slug>-spec.md` or another user-requested location.
3. Before Step 1 intent work in every render-bound SPEC run, run the **Render Style Baseline Gate** and ask the user which rendering family the image should belong to. Do not infer this silently from words like "anime", "editorial", "camera", "leather", "painterly", or a style wrapper name, because those terms can pull the image model toward different render families. Ask with these five choices and recommended mixes:
   - `axis_1_2d_anime`: strict 2D anime / cel-shaded ink illustration. Use when the user wants stable anime linework, simplified skin, graphic materials, and no photo/cosplay/3D drift.
   - `axis_2_semi_real_concept`: semi-realistic painterly concept art. Use for anime-like faces with more realistic lighting/materials and mood painting.
   - `axis_3_3d_render`: 3D render / figure / plastic-to-CG form. Use only when the user wants model/figure/CG volume.
   - `axis_4_live_action_cosplay`: live-action / cosplay / fashion-photo realism. Use only when the user explicitly wants a realistic person/photo/cosplay read.
   - `axis_5_game_cg_key_visual`: game/CG key visual. Use for polished key art that may mix anime design with cinematic lighting.
   Recommended combinations: `axis_1 + axis_2` for anime with painterly mood; `axis_1 + axis_5` for anime game-key-visual polish; `axis_2 + axis_5` for semi-real cinematic concept art; `axis_4 + axis_5` only for cosplay/live-action poster reads. Avoid `axis_1 + axis_4` unless the user explicitly wants anime-cosplay ambiguity.
   Record the answer in `RENDER_STYLE_USER_DECISION`, the primary axis in `RENDER_STYLE_PRIMARY_AXIS`, secondary axes in `RENDER_STYLE_SECONDARY_AXES`, and the allowed/disallowed mix in `RENDER_STYLE_MIXING_POLICY` / `RENDER_STYLE_DRIFT_GUARD`. Keep `PRE_IMAGE_HANDOFF_READY: no` until this is resolved. If the user already gave an explicit same-turn answer to this exact five-axis question, quote it; otherwise ask before continuing.
4. Select exactly one intake route in Step 0 before normal stage work:
   - `image_development`: the user provides or references an already-generated/source image to develop, correct, repaint, or continue.
   - `prompt_only`: the user requests a first image from text/prompt/spec only, with no existing image evidence.
   The inactive branch must be marked `not_applicable` and must not impose its evidence requirements on the active branch.
5. Fill the PIVA gates before final handoff: PLAN captures user commands/non-negotiables, IMPLEMENT maps Step 0-8 and object-research transfer, VERIFY checks prompt/spec conflicts before generation, and AUDIT defines pre/post-image command and visual verdict triggers.
6. Create a theory-read proof artifact from `templates/theory-read-proof-template.md`, record its path in `THEORY_READ_PROOF_PATH`, and keep it updated during the run.
7. Read the relevant step theory before each step and record the read in the proof artifact, preferably via `python scripts/record_theory_read.py <proof-path> <step> <file> ...`.
8. Run the structural preflight before any value, face, line, color, texture, or image-generation work:
   - Step 0: route gate plus active intake branch
   - Step 2: composition and object-role summary
   - Step 2.1: perspective rig / horizon / vanishing points / support planes / scale anchors / protagonist-to-object scale relationship / projected camera-cut scale transfer
   - Step 2.2: perspective-plane object inventory plus occluder-mass inventory
   - Step 2.2M: merge the route-specific evidence into one normalized Scene Contract
   - Step 2.3: anatomy as object inventory plus anatomy structure gate and protected-chain visibility table
   - Step 2.4: object-knowledge query plan by lane
   - Step 2.5: object-research handoff when needed
   - Step 2.6: object relationship check plus occlusion layer graph, separation cue plan, and all-object distortion lock
   - Step 2.7: anatomy-on-object relationship check
   - Step 2.8: conditional blockout / modeling contract. First decide whether Blender is required. Use `.blend`/render-pass/visual-guide/user-checkpoint only for structurally complex scenes; skip Blender for backgroundless/simple character-only scenes with no scale-critical, contact, grip, source-image structure, or hard-surface staging need.
   - Step 2.9: image translation lock, including detail-after-blockout priority and the approved visual-guide image input stack when a visual guide exists, or direct compact prompt handoff when Step 2.8 explicitly skipped Blender.
9. If the task is an upgrade, repaint, correction, continuation, or development of a user-provided/generated source image, set `INPUT_ROUTE: image_development` and identify the concrete objects already present in the source image before finalizing Step 2.2. Separate them into:
   - primary retained objects
   - structurally clear objects
   - structurally uncertain objects
   Record the image/previous-result diagnostic in Step 0A as `PREVIOUS_IMAGE_VISUAL_VERDICT_SUMMARY`; do not reuse `POST_IMAGE_VISUAL_VERDICT_*` for this pre-existing source verdict.
   Also fill `SOURCE_IMAGE_ACTUAL_CONDITIONING` and `IMAGE_DEVELOPMENT_ALLOWED`: if the source pixels/control image cannot actually be supplied to generation, mark the run as `prompt_only_fallback` or `blocked` and describe it as a source-informed reinterpretation rather than true image development.
   Apply the source-image style/design firewall by default: the source image may provide object identity, relationships, pose/action facts, camera/perspective evidence, structural scale witnesses, and failure clues, but it must not provide the final style, palette, linework, brush/medium texture, character/costume design, creature design, prop design, or composition-design motifs unless the user explicitly requests source-style preservation. Fill `SOURCE_IMAGE_TRANSFER_SCOPE`, `SOURCE_IMAGE_STYLE_DESIGN_FIREWALL`, `SOURCE_IMAGE_ALLOWED_TRANSFER`, `SOURCE_IMAGE_FORBIDDEN_TRANSFER`, `SOURCE_IMAGE_REDESIGN_DIRECTIVE`, and `SOURCE_IMAGE_PROMPT_FIREWALL` in Step 0A.
10. If the task has no existing image and is a first-generation text/prompt request, set `INPUT_ROUTE: prompt_only`, fill Step 0B from prompt-derived candidates/assumptions, and leave source-image verdict fields `not_applicable`.
11. Both Step 0 routes must merge at Step 2.2M before Step 2.3. Downstream steps consume the Step 2.2M normalized Scene Contract, not branch-specific raw notes.
    The Scene Contract is the common join point for `image_development` and `prompt_only` and must include:
    - stable object ids (`OBJECT_REGISTRY`)
    - explicit relationship triples (`RELATIONSHIP_CONTRACT`)
    - action/contact target and forbidden-target rules (`ACTION_CONTACT_CONTRACT`)
    - post-action/cut result state (`POST_ACTION_OBJECT_STATE_CONTRACT`) when a target is severed, damaged, or structurally changed
    - visible target cut-plane/cross-section rules (`TARGET_CUT_PLANE_VISIBILITY_CONTRACT`) so the model cannot hide unresolved cuts behind a character, cloak, or effect
    - protagonist/background-humanoid/container scale parity (`SCALE_PARITY_CONTRACT`)
    - protected left/right anatomy chains (`PROTECTED_ANATOMY_CHAINS`)
    - cloak/cape/hood attachment/origin rules (`GARMENT_ATTACHMENT_CONTRACT`) when relevant
11. List background objects by perspective plane, not as generic atmosphere:
   - support / ground / track plane
   - left vertical plane
   - right vertical plane
   - overhead plane
   - foreground frame
   - background depth
   - effects
   - text / glyph objects
12. Treat every visible human, humanoid object, and humanoid monster as anatomy in Step 2.3 unless the user explicitly marks it as a non-anatomical symbol/statue/icon/abstract pattern. This includes protagonists, passengers, drivers, crowds, background people, androids, demons, werewolves, beast-men, and source-image humanoids. Background humanoids may be low detail, but they are anatomy scale objects, not texture. Step 2.1 must create `HERO_BACKGROUND_HUMANOID_SCALE_COMPARISON_TABLE`; Step 2.2 must transfer every visible humanoid candidate into Step 2.2M and then Step 2.3; Step 2.8/2.9/Step 8 must prove and preserve protagonist-to-secondary-humanoid scale parity.
13. Treat the human figure as an object stack in Step 2.3:
   - primary anatomy object
   - anatomy sub-objects
   - anatomy contact objects
   - anatomy scale relationships to supports, props, and vehicles
14. For `image_development` runs, also identify any visible hands, gripping poses, finger silhouettes, or hand-held props that are important to the scene read.
15. For `image_development` runs, prefer Step 2.5 object research on the recognized source-image objects whenever their structure, material, scale, perspective role, or style-critical construction would benefit from confirmation, even if the objects are already visible in the source image.
13. If the scene shows a meaningful amount of human figure information beyond a close face crop, run the Step 2.3 anatomy structure gate before Step 2.5. Lock age band, sex classification, proportion logic, and limb-chain logic before treating hands as a local problem.
14. If hands or fingers are visible and they are focal, close to camera, expressive, foreshortened, or holding a prop/weapon, treat them as an anatomy submodule under the Step 2.3 body decision, not as a free-floating object guess.
15. For anatomy-gated scenes, default toward Step 2.5 lookup / research of:
   - one age-band body base card
   - one sex-classification overlay card
   - the hand anatomy submodule
   before trusting raw model intuition.
16. For structurally important scenes, Step 2.4 must plan object research in separate lanes:
   - anatomy
   - core scale anchors
   - container capacity / occupancy scale anchors
   - hard-surface background / architecture
   - weapon / prop
   - effects / text
   Container capacity / occupancy scale anchors are mandatory whenever a tram, train, bus, car, elevator, room, corridor, interior, cabin, building, or other human-enterable object affects scale. Object research must determine adult capacity/occupancy, XYZ volume, dimensions or module count, entry/exit scale, repeated human-scale modules, internal occupant anatomy anchors, and final prompt locks.
   Human-enterable object research must split researched objects into `human_enterable_objects` and `non_enterable_objects`. For every human-enterable object, blend at least one passenger/driver/occupant/mannequin/silhouette or implied occupant block inside/at a door/window/seat/aisle/floor module and use it as an anatomy scale witness before comparing protagonist/main humans/humanoids/humanoid monsters.
   Entry height alone never passes a human-enterable object. The composite scale verdict must pass all six parts: `ENTRY_FIT_CHECK`, `XYZ_VOLUME_CHECK`, `CAPACITY_CLASS_CHECK`, `OCCUPANT_ANCHOR_CHECK`, `MODULE_REPETITION_CHECK`, and `HUMAN_ENTERABLE_SCALE_VERDICT`.
   Activate `SCALE_CRITICAL_MODE: yes` when the scene contains both (a) any human-enterable object and (b) a protagonist/main human/humanoid/humanoid monster whose size must be compared to that object. Before locking composition, record camera class as a first-class user-controllable input: `USER_CAMERA_CLASS_PRESET`, `USER_CAMERA_CLASS_LOCK_LEVEL`, and `USER_CAMERA_CLASS_REASON`. In scale-critical mode:
   - Object research must return numeric ratio fields, not prose alone: `CONTAINER_SCALE_RATIO_TABLE`, `HUMAN_ENTERABLE_COMPOSITE_SCALE_TABLE`, `PROTAGONIST_TO_ENTRY_RATIO`, `PROTAGONIST_TO_OCCUPANT_RATIO`, `PROTAGONIST_TO_CONTAINER_WIDTH_RATIO`, `PROTAGONIST_TO_CONTAINER_LENGTH_RATIO`, `MAX_PROTAGONIST_SCREEN_OCCUPANCY`, and `SCALE_CRITICAL_FAIL_NUMBERS`.
   - The scale proof overrides face detail, Redjuice density, action drama, beauty framing, and style fidelity. If the chosen camera cannot prove the protagonist fits the tram/room/building/vehicle, widen the shot, add visible doors/windows/passengers, or use a separate face/detail inset instead of enlarging the protagonist.
   - Camera conflicts must be explicit. `soft` or `adaptive` camera locks may be resolved to a scale-proving wide/long shot; `hard` close/portrait/medium locks block image handoff until the user explicitly changes either the camera lock or the scale goal.
   - Step 2.1 must fill the scale shot-class gate: `SCALE_CRITICAL_SHOT_CLASS`, `FULL_CONTAINER_VISIBILITY_REQUIREMENT`, `SCALE_WITNESS_MIN_COUNT`, `HERO_TO_MODULE_VISUAL_RATIO`, `CLOSEUP_BLOCKED_UNTIL_SCALE_PASS`, and `FACE_FOCAL_DEMOTION_FOR_SCALE`.
   - Camera cuts and scale adjustments must additionally follow `perspective calculation -> blockout/guide -> final prompt`. Step 2.1 must fill `PERSPECTIVE_SCALE_TRANSFER_MODE`, `HERO_FOOTPOINT_PLANE`, `BASELINE_OBJECT`, `PROJECTED_BASELINE_TO_HERO_POSITION`, `SCREEN_OCCUPANCY_IS_DERIVED`, `SCREEN_OCCUPANCY_MUST_NOT_OVERRIDE_WORLD_SCALE`, and `CAMERA_CUT_SCALE_RECONCILIATION`. A nearby door is optional for ordinary scenes; the mandatory requirement is projecting a reliable baseline through the shared perspective grid to the protagonist/support plane.
   - In scale-critical human-enterable scenes, use a temporary adult scale proxy before the composite: fill `SCALE_PROXY_DUMMY_REQUIRED: yes`, `SCALE_PROXY_DUMMY_HEIGHT`, `SCALE_PROXY_DUMMY_BASELINE_OBJECT`, `SCALE_PROXY_DUMMY_PLACEMENT_PLAN`, and `SCALE_PROXY_DUMMY_TO_HERO_PROJECTION`. The sequence is `perspective calculation -> door/occupant-side adult dummy placement -> dummy-to-hero projection -> blockout size lock -> hide/delete dummy while retaining measurement trace -> visual guide composite -> user approval -> image input stack/handoff`.
   - For long vehicles, default to extreme-wide / wide scale shot, full container visibility, repeated door/window/passenger/module witnesses, protagonist roughly one adult door/window/passenger height, and protagonist normally under 5% of visible vehicle length when vehicle length is the main scale witness.
   - Step 2.8 and Step 2.9 must set `BLENDER_GUIDE_STRENGTH: strict guide`; painterly looseness may affect edges, texture, and value grouping only after the strict scale blockout passes.
   - Step 2.8 must fill `CAMERA_CLASS_BLOCKOUT_LOCK`, `FULL_CONTAINER_VISIBILITY_BLOCKOUT_CHECK`, and `SCALE_WITNESS_VISIBILITY_COUNT_CHECK`; blockout review must prove the chosen camera class, not merely list a camera.
   - Step 2.8 must transfer the perspective calculation into visual evidence via `PERSPECTIVE_CALCULATION_BLOCKOUT_TRANSFER`, `PROJECTED_BASELINE_BLOCKOUT_CHECK`, and `SCREEN_OCCUPANCY_BLOCKOUT_RECONCILIATION`. For scale-critical scenes it must also fill `SCALE_PROXY_DUMMY_BLOCKOUT_PLACEMENT`, `SCALE_PROXY_DUMMY_BLOCKOUT_CHECK`, `SCALE_PROXY_DUMMY_REMOVAL_POLICY`, `SCALE_PROXY_TRACE_OVERLAY`, and `SCALE_PROXY_TO_HERO_BLOCKOUT_VERDICT`. Text-only projection math is not enough for render-bound handoff.
   - Step 2.8 must fill `SCALE_VISUAL_GUIDE_PACKAGE` and Step 2.9 must fill `SCALE_VISUAL_GUIDE_PROMPT_LOCK`; prompt prose alone cannot unlock image generation for a scale-critical human-enterable object.
   - Step 2.8 must also create a user-reviewable `VISUAL_GUIDE_COMPOSITE_PATH`: one composite image combining clay/solid blockout, lineart/wire, depth/normal/mask inset, perspective/vanishing lines, protagonist footpoint, projected baseline, door/passenger/protagonist height markers, support plane, and contact/cut/grip markers. Use `scripts/create_visual_guide_composite.py` when practical.
   - In scale-critical scenes, set `SCALE_COMPOSITE_HARD_LOCK: yes`: the approved composite is not the sole authority for the whole image, but it is the binding visual authority for scale. Character/object size, footpoints, door/passenger/container ratios, and screen occupancy must follow the composite overlays; if style, action, beauty framing, or prompt wording conflicts, composite scale wins.
   - After creating the visual guide composite, stop at the visual-guide checkpoint. Set `USER_VISUAL_GUIDE_CHECKPOINT_REQUIRED: yes`, show or reference the composite for user review, capture `USER_VISUAL_GUIDE_FEEDBACK`, apply the final feedback, and keep `PRE_IMAGE_HANDOFF_READY: no` until `USER_VISUAL_GUIDE_APPROVAL_STATUS: approved` and `USER_VISUAL_GUIDE_FEEDBACK_APPLIED: pass`.
   - Step 2.9 must fill `VISUAL_GUIDE_COMPOSITE_PROMPT_LOCK` and `IMAGE_INPUT_STACK_PLAN`: the composite is supplied to image generation as a structure reference for camera/perspective/scale/support/contact/object placement, while final art must not copy gray clay material, labels, arrows, or guide text.
   - The approved composite is not the only authority. Step 2.9 must fill `PRE_COMPOSITE_EVIDENCE_STACK_LOCK`, `SCALE_PROXY_TRACE_PROMPT_LOCK`, and `COMPOSITE_IS_REFERENCE_NOT_SOLE_AUTHORITY`: image generation inherits immutable user commands, source image/conditioning, object research, Step 2.1 perspective math, scale-proxy dummy projection, Blender blockout passes, visibility report, approved composite, and the compiled final prompt together.
   - Step 2.9 must also fill `SCALE_MUST_FOLLOW_COMPOSITE_PROMPT_LOCK`, and Step 8 must fill `SCALE_COMPOSITE_HARD_LOCK_VERDICT_CHECK`. If a generated image does not match the composite scale markers/ratios, it fails even if the style, face, or action looks good.
   - Step 2.9 must also fill the actual image-generation conditioning contract: `IMAGE_GEN_STRUCTURE_CONDITIONING_MODE`, `IMAGE_GEN_STRUCTURE_CONDITIONING_STRENGTH`, `IMAGE_GEN_STRUCTURE_CONDITIONING_INPUTS`, `IMAGE_GEN_STRUCTURE_CONDITIONING_LIMITS`, and `IMAGE_GEN_HANDOFF_PACKAGE_PATH`.
   - Use `openai_high_fidelity_image_inputs` when the runtime can attach the source image, approved visual guide composite, and optional clay/lineart/depth images to image generation. Use `external_controlnet` only when an external generator actually supports ControlNet/depth/lineart controls. Use `blocked_text_only` when image inputs cannot be supplied; in that state image generation is blocked rather than pretending prompt text can enforce scale.
   - Before `PRE_IMAGE_HANDOFF_READY: yes`, run `python scripts/create_image_gen_handoff_package.py <spec-path> --out <manifest-path> --prompt-out <handoff-prompt-path>` and record the manifest path in `IMAGE_GEN_HANDOFF_PACKAGE_PATH`.
   - Placeholder/proxy/SVG-only blockouts, “Blender unavailable” manifests, or unreviewed pseudo-passes may keep the run as `PRE_IMAGE_HANDOFF_READY: no`, but they must not unlock image generation for scale-critical scenes. This restriction does not ban the temporary adult scale proxy above; that dummy is valid only as a measured blockout witness and must be hidden/deleted before the composite/final art while its measurement trace remains.
   - If Blender is unavailable and a proxy visual-guide package is created, label it honestly as proxy evidence in `REAL_BLOCKOUT_EVIDENCE_STATUS`, `BLENDER_BLOCKOUT_REVIEW`, and `SCALE_VISUAL_GUIDE_PACKAGE`. Do not describe proxy outputs as real Blender renders or independent ControlNet/depth passes.
   - Proxy clay/lineart/depth/composite files must be meaningfully distinct before they are shown to the user: clay/solid uses filled masses and readable support planes; lineart/wire uses outlines, VP/grid/contact lines, and minimal fills; depth uses grayscale foreground-to-background separation with no decorative color/effect noise; composite displays the source passes as separate insets plus overlay notes. Do not save the same or near-identical guide image under multiple pass names.
   - When a user revises the clay/visual guide, update the relevant proxy/Blender pass artifacts or explicitly mark old pass artifacts stale. Do not leave `BLENDER_PASS_OUTPUTS` pointing at visually obsolete passes while only the composite has been corrected.
   - Step 2.9 must translate the camera into natural image language via `CAMERA_CLASS_PROMPT_OPENING`, `SCALE_CRITICAL_SHOT_CLASS_PROMPT_LOCK`, and `FACE_FOCAL_DEMOTION_PROMPT_LOCK`. It must also fill `PERSPECTIVE_CALCULATION_PROMPT_LOCK` and `SCREEN_OCCUPANCY_DERIVED_PROMPT_LOCK`, so the final handoff says screen/crop prominence comes from the camera while world scale follows the projected baseline at the protagonist footpoint. The final handoff prompt must open with the scale-proof camera sentence: visible/implicit internal occupant anatomy, door/window/seat/aisle modules, container length/width, protagonist screen occupancy, no close-up, face/eyes as small accents, and explicit “no drama/style/action scale enlargement” language.
17. Blender route policy:
   - Step 2.8 must fill a route decision before creating any `.blend` or visual-guide artifact.
   - Set `BLENDER_BLOCKOUT_REQUIRED: yes` only when the scene has background structures, architecture, vehicles, machinery, weapons/props with meaningful contact or grip mechanics, human-enterable scale comparison, complex perspective/support/contact, source-image structure that must be visually confirmed, or an explicit user request for Blender/3D/blockout/ControlNet/img2img.
   - Set `BLENDER_BLOCKOUT_REQUIRED: no` when the request is a simple prompt-only character portrait/half-body/full-body/fashion pinup on no background, plain background, abstract backdrop, or unspecified background, and no required object needs structural visual confirmation.
   - In the skip route, do not create `.blend` files, Blender render scripts, clay/lineart/depth/normal/mask pass outputs, visual-guide composites, ControlNet/img2img plans, or user visual-guide checkpoints. Mark those fields `not_applicable`, fill the skip reason, keep Step 2.8 as a 2D/anatomy/pose structural checklist, and let Step 2.9 use `IMAGE_GEN_STRUCTURE_CONDITIONING_MODE: direct_text_prompt`.
   - A skipped Blender route never bypasses anatomy, hand/finger, object-distortion, style, prompt-compiler, validator, or pipeline gates. If later fields discover a real structural staging risk, reopen Step 2.8 and switch to the Blender route before image handoff.
18. All named objects have a no-distortion rule. Do not allow style, hand/finger correction, cloak/blood/effects, action posing, or prompt compression to bend, warp, melt, resize, fuse, absorb, or texture-replace any registered object unless the user explicitly requests stylized deformation.
19. Step 8 must include a protagonist-to-object scale verdict and a humanoid scale-parity verdict. Compare the main character against visible humans/passengers/background humans/humanoids/humanoid monsters first, then doors, windows, vehicles, props, architecture modules, creature modules, and repeated scale witnesses. Size may change only by real body/object size, declared depth-plane transfer, perspective/lens projection, or explicit user symbolic-scale opt-in. Fail/rerender if drama, Redjuice density, focal importance, action, beauty, or composition enlarges/shrinks any person or object.
20. Step 8 must audit every explicit user instruction and every non-negotiable spec command one by one. A final pass cannot be claimed unless each item is satisfied, explicitly not applicable, or listed as a revision/rerender trigger.

21. Occlusion / protected-chain policy:
   - If a scene contains cloaks, hoods, hair masses, smoke, blood, glow, wings, creature bodies, black costume texture, heavy shadows, or dense background near anatomy/props, treat it as an occlusion-risk scene.
   - Read `references/theory-02g-occlusion-layer-separation.md` and record the read in the theory proof.
   - Build an occlusion layer graph before image translation: protected chains, occluder masses, depth order, visible landmarks, separation cues, and occlusion budget.
   - Protected chains include shoulder->elbow->wrist->hand, hip->knee->ankle->boot, palm->individual fingers->prop, and weapon hilt->blade->contact.
   - A cloak/hair/effect may overlap a chain but may not own its silhouette. If the chain cannot be traced, move/reduce the occluder or add rim light, negative-space slit, value/color edge, cast shadow, contour notch, or mask separation.
   - Final prompts must state the visual solution for high-risk overlaps, e.g. “red cloak behind black armored arm with a thin sky-blue rim gap,” not only “arm visible.”
   - Hands do not pass by existence alone. Any visible or pose-relevant hand must have a finger-topology lock: wrist -> palm block -> thumb wedge -> index/middle/ring/little start/direction/end or an explicit overlap/contact cue.
   - For each visible hand, assign a hand detail budget before style: focal/support/background role, minimum screen-read target, palm/thumb/finger detail required, and nearby cloak/blood/armor/background detail that must be reduced first.
   - Finger occlusion needs its own separation rule. A hand may be small or partially hidden, but it must not become a fused claw, black lump, melted glove, decorative armor noise, blood smear, or cloak tear. Use negative-space gaps, rim/value/hue edges, contour notches, or move the hand against a simpler background.
   - Step 8 must fail any visible hand that merely exists but does not read as human hand topology. “Hand present” is not enough; palm/thumb/finger structure must be readable at reduced size.
22. Object-density / structural-scale edge-case policy:
   - If a human figure appears in a scene with many props, vehicles, creatures, buildings, weapons, signage, particles, blood, smoke, crowds, or dense background systems, treat it as an anatomy-first density edge case.
   - Read `references/theory-02e-object-density-human-priority.md` and `references/theory-02f-structural-scale-capacity-verdict.md`, then record both reads in the theory proof.
   - Keep perspective, geometric blockout, scale anchors, support planes, and contact planes intact.
   - Within those structure locks, preserve body proportion, limb chains, hands, individual fingers, feet, grip, and contact anatomy before non-human detail.
   - Reduce background density, particle count, blood overlap, costume micro-trim, signage, creature texture, or prop clutter before hiding or fusing human anatomy.
   - Treat preservation as identity + shape quality + scale relation + relationship; a present-but-misshapen face, absorbed pants silhouette, interrupted arm chain, or protagonist-sized vehicle is still a failure.
   - Do not solve anatomy failures by pushing hands or feet unnaturally toward camera unless the composition intentionally requires that foreshortening.
22. Unknown object policy:
   - If an object cannot be named, functionally defined, placed on a plane, or assigned a relationship, do not convert it into random texture, fake signage, fake machinery, or unidentified pattern.
   - Resolve it by asking the user, researching it, removing it, replacing it with a known object, intentionally abstracting it with a declared function, or stopping the render-bound flow.
23. Blender / ControlNet hard-route policy:
   - Use Blender for every render-bound SPEC run. Do not treat Blender as conditional for final illustration or image-generation handoffs.
   - Set `BLENDER_BLOCKOUT_REQUIRED: yes` for all render-bound SPEC artifacts, including simple portraits; lower-complexity scenes may use a minimal camera/plane/mannequin blockout, but they still need Blender evidence.
   - When `BLENDER_BLOCKOUT_REQUIRED: yes`, create or reference a `.blend` file and a Blender Python render script before Step 3.
   - Render at least a clay/solid pass and one structure pass usable for conditioning or review: lineart/wire, depth, normal, or mask.
   - Each pass must be visually and functionally distinct. Clay/solid emphasizes volume and support masses; lineart/wire emphasizes outlines, perspective, and contact structure; depth/normal/mask emphasizes separable spatial or instance information. If the files are identical or nearly identical, they are not valid separate passes.
   - Record the `.blend`, render script, pass outputs, visual review, machine-readable visibility report, and downstream ControlNet/img2img plan in Step 2.8.
   - For scale-critical human-enterable scenes, place the temporary adult dummy/mannequin by a door/window/occupant landmark during the Blender/blockout phase, project that height to the protagonist footpoint, then hide/delete the dummy before composite export while retaining its height line, footpoint, and projected baseline trace.
   - After the Blender passes, create `VISUAL_GUIDE_COMPOSITE_PATH` before Step 2.9: one user-reviewable composite image that combines the clay/solid blockout, lineart/wire or mask structure, depth/normal inset when available, and drawn overlays for perspective/vanishing lines, support plane, projected baseline, protagonist footpoint, scale witnesses, scale-proxy trace, and important contact/cut/grip markers. The composite is not a substitute for distinct source passes; it must show or reference which distinct pass contributed which structural evidence.
   - The visual guide composite is the bridge between perspective math and image generation, but it is not the sole authority. It must travel with the source image, object research, perspective calculations, scale-proxy projection, Blender pass outputs, visibility review, and compiled final prompt. Raw equations, prose-only prompt locks, or composite-only handoffs cannot replace the full stack for render-bound handoff.
   - Stop at the visual-guide checkpoint after the composite is created. Set `USER_VISUAL_GUIDE_CHECKPOINT_REQUIRED: yes`, record `USER_VISUAL_GUIDE_FEEDBACK`, revise the blockout/composite if the user gives feedback, and do not proceed to Step 3 / Step 8 pre-image handoff / image generation until `USER_VISUAL_GUIDE_APPROVAL_STATUS: approved` and `USER_VISUAL_GUIDE_FEEDBACK_APPLIED: pass`.
   - Step 2.9 must record `VISUAL_GUIDE_COMPOSITE_PROMPT_LOCK`, `IMAGE_INPUT_STACK_PLAN`, `PRE_COMPOSITE_EVIDENCE_STACK_LOCK`, `SCALE_MUST_FOLLOW_COMPOSITE_PROMPT_LOCK`, and `COMPOSITE_IS_REFERENCE_NOT_SOLE_AUTHORITY`: the approved composite is supplied as a structure reference for camera, perspective, scale, support/contact, and placement. For scale, it is a hard lock; final art must still not copy gray clay material, labels, arrows, guide text, or the temporary scale dummy.
   - A blockout pass is not valid just because files exist. Step 2.8 must prove `BLOCKOUT_CORE_OBJECT_VISIBILITY`, `BLOCKOUT_TARGET_CONTACT_VISIBILITY` when action/contact exists, and `BLOCKOUT_CAMERA_OCCLUSION_CHECK`; render-bound handoff requires `BLENDER_VISIBILITY_REPORT_PATH` and `BLENDER_VISIBILITY_REPORT_REVIEW`.
   - The visibility report must show `report_ready: true`, `camera_not_occluded_by_buildings: true`, required `core_objects.*.visible: true`, required `target_contacts.*.visible: true` with `forbidden_target_hit: false`, and required `scale_anchors.*.visible: true`.
   - Treat Blender as structural evidence, not as the final aesthetic authority. The default handoff is a **loose guide** for edge treatment, mood, value grouping, and painterly compression only after structural invariants pass: camera, support/contact, scale anchors, perspective size relationships, adult/sex/age scale logic, major silhouettes, protected-chain landmarks, and named object/anatomy instance separation are non-negotiable.
   - Partial occlusion and dark massing are allowed only inside the Step 2.6/2.8 occlusion budget. They must not absorb shoulder-elbow-wrist-hand chains, hip-knee-ankle-boot chains, finger-to-prop chains, weapon hilt-to-blade chains, face planes, pants silhouettes, or vehicle/container scale anchors.
   - Do not let later style, value, line, color, or texture stages override the approved Blender camera, contact points, support planes, scale anchors, or named non-negotiable object relationships.
   - Do not let Blender harden the final image into a CAD-like, plastic, over-explained, or mannequin-like composition when the user’s target is painterly, editorial, anime, symbolic, or mood-first.
   - Do not express power hierarchy by making the ruler physically larger than perspective, anatomy, or adult male/female scale logic allows. For commercial illustration, show authority through staging, framing, value, gesture, costume, eye line, camera height, and detail priority rather than hieratic body-size distortion unless the user explicitly asks for symbolic scale.
   - If Blender is installed locally, prefer background rendering through the discovered `blender.exe` path; if unavailable, ask for/export viewport renders rather than pretending the `.blend` was reviewed.
24. User checkpoints:
   - Checkpoint A after perspective rig / composition direction when the view can branch.
   - Checkpoint B after unknown-object triage or object query when naming / replacement decisions are needed.
   - Checkpoint C after visual guide composite creation. Show or reference the composite, collect user feedback, apply the final feedback, and keep pre-image handoff blocked until the user approves the composite.
   - Checkpoint D before image generation when structure is locked and later corrections would be expensive.
   - If the choice is obvious and non-branching, record the assumed direction in the checkpoint field; if it is materially branching, ask the user before continuing.
25. Execute the stages in `references/main-process.md` in order unless the user explicitly scopes the task to a subset of stages.
26. Fill the stage results under clear headings and template fields, not just summary prose:
   - intent
   - silhouette/composition
   - perspective rig
   - object inventory from perspective
   - anatomy structure gate
   - anatomy primitive blockout
   - object knowledge query plan
   - object research handoff, if needed
   - object relationship check
   - anatomy-on-object relationship check
   - 3D blockout / modeling contract
   - Blender blockout artifacts and pass outputs when required
   - shared perspective / scale lock
   - detail-after-blockout lock
   - image translation lock
   - value
   - face
   - line/shape
   - color/accent
   - texture
   - final check
27. If background objects, props, furniture, machinery, weapons, signage, vehicles, architectural structures, source-image upgrade objects, visible hands/fingers, or anatomy-gated human figure structures need believable form, hand off to `object-research-skill` after Step 2.4 and before Step 2.6.
28. When Step 2.5 is required for a render-bound scene, create an object-research artifact from `templates/object-research-artifact-template.md` and record its path in the spec field `OBJECT_RESEARCH_ARTIFACT_PATH`. When the artifact is produced via a sub-agent or Codex bridge call, also record the invocation log path in `OBJECT_RESEARCH_INVOCATION_LOG_PATH` so the spec, artifact, and log can be cross-checked.
29. After the object-research handoff, revise object scale, perspective locks, inter-object contact, body structure, limb-chain logic, individual finger-chain modeling, and material planning before continuing to value design.
30. If the user requests the workspace reference look, read `references/style-guide.md`, record that read in the proof artifact, and fold its rules into the stage decisions only after structure locks remain readable.
31. Before setting `PRE_IMAGE_HANDOFF_READY: yes`, run the Final Prompt Compiler in Step 8:
   - `STRUCTURE_LOCK_SUMMARY`: internal high-risk structure summary only.
   - `AESTHETIC_RECOVERY_CHECK`: prove composition pressure, face/eye focal read, value masses, line/texture hierarchy, palette/accent discipline, and anti-generic style survived the structural gates.
   - `AESTHETIC_RENDER_BRIEF`: rewrite the render target as compact production image language.
   - `NEGATIVE_PROMPT_LIMITED`: keep only concrete failure defenses.
   - `FINAL_IMAGE_PROMPT_COMPILED`: the only pre-image prompt the pipeline should emit. Do not include schema field names, Tier labels, object IDs, validator/verdict jargon, or raw checklist prose.
32. Before treating the spec as complete, run `python scripts/validate_illustrate_spec.py <spec-path> --strict-object-research`.
33. If the validator fails, revise the failed sections instead of skipping forward.
34. Before any draft render handoff, run `python scripts/run_illustrate_pipeline.py <spec-path> --strict-object-research --emit-conditioning-manifest <manifest-path> --emit-conditioning-prompt <handoff-prompt-path>`.
35. If the user ultimately wants an image render, finish the theory-driven spec first, pass validation and the pipeline runner, then hand off to draft image generation.
36. Treat every generated image as a draft candidate until post-image visual verdict passes. After a generated image exists, set `POST_IMAGE_VERDICT_REQUIRED: yes`, fill the inline JSON and artifact, and accept only when contact target, cut-plane visibility, unknown cut-form rejection, dense environment, scale parity, scale visual guide compliance, hands/fingers, functional weapon grip, wrist force path, both arms, garment attachment, object distortion, command inheritance, and style all pass.

## CRITIQUE mode

1. Identify what artifact is being reviewed: illustration, prompt, process document, or stage output.
2. Read `references/main-process.md`.
3. Evaluate the artifact stage by stage against the process.
4. If a step has a mapped theory file, read it before judging that step.
5. Treat the user's verdict as the primary success/failure label whenever the user provides one.
6. Report findings in process order. Be explicit about what is missing, weak, or contradictory.
7. Structure the output as:
   - `User Verdict`
   - `System Read`
     - `intent`
     - `process`
     - `readability`
     - `delivery`
   - `Agreement / Tension`
   - `Next Move`
8. Recommend corrections as concrete edits, not vague advice.

## EXTEND mode

1. Treat each user-provided theory as an individual unit, not as a paragraph to merge into a generic step summary.
2. Clean formatting noise such as broken hyperlink residue, but do not discard semantic content.
3. Save each theory as its own file in `references/` using a stable name such as `theory-01-intent.md`.
4. Update `references/main-process.md` so the affected step points to the new theory file.
5. If the new theory changes how the skill should activate or route, update this `SKILL.md`.
6. Preserve the rule that process is the skeleton and theories are attached modules.

## Command Immutability (PSE absorption)

The PSE chain (PLAN -> SPEC -> EXECUTE -> VERIFY) is absorbed into the SPEC artifact so that user commands cannot be diluted, paraphrased, summarized, or silently dropped between stages.

1. Capture the user's exact instructions verbatim into `IMMUTABLE_USER_COMMANDS_VERBATIM` as a bulleted list. Each bullet is one discrete command or non-negotiable. Do not translate, shorten, rewrap, or normalize wording. Preserve the original language.
2. Set `COMMAND_DILUTION_POLICY: forbid` in the spec global header. Any other value fails validation for render-bound runs.
3. Each PIVA stage and Step 8 must repeat every IMMUTABLE_USER_COMMANDS_VERBATIM line as a verbatim substring inside its inheritance field:
   - `## PLAN Gate` -> `PLAN_COMMAND_INHERITANCE`
   - `## IMPLEMENT Gate` -> `IMPLEMENT_COMMAND_INHERITANCE`
   - `## VERIFY Gate` -> `VERIFY_COMMAND_INHERITANCE`
   - `## AUDIT Gate` -> `AUDIT_COMMAND_INHERITANCE`
   - `## Step 8 Final Check` -> `USER_COMMAND_COMPLIANCE_CHECK`
4. Each stage's inheritance field must do more than echo: append the stage-specific treatment after the verbatim quote (PLAN: "is non-negotiable / scale witness / object lock"; IMPLEMENT: "carried by Step X.Y field"; VERIFY: "guarded by pre-image test"; AUDIT: "fail/rerender trigger"; Step 8: "satisfied/partial/failed/not_applicable").
5. The validator runs a substring inheritance check (whitespace + case insensitive) and fails the spec if any immutable command goes missing or is paraphrased at any stage.
6. If a command becomes irrelevant or is superseded by a later user instruction, the user must explicitly retire it. Record the retired command and the retirement reason as a comment line inside `IMMUTABLE_USER_COMMANDS_VERBATIM` (e.g., prefixed with `# retired:`) rather than silently dropping it.
7. Image generation handoff is blocked while any inheritance field is empty, placeholder, or fails the substring check.

This rule absorbs Qplan's PSE handoff discipline: every stage proves it inherited the previous stage's commitments, so prompts and instructions cannot be quietly diluted between PLAN and the final image.

## Failure-First Loop

Recurring failures (finger fusion, protagonist-vs-container scale mismatch, hand-prop occlusion) are not solved by adding more rule paragraphs. They are solved by closing the feedback loop between past failures and the next render handoff.

1. Maintain `FAILURE_CATALOG_PATH` (default `.omx/failures.md`) as a cumulative log. Each entry records: run id, scene type, failure pattern, root cause, fix that worked, fix that did not.
2. Every render-bound SPEC quotes applicable past entries verbatim into `INHERITED_FAILURE_LESSONS`. "None" is allowed only as `none_with_reason: ...` explaining why no entry applies.
3. Every inherited lesson has a one-to-one matching entry in `NEGATIVE_PROMPT_DEFENSE`: a concrete prompt-side phrase that fights the named failure. Generic "bad hands / bad anatomy" alone is rejected; each defense must trace to a lesson.
4. `SCALE_CRITICAL_PROMPT_OPENING` must appear at the very start of `FINAL_IMAGE_PROMPT_COMPILED` for new specs (legacy `IMAGE_GEN_HANDOFF_PROMPT` only for old artifacts). Scale proof comes before face / style / action wording, not after. Brief leading framing such as "wide shot, " is allowed; long character/style preludes are not.
5. After each render, set `POST_IMAGE_VERDICT_REQUIRED: yes` and fill `POST_IMAGE_VISUAL_VERDICT_JSON` with structured booleans: `container_scale_pass`, `hero_fits_inside_object`, `occupant_anchor_valid`, `protagonist_to_occupant_ratio_pass`, `scale_visual_guide_pass`, `target_contact_pass`, `cut_plane_visibility_pass`, `unknown_cut_form_pass`, `dense_environment_pass`, `hand_topology_pass`, `finger_separation_pass`, `weapon_grip_mechanics_pass`, `wrist_force_path_pass`, `both_arms_present_pass`, `garment_attachment_pass`, `named_object_distortion_pass`, `command_inheritance_pass`, `style_target_pass`, `rerender_required`, plus `fail_reasons` and `rerender_priorities_tier_0_to_3`.
6. If any `*_pass` is false, `rerender_required` must be true and `POST_IMAGE_ACCEPTED` must be `no`. The validator rejects the contradiction "failures present but rerender_required: false" or "rerender_required: true but POST_IMAGE_ACCEPTED: yes."
7. A failed post-image verdict activates the repair compiler, not a blind rerun. Fill `POST_IMAGE_FAILURE_KEY_ROUTING`, create `templates/post-image-repair-artifact-template.md`, set `POST_IMAGE_REPAIR_COMPILER_STATUS: pass`, write `POST_IMAGE_NEXT_DRAFT_PROMPT`, and set `REGENERATION_GATE_STATUS: pass` before the next draft. `scripts/run_illustrate_pipeline.py` must emit `POST_IMAGE_NEXT_DRAFT_PROMPT` for this state; otherwise it emits `FINAL_IMAGE_PROMPT_COMPILED` for pre-image handoff.
8. `POST_IMAGE_NEXT_DRAFT_PROMPT` must differ from the failed compiled prompt; it must explicitly carry every failed verdict key into repair wording while remaining image language. For example, `target_contact_pass` promotes actor/tool/target/forbidden-target wording; `scale_visual_guide_pass` promotes guide-backed passenger/container/ratio witnesses; `cut_plane_visibility_pass` and `unknown_cut_form_pass` promote visible cut-plane/no-hidden-cut/no-protrusion wording; `weapon_grip_mechanics_pass` and `wrist_force_path_pass` promote hilt-in-palm, thumb opposition, finger wrap, and forearm/wrist load path; `garment_attachment_pass` promotes shoulder/collar/back attachment-origin wording.
9. If a failed key is scale-related (`container_scale_pass`, `hero_fits_inside_object`, `occupant_anchor_valid`, `protagonist_to_occupant_ratio_pass`, or `scale_visual_guide_pass`), repair camera/framing first through `POST_IMAGE_SCALE_FAILURE_SHOT_CLASS_ESCALATION` and the repair artifact's `SCALE_FAILURE_SHOT_CLASS_ESCALATION`: widen to extreme-wide/wide scale shot, reduce protagonist screen share, show the full container, add door/window/passenger/module witnesses, and demote face/eyes to small bright accents. Adding more ratio prose without changing shot class is not valid repair.
10. If a failed key is scale, cut-plane, or weapon-grip related, escalate immediately from text-only prompt repair to a visual guide package: annotated mask, crop guide, blockout overlay, lineart/depth/control pass, or equivalent evidence that separates IDs such as target neck vs forbidden body/wing, head-side/body-side cut plane, blade vs effect, cloak vs arm, passenger anchors vs texture, hilt vs palm, and wrist/forearm force path.
11. After every confirmed failure, append a new entry to `FAILURE_CATALOG_PATH` so the next SPEC can inherit it. The catalog is the long-term memory; the spec fields are the per-run instantiation.
12. Never label the first generated image as accepted just because pre-image validation passed. Pre-image validation authorizes a draft; post-image verdict authorizes acceptance.

## Working rules

- Run the process as `theory -> decision rule -> execution -> output -> gate`.
- Do not skip a gate just because the likely answer feels obvious.
- Do not claim that SPEC mode was completed correctly if the required stage fields are missing from the working artifact.
- For render-bound SPEC runs, do not jump directly from the raw user prompt to image generation.
- Object research must return draw-ready locks by lane: matched cards, missing/weak cards, scale/perspective locks, relationship notes, distortion fail conditions, and generation prompt locks.
- Step 2.6 must check object-object scale, occlusion, contact/support, collision, material/light interaction, rigid geometry, and text/glyph policy.
- Step 2.7 must check anatomy on top of objects: support, hand-prop relation, functional grip mechanics, wrist/forearm force path, foot-surface relation, torso action relation, and fail conditions.
- Text-only prompt locks do not count as execution evidence for scale-critical scenes, cutting/severing actions, or weapon/prop gripping hands. Fill `TEXT_ONLY_LOCKS_REJECTION` and route those risks through Step 2.8 visual guide packages, Step 2.9 prompt locks, and Step 8 verdict checks.
- Blender hard-route does not replace Step 2.1-2.7; it consumes their perspective, object, anatomy, and relationship locks and turns them into a reviewable/conditionable blockout.
- Blender hard-route is an evidence route, not a rigidity route: Step 2.8 must explicitly separate `STRUCTURAL_INVARIANTS_TO_PRESERVE` from `PAINTERLY_FREEDOMS_ALLOWED`, so the final handoff can use Blender as a loose guide for mood/edge treatment while keeping scale, contact, protected chains, and object/anatomy instance ownership strict. **Exception**: when `SCALE_CRITICAL_MODE: yes`, both lists must apply but `STRUCTURAL_INVARIANTS_TO_PRESERVE` dominates and `PAINTERLY_FREEDOMS_ALLOWED` may not loosen scale, occupant anchor, container ratio, or container module geometry.
- For scenes with full-body, humanoid, creature, architecture, vehicles, rooftops, streets, props, weapons, or strong perspective, Step 2.8 must use constructive geometric blockout: environment primitives and anatomy primitives must share one perspective grid and one scale system before detail is allowed.
- Step 2.8 must create or point to visual guide evidence packages for high-risk structure: `SCALE_VISUAL_GUIDE_PACKAGE`, `CUT_PLANE_VISUAL_GUIDE_PACKAGE`, and `GRIP_MECHANICS_VISUAL_GUIDE_PACKAGE` when those risks are present. These packages can be masks, overlays, Blender pass crops, lineart/depth/control references, or annotated blockout notes, but they cannot be prose-only.
- Human anatomy must be blockout-first when the body read matters: head sphere / box, ribcage box or barrel, pelvis box, limb cylinder chains, sphere joints, hand blocks / thumb wedges / individual thumb-index-middle-ring-little finger cylinder chains, and foot wedges on the support plane.
- Environment structure must also be blockout-first: slabs, boxes, planes, grids, mounted rectangles, support surfaces, facade modules, and scale anchors must be named before dense city, texture, signage, glow, or atmospheric detail.
- For architecture-scale scenes with figures, Step 2.8 must explicitly check body-to-architecture scale: window-to-head size, parapet/railing-to-body height, footprint on the support plane, and whether foreground enlargement is matched by nearby foreground anchors.
- For dense render-bound scenes, the final image prompt must be tiered rather than exhaustive: Tier 0 macro camera/scale/support/capacity; Tier 1 face plane and anatomy/limb/lower-body silhouettes; Tier 2 key props/contacts/separations; Tier 3 style/texture/effects that can be reduced.
- Irreversible structure does not mean dumping every registry item into the final prompt. Keep exhaustive lists in the spec/verdict; put only the highest-risk Tier 0-2 visual outcomes into `STRUCTURE_LOCK_SUMMARY`, then compile them into natural visual phrases inside `FINAL_IMAGE_PROMPT_COMPILED`.
- Camera class is compiled before style. For scale-critical scenes, `FINAL_IMAGE_PROMPT_COMPILED` begins with a natural camera/scale sentence such as “Extreme wide scale shot, no close-up heroine,” then names full container visibility, repeated modules, passenger/occupant witnesses, protagonist screen share, and face/eyes as small accents.
- Camera cuts and scale changes are never compiled directly from the user's wording. First compute scale in Step 2.1 by projecting a measured baseline to the protagonist/support plane, then prove it in Step 2.8 blockout/guide evidence, then translate it in Step 2.9/Step 8 natural prompt language. Screen occupancy, full-shot/knee-shot framing, and close camera crops are allowed only when marked as derived from camera perspective and explicitly prevented from overriding physical/world scale.
- Do not pass raw field names (`SCALE_VISUAL_GUIDE_PACKAGE`, `GRIP_MECHANICS_PROMPT_LOCK`, etc.), Tier labels, object IDs, validator/verdict terms, or Step numbers to image generation. Convert them to visible outcomes such as "long tram cabin with repeated window bays and passenger silhouettes" or "katana hilt seated in her palm with thumb opposition."
- Verdict must fail existence-only preservation: fail if a part exists but has wrong scale, wrong shape quality, broken contact/support, fusion/absorption, distortion/warping/melting, wrong protagonist-to-object scale, or wrong container capacity.
- Step 2.9 must lock image-generation priority order and non-negotiable structure before style density is allowed.
- Step 2.9 must state that primitive blockout, perspective, contact, and scale are solved before face, costume, lighting, color, texture, or decorative detail.
- Step 2.9 must state the Blender conditioning strength: `loose guide`, `medium guide`, or `strict guide`. Default to `loose guide` for painterly/editorial/anime/image-generation handoffs **unless `SCALE_CRITICAL_MODE: yes`**, the user asks for technical precision, product accuracy, orthographic consistency, or a mechanically exact scene — any of those forces `strict guide`. Loose guide never loosens scale, contact, protected-chain landmarks, or separate-instance ownership; in `SCALE_CRITICAL_MODE: yes` runs, strict guide overrides every loose-guide / painterly compression default elsewhere in this file.
- Step 2.9 must explicitly lock `NO_HIERATIC_SCALE_DISTORTION` for commercial illustration scenes with human figures: foreground adult men may appear larger in screen space than a farther seated woman when perspective requires it, while still remaining lower-detail and subordinate by value/composition.
- Treat any prompt/order to make the protagonist or another important human/humanoid larger/smaller for emphasis as invalid for scale. Ignore the size command and satisfy emphasis through camera placement, value, lighting, framing, gesture, silhouette, focus, color accent, or detail priority. The Step 2.1 perspective process is the only place where drawing size is computed.
- Every visible human/humanoid must be comparable against the protagonist through `HUMANOID_DEPTH_PLANE_MAP` and `HERO_SECONDARY_HUMANOID_SCALE_PARITY_LOCK`; background passengers/crowds are not decorative scale texture.
- In human-enterable-object scenes, compare protagonist -> internal occupant anatomy anchor -> doors/windows/seats/aisles/floor modules -> whole object. If those disagree, revise object scale before style.
- For action scenes where a target is cut/severed/damaged, Step 2.2M and Step 2.8/2.9 must preserve the post-action object state: visible target cut plane/cross-section, head-side/body-side continuity when relevant, no unknown protrusions/blobs, and a fail trigger if the cut is hidden by protagonist, cloak, weapon, blood, or effects.
- Step 2.3 must lock an age-band body base, a sex-classification read, a temporary default body-type baseline, and the hand submodule relationship before hand rendering decisions are trusted.
- For visible hands and fingers, especially focal hands, expressive gestures, foreshortened poses, or prop-holding grips, default toward Step 2.5 as an anatomy submodule lookup instead of guessing.
- For grounded full-body or standing poses, Step 2.3 must include support-leg, balance-line, and shoulder/pelvis logic that explains why the pose is physically supportable.
- For anatomy-gated scenes, Step 2.5 should return the anatomy references that Step 2.7 will apply: age-band body base, sex overlay, and hand submodule when hands matter.
- For visible hands that materially affect silhouette or storytelling, Step 2.3 must include a hand silhouette read and an individual finger-chain modeling note before Step 3. Do not group or fuse fingers as a shortcut, even when the hand is small or the scene is object-dense.
- For every visible hand, Step 2.3 must fill `HAND_DETAIL_BUDGET`, `FINGER_TOPOLOGY_CHAIN_LOCK`, and `FINGER_TOPOLOGY_FAIL_CONDITIONS`; Step 2.6 must fill `FINGER_OCCLUSION_SEPARATION_RULE`; Step 2.9 must carry the lock into `PROMPT_FINGER_TOPOLOGY_LOCK`; Step 8 must judge `FINGER_TOPOLOGY_VERDICT_CHECK`.
- The final image prompt must mention each visible hand separately when hands matter. Do not write generic “hands readable.” Name the sword/prop hand, rear/free hand, support hand, or gesture hand, and state palm block, thumb wedge, separated finger shapes/gaps, and what nearby detail is suppressed before finger topology is sacrificed.
- For weapon/prop hands, finger topology alone is insufficient. Step 2.7 must specify functional grip mechanics (`FUNCTIONAL_GRIP_MECHANICS_CONTRACT`) and wrist/forearm load transfer (`WRIST_FORCE_PATH_CHECK`); Step 2.8 must provide a visual guide; Step 2.9 must lock hilt-in-palm/thumb opposition/finger wrap/neutral wrist wording; Step 8 must fail impossible grip even when all fingers are separated.
- Finger-collapse prevention is a skill-level gate. Before prompt handoff, identify the likely failure cause: prompt attention overload, hands too small on screen, weapon guard/hilt/sleeve/blood/cloak occlusion, dark costume texture absorption, or generic “hand visible” wording. Fix the cause structurally by simplifying nearby detail, adding negative-space/rim/value separation, naming one hand at a time, and preserving wrist -> palm block -> thumb wedge -> index/middle/ring/little chain. If the hand cannot be readable at the chosen camera/framing, change framing or reduce occluders/background density before generation; do not fuse fingers or enlarge hands outside anatomy scale.
- When Step 2.5 is needed, Step 2.6 and Step 2.7 are mandatory before Step 3.
- Keep style knowledge out of this file; point to `references/style-guide.md`.
- Keep user-specific context out of this file; point to `references/domain_context.md`.
- If the user gives a new theory in Korean, it is acceptable for the reference file to stay close to the user's original meaning while the process file remains English.
- If the user asks only for one stage, still state what upstream assumptions you inherited.

## Required SPEC artifact

For full-scene SPEC runs that are meant to drive rendering:

1. Create or update a spec file from `templates/illustrate-spec-template.md`.
2. Create or update a proof file from `templates/theory-read-proof-template.md` and record its path in the spec.
3. Fill all global fields plus every required step field.
4. If Step 2.5 is required, create an object-research artifact from `templates/object-research-artifact-template.md` and record its path in the spec.
5. Mark gate status explicitly per step.
6. Run `scripts/validate_illustrate_spec.py` before claiming completion.
7. Run `scripts/run_illustrate_pipeline.py` before any draft image-generation handoff.
8. After generation, run the post-image visual verdict before treating the output as accepted.
8. Keep validator / pipeline output as part of the verification trail.

## Silent pre-image handoff

When the user ultimately asked for an image and the SPEC, theory proof, object
research artifacts, validation, and pipeline runner have all passed, continue
directly to the draft image-generation tool instead of posting a long chat
status report.

- Do not print Step 1-8 summaries, full artifact path lists, full prompts, or
  validator logs immediately before image generation.
- Keep those details in the spec, proof, object-research artifact, pipeline log,
  and emitted prompt file.
- If a required checkpoint is genuinely blocking handoff (for example a
  scale-critical visual-guide approval), ask only for that checkpoint; otherwise
  do not create a user-facing pause.
- Use a single image-generation call with the shortest production prompt that
  preserves the compiled non-negotiables.
- If image generation fails, report only the minimal actionable error and retry
  with backoff / a shorter prompt rather than streaming the full workflow state.
- Step 1-8 stage bullets are for stopped text deliverables, critique/handoff
  summaries, or explicit user requests for proof; they are not a mandatory
  pre-image chat report after the pipeline has already passed.

## Outputs

Prefer concise, production-usable outputs:

- one-line scene intent
- composition map
- value plan
- facial focal rules
- line and shape hierarchy
- palette and accent plan
- texture density plan
- final gate verdict

When extending the skill, list changed files and the new theory-to-step mapping.
