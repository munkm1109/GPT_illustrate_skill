# Illustrate Spec Template

Use this template for `illustrate-skill` `SPEC` runs that are meant to produce a final illustration or image-generation handoff.

Recommended workflow:

1. Copy this file to a working spec path such as `.omx/runs/<YYYYMMDD>-<scene-slug>-spec.md`.
2. Create a theory-read proof artifact from `templates/theory-read-proof-template.md` and record its path in `THEORY_READ_PROOF_PATH`.
3. Fill the PIVA lifecycle gates first: PLAN captures requirements, IMPLEMENT maps Step 0-8 work, VERIFY proves the prompt/spec before image generation, and AUDIT defines command/visual fail triggers.
4. Before Step 1, ask and record the Render Style Baseline Gate. The user must choose one primary target among the five render families and may approve a recommended mix before image handoff.
5. Choose exactly one Step 0 intake route: `image_development` for developing an already-generated/source image, or `prompt_only` for 100% prompt-based first generation.
6. Resolve the structural preflight in order: render style baseline -> route intake -> intent -> perspective rig -> scale-anchor judgment -> object inventory -> Step 2.2M normalized Scene Contract -> anatomy object inventory -> object query -> relationship checks -> Step 2.8 Blender route decision -> execution-proof visual guide gates only when scale/cut/grip/structural staging requires them -> structural-invariant/painterly-freedom split -> image translation lock.
7. If Step 2.5 is needed, create an object-research artifact from `templates/object-research-artifact-template.md`.
8. Pause at user checkpoints when direction is ambiguous, unknown objects remain, or a user-visible branch must be chosen.
9. Do not replace unknown objects with random patterns, fake signage, fake mechanical texture, or unidentified noise.
10. Fill every field before claiming the staged spec is complete.
11. Run `python scripts/validate_illustrate_spec.py <spec-path> --strict-object-research`.
12. Revise failed sections until the validator passes.
13. Run `python scripts/run_illustrate_pipeline.py <spec-path> --strict-object-research`.
14. For render-bound deliverables, Step 2.8 must decide the Blender route. Use `BLENDER_BLOCKOUT_REQUIRED: yes` only for background structures, architecture, vehicles, machinery, weapons/props with meaningful contact/grip, scale-critical human-enterable scenes, complex perspective/support/contact, source-image structural confirmation, or explicit user request. If the user gives no background or asks for no/simple/plain background and the scene is a simple character-only prompt with no structural staging risk, set `BLENDER_BLOCKOUT_REQUIRED: no`, mark Blender/visual-guide/ControlNet fields `not_applicable`, and continue to compact direct image prompt handoff after validation/pipeline.
15. Text-only locks are never enough for scale-critical, action-cut, or weapon-grip failures: those cases must carry a visual guide package (mask/overlay/blockout/lineart/depth/control reference), prompt lock, and Step 8 verdict check before image generation.
16. Before `PRE_IMAGE_HANDOFF_READY: yes`, run the Final Prompt Compiler: summarize structure locks internally, restore aesthetic image language, limit negative prompts, and write `FINAL_IMAGE_PROMPT_COMPILED` without schema field names such as `SCALE_VISUAL_GUIDE_PACKAGE`, `Tier 0`, or validator/verdict jargon.
17. Fill `POST_IMAGE_VISUAL_VERDICT_*` only after an image exists and `POST_IMAGE_VERDICT_REQUIRED: yes`; first generation is a draft candidate and cannot be treated as accepted until the post-image visual verdict passes.
18. If post-image verdict fails (`rerender_required: true`, `POST_IMAGE_ACCEPTED: no`), create `templates/post-image-repair-artifact-template.md`, route every failed key through `POST_IMAGE_FAILURE_KEY_ROUTING`, compile `POST_IMAGE_NEXT_DRAFT_PROMPT`, set `POST_IMAGE_REPAIR_COMPILER_STATUS: pass` and `REGENERATION_GATE_STATUS: pass`, and rerun only from the repaired prompt (never the unchanged failed prompt).

[ILLUSTRATE_SPEC]

REQUEST_SUMMARY: <normalize the user request into one concise brief>
USER_COMMAND_CHECKLIST: <list every explicit user command and non-negotiable request; Step 8 must audit each item>
IMMUTABLE_USER_COMMANDS_VERBATIM:
- <verbatim quoted user instruction; do NOT paraphrase, summarize, translate, or shorten>
- <one line per discrete command/non-negotiable; preserve original language and wording>
- <every line listed here is the inheritance source for PLAN/IMPLEMENT/VERIFY/AUDIT/Step 8>
COMMAND_DILUTION_POLICY: <"forbid"; downstream stages must reference each immutable command as a substring, not as a paraphrase or summary>
DELIVERABLE: <spec only | spec + image generation>
WORKSPACE_STYLE_MODE: <workspace reference style | derived skill | custom>
RENDER_STYLE_BASELINE_QUESTION: <the exact initial question asked to the user; must present all five axes: axis_1_2d_anime, axis_2_semi_real_concept, axis_3_3d_render, axis_4_live_action_cosplay, axis_5_game_cg_key_visual, plus recommended mix guidance>
RENDER_STYLE_USER_DECISION: <verbatim user answer or "pending_user_answer"; PRE_IMAGE_HANDOFF_READY must remain no while pending>
RENDER_STYLE_PRIMARY_AXIS: <axis_1_2d_anime|axis_2_semi_real_concept|axis_3_3d_render|axis_4_live_action_cosplay|axis_5_game_cg_key_visual|custom_user_axis>
RENDER_STYLE_SECONDARY_AXES: <none|axis_1_2d_anime|axis_2_semi_real_concept|axis_3_3d_render|axis_4_live_action_cosplay|axis_5_game_cg_key_visual|custom_mix; list approved secondary axes only>
RENDER_STYLE_MIXING_POLICY: <allowed/recommended mix, e.g. axis_1+axis_2 for anime painterly mood, axis_1+axis_5 for anime game key visual, axis_2+axis_5 for cinematic concept art, axis_4+axis_5 only for cosplay poster; state why>
RENDER_STYLE_DRIFT_GUARD: <explicitly forbidden drift families, e.g. no live-action/cosplay/photo realism, no 3D figure look, no semi-real skin pores, no pastel anime drift>
RENDER_STYLE_PROMPT_ANCHOR: <first-sentence natural-language prompt anchor that locks the chosen render family before materials/camera/style details>
SOURCE_IMAGE_UPGRADE: <yes|no>
INPUT_ROUTE: <image_development|prompt_only>
SOURCE_IMAGE_ACTUAL_CONDITIONING: <yes|no|not_applicable; yes only when the actual source image can be supplied to image generation/control conditioning>
IMAGE_DEVELOPMENT_ALLOWED: <yes|blocked|prompt_only_fallback|not_applicable; prompt_only_fallback means source was analyzed but generation is text-only reinterpretation>
OBJECT_RESEARCH_REQUIRED: <yes|no>
SCALE_CRITICAL_MODE: <yes|no; yes when a protagonist/main human/humanoid/humanoid monster is compared against a human-enterable object>
SCALE_CRITICAL_REASON: <why scale-critical mode is active or not_applicable>
USER_CAMERA_CLASS_PRESET: <not_applicable | extreme_wide_scale_shot | wide_establishing_shot | wide_action_shot | full_body_action_shot | medium_action_shot | close_portrait_shot | low_angle_hero_shot | top_down_diagrammatic_shot | telephoto_compressed_city_shot | dutch_angle_dynamic_shot | custom_user_camera_class>
USER_CAMERA_CLASS_LOCK_LEVEL: <soft|hard|adaptive|not_applicable; hard preserves the user preset, adaptive allows repair escalation, soft allows scale-safe correction>
USER_CAMERA_CLASS_REASON: <why this camera class was chosen by the user or assumed; not_applicable only when deliverable is spec-only/non-render-bound>
IMAGE_GEN_READY: <no>
PRE_IMAGE_HANDOFF_READY: <no>
POST_IMAGE_VERDICT_REQUIRED: <no>
POST_IMAGE_ACCEPTED: <not_applicable>
THEORY_READ_PROOF_PATH: <relative path>
FAILURE_CATALOG_PATH: <relative path to .omx/failures.md or equivalent cumulative failure log; "none" only if no prior runs exist>
INHERITED_FAILURE_LESSONS:
- <one bullet per applicable past-failure pattern from FAILURE_CATALOG_PATH; quote the lesson verbatim with date/run id>
- <e.g., "20260424-10 dragon-tram: 검 손잡이가 hilt+blade로 손가락 위를 덮어 finger fusion 발생">
- <"none_with_reason: <why no prior failures apply>" is the only valid empty state>
NEGATIVE_PROMPT_DEFENSE:
- <one specific negative-prompt phrase per inherited lesson; concrete word/clause that fights the named failure>
- <e.g., "no fused fingers behind sword guard; sword hilt below wrist line, not crossing finger silhouettes">
- <generic "bad hands" / "bad anatomy" alone is insufficient; each defense must trace to a lesson>

## PLAN Gate
THEORY_FILES:
- illustrate-skill/references/pipeline-plan-implement-verify-audit.md

PIVA_MODE: enabled
PLAN_USER_COMMAND_SOURCE: <quote/normalize the explicit user commands and source prompt policy>
PLAN_COMMAND_INHERITANCE: <one row per IMMUTABLE_USER_COMMANDS_VERBATIM line; each row repeats the verbatim command and notes how PLAN treats it (non-negotiable / scale witness / object lock / style lock); paraphrase forbidden>
PLAN_NON_NEGOTIABLES: <structure/style/scale/object/anatomy commands that must not be broken>
PLAN_OBJECT_ANATOMY_SCALE_WITNESSES: <objects, humans/passengers, doors/windows, props, architecture, creature modules, or other witnesses used to prove scale>
PLAN_HUMANOID_ANATOMY_SCALE_PARITY: <which visible humans/humanoids/humanoid monsters become anatomy objects and how protagonist scale will be compared against them by perspective depth plane>
PLAN_PREVIOUS_FAILURES: <known prior failures to prevent, or none_with_reason>
PLAN_GATE_STATUS: <pass|needs_revision>

## IMPLEMENT Gate
THEORY_FILES:
- illustrate-skill/references/pipeline-plan-implement-verify-audit.md

IMPLEMENT_COMMAND_INHERITANCE: <repeat every IMMUTABLE_USER_COMMANDS_VERBATIM line verbatim; for each, name the Step 0-8 field(s) that carry it; paraphrase forbidden>
IMPLEMENT_STEP_MAP: <how existing Step 0-8 fields implement each plan non-negotiable>
IMPLEMENT_OBJECT_RESEARCH_TRANSFER: <how object research/card results become scale witnesses, prompt locks, verify tests, and audit triggers>
IMPLEMENT_SCALE_TRANSFER: <how perspective/scale/capacity facts transfer into Step 2.1/2.8/2.9 and prompt language>
IMPLEMENT_HUMANOID_SCALE_TRANSFER: <how Step 2.2 visible humanoid candidates transfer to Step 2.3 anatomy objects, Step 2.8 parity blockout, Step 2.9 prompt lock, and Step 8 verdict>
IMPLEMENT_STYLE_TRANSFER: <how style wrapper rules apply after structure locks pass>
IMPLEMENT_PROMPT_DRAFT_TRANSFER: <how final prompt carries only highest-risk visual outcomes without losing non-negotiables>
IMPLEMENT_GATE_STATUS: <pass|needs_revision>

## VERIFY Gate
THEORY_FILES:
- illustrate-skill/references/pipeline-plan-implement-verify-audit.md

VERIFY_COMMAND_INHERITANCE: <repeat every IMMUTABLE_USER_COMMANDS_VERBATIM line verbatim; for each, name the pre-image test that proves the prompt cannot violate it; paraphrase forbidden>
VERIFY_OBJECT_DISTORTION_TEST: <pre-image test that all named objects keep silhouette/axis/function/material/scale and do not bend/warp/melt/fuse>
VERIFY_HERO_OBJECT_SCALE_TEST: <pre-image test comparing protagonist against scale witnesses and checking prompt wording cannot create giant/protagonist-sized object drift>
VERIFY_HUMANOID_SCALE_PARITY_TEST: <pre-image test comparing protagonist to each background human/humanoid/humanoid monster by depth plane and rejecting miniature/giant/texture humanoids>
VERIFY_OBJECT_RESEARCH_TRANSFER_TEST: <pre-image test that researched facts appear in prompt locks and audit fields, not only in research artifact>
VERIFY_STYLE_TARGET_TEST: <pre-image test that target style is actionable line/plane/value/texture grammar, not just a label>
VERIFY_PROMPT_CONFLICT_TEST: <identify action/camera/style words that could overpower scale, object geometry, or command locks; record mitigation>
VERIFY_GATE_STATUS: <pass|needs_revision>

## AUDIT Gate
THEORY_FILES:
- illustrate-skill/references/pipeline-plan-implement-verify-audit.md

AUDIT_COMMAND_INHERITANCE: <repeat every IMMUTABLE_USER_COMMANDS_VERBATIM line verbatim; for each, list pre-image and post-image triggers that fail/rerender on violation; paraphrase forbidden>
AUDIT_PRE_IMAGE_COMMAND_AUDIT: <one-by-one pre-image audit of IMMUTABLE_USER_COMMANDS_VERBATIM and PLAN_NON_NEGOTIABLES; status per command: satisfied / partial / failed / not_applicable>
AUDIT_PRE_IMAGE_NON_NEGOTIABLE_AUDIT: <pre-image audit of object distortion, hero/object scale, humanoid scale parity, object research transfer, style transfer, and prompt conflicts>
AUDIT_HUMANOID_SCALE_PARITY_TRIGGER: <post-image fail/rerender trigger when protagonist and any visible background human/humanoid/humanoid monster break perspective-only scale parity>
AUDIT_POST_IMAGE_VISUAL_AUDIT_PLAN: <post-image visual checks to run before accepting output; include scale, object distortion, command compliance, style fidelity>
AUDIT_RERENDER_TRIGGERS: <concrete failures that force revision/rerender>
AUDIT_GATE_STATUS: <pass|needs_revision>
IMAGE_HANDOFF_GATE_STATUS: <pass|blocked>

## Step 0 Route Gate

INPUT_ROUTE: <image_development|prompt_only>
ROUTE_REASON: <why the request uses this route; image_development means an existing/generated/source image is being developed; prompt_only means first generation from text only>
EXISTING_IMAGE_INPUT: <yes|no>
PROMPT_ONLY_GENERATION: <yes|no>
SOURCE_IMAGE_ACTUAL_CONDITIONING: <yes|no|not_applicable; yes only when source pixels/control reference can actually condition generation>
IMAGE_DEVELOPMENT_ALLOWED: <yes|blocked|prompt_only_fallback|not_applicable>
IMAGE_DEVELOPMENT_CONDITIONING_NOTE: <if image_development has no actual conditioning, state that this is descriptive reinterpretation/prompt-only fallback, not true image development>
ACTIVE_INTAKE_BRANCH: <step_0a_existing_image_development|step_0b_prompt_only>
INACTIVE_BRANCH_POLICY: <the inactive branch must remain not_applicable and must not impose source/post-image evidence on prompt-only generation>
ROUTE_GATE_STATUS: <pass|needs_revision>
GATE_STATUS: <pass|needs_revision>

## Step 0A Existing Image Development Intake

SOURCE_IMAGE_REFERENCE: <path/name/description of the existing or previously generated image being developed, or not_applicable when inactive>
PREVIOUS_IMAGE_VISUAL_VERDICT_SUMMARY: <source/previous image findings: pass/fail on scale, hands, object distortion, command compliance, style; not the post-verdict for a new image>
SOURCE_IMAGE_OBJECTS_PRESENT: <recognized concrete objects already visible in the source image; transfer to Step 2.2>
SOURCE_IMAGE_TRANSFER_SCOPE: <structure_only by default: source can transfer object identity, relationships, pose/action, scale/perspective evidence, and failure clues; source style/design requires explicit user opt-in>
SOURCE_IMAGE_STYLE_DESIGN_FIREWALL: <explicitly forbid carrying over source style, palette, linework, brush/medium texture, character/costume design, creature design, prop design, or composition-design motifs unless the user explicitly requested them>
SOURCE_IMAGE_ALLOWED_TRANSFER: <allowed source evidence: concrete objects, support/contact, perspective, scale witnesses, action target, anatomy/hand/prop failures, rough story beat>
SOURCE_IMAGE_FORBIDDEN_TRANSFER: <forbidden source evidence: source rendering style, color palette, line style, medium texture, costume/design language, creature design language, decorative motifs, and source-specific composition design if a new style is requested>
SOURCE_IMAGE_REDESIGN_DIRECTIVE: <how the target style/wrapper must redesign silhouette, value, line, palette, costume/creature/detail language after structure locks pass>
SOURCE_IMAGE_PROMPT_FIREWALL: <final prompt wording that says source image is structure/object reference only and must not copy source style/design/palette/linework/brush/design motifs>
PRESERVE_OBJECTS: <structural objects/relationships to keep; do not list source style/design here unless explicitly requested>
CHANGE_OBJECTS: <objects/features/failures to revise>
REMOVE_OBJECTS: <objects/features to remove, or none_with_reason>
FAILURE_CAUSE_MAP: <failure -> likely cause -> next-spec prevention rule>
PREVIOUS_IMAGE_LESSONS: <lessons inherited from this image, distinct from cumulative FAILURE_CATALOG_PATH>
ROUTE_A_OUTPUT_TO_STEP_1_2_2: <how this branch fills Step 1 intent and Step 2.2 source object inventory>
GATE_STATUS: <pass|not_applicable|needs_revision>

## Step 0B Prompt-Only Intake

PROMPT_OBJECT_CANDIDATES: <objects implied by the text prompt; no existing image evidence required>
PROMPT_IMPLIED_ENVIRONMENT: <environment/plane/scale assumptions derived from prompt language>
PROMPT_IMPLIED_ANATOMY: <human/humanoid/hand/pose candidates implied by the prompt, or none_with_reason>
PROMPT_AMBIGUITY_ASSUMPTIONS: <explicit assumptions made without asking; unknowns that must be researched or locked later>
ROUTE_B_OUTPUT_TO_STEP_1_2_2: <how this branch fills Step 1 intent and Step 2.2 object inventory>
GATE_STATUS: <pass|not_applicable|needs_revision>

## Step 1 Intent
THEORY_FILES:
- illustrate-skill/references/theory-01-intent.md

SCENE_INTENT_SENTENCE:
ENVIRONMENT:
TIME_OR_LIGHTING:
ROLE:
ACTION:
EMOTION_AXIS:
AUDIENCE_FEELING:
GATE_STATUS: <pass|needs_revision>

## Step 2 Composition
THEORY_FILES:
- illustrate-skill/references/theory-02-composition-silhouette.md
- illustrate-skill/references/theory-02b-balance-cog.md
- illustrate-skill/references/theory-02j-camera-class-scale-gate.md

THUMBNAIL_SET:
CHOSEN_COMPOSITION_TYPE:
CHARACTER_POSITION:
CAMERA_ANGLE:
USER_CAMERA_CLASS_PRESET: <repeat global user camera preset exactly; not_applicable only when no camera preference exists>
USER_CAMERA_CLASS_LOCK_LEVEL: <repeat global lock level exactly>
USER_CAMERA_CLASS_REASON: <camera intent and tradeoff: scale proof, action drama, portrait emotion, architecture read, etc.>
CAMERA_CLASS_CONFLICT_STATUS: <none|conflict|resolved|not_applicable; conflict when user camera class fights scale/object/action proof>
CAMERA_CLASS_CONFLICT_REASON: <if conflict/resolved, explain e.g. close portrait cannot prove tram/person scale; otherwise none_with_reason>
CAMERA_CLASS_RESOLUTION: <if soft/adaptive conflict, chosen camera override; if hard conflict, block/ask before image handoff; otherwise none_with_reason>
CHOSEN_CAMERA_CLASS: <actual camera class used downstream; for scale-critical human-enterable scenes default extreme_wide_scale_shot or wide_scale_shot unless explicitly resolved>
CAMERA_CLASS_VISUAL_TRANSLATION: <natural picture-language translation of the camera class; no raw field names in final prompt>
BLACK_MASS_MAP:
NEGATIVE_SPACE_BALANCE:
FLOW_DIRECTION_MAP:
COMPOSITION_OBJECT_ROLE_SUMMARY:
USER_CHECKPOINT_A_DIRECTION:
GATE_STATUS: <pass|needs_revision>

## Step 2.1 Perspective Rig
THEORY_FILES:
- illustrate-skill/references/theory-02-composition-silhouette.md
- illustrate-skill/references/theory-02f-structural-scale-capacity-verdict.md
- illustrate-skill/references/theory-02h-object-distortion-command-verdict.md
- illustrate-skill/references/theory-02i-all-humanoids-anatomy-perspective-scale.md
- illustrate-skill/references/theory-02j-camera-class-scale-gate.md

CAMERA_POSITION:
SCALE_CRITICAL_SHOT_CLASS: <if SCALE_CRITICAL_MODE yes: extreme_wide_scale_shot / wide_scale_shot / wide_establishing_shot that proves scale; else not_applicable>
FULL_CONTAINER_VISIBILITY_REQUIREMENT: <if scale-critical: minimum full vehicle/container visibility, e.g. 2-3 cars or 12+ window/door bays; include number>
SCALE_WITNESS_MIN_COUNT: <if scale-critical: minimum visible passengers/doors/windows/modules/rails/building modules; include number>
HERO_TO_MODULE_VISUAL_RATIO: <if scale-critical: protagonist height relative to one door/window/passenger/adult module and visible container length; include number/ratio>
CLOSEUP_BLOCKED_UNTIL_SCALE_PASS: <yes|no|not_applicable; yes for scale-critical unless user explicitly accepts blocked hard conflict>
FACE_FOCAL_DEMOTION_FOR_SCALE: <if scale-critical: face/eyes remain small bright accents, not a close-up portrait, until scale verdict passes>
PERSPECTIVE_SCALE_TRANSFER_MODE: <projected_measurement|depth_plane_projection|blockout_projection|not_applicable; required when camera cut or scale changes>
HERO_FOOTPOINT_PLANE: <support/depth plane of protagonist feet/body contact, e.g. tram_roof_plane; include how it connects to perspective grid>
BASELINE_OBJECT: <object used as measurement baseline, e.g. 1.95m tram door / 1.65m passenger / roof width; it does not need to sit next to the protagonist>
PROJECTED_BASELINE_TO_HERO_POSITION: <numeric projection of baseline to protagonist foot position, e.g. projected door height at H1 footpoint = 1.95m, H1=1.58m=0.81 door>
SCREEN_OCCUPANCY_IS_DERIVED: <yes|no|not_applicable; yes means screen size comes from camera/crop after world scale is solved>
SCREEN_OCCUPANCY_MUST_NOT_OVERRIDE_WORLD_SCALE: <yes|no|not_applicable; yes means screen share can never resize the protagonist/object in-world>
CAMERA_CUT_SCALE_RECONCILIATION: <how requested camera cut/full-shot/close distance is reconciled with projected world scale before prompt handoff>
SCALE_PROXY_DUMMY_REQUIRED: <yes|no; yes for scale-critical human-enterable scenes so a temporary adult dummy/mannequin is used as the near-door scale witness before visual guide composite>
SCALE_PROXY_DUMMY_HEIGHT: <numeric adult dummy/mannequin height, e.g. 1.65m or 1.70m; use same units as the door/passenger/protagonist scale ladder>
SCALE_PROXY_DUMMY_BASELINE_OBJECT: <door/window/aisle/seat/roof/cabin landmark the temporary dummy stands beside; must be on the same perspective grid as the protagonist projection>
SCALE_PROXY_DUMMY_PLACEMENT_PLAN: <where the temporary adult dummy is placed during perspective calculation, e.g. beside tram door D1 on the roof/cabin depth plane; include footpoint and near/far relation>
SCALE_PROXY_DUMMY_TO_HERO_PROJECTION: <numeric projection from temporary dummy/door baseline to protagonist footpoint; this happens before blockout and before composite generation>
HORIZON_LINE:
VANISHING_POINTS:
PRIMARY_DEPTH_AXIS:
SUPPORT_PLANES:
VERTICAL_PLANE_LOCKS:
SCALE_ANCHOR_OBJECTS:
SCALE_ANCHOR_CANDIDATES: <list all possible human/object/architecture/vehicle anchors before choosing; include doors/windows/tram/parapets/signage/crowd when present>
SCALE_BASELINE_SELECTION: <state the primary baseline, usually adult human body/head/door; explain why it is reliable in this camera>
SCALE_ANCHOR_RANKING: <rank primary/secondary/tertiary anchors by reliability and depth plane>
SCALE_RATIO_JUDGMENT_METHOD: <how ratios are judged: human height to door, head to window, foot to support plane, tram roof to passenger body, etc.>
SCALE_CRITICAL_RATIO_TARGETS: <if SCALE_CRITICAL_MODE yes: numeric ratio targets for protagonist vs occupant/entry/container width/container length/screen occupancy>
MAX_PROTAGONIST_SCREEN_OCCUPANCY: <if SCALE_CRITICAL_MODE yes: maximum screen share or container-relative fraction allowed before protagonist reads giant; include number/percent>
PROTAGONIST_ENTRY_FIT_TEST: <if SCALE_CRITICAL_MODE yes: numeric adult body vs door/entry/aisle/roof/cabin fit test>
NEAR_PLANE_ANCHOR_CHECK: <anchors sharing the character's plane; these must override distant decorative detail>
DEPTH_PLANE_SCALE_TRANSFER: <how scale is transferred from near plane to mid/background through perspective grid and repeated modules>
FUNCTIONAL_SIZE_TESTS: <door must admit adult, tram must fit passengers, weapon must be wieldable, parapet must be knee/waist height, etc.>
SCALE_ANCHOR_FAIL_CONDITIONS: <tiny doors/tram/windows, giant character read, toy vehicle read, pattern-like architecture, missing scale ladder>
SCALE_ANCHOR_VERDICT_HANDOFF: <specific checks visual verdict must run after generation and rerender if failed>
HERO_OBJECT_SCALE_RELATIONSHIP_CHECK: <compare protagonist against visible humans/passengers, doors, windows, vehicles, props, architecture modules, creature modules, and repeated scale witnesses; explain depth-plane transfer>
HERO_BACKGROUND_HUMANOID_SCALE_COMPARISON_TABLE: <row for protagonist and every visible background human/humanoid/humanoid monster: role/name, anatomy object id, depth plane, expected head/body scale after perspective transfer, comparison witness, pass/fail trigger>
HERO_HUMANOID_SCALE_COMPARISON_PLAN: <how protagonist scale will be compared against every other human/humanoid/humanoid monster by depth plane; include pass/fail ratio logic>
PERSPECTIVE_ONLY_SCALE_LOCK: <scale changes allowed only by actual object size, declared depth/perspective/lens, or explicit user symbolic-scale request; no drama/style/focus scale exaggeration>
IRREVERSIBLE_STRUCTURE_REGISTRY: <all named anatomy parts and objects that may not be omitted, fused, resized, absorbed, or reinterpreted unless explicitly marked removable>
CONTACT_PLANES:
PERSPECTIVE_FAIL_CONDITIONS:
GATE_STATUS: <pass|needs_revision>

## Step 2.2 Object Inventory from Perspective
THEORY_FILES:
- illustrate-skill/references/theory-02-composition-silhouette.md
- illustrate-skill/references/theory-02e-object-density-human-priority.md
- illustrate-skill/references/theory-02g-occlusion-layer-separation.md
- illustrate-skill/references/theory-02h-object-distortion-command-verdict.md
- illustrate-skill/references/theory-02i-all-humanoids-anatomy-perspective-scale.md
- illustrate-skill/references/theory-02j-camera-class-scale-gate.md
- illustrate-skill/references/theory-08a-final-prompt-compiler-aesthetic-recovery.md

SOURCE_IMAGE_OBJECTS_PRESENT:
PRIMARY_RETAINED_OBJECTS:
STRUCTURALLY_CLEAR_SOURCE_OBJECTS:
STRUCTURALLY_UNCERTAIN_SOURCE_OBJECTS:
FOREGROUND_FRAME_OBJECTS:
SUPPORT_PLANE_OBJECTS:
LEFT_VERTICAL_PLANE_OBJECTS:
RIGHT_VERTICAL_PLANE_OBJECTS:
OVERHEAD_PLANE_OBJECTS:
BACKGROUND_DEPTH_OBJECTS:
EFFECT_OBJECTS:
TEXT_OR_GLYPH_OBJECTS:
UNKNOWN_OBJECT_TRIAGE:
VISIBLE_HUMANOID_OBJECT_CANDIDATES: <every visible human/humanoid/humanoid monster candidate from source image and scene brief; transfer all to Step 2.3 anatomy unless explicitly symbolic/non-anatomical>
OBJECT_DISTORTION_RISK_INVENTORY: <named objects whose silhouette, axis, functional geometry, material boundary, or scale could be warped by style/correction/action; include no-distortion fail condition per object>
OCCLUDER_MASS_INVENTORY: <list cloak/hair/smoke/blood/effects/black costume/background/creature masses that could absorb protected anatomy or props>
OBJECT_DENSITY_EDGE_CASE: <active|not_active; active when human figure + many objects/effects/background systems>
HUMAN_PRIORITY_DENSITY_REDUCTION_PLAN: <if active, name non-human density to reduce before sacrificing anatomy>
GATE_STATUS: <pass|needs_revision>

## Step 2.2M Merge Gate: Normalized Scene Graph

MERGED_FROM_ROUTE: <image_development|prompt_only; must match INPUT_ROUTE>
SCENE_CONTRACT_VERSION: <v1 or later; canonical contract schema used by both intake routes>
SCENE_INTENT_LOCK: <single canonical intent after Step 0 branch and Step 1 agree>
COMPOSITION_LOCK: <canonical composition/camera/focal decision after branch-specific evidence is normalized>
PERSPECTIVE_LOCK: <canonical perspective/depth/support-plane/scale-anchor summary from Step 2.1 and Step 2.2>
OBJECT_REGISTRY: <stable ids for every mandatory object/anatomy instance, e.g. H1 heroine; T1 tram; P1 passenger; D1 dragon_head; D2 dragon_neck target; D3 dragon_body forbidden target; K1 katana; G1 cloak>
RELATIONSHIP_CONTRACT: <explicit relationship triples: H1 stands_on T1.roof; K1 contacts/cuts D2 not D3; G1 attached_to H1.shoulders/collar; buildings surround T1; P1 inside T1>
ACTION_CONTACT_CONTRACT: <if action/contact exists: actor, tool/body part, target object/subpart, forbidden targets, visible contact landmarks; else not_applicable with reason>
POST_ACTION_OBJECT_STATE_CONTRACT: <if cutting/severing/damaging action exists: visible post-action state of target and adjacent parts; name clean cut-plane/cross-section, head-side/body-side continuity, no unknown protrusions, and fail if hidden/ambiguous; else not_applicable with reason>
TARGET_CUT_PLANE_VISIBILITY_CONTRACT: <if a target is cut: the exact visible cut-plane/cross-section landmarks that must stay readable and cannot be hidden by protagonist/cloak/effects; else not_applicable with reason>
SCALE_PARITY_CONTRACT: <protagonist/main figure vs every passenger/background humanoid/human-enterable object; perspective-only scale rules and fail triggers>
PROTECTED_ANATOMY_CHAINS: <left/right/both chains with visible landmarks: shoulder-elbow-wrist-hand, palm/thumb/fingers, hip-knee-ankle-foot, weapon chain; no extra/missing limbs>
GARMENT_ATTACHMENT_CONTRACT: <for cloak/cape/hood/large garment: origin, shoulder/collar/neck/back/clasp anchors, free tail direction, and rule that garment cannot replace limbs/torso; else not_applicable with reason>
OBJECT_REGISTRY_BY_PLANE: <all retained/generated objects grouped by plane; includes source-image objects for image_development and prompt candidates for prompt_only>
ANATOMY_CANDIDATE_REGISTRY: <all human/humanoid/hand candidates that transfer to Step 2.3>
SOURCE_PRESERVATION_LOCK: <image_development preservation/change/remove map, or not_applicable for prompt_only>
PROMPT_ONLY_ASSUMPTION_LOCK: <prompt_only assumptions and unknowns, or not_applicable for image_development>
OBJECT_RESEARCH_TRIGGER_SUMMARY: <which objects/anatomy/scale anchors must trigger Step 2.4/2.5 research>
MERGE_CONFLICTS: <branch-to-common-flow conflicts and resolution; none_with_reason if none>
SCENE_CONTRACT_GATE_STATUS: <pass|needs_revision>
MERGE_GATE_STATUS: <pass|needs_revision>
GATE_STATUS: <pass|needs_revision>

## Step 2.3 Anatomy Structure Gate
THEORY_FILES:
- illustrate-skill/references/theory-02c-anatomy-structure-gate.md
- illustrate-skill/references/theory-02d-geometric-blockout.md
- illustrate-skill/references/theory-02e-object-density-human-priority.md
- illustrate-skill/references/theory-02f-structural-scale-capacity-verdict.md
- illustrate-skill/references/theory-02g-occlusion-layer-separation.md
- illustrate-skill/references/theory-02i-all-humanoids-anatomy-perspective-scale.md

ANATOMY_GATE_REQUIRED: <yes|no>
ANATOMY_PRIMARY_OBJECT:
ANATOMY_SUB_OBJECTS:
ANATOMY_CONTACT_OBJECTS:
ALL_HUMANOID_ANATOMY_INVENTORY: <list every human, humanoid object, and humanoid monster in the image, including passengers/crowds/background figures; no visible humanoid may remain only texture/silhouette unless explicitly symbolic>
SECONDARY_HUMANOID_ANATOMY_OBJECTS: <background passengers/crowds/drivers/humanoid monsters with role, anatomy class, detail budget, and minimum readable landmarks>
HUMANOID_ANATOMY_TRANSFER_TABLE: <candidate -> anatomy object id -> primary/secondary/background -> required visible landmarks -> allowed simplification; no texture-only humanoids>
HUMANOID_DEPTH_PLANE_MAP: <depth plane and perspective relation for protagonist and every secondary humanoid>
HERO_SECONDARY_HUMANOID_SCALE_PARITY_LOCK: <protagonist compared to each secondary human/humanoid; same adult scale after depth transfer unless explicit exception>
NO_STYLIZED_SCALE_EXAGGERATION_LOCK: <no enlarging/shrinking characters or objects for drama, style, importance, beauty, action, or composition unless user explicitly asks>
AGE_BAND: <초등학생|중학생|고등학생|20대초반|20대후반|30대초반|30대후반|40대초반|40대후반|50대초반|50대후반|not_applicable>
SEX_CLASSIFICATION:
BODY_TYPE_BASELINE:
BODY_ANATOMY_BASE_CARD:
SEX_OVERLAY_CARD:
HAND_ANATOMY_SUBMODULE_CARD:
STYLIZATION_LEVEL:
HEAD_TO_BODY_RATIO:
RIBCAGE_PELVIS_RELATION:
SHOULDER_WIDTH_NOTE:
HIP_WIDTH_NOTE:
LIMB_PROPORTION_NOTE:
ELBOW_WRIST_CHAIN_NOTE:
HIP_KNEE_ANKLE_CHAIN_NOTE:
HAND_SIZE_RELATIVE_NOTE:
FOOT_SIZE_RELATIVE_NOTE:
LOWER_BODY_SILHOUETTE_LOCK: <pants/skirt/armor may style the legs but must preserve separate thigh-knee-shin-ankle/boot silhouettes; no black-costume texture absorption>
PROTECTED_ANATOMY_CHAIN_VISIBILITY: <for each visible/partial limb chain, state required landmarks such as shoulder-elbow-wrist-hand or hip-knee-ankle-boot and what may be occluded>
VISIBLE_HANDS_AND_POSES:
HAND_SILHOUETTE_NOTE:
FINGER_GROUPING_NOTE: <legacy field name; fill with individual thumb/index/middle/ring/little finger-chain modeling, not grouping/fusion>
HAND_DETAIL_BUDGET: <for each visible hand: focal/support/background, screen-size/readability target, required palm/thumb/finger detail, and nearby detail to reduce first>
FINGER_TOPOLOGY_CHAIN_LOCK: <for each visible hand: wrist->palm block->thumb wedge->index/middle/ring/little start/direction/end or overlap cue; no fused claw, black lump, melted glove, or decorative noise>
FINGER_TOPOLOGY_FAIL_CONDITIONS: <fail if a visible hand merely exists but lacks readable palm/thumb/finger topology, negative-space/value gaps, or human glove/skin silhouette>
SUPPORTING_LEG_NOTE:
BALANCE_LINE_NOTE:
SHOULDER_PELVIS_TILT_NOTE:
ANATOMY_PRIMITIVE_BLOCKOUT:
HEAD_PRIMITIVE:
RIBCAGE_PRIMITIVE:
PELVIS_PRIMITIVE:
LIMB_CYLINDER_CHAIN:
JOINT_SPHERE_MAP:
HAND_FOOT_PRIMITIVES:
ANATOMY_PRIMITIVE_FAIL_CONDITIONS:
ANATOMY_RESEARCH_DECISION_NOTE:
GATE_STATUS: <pass|not_applicable|needs_revision>

## Step 2.4 Object Knowledge Query Plan
THEORY_FILES:
- object-research-skill/SKILL.md

RESEARCH_LANES:
LOCAL_CARD_LOOKUP_PLAN:
EXISTING_MATCHED_CARDS:
MISSING_OR_WEAK_CARDS:
RESEARCH_REQUIRED_OBJECTS:
QUERY_TERMS:
CONFIDENCE_BY_OBJECT:
DRAW_READY_LOCKS_NEEDED:
CONTAINER_CAPACITY_RESEARCH_NEEDED: <for tram/train/bus/car/elevator/room/corridor/interior/cabin: capacity/dimensions/entry-exit/module research required or not_applicable>
CONTAINER_SCALE_RATIO_TABLE_NEEDED: <if SCALE_CRITICAL_MODE yes: require numeric ratio table from object research, not prose-only scale claims>
HUMAN_ENTERABLE_COMPOSITE_SCALE_PLAN: <for each human-enterable object, require entry fit + XYZ volume + capacity class + occupant anchor + module repetition + final composite verdict, or not_applicable>
USER_CHECKPOINT_B_OBJECT_DIRECTION:
GATE_STATUS: <pass|not_applicable|needs_revision>

## Step 2.5 Object Research Handoff
THEORY_FILES:
- object-research-skill/SKILL.md

HANDOFF_REQUIRED: <yes|no>
OBJECT_RESEARCH_ARTIFACT_PATH: <relative path or not_applicable>
OBJECT_RESEARCH_INVOCATION_LOG_PATH: <relative path to invocation log when artifact is produced via sub-agent or Codex bridge; not_applicable when HANDOFF_REQUIRED is no or artifact was hand-authored>
SCENE_TYPE:
REQUIRED_OBJECTS:
RESEARCH_LANES_USED:
PASSENGER_INSTANCE_REGISTRY: |
  # One YAML entry per passenger/driver/occupant instance for every human-enterable
  # object in scope. Required when SCALE_CRITICAL_MODE: yes; not_applicable otherwise.
  # Each entry must name the container, the depth plane, and at least one visible
  # landmark so the operator/Codex/validator can treat the passenger as an
  # individual anatomy instance, not as background texture.
  - passenger_id: <P1>
    container: <tram_cabin_left | bus_aisle | room_corridor | ...>
    depth_plane: <near | mid | far> (<distance/m if known>)
    visible_landmarks: <head_through_window | torso_at_seat | shoulder_silhouette | implied_block_only>
    seat_or_floor_relation: <seated | standing | leaning | implied>
    expected_size_vs_protagonist: <ratio, e.g. ~1.0 adult>
    pass_or_fail: <pass | needs_revision | not_applicable>
  - <repeat per passenger; minimum one entry when human-enterable object is in scope>
ANATOMY_REFERENCES_RESEARCHED:
SOURCE_IMAGE_OBJECTS_RESEARCHED:
SOURCE_IMAGE_RESEARCH_DECISION_NOTE:
HANDS_OR_FINGER_POSES_RESEARCHED:
HAND_RESEARCH_DECISION_NOTE:
BACKGROUND_OBJECTS_RESEARCHED:
SCALE_ANCHOR_OBJECTS_RESEARCHED:
CONTAINER_CAPACITY_OBJECTS_RESEARCHED: <container objects researched for occupancy/capacity/internal volume, or not_applicable>
CONTAINER_CAPACITY_RESEARCH_APPLIED: <how capacity/dimensions/entry-exit/modules are passed to Step 2.6/2.8/2.9, or not_applicable>
CONTAINER_SCALE_RATIO_TABLE_APPLIED: <numeric rows transferred from object artifact: object/module/entry/occupant/protagonist/threshold/pass-fail>
HUMAN_ENTERABLE_COMPOSITE_SCALE_TABLE: <object_id | type | capacity_class | expected_occupancy | X width | Y height | Z length/depth | entry/door | occupant anchors | module repetition | pass/fail>
ENTRY_FIT_CHECK_APPLIED: <pass/fail with numeric protagonist-vs-entry height/width/aisle clearance; this is only one subcheck, not the whole container verdict>
XYZ_VOLUME_CHECK_APPLIED: <pass/fail with X width, Y height, Z length/depth/internal volume; reject thin/tall boxes that cannot contain occupants>
CAPACITY_CLASS_CHECK_APPLIED: <pass/fail with expected occupancy class such as single occupant, small room, bus, tram, 100_plus_passengers, etc.>
OCCUPANT_ANCHOR_CHECK_APPLIED: <pass/fail with driver/passenger/occupant/mannequin/silhouette anchor used as anatomy scale witness>
MODULE_REPETITION_CHECK_APPLIED: <pass/fail with repeated human-scale doors/windows/bays/seats/aisles/floor modules proving length/depth>
HUMAN_ENTERABLE_SCALE_VERDICT_APPLIED: <pass/fail composite; pass only if entry fit, XYZ volume, capacity class, occupant anchor, and module repetition all pass>
PROTAGONIST_TO_ENTRY_RATIO_APPLIED: <numeric protagonist-to-door/entry/aisle fit ratio transferred from object artifact>
PROTAGONIST_TO_OCCUPANT_RATIO_APPLIED: <numeric protagonist-to-passenger/driver/occupant scale ratio after perspective transfer>
PROTAGONIST_TO_CONTAINER_WIDTH_RATIO_APPLIED: <numeric protagonist body/footprint vs container usable width/roof/cabin/platform width>
PROTAGONIST_TO_CONTAINER_LENGTH_RATIO_APPLIED: <numeric protagonist footprint/body vs full vehicle/room/corridor/building module length>
SCALE_CRITICAL_FAIL_NUMBERS_APPLIED: <numeric thresholds that fail/rerender giant protagonist or toy-container reads>
SCALE_EMPHASIS_OVERRIDE_POLICY_APPLIED: <how commands to enlarge/shrink figures for emphasis are ignored and replaced by perspective/value/framing/detail>
STRUCTURALLY_UNCERTAIN_OBJECTS:
UNKNOWN_OBJECTS_RESOLUTION:
LOOKUP_RESULT:
RESEARCH_ACTION:
RETURNED_CARDS_OR_RECIPES:
GATE_STATUS: <pass|not_applicable|needs_revision>

## Step 2.6 Object Relationship Check
THEORY_FILES:
- object-research-skill output
- illustrate-skill/references/theory-02g-occlusion-layer-separation.md
- illustrate-skill/references/theory-02h-object-distortion-command-verdict.md

APPLY_STATUS: <applied|not_applicable|needs_revision>
SCALE_RELATION_TABLE:
OCCLUSION_ORDER:
OCCLUSION_LAYER_GRAPH: <foreground/mid/background layer ownership; who is in front/behind; protected chains vs occluder masses>
PROTECTED_CHAIN_EXPOSURE_RULES: <minimum visible landmarks and occlusion budget for arms/legs/hands/weapons/other protected chains>
SEPARATION_CUE_PLAN: <rim light, negative-space slit, value/hue/material edge, cast shadow, contour notch, or mask boundary for high-risk overlaps>
FINGER_OCCLUSION_SEPARATION_RULE: <for each visible hand, state what touches/backs it, minimum finger gap/value/rim cue, and which cloak/blood/armor/background details reduce before finger topology is sacrificed>
CONTACT_AND_SUPPORT:
OBJECT_ANATOMY_SEPARATION_LOCKS: <limbs/props/cloak/hood/effects remain separate instances; cloak may overlap but not absorb arms/hands/weapons/object silhouettes>
IRREVERSIBLE_OBJECT_ANATOMY_LOCKS: <all registered objects/anatomy parts survive as separate structural instances; density/style may simplify only non-structural texture>
MATERIAL_LIGHT_INTERACTION:
RIGID_OBJECT_GEOMETRY_LOCKS:
ALL_OBJECT_DISTORTION_LOCK: <all named objects keep identity, silhouette, axis/continuity, functional geometry, material boundary, and scale relation; no unintended bend/warp/melt/resize/fuse/absorb/texture replacement>
TEXT_RENDERING_POLICY:
GATE_STATUS: <pass|not_applicable|needs_revision>

## Step 2.7 Anatomy-on-Object Relationship Check
THEORY_FILES:
- illustrate-skill/references/theory-02c-anatomy-structure-gate.md

BODY_SUPPORT_LOGIC:
ANATOMY_STRUCTURE_APPLY_NOTE:
HAND_PROP_RELATION:
HAND_STRUCTURE_APPLY_NOTE:
FUNCTIONAL_GRIP_MECHANICS_CONTRACT: <for weapon/prop hands: how the palm, thumb opposition, finger wrap, hilt/contact surface, knuckle line, wrist angle, and forearm force path make the grip functional; else not_applicable with reason>
WRIST_FORCE_PATH_CHECK: <for weapon/prop hands: pass/fail check that wrist aligns with forearm/load direction and does not bend into an impossible force path; else not_applicable with reason>
FOOT_OBJECT_RELATION:
TORSO_ACTION_RELATION:
ANATOMY_OBJECT_FAIL_CONDITIONS:
GATE_STATUS: <pass|not_applicable|needs_revision>

## Step 2.8 3D Blockout / Modeling Contract
THEORY_FILES:
- illustrate-skill/references/theory-02-composition-silhouette.md
- illustrate-skill/references/theory-02d-geometric-blockout.md
- illustrate-skill/references/theory-02e-object-density-human-priority.md
- illustrate-skill/references/theory-02f-structural-scale-capacity-verdict.md
- illustrate-skill/references/theory-02g-occlusion-layer-separation.md
- illustrate-skill/references/theory-02h-object-distortion-command-verdict.md
- illustrate-skill/references/theory-02i-all-humanoids-anatomy-perspective-scale.md
- illustrate-skill/references/theory-02j-camera-class-scale-gate.md

PRIMITIVE_BLOCKS:
ENVIRONMENT_PRIMITIVE_BLOCKOUT:
SHARED_PERSPECTIVE_GRID:
METER_SCALE_LOCK:
ABSOLUTE_SCALE_LADDER: <human/body/head baseline -> doors/windows/tram/parapets/props/creatures/background modules with explicit relative sizes>
OBJECT_ANATOMY_SCALE_INVARIANTS: <object/anatomy size ratios from blockout that painterly rendering may not resize or reinterpret>
HUMANOID_SCALE_PARITY_BLOCKOUT_CHECK: <blockout evidence comparing protagonist to each secondary/background humanoid on its depth plane; fail if passenger/crowd/humanoid monster becomes miniature, giant, doll, or texture>
OBJECT_DISTORTION_BLOCKOUT_CHECK: <blockout evidence that named objects keep axis, silhouette, function, material boundary, and scale relation before style/detail>
IRREVERSIBLE_STRUCTURE_INVARIANTS: <all named object/anatomy identities, scale, contact, support, and occlusion relationships that cannot be sacrificed>
ANATOMY_TO_ARCHITECTURE_SCALE_CHECK:
WINDOW_TO_HEAD_SIZE_CHECK:
PARAPET_TO_BODY_HEIGHT_CHECK:
DOOR_VEHICLE_FUNCTIONAL_SCALE_CHECK: <when relevant: doors/exits/trams/vehicles remain human-usable and not miniaturized>
PASSENGER_CAPACITY_SCALE_CHECK: <when tram/train/bus/vehicle relevant: full cabin reads as many-adult passenger capacity, with long car length, repeated door/window bays, and protagonist occupying only a small roof fraction>
INTERNAL_OCCUPANT_ANATOMY_SCALE_CHECK: <for every human_enterable object: blockout includes at least one internal passenger/driver/occupant/mannequin/silhouette or implied occupant block and compares protagonist/main figures to it through perspective>
XYZ_VOLUME_BLOCKOUT_CHECK: <blockout pass/fail for X width, Y height, Z length/depth/internal volume; object must be physically enterable, not merely taller than protagonist>
CAPACITY_CLASS_BLOCKOUT_CHECK: <blockout pass/fail that the object reads as its intended capacity class, e.g. tram/bus/room/100_plus_passengers, not a booth/toy/prop>
MODULE_REPETITION_BLOCKOUT_CHECK: <blockout pass/fail for repeated doors/windows/bays/seats/aisles/floor modules along depth/length>
HUMAN_ENTERABLE_COMPOSITE_BLOCKOUT_VERDICT: <pass/fail composite after real/proxy blockout; pass only if entry, XYZ, capacity, occupant, and module checks pass>
STRICT_SCALE_BLOCKOUT_REQUIRED: <yes when SCALE_CRITICAL_MODE yes; strict guide and real blockout evidence required before image generation>
STRICT_SCALE_BLOCKOUT_RATIO_REVIEW: <numeric review from blockout: protagonist vs occupant/entry/container width/container length/screen occupancy; list pass/fail>
REAL_BLOCKOUT_EVIDENCE_STATUS: <real_blender_pass|blocked_no_blender|blocked_proxy_only|not_applicable; proxy/placeholder cannot unlock PRE_IMAGE_HANDOFF_READY/IMAGE_GEN_READY for scale-critical scenes; if proxy is used, explicitly say it is not a true Blender render pass>
FOOTPRINT_ON_SUPPORT_PLANE_CHECK:
DETAIL_AFTER_BLOCKOUT_LOCK:
INSTANCE_MASK_SEPARATION_PLAN: <mask/color-pass plan separating protected chains from cloak/hair/effects/background occluders>
PROTECTED_CHAIN_MASK_REVIEW: <review mask/blockout proves protected chains remain traceable before style translation>
CAMERA_BLOCKOUT:
DEPTH_LAYER_ORDER:
CONTACT_POINTS:
SCALE_CHECK:
CAMERA_CLASS_BLOCKOUT_LOCK: <blockout must use the chosen camera class; for scale-critical scenes it must be a reviewed wide/long scale shot, not a portrait/medium hero shot>
FULL_CONTAINER_VISIBILITY_BLOCKOUT_CHECK: <pass/fail proof that the blockout shows the full human-enterable object/container length/width/volume needed for scale>
SCALE_WITNESS_VISIBILITY_COUNT_CHECK: <pass/fail numeric count of visible passengers/doors/windows/modules/rails/anchors in the blockout/render passes>
PERSPECTIVE_CALCULATION_BLOCKOUT_TRANSFER: <copy Step 2.1 projection into blockout/guide: footpoint plane, baseline object, projected height/ratio, and camera crop>
PROJECTED_BASELINE_BLOCKOUT_CHECK: <blockout pass/fail: projected baseline at protagonist position matches protagonist size; include numeric ratio>
SCREEN_OCCUPANCY_BLOCKOUT_RECONCILIATION: <blockout pass/fail: screen occupancy/crop derives from camera and does not override world scale>
SCALE_PROXY_DUMMY_BLOCKOUT_PLACEMENT: <temporary adult dummy/mannequin placement inside Blender/blockout next to the baseline door/window/occupant landmark; include height and depth plane>
SCALE_PROXY_DUMMY_BLOCKOUT_CHECK: <pass/fail blockout check that dummy, door/occupant, and protagonist share the projected scale ratio before any painterly/stylistic translation>
SCALE_PROXY_DUMMY_REMOVAL_POLICY: <hide/delete the temporary dummy before visual guide composite/final image, but keep measurement trace/height line/baseline overlay; the dummy itself must not appear as a character unless explicitly requested>
SCALE_PROXY_TRACE_OVERLAY: <measurement trace retained after dummy removal: height line, footpoint, projected baseline, door/passenger/protagonist ratio markers in the visual guide composite>
SCALE_PROXY_TO_HERO_BLOCKOUT_VERDICT: <pass/fail verdict that the dummy-derived projection fixes protagonist scale relative to door/passengers/container before composite approval>
BLENDER_ROUTE_DECISION: <use_blender|skip_blender; decide before creating any .blend or visual guide>
BLENDER_ROUTE_DECISION_REASON: <why the scene does or does not need structural 3D evidence; mention background/simple/no-background, scale-critical, contact/grip, perspective, source-image structure, and user request signals>
BLENDER_SKIP_REASON: <required when BLENDER_BLOCKOUT_REQUIRED no: e.g. prompt-only simple character scene, no background or simple/plain/abstract background, no human-enterable scale object, no hard-surface environment, no complex contact/grip/action, no source-image structural confirmation>
OPTIONAL_3D_REFERENCE_PLAN: <Blender/pass plan when BLENDER_BLOCKOUT_REQUIRED yes; when skipped, say direct_text_prompt route and no .blend/render passes/visual composite/controlnet/img2img>
BLENDER_BLOCKOUT_REQUIRED: <yes|no; yes only for structural staging risk or explicit user request, no for backgroundless/simple character-only render-bound scenes>
BLENDER_SCENE_PATH: <relative path to .blend or not_applicable>
BLENDER_RENDER_SCRIPT_PATH: <relative path to blender python script or not_applicable>
BLENDER_PASS_OUTPUTS: <clay=path | lineart=path | depth=path | normal=path | mask=path | not_applicable; pass files must be visually/functionally distinct, not duplicate saves>
BLENDER_BLOCKOUT_REVIEW: <camera, scale, contact, support, and silhouette review or not_applicable; if BLENDER_BLOCKOUT_REQUIRED no, state not_applicable because the route is direct prompt, not blocked proxy evidence>
BLENDER_GUIDE_STRENGTH: <loose guide|medium guide|strict guide|not_applicable>
BLOCKOUT_CORE_OBJECT_VISIBILITY: <pass/fail after viewing pass PNGs: every mandatory Scene Contract object id is visible enough to guide generation; not hidden by buildings/camera/foreground masses>
BLOCKOUT_TARGET_CONTACT_VISIBILITY: <pass/fail for action scenes: actor/tool/body part visibly contacts the intended target subpart and avoids forbidden target objects; else not_applicable>
BLOCKOUT_CAMERA_OCCLUSION_CHECK: <pass/fail: camera is not blocked by facades/foreground/dragon/cloak; the pass PNG shows the core scene, not only occluders>
BLENDER_VISIBILITY_REPORT_PATH: <relative path to JSON visibility report or not_applicable for spec-only; required for render-bound PRE_IMAGE_HANDOFF_READY: yes>
BLENDER_VISIBILITY_REPORT_REVIEW: <pass/fail summary of report_ready, camera_not_occluded_by_buildings, core_objects.visible, target_contacts.visible, scale_anchors.visible>
VISUAL_GUIDE_COMPOSITE_REQUIRED: <yes|no; yes when Blender/visual structure conditioning is required, no for backgroundless/simple direct_text_prompt scenes>
VISUAL_GUIDE_COMPOSITE_PATH: <relative path to annotated composite PNG made from clay + lineart/wire + depth/normal/mask plus scale/perspective overlays>
VISUAL_GUIDE_COMPOSITE_SOURCE_PASSES: <clay/solid pass path, lineart/wire pass path, depth/normal/mask pass path used in the composite; state whether these are true Blender passes or distinct proxy passes>
VISUAL_GUIDE_COMPOSITE_OVERLAYS: <drawn overlays: perspective/vanishing lines, protagonist footpoint, projected baseline, door/passenger/protagonist height markers, support plane, contact/cut/grip markers; composite should show distinct pass contributions, not one duplicated image>
VISUAL_GUIDE_COMPOSITE_REVIEW: <pass|needs_revision|not_applicable; review the composite as the user-visible structure guide, not just raw Blender pass existence>
VISUAL_GUIDE_COMPOSITE_CONDITIONING_ROLE: <how this composite will be supplied to image generation as an image/reference/conditioning guide; must say final art must not copy gray clay colors, labels, or guide text>
SCALE_COMPOSITE_HARD_LOCK: <yes|no; yes for scale-critical scenes: the approved visual guide composite's scale markers, footpoints, projected baselines, and dummy-derived traces are binding for scale even though the composite is not the sole authority for the whole image>
USER_VISUAL_GUIDE_CHECKPOINT_REQUIRED: <yes|no; yes means pause after the composite and ask the user for visual feedback before Step 2.9/Step 3/image generation; no when BLENDER_BLOCKOUT_REQUIRED no>
USER_VISUAL_GUIDE_FEEDBACK: <user feedback verbatim or approval summary; "pending_user_review" while waiting>
USER_VISUAL_GUIDE_FEEDBACK_APPLIED: <pass|needs_revision|not_applicable; pass only after the final user feedback was applied or explicitly accepted as no-change>
USER_VISUAL_GUIDE_APPROVAL_STATUS: <pending|approved|needs_revision|not_applicable; PRE_IMAGE_HANDOFF_READY must remain no until approved>
SCALE_VISUAL_GUIDE_PACKAGE: <if scale-critical/render-bound: concrete visual guide evidence package for scale, e.g. annotated blockout/mask/overlay/lineart/depth/control reference that shows protagonist, passengers, doors/windows, container length/width/volume; not prose-only>
CUT_PLANE_VISUAL_GUIDE_PACKAGE: <if cutting/severing action exists: concrete visual guide evidence package showing target cut plane/cross-section, head-side/body-side continuity, no hidden cut, no unknown protrusion; not prose-only>
GRIP_MECHANICS_VISUAL_GUIDE_PACKAGE: <if weapon/prop hand matters: concrete visual guide evidence package showing palm block, thumb wedge/opposition, finger wrap, hilt position, wrist/forearm force path; not prose-only>
STRUCTURAL_INVARIANTS_TO_PRESERVE: <camera/support/contact/scale/object-identity locks that image generation must keep>
PAINTERLY_FREEDOMS_ALLOWED: <compression/massing/partial occlusion allowed only after support/contact/scale and protected-chain traceability remain readable; no body/object-size distortion unless explicitly requested>
STRUCTURE_OVER_PAINTERLY_LOCK: <Blender/object/anatomy scale, contact, occlusion budget, protected-chain landmarks, and separate-instance locks override painterly compression; style only changes line/color/texture/detail>
NO_STRUCTURAL_SACRIFICE_RULE: <if conflict occurs, reduce background/effects/texture/signage/costume noise first; never delete, merge, shrink, or reinterpret registered structures>
CONTROLNET_CONDITIONING_PLAN: <depth/lineart/normal/mask/img2img plan plus guide strength, or not_applicable>
BLOCKOUT_REVIEW_STATUS: <pass|needs_revision|not_applicable>
USER_CHECKPOINT_C_BLOCKOUT_DIRECTION:
GATE_STATUS: <pass|needs_revision>

## Step 2.9 Image Translation Lock
THEORY_FILES:
- illustrate-skill/references/theory-08-final-check-correction.md
- illustrate-skill/references/theory-02d-geometric-blockout.md
- illustrate-skill/references/theory-02e-object-density-human-priority.md
- illustrate-skill/references/theory-02f-structural-scale-capacity-verdict.md
- illustrate-skill/references/theory-02g-occlusion-layer-separation.md
- illustrate-skill/references/theory-02h-object-distortion-command-verdict.md
- illustrate-skill/references/theory-02i-all-humanoids-anatomy-perspective-scale.md
- illustrate-skill/references/theory-02j-camera-class-scale-gate.md

GENERATION_PRIORITY_ORDER:
NON_NEGOTIABLE_LOCKS:
STYLE_ALLOWED_AFTER_STRUCTURE:
ANATOMY_OVER_DENSITY_LOCK: <for dense scenes, state human body/hands/fingers/feet/contact survive before background/effects/detail>
SCENE_CONTRACT_PROMPT_LOCK: <compact final-prompt wording that carries object ids/roles, relationship contract, target contact, scale parity, and protected-chain/garment attachment rules without dumping the full registry>
ACTION_CONTACT_PROMPT_LOCK: <if action/contact exists: final-prompt wording that names actor/tool/target subpart and forbidden targets, e.g. "katana cuts D2 neck cross-section, not D3 body/wing">
CAMERA_CLASS_PROMPT_OPENING: <natural first-sentence camera translation, e.g. "Extreme wide scale shot, no close-up heroine"; no schema field names>
SCALE_OVER_STYLE_LOCK: <absolute scale ladder and functional object size survive before style, drama, focal exaggeration, density, or painterly massing>
HUMANOID_SCALE_PARITY_PROMPT_LOCK: <compact prompt wording that protagonist, passengers/background humans, humanoids, and humanoid monsters share one perspective scale; no style/drama/focal size exaggeration>
HUMAN_ENTERABLE_OCCUPANT_PROMPT_LOCK: <compact prompt wording that human-enterable objects contain visible/implied occupant anatomy scale anchors and that protagonist/main figures are sized against them through perspective>
SCALE_CRITICAL_PROMPT_OPENING: <first prompt sentence for scale-critical scenes: occupant/door/window/seat/aisle/container-length proof before face/action/style>
SCALE_CRITICAL_SHOT_CLASS_PROMPT_LOCK: <if scale-critical: prompt must force wide/long scale shot, full container visibility, small protagonist screen share, repeated modules, no close-up>
FACE_FOCAL_DEMOTION_PROMPT_LOCK: <if scale-critical: keep face/eyes as small bright accents; forbid portrait/face-first framing until scale passes>
PERSPECTIVE_CALCULATION_PROMPT_LOCK: <natural image-language transfer of projected baseline/footpoint/depth-plane calculation; no raw schema field names>
SCREEN_OCCUPANCY_DERIVED_PROMPT_LOCK: <natural image-language rule: screen/crop prominence comes from camera perspective and must not resize world scale>
PROMPT_ATTENTION_BUDGET_LOCK: <compress prompt so macro scale, face structure, limb silhouettes, and key contacts are not drowned by exhaustive object lists>
TIERED_IMAGE_PROMPT_LOCKS: <Tier 0 macro scale/camera/capacity; Tier 1 face/anatomy/lower body; Tier 2 key prop/contact/separation; Tier 3 style/detail reductions>
OCCLUSION_TRANSLATION_LOCK: <prompt-level visual solution for high-risk overlaps: which occluder moves behind, which chain gets rim/negative-space/value edge, what detail reduces first>
ALL_OBJECTS_ANATOMY_IRREVERSIBLE_LOCK: <every named object/anatomy instance is mandatory unless explicitly removable; no sacrifice to density, cloak, hood, effects, background, or style>
OBJECT_DISTORTION_PROMPT_LOCK: <compact final-prompt language forbidding unintended object bending, warping, melting, resizing, fusion, absorption, or texture replacement; name highest-risk objects>
PROMPT_FINGER_TOPOLOGY_LOCK: <prompt-level one-hand-at-a-time finger topology wording; name palm block, thumb wedge, separated finger shapes/gaps, and detail reductions for each visible hand>
BLENDER_GUIDE_STRENGTH: <loose guide|medium guide|strict guide|not_applicable; use not_applicable when BLENDER_BLOCKOUT_REQUIRED no>
TEXT_ONLY_LOCKS_REJECTION: <state which scale/contact/cut-plane/grip problems cannot be solved by prompt prose alone and which visual guide/blockout/mask evidence must be used instead; for simple direct_text_prompt scenes, state why none of those high-risk gates apply>
VISUAL_GUIDE_COMPOSITE_PROMPT_LOCK: <natural prompt language for annotated visual guide when used; not_applicable for direct_text_prompt/no-Blender scenes>
IMAGE_INPUT_STACK_PLAN: <which images are actually supplied to generation; for BLENDER_BLOCKOUT_REQUIRED no, use direct_text_prompt/no image input and compact final prompt>
PRE_COMPOSITE_EVIDENCE_STACK_LOCK: <state that image generation inherits the full evidence stack; include Blender/composite only when present, otherwise cite immutable user commands, object/anatomy locks, style guide, and final prompt>
SCALE_PROXY_TRACE_PROMPT_LOCK: <natural prompt/conditioning language that the approved guide carries dummy-derived height traces/baselines but no visible dummy character; protagonist size follows those traces>
COMPOSITE_IS_REFERENCE_NOT_SOLE_AUTHORITY: <state that the visual guide composite is one strong structure reference image, not a replacement for source image, object research, perspective math, blockout review, or final prompt locks>
SCALE_MUST_FOLLOW_COMPOSITE_PROMPT_LOCK: <hard scale instruction for image generation: all character/object size, footpoint, door/passenger/container ratio, and screen occupancy follow the approved composite scale overlays; if style/action/beauty prompt pressure conflicts, composite scale wins>
IMAGE_GEN_STRUCTURE_CONDITIONING_MODE: <openai_high_fidelity_image_inputs|external_controlnet|direct_text_prompt|blocked_text_only|not_applicable; use direct_text_prompt only for simple no-Blender scenes with no structural visual-guide requirement>
IMAGE_GEN_STRUCTURE_CONDITIONING_STRENGTH: <strict_structure|medium_structure|loose_reference|not_applicable; strict_structure for scale/contact/cut/grip-critical scenes>
IMAGE_GEN_STRUCTURE_CONDITIONING_INPUTS: <ordered actual image inputs for image_gen: source image, approved visual guide composite, optional clay/lineart/depth/mask; include local path or file id and role>
IMAGE_GEN_STRUCTURE_CONDITIONING_LIMITS: <state that OpenAI image inputs are strong reference/conditioning but not pixel-perfect ControlNet; if true ControlNet is required use external_controlnet and block text-only generation>
IMAGE_GEN_HANDOFF_PACKAGE_PATH: <relative path to JSON handoff manifest produced by scripts/create_image_gen_handoff_package.py; must exist before PRE_IMAGE_HANDOFF_READY yes>
SCALE_VISUAL_GUIDE_PROMPT_LOCK: <how the image prompt must explicitly obey the scale visual guide package; include protagonist/passenger/container witness wording>
CUT_PLANE_VISIBILITY_PROMPT_LOCK: <how the image prompt must preserve visible cut plane/cross-section and reject hidden/ambiguous/unknown protrusion solutions>
GRIP_MECHANICS_PROMPT_LOCK: <how the image prompt must preserve functional weapon/prop grip mechanics, wrist force path, and hilt-in-palm relation beyond finger separation>
PAINTERLY_COMPRESSION_ALLOWANCE:
NO_HIERATIC_SCALE_DISTORTION:
SCALE_EMPHASIS_OVERRIDE_PROMPT_LOCK: <ignore/override any large/small-for-emphasis command; figure size only from actual object size + Step 2.1 perspective/depth/lens transfer; emphasis via value/framing/detail>
VERDICT_SCALE_AND_MIXING_FAILS: <must fail/rerender if object scale is wrong, doors/vehicles/windows miniaturize, anatomy/object parts fuse, or cloak/hood absorbs limbs/props>
VERDICT_IRREVERSIBLE_STRUCTURE_FAILS: <must fail/rerender if any registered object/anatomy instance is omitted, fused, resized, absorbed, converted into texture, or structurally misunderstood>
PROMPT_COMPRESSION_RULE:
UNKNOWN_OBJECT_POLICY_LOCK:
USER_CHECKPOINT_D_PRE_RENDER_DIRECTION:
GATE_STATUS: <pass|needs_revision>

## Step 3 Value
THEORY_FILES:
- illustrate-skill/references/theory-03-lighting-value.md

LIGHTING_PLAN:
VALUE_COUNT_DECISION:
GRAYSCALE_VALUE_MAP:
FOCAL_CONTRAST_ZONE:
OUTER_AREA_SUPPRESSION_PLAN:
MATERIAL_EDGE_PLAN:
GATE_STATUS: <pass|needs_revision>

## Step 4 Face
THEORY_FILES:
- illustrate-skill/references/theory-04-face-eyes.md
- illustrate-skill/references/theory-04a-face-emotion-patterns.md
- illustrate-skill/references/theory-02f-structural-scale-capacity-verdict.md

SURFACE_INNER_EMOTION:
MAIN_SUPPORT_EMOTION:
INTENSITY:
EYE_RENDER_PLAN:
FACE_STRUCTURE_QUALITY_LOCK: <preserve intended adult/beautified face plane, jaw/chin/cheek/eye spacing; reject flattened dumpling-wide face drift>
FACE_FOCAL_MAP:
NATURAL_ACTING_LOCK:
ANTI_DIRECT_EXPRESSION_LOCK:
GATE_STATUS: <pass|needs_revision>

## Step 5 Line & Shape
THEORY_FILES:
- illustrate-skill/references/theory-05-line-shape.md
- illustrate-skill/references/theory-05a-hands-fingers.md
- illustrate-skill/references/theory-02f-structural-scale-capacity-verdict.md
- illustrate-skill/references/theory-02g-occlusion-layer-separation.md

LINE_HIERARCHY:
LINE_WEIGHT_MAP:
SHAPE_DECOMPOSITION_PLAN:
GAZE_GUIDANCE_MOTIF_MAP:
HAND_LINE_PRIORITY_NOTE: <must preserve individual finger-chain separation before costume/prop/effect detail; no finger grouping/fusion shortcut>
LOWER_BODY_LINE_PRIORITY_NOTE: <legs/pants/boots require clear thigh-knee-shin-ankle silhouette and edge hierarchy before costume straps/black texture>
PROTECTED_CHAIN_EDGE_SEPARATION_PLAN: <line/value/edge plan that lets viewer trace protected chains across or near cloak/hair/effects/background>
GATE_STATUS: <pass|needs_revision>

## Step 6 Color & Accent
THEORY_FILES:
- illustrate-skill/references/theory-06-color-palette-point.md

PALETTE_SELECTION:
ACCENT_PLACEMENT_MAP:
NON_PLASTIC_SKIN_TONE_LOCK:
GATE_STATUS: <pass|needs_revision>

## Step 7 Texture
THEORY_FILES:
- illustrate-skill/references/theory-07-texture-density.md

TEXTURE_DENSITY_MAP:
ROUGH_SMOOTH_SEPARATION_PLAN:
SECONDARY_SYMBOL_PLACEMENT:
GATE_STATUS: <pass|needs_revision>

## Step 8 Final Check
THEORY_FILES:
- illustrate-skill/references/theory-08-final-check-correction.md
- illustrate-skill/references/theory-02f-structural-scale-capacity-verdict.md
- illustrate-skill/references/theory-02g-occlusion-layer-separation.md
- illustrate-skill/references/theory-02h-object-distortion-command-verdict.md
- illustrate-skill/references/theory-02i-all-humanoids-anatomy-perspective-scale.md
- illustrate-skill/references/theory-02j-camera-class-scale-gate.md

SCALE_ANCHOR_VERDICT_CHECK: <confirm generated image preserves scale ladder, functional-size anchors, and object/anatomy ratios; list failures if any>
HERO_OBJECT_SCALE_VERDICT_CHECK: <final comparison of protagonist against objects/visible humans/passengers/doors/windows/vehicles/props/architecture/creatures; fail if scale parity or perspective transfer is wrong>
HUMANOID_SCALE_PARITY_VERDICT_CHECK: <final audit that protagonist and every visible human/humanoid/humanoid monster obey shared perspective scale; fail miniature/doll/giant/background-texture humanoids>
PASSENGER_CAPACITY_VERDICT_CHECK: <for tram/train/bus/vehicle, confirm full vehicle reads as many-adult passenger cabin, not protagonist-sized prop/platform>
INTERNAL_OCCUPANT_SCALE_VERDICT_CHECK: <for every human_enterable object, confirm internal occupant/passenger/driver/mannequin/silhouette anatomy exists or is implied by modules and protagonist/main figures match by perspective>
ENTRY_FIT_VERDICT_CHECK: <pass/fail for protagonist vs entry/door/aisle clearance; local subcheck only>
XYZ_VOLUME_VERDICT_CHECK: <pass/fail for width/height/length/depth/internal-volume read; reject impossible skinny/tall containers>
CAPACITY_CLASS_VERDICT_CHECK: <pass/fail that the object reads as the intended occupancy class, e.g. 100_plus tram vs single-person booth>
OCCUPANT_ANCHOR_VERDICT_CHECK: <pass/fail that occupant/driver/passenger/mannequin/silhouette anchor exists or is strongly implied and matches protagonist by depth plane>
MODULE_REPETITION_VERDICT_CHECK: <pass/fail that repeated human-scale bays/windows/doors/seats/aisle/floor modules prove container length/depth>
HUMAN_ENTERABLE_SCALE_VERDICT: <pass/fail composite; cannot pass unless ENTRY_FIT, XYZ_VOLUME, CAPACITY_CLASS, OCCUPANT_ANCHOR, and MODULE_REPETITION all pass>
ACTION_CONTACT_VERDICT_CHECK: <post-image pass/fail: actor/tool/body part hits the intended target subpart and not a forbidden object/body part; list rerender trigger>
SCALE_VISUAL_GUIDE_VERDICT_CHECK: <post-image pass/fail: generated image obeys the scale visual guide package; protagonist/passengers/doors/windows/container proportions match visual evidence, not only prompt text>
CAMERA_CLASS_VERDICT_CHECK: <post-image pass/fail: chosen camera class survived; fail if the model drifted from wide scale shot into close/medium/hero portrait framing>
SCALE_CRITICAL_SHOT_CLASS_VERDICT_CHECK: <if scale-critical: pass/fail that full container visibility, small protagonist occupancy, repeated modules, and no-close-up rule survived>
PERSPECTIVE_CALCULATION_VERDICT_CHECK: <post-image pass/fail checks projected baseline/footpoint/depth-plane calculation survived the image>
SCREEN_OCCUPANCY_WORLD_SCALE_VERDICT_CHECK: <post-image pass/fail checks screen crop/occupancy did not override physical/world scale>
VISUAL_GUIDE_COMPOSITE_VERDICT_CHECK: <post-image pass/fail check that the generated image followed the approved visual guide composite for camera, perspective, scale, support/contact, and object placement without copying guide labels/clay material>
USER_VISUAL_GUIDE_APPROVAL_VERDICT_CHECK: <pre/post-image audit that final image generation happened only after user visual-guide approval and final feedback application>
SCALE_PROXY_TRACE_VERDICT_CHECK: <pre/post-image pass/fail: dummy-derived measurement trace/height line/baseline was used to size the protagonist, but the temporary dummy itself is hidden/deleted from the final art>
PRE_COMPOSITE_EVIDENCE_STACK_VERDICT_CHECK: <pre/post-image audit that final generation used source/user/object/perspective/blockout/composite/final-prompt stack together; fail if it relied only on composite or only on text>
SCALE_COMPOSITE_HARD_LOCK_VERDICT_CHECK: <pre/post-image pass/fail: scale follows the approved visual guide composite exactly enough for protagonist/door/passenger/container ratios; fail/rerender if scale drifts from composite even when the rest of the image is attractive>
CUT_PLANE_VISIBILITY_VERDICT_CHECK: <post-image pass/fail: target cut-plane/cross-section is visible on required sides and not hidden behind protagonist/cloak/effects; list rerender trigger>
CUT_RESULT_UNKNOWN_FORM_VERDICT_CHECK: <post-image pass/fail: no unrecognizable sprouts/blobs/forms emerge from the cut; blood/effect stays separate from target anatomy/object state>
WEAPON_GRIP_MECHANICS_VERDICT_CHECK: <post-image pass/fail: grip is mechanically plausible with palm, thumb, finger wrap, hilt position, and force-bearing hand relation; finger count alone is insufficient>
WRIST_FORCE_PATH_VERDICT_CHECK: <post-image pass/fail: wrist and forearm carry the weapon/prop load without impossible bend/twist; list rerender trigger>
POST_IMAGE_VISUAL_VERDICT_JSON: |
  {
    "container_scale_pass": null,
    "hero_fits_inside_object": null,
    "occupant_anchor_valid": null,
    "protagonist_to_occupant_ratio_pass": null,
    "scale_visual_guide_pass": null,
    "target_contact_pass": null,
    "cut_plane_visibility_pass": null,
    "unknown_cut_form_pass": null,
    "dense_environment_pass": null,
    "hand_topology_pass": null,
    "finger_separation_pass": null,
    "weapon_grip_mechanics_pass": null,
    "wrist_force_path_pass": null,
    "both_arms_present_pass": null,
    "garment_attachment_pass": null,
    "named_object_distortion_pass": null,
    "command_inheritance_pass": null,
    "style_target_pass": null,
    "rerender_required": null,
    "fail_reasons": [],
    "rerender_priorities_tier_0_to_3": []
  }
POST_IMAGE_VISUAL_VERDICT_ARTIFACT_PATH: <relative path to file-based verdict artifact (templates/post-image-visual-verdict-artifact-template.md). Required only when POST_IMAGE_VERDICT_REQUIRED: yes; use not_applicable before first generation / when no generated image is being accepted. The validator cross-checks this artifact's VERDICT_JSON against POST_IMAGE_VISUAL_VERDICT_JSON above.>
POST_IMAGE_FAILURE_KEY_ROUTING: <not_applicable before first generation / when accepted; if verdict fails, map every failed POST_IMAGE_VISUAL_VERDICT_JSON key to the Scene Contract / prompt-lock / guide patch that will fix it>
POST_IMAGE_REPAIR_ARTIFACT_PATH: <not_applicable before first generation / when accepted; required path to templates/post-image-repair-artifact-template.md artifact when rerender_required is true>
POST_IMAGE_REPAIR_COMPILER_STATUS: <pass|needs_revision|not_applicable>
POST_IMAGE_NEXT_DRAFT_PROMPT: <not_applicable before first generation / when accepted; repaired next prompt required when rerender_required is true and must not equal the failed compiled prompt>
POST_IMAGE_SCALE_FAILURE_SHOT_CLASS_ESCALATION: <not_applicable unless a scale-related verdict key failed; then patch camera/framing first: widen shot, reduce protagonist screen share, show full container, add witnesses, demote face focal>
REGENERATION_GATE_STATUS: <pass|blocked|not_applicable>
OBJECT_ANATOMY_MIXING_CHECK: <confirm no limb/hand/weapon/object is absorbed by cloak/hood/background/effects; list rerender triggers>
OBJECT_DISTORTION_VERDICT_CHECK: <audit each named/high-risk object for no unintended bend, warp, melt, resize, fusion, absorption, texture replacement, or functional impossibility; list rerender triggers>
PROTECTED_CHAIN_TRACE_VERDICT: <trace each protected chain by visible landmarks; fail if arm/leg/hand/weapon chain cannot be followed without inference>
GARMENT_ATTACHMENT_VERDICT_CHECK: <for cloak/cape/hood/large garment: verify visible attachment origin/anchors and fail if the garment floats, replaces a limb/torso, or has no structural origin>
FACE_AND_LOWER_BODY_VERDICT_CHECK: <confirm face plane is not flattened and lower-body/pants anatomy silhouettes are not absorbed by costume texture>
IRREVERSIBLE_STRUCTURE_CHECK: <confirm all registered anatomy/object instances survived with identity, scale, support/contact, and separation intact>
HAND_READABILITY_CHECK:
FINGER_TOPOLOGY_VERDICT_CHECK: <fail/rerender if any visible hand is only present but fused, claw-like, melted into black costume/cloak/blood, or lacks readable palm/thumb/finger separation>
FINAL_CORRECTION_LIST:
USER_COMMAND_COMPLIANCE_CHECK: <one-by-one audit of USER_COMMAND_CHECKLIST and non-negotiable spec commands: satisfied / partial / failed / not_applicable with rerender triggers>
AESTHETIC_RECOVERY_CHECK: <after structural checks pass, confirm composition pressure, face/eye focal, value massing, line/texture hierarchy, palette/accent discipline, and anti-generic style read are restored>
STRUCTURE_LOCK_SUMMARY: <internal compiler summary of only the highest-risk surviving structure locks; no exhaustive registry dump>
AESTHETIC_RENDER_BRIEF: <production image-language brief: focal face/eyes, composition/background pressure, value/lighting, line/shape, color/accent, texture/density>
NEGATIVE_PROMPT_LIMITED: <short specific negatives from failure lessons and high-risk structure only; avoid long validator/legal lists>
FINAL_IMAGE_PROMPT_COMPILED: <final production image prompt in natural visual language; no schema field names, Tier labels, object IDs, validator/verdict jargon, or raw checklist prose>
FINAL_PROMPT_COMPILER_STATUS: <pass|needs_revision|not_applicable>
AESTHETIC_RECOVERY_GATE_STATUS: <pass|needs_revision|not_applicable>
FINAL_GATE_STATUS: <pass|needs_revision>

IMAGE_GEN_HANDOFF_PROMPT: <legacy mirror only; prefer FINAL_IMAGE_PROMPT_COMPILED for pipeline emission>

[/ILLUSTRATE_SPEC]
