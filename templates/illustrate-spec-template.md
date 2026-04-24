# Illustrate Spec Template

Use this template for `illustrate-skill` `SPEC` runs that are meant to produce a final illustration or image-generation handoff.

Recommended workflow:

1. Copy this file to a working spec path such as `.omx/runs/<YYYYMMDD>-<scene-slug>-spec.md`.
2. Create a theory-read proof artifact from `templates/theory-read-proof-template.md` and record its path in `THEORY_READ_PROOF_PATH`.
3. Resolve the structural preflight in order: perspective rig -> object inventory -> anatomy object inventory -> object query -> relationship checks -> Blender-backed 3D blockout -> structural-invariant/painterly-freedom split -> image translation lock.
4. If Step 2.5 is needed, create an object-research artifact from `templates/object-research-artifact-template.md`.
5. Pause at user checkpoints when direction is ambiguous, unknown objects remain, or a user-visible branch must be chosen.
6. Do not replace unknown objects with random patterns, fake signage, fake mechanical texture, or unidentified noise.
7. Fill every field before claiming the staged spec is complete.
8. Run `python scripts/validate_illustrate_spec.py <spec-path> --strict-object-research`.
9. Revise failed sections until the validator passes.
10. Run `python scripts/run_illustrate_pipeline.py <spec-path> --strict-object-research`.
11. For any render-bound deliverable, keep `BLENDER_BLOCKOUT_REQUIRED: yes`, create the `.blend`/render script/pass outputs, review the pass PNGs, choose `BLENDER_GUIDE_STRENGTH`, and hand the pipeline-approved spec to image generation only after `IMAGE_GEN_READY: yes`.

[ILLUSTRATE_SPEC]

REQUEST_SUMMARY: <normalize the user request into one concise brief>
DELIVERABLE: <spec only | spec + image generation>
WORKSPACE_STYLE_MODE: <workspace reference style | derived skill | custom>
SOURCE_IMAGE_UPGRADE: <yes|no>
OBJECT_RESEARCH_REQUIRED: <yes|no>
IMAGE_GEN_READY: <no>
THEORY_READ_PROOF_PATH: <relative path>

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
GATE_NOTE:

## Step 2 Composition
THEORY_FILES:
- illustrate-skill/references/theory-02-composition-silhouette.md
- illustrate-skill/references/theory-02b-balance-cog.md

THUMBNAIL_SET:
CHOSEN_COMPOSITION_TYPE:
CHARACTER_POSITION:
CAMERA_ANGLE:
BLACK_MASS_MAP:
NEGATIVE_SPACE_BALANCE:
FLOW_DIRECTION_MAP:
COMPOSITION_OBJECT_ROLE_SUMMARY:
USER_CHECKPOINT_A_DIRECTION:
GATE_STATUS: <pass|needs_revision>
GATE_NOTE:

## Step 2.1 Perspective Rig
THEORY_FILES:
- illustrate-skill/references/theory-02-composition-silhouette.md

CAMERA_POSITION:
HORIZON_LINE:
VANISHING_POINTS:
PRIMARY_DEPTH_AXIS:
SUPPORT_PLANES:
VERTICAL_PLANE_LOCKS:
SCALE_ANCHOR_OBJECTS:
CONTACT_PLANES:
PERSPECTIVE_FAIL_CONDITIONS:
GATE_STATUS: <pass|needs_revision>
GATE_NOTE:

## Step 2.2 Object Inventory from Perspective
THEORY_FILES:
- illustrate-skill/references/theory-02-composition-silhouette.md

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
GATE_STATUS: <pass|needs_revision>
GATE_NOTE:

## Step 2.3 Anatomy Structure Gate
THEORY_FILES:
- illustrate-skill/references/theory-02c-anatomy-structure-gate.md
- illustrate-skill/references/theory-02d-geometric-blockout.md

ANATOMY_GATE_REQUIRED: <yes|no>
ANATOMY_PRIMARY_OBJECT:
ANATOMY_SUB_OBJECTS:
ANATOMY_CONTACT_OBJECTS:
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
VISIBLE_HANDS_AND_POSES:
HAND_SILHOUETTE_NOTE:
FINGER_GROUPING_NOTE:
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
GATE_NOTE:

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
USER_CHECKPOINT_B_OBJECT_DIRECTION:
GATE_STATUS: <pass|not_applicable|needs_revision>
GATE_NOTE:

## Step 2.5 Object Research Handoff
THEORY_FILES:
- object-research-skill/SKILL.md

HANDOFF_REQUIRED: <yes|no>
OBJECT_RESEARCH_ARTIFACT_PATH: <relative path or not_applicable>
SCENE_TYPE:
REQUIRED_OBJECTS:
RESEARCH_LANES_USED:
ANATOMY_REFERENCES_RESEARCHED:
SOURCE_IMAGE_OBJECTS_RESEARCHED:
SOURCE_IMAGE_RESEARCH_DECISION_NOTE:
HANDS_OR_FINGER_POSES_RESEARCHED:
HAND_RESEARCH_DECISION_NOTE:
BACKGROUND_OBJECTS_RESEARCHED:
SCALE_ANCHOR_OBJECTS_RESEARCHED:
STRUCTURALLY_UNCERTAIN_OBJECTS:
UNKNOWN_OBJECTS_RESOLUTION:
LOOKUP_RESULT:
RESEARCH_ACTION:
RETURNED_CARDS_OR_RECIPES:
GATE_STATUS: <pass|not_applicable|needs_revision>
GATE_NOTE:

## Step 2.6 Object Relationship Check
THEORY_FILES:
- object-research-skill output

APPLY_STATUS: <applied|not_applicable|needs_revision>
SCALE_RELATION_TABLE:
OCCLUSION_ORDER:
CONTACT_AND_SUPPORT:
COLLISION_CHECK:
MATERIAL_LIGHT_INTERACTION:
RIGID_OBJECT_GEOMETRY_LOCKS:
TEXT_RENDERING_POLICY:
GATE_STATUS: <pass|not_applicable|needs_revision>
GATE_NOTE:

## Step 2.7 Anatomy-on-Object Relationship Check
THEORY_FILES:
- illustrate-skill/references/theory-02c-anatomy-structure-gate.md

BODY_SUPPORT_LOGIC:
ANATOMY_STRUCTURE_APPLY_NOTE:
HAND_PROP_RELATION:
HAND_STRUCTURE_APPLY_NOTE:
FOOT_OBJECT_RELATION:
TORSO_ACTION_RELATION:
ANATOMY_OBJECT_FAIL_CONDITIONS:
GATE_STATUS: <pass|not_applicable|needs_revision>
GATE_NOTE:

## Step 2.8 3D Blockout / Modeling Contract
THEORY_FILES:
- illustrate-skill/references/theory-02-composition-silhouette.md
- illustrate-skill/references/theory-02d-geometric-blockout.md

PRIMITIVE_BLOCKS:
ENVIRONMENT_PRIMITIVE_BLOCKOUT:
SHARED_PERSPECTIVE_GRID:
METER_SCALE_LOCK:
ANATOMY_TO_ARCHITECTURE_SCALE_CHECK:
WINDOW_TO_HEAD_SIZE_CHECK:
PARAPET_TO_BODY_HEIGHT_CHECK:
FOOTPRINT_ON_SUPPORT_PLANE_CHECK:
DETAIL_AFTER_BLOCKOUT_LOCK:
CAMERA_BLOCKOUT:
DEPTH_LAYER_ORDER:
CONTACT_POINTS:
SCALE_CHECK:
PERSPECTIVE_CHECK:
OPTIONAL_3D_REFERENCE_PLAN: <mandatory Blender blockout/pass plan for render-bound runs; not_applicable only for spec-only runs>
BLENDER_BLOCKOUT_REQUIRED: <yes for render-bound | no only for spec-only>
BLENDER_SCENE_PATH: <relative path to .blend or not_applicable>
BLENDER_RENDER_SCRIPT_PATH: <relative path to blender python script or not_applicable>
BLENDER_PASS_OUTPUTS: <clay=path | lineart=path | depth=path | normal=path | mask=path | not_applicable>
BLENDER_BLOCKOUT_REVIEW: <camera, scale, contact, support, and silhouette review or not_applicable>
BLENDER_GUIDE_STRENGTH: <loose guide|medium guide|strict guide|not_applicable>
STRUCTURAL_INVARIANTS_TO_PRESERVE: <camera/support/contact/scale/object-identity locks that image generation must keep>
PAINTERLY_FREEDOMS_ALLOWED: <compression/massing/partial occlusion allowed after support/contact/scale remain readable; no body-size distortion unless explicitly requested>
CONTROLNET_CONDITIONING_PLAN: <depth/lineart/normal/mask/img2img plan plus guide strength, or not_applicable>
BLOCKOUT_REVIEW_STATUS: <pass|needs_revision|not_applicable>
USER_CHECKPOINT_C_BLOCKOUT_DIRECTION:
GATE_STATUS: <pass|needs_revision>
GATE_NOTE:

## Step 2.9 Image Translation Lock
THEORY_FILES:
- illustrate-skill/references/theory-08-final-check-correction.md
- illustrate-skill/references/theory-02d-geometric-blockout.md

GENERATION_PRIORITY_ORDER:
NON_NEGOTIABLE_LOCKS:
STYLE_ALLOWED_AFTER_STRUCTURE:
BLENDER_GUIDE_STRENGTH:
PAINTERLY_COMPRESSION_ALLOWANCE:
NO_HIERATIC_SCALE_DISTORTION:
PROMPT_COMPRESSION_RULE:
UNKNOWN_OBJECT_POLICY_LOCK:
USER_CHECKPOINT_D_PRE_RENDER_DIRECTION:
GATE_STATUS: <pass|needs_revision>
GATE_NOTE:

## Step 3 Value
THEORY_FILES:
- illustrate-skill/references/theory-03-lighting-value.md

LIGHTING_PLAN:
VALUE_COUNT_DECISION:
GRAYSCALE_VALUE_MAP:
FOCAL_CONTRAST_ZONE:
OUTER_AREA_SUPPRESSION_PLAN:
MATERIAL_EDGE_PLAN:
GRAYSCALE_REDUCTION_TEST:
GATE_STATUS: <pass|needs_revision>
GATE_NOTE:

## Step 4 Face
THEORY_FILES:
- illustrate-skill/references/theory-04-face-eyes.md
- illustrate-skill/references/theory-04a-face-emotion-patterns.md

SURFACE_INNER_EMOTION:
MAIN_SUPPORT_EMOTION:
INTENSITY:
EYE_RENDER_PLAN:
EXPRESSION_NOTE:
FACE_FOCAL_MAP:
EYE_LIGHT_CONSISTENCY_NOTE:
ASYMMETRY_NOTE:
NATURAL_ACTING_LOCK:
ANTI_DIRECT_EXPRESSION_LOCK:
GATE_STATUS: <pass|needs_revision>
GATE_NOTE:

## Step 5 Line & Shape
THEORY_FILES:
- illustrate-skill/references/theory-05-line-shape.md
- illustrate-skill/references/theory-05a-hands-fingers.md

LINE_HIERARCHY:
LINE_WEIGHT_MAP:
SHAPE_DECOMPOSITION_PLAN:
GAZE_GUIDANCE_MOTIF_MAP:
HAND_LINE_PRIORITY_NOTE:
LINE_VS_SHAPE_ROLE_NOTE:
GATE_STATUS: <pass|needs_revision>
GATE_NOTE:

## Step 6 Color & Accent
THEORY_FILES:
- illustrate-skill/references/theory-06-color-palette-point.md

PALETTE_SELECTION:
ACCENT_PLACEMENT_MAP:
BASE_SUPPORT_ACCENT_ROLE_NOTE:
PER_PART_COLOR_DISTRIBUTION_NOTE:
NON_PLASTIC_SKIN_TONE_LOCK:
VALUE_PRESERVATION_NOTE:
GATE_STATUS: <pass|needs_revision>
GATE_NOTE:

## Step 7 Texture
THEORY_FILES:
- illustrate-skill/references/theory-07-texture-density.md

TEXTURE_DENSITY_MAP:
ROUGH_SMOOTH_SEPARATION_PLAN:
SECONDARY_SYMBOL_PLACEMENT:
GLOBAL_GRAIN_NOTE:
LOCAL_TEXTURE_EMPHASIS_NOTE:
NON_PLASTIC_SKIN_SURFACE_NOTE:
GATE_STATUS: <pass|needs_revision>
GATE_NOTE:

## Step 8 Final Check
THEORY_FILES:
- illustrate-skill/references/theory-08-final-check-correction.md

NORMAL_VIEW_CHECK:
REDUCED_SIZE_CHECK:
GRAYSCALE_CHECK:
HAND_READABILITY_CHECK:
FINAL_CORRECTION_LIST:
OUTPUT_MEDIUM_NOTE:
SELF_FEEDBACK_NOTE:
ARCHIVE_NOTE:
FINAL_GATE_STATUS: <pass|needs_revision>
FINAL_GATE_NOTE:

IMAGE_GEN_HANDOFF_PROMPT:
ARCHIVE_PATH:

[/ILLUSTRATE_SPEC]
