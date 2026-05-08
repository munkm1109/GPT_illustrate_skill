#!/usr/bin/env python3
"""Validate an illustrate-skill SPEC artifact and linked evidence."""

from __future__ import annotations

import argparse
import io
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path


def force_utf8_stdio() -> None:
    """Keep CLI diagnostics from crashing on Windows cp949 consoles.

    Prefer `reconfigure()` because it updates the existing TextIO stream in
    place. Fall back to wrapping `.buffer` only for older/nonstandard streams
    that do not support reconfiguration.
    """
    for stream_name in ("stdout", "stderr"):
        stream = getattr(sys, stream_name)
        encoding = (getattr(stream, "encoding", None) or "").lower().replace("_", "-")
        if encoding in {"utf-8", "utf8", "cp65001"}:
            continue
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            buffer = getattr(stream, "buffer", None)
            if buffer is not None:
                setattr(
                    sys,
                    stream_name,
                    io.TextIOWrapper(buffer, encoding="utf-8", errors="replace"),
                )


force_utf8_stdio()


GLOBAL_FIELDS = [
    "REQUEST_SUMMARY",
    "USER_COMMAND_CHECKLIST",
    "DELIVERABLE",
    "WORKSPACE_STYLE_MODE",
    "RENDER_STYLE_BASELINE_QUESTION",
    "RENDER_STYLE_USER_DECISION",
    "RENDER_STYLE_PRIMARY_AXIS",
    "RENDER_STYLE_SECONDARY_AXES",
    "RENDER_STYLE_MIXING_POLICY",
    "RENDER_STYLE_DRIFT_GUARD",
    "RENDER_STYLE_PROMPT_ANCHOR",
    "SOURCE_IMAGE_UPGRADE",
    "INPUT_ROUTE",
    "SOURCE_IMAGE_ACTUAL_CONDITIONING",
    "IMAGE_DEVELOPMENT_ALLOWED",
    "OBJECT_RESEARCH_REQUIRED",
    "USER_CAMERA_CLASS_PRESET",
    "USER_CAMERA_CLASS_LOCK_LEVEL",
    "USER_CAMERA_CLASS_REASON",
    "IMAGE_GEN_READY",
    "PRE_IMAGE_HANDOFF_READY",
    "POST_IMAGE_VERDICT_REQUIRED",
    "POST_IMAGE_ACCEPTED",
    "THEORY_READ_PROOF_PATH",
]

RENDER_STYLE_AXES = {
    "axis_1_2d_anime",
    "axis_2_semi_real_concept",
    "axis_3_3d_render",
    "axis_4_live_action_cosplay",
    "axis_5_game_cg_key_visual",
}

RENDER_STYLE_PRIMARY_ALLOWED = RENDER_STYLE_AXES | {"custom_user_axis"}

RENDER_STYLE_PENDING_MARKERS = {
    "pending_user_answer",
    "pending",
    "not_asked",
    "unresolved",
    "assumed",
    "auto",
    "추정",
    "가정",
    "미확정",
}

RENDER_STYLE_MIX_KEYWORDS = [
    "mix",
    "combination",
    "combine",
    "axis_1+axis_2",
    "axis_1 + axis_2",
    "axis_1+axis_5",
    "axis_1 + axis_5",
    "axis_2+axis_5",
    "axis_2 + axis_5",
    "axis_4+axis_5",
    "axis_4 + axis_5",
    "recommended",
    "allowed",
    "avoid",
    "조합",
    "추천",
    "허용",
    "금지",
]

RENDER_STYLE_DRIFT_KEYWORDS = [
    "drift",
    "no ",
    "avoid",
    "forbid",
    "photoreal",
    "photo",
    "cosplay",
    "live-action",
    "3d",
    "semi-real",
    "skin pore",
    "실사",
    "코스프레",
    "사진",
    "금지",
    "방지",
]

PIVA_FIELDS = [
    "PIVA_MODE",
    "PLAN_USER_COMMAND_SOURCE",
    "PLAN_NON_NEGOTIABLES",
    "PLAN_OBJECT_ANATOMY_SCALE_WITNESSES",
    "PLAN_HUMANOID_ANATOMY_SCALE_PARITY",
    "PLAN_PREVIOUS_FAILURES",
    "PLAN_GATE_STATUS",
    "IMPLEMENT_STEP_MAP",
    "IMPLEMENT_OBJECT_RESEARCH_TRANSFER",
    "IMPLEMENT_SCALE_TRANSFER",
    "IMPLEMENT_HUMANOID_SCALE_TRANSFER",
    "IMPLEMENT_STYLE_TRANSFER",
    "IMPLEMENT_PROMPT_DRAFT_TRANSFER",
    "IMPLEMENT_GATE_STATUS",
    "VERIFY_OBJECT_DISTORTION_TEST",
    "VERIFY_HERO_OBJECT_SCALE_TEST",
    "VERIFY_HUMANOID_SCALE_PARITY_TEST",
    "VERIFY_OBJECT_RESEARCH_TRANSFER_TEST",
    "VERIFY_STYLE_TARGET_TEST",
    "VERIFY_PROMPT_CONFLICT_TEST",
    "VERIFY_GATE_STATUS",
    "AUDIT_PRE_IMAGE_COMMAND_AUDIT",
    "AUDIT_PRE_IMAGE_NON_NEGOTIABLE_AUDIT",
    "AUDIT_HUMANOID_SCALE_PARITY_TRIGGER",
    "AUDIT_POST_IMAGE_VISUAL_AUDIT_PLAN",
    "AUDIT_RERENDER_TRIGGERS",
    "AUDIT_GATE_STATUS",
    "IMAGE_HANDOFF_GATE_STATUS",
]

PIVA_STATUS_FIELDS = {
    "PLAN_GATE_STATUS": {"pass", "needs_revision"},
    "IMPLEMENT_GATE_STATUS": {"pass", "needs_revision"},
    "VERIFY_GATE_STATUS": {"pass", "needs_revision"},
    "AUDIT_GATE_STATUS": {"pass", "needs_revision"},
    "IMAGE_HANDOFF_GATE_STATUS": {"pass", "blocked"},
}

PIVA_THEORY_FILE = "illustrate-skill/references/pipeline-plan-implement-verify-audit.md"

SECTION_ORDER = [
    "## Step 0 Route Gate",
    "## Step 1 Intent",
    "## Step 2 Composition",
    "## Step 2.1 Perspective Rig",
    "## Step 2.2 Object Inventory from Perspective",
    "## Step 2.2M Merge Gate: Normalized Scene Graph",
    "## Step 2.3 Anatomy Structure Gate",
    "## Step 2.4 Object Knowledge Query Plan",
    "## Step 2.5 Object Research Handoff",
    "## Step 2.6 Object Relationship Check",
    "## Step 2.7 Anatomy-on-Object Relationship Check",
    "## Step 2.8 3D Blockout / Modeling Contract",
    "## Step 2.9 Image Translation Lock",
    "## Step 3 Value",
    "## Step 4 Face",
    "## Step 5 Line & Shape",
    "## Step 6 Color & Accent",
    "## Step 7 Texture",
    "## Step 8 Final Check",
]

SECTION_FIELDS = {
    "## Step 0 Route Gate": [
        "INPUT_ROUTE",
        "ROUTE_REASON",
        "EXISTING_IMAGE_INPUT",
        "PROMPT_ONLY_GENERATION",
        "SOURCE_IMAGE_ACTUAL_CONDITIONING",
        "IMAGE_DEVELOPMENT_ALLOWED",
        "IMAGE_DEVELOPMENT_CONDITIONING_NOTE",
        "ACTIVE_INTAKE_BRANCH",
        "INACTIVE_BRANCH_POLICY",
        "ROUTE_GATE_STATUS",
        "GATE_STATUS",
    ],
    "## Step 1 Intent": [
        "SCENE_INTENT_SENTENCE",
        "ENVIRONMENT",
        "TIME_OR_LIGHTING",
        "ROLE",
        "ACTION",
        "EMOTION_AXIS",
        "AUDIENCE_FEELING",
        "GATE_STATUS",
    ],
    "## Step 2 Composition": [
        "THUMBNAIL_SET",
        "CHOSEN_COMPOSITION_TYPE",
        "CHARACTER_POSITION",
        "CAMERA_ANGLE",
        "USER_CAMERA_CLASS_PRESET",
        "USER_CAMERA_CLASS_LOCK_LEVEL",
        "USER_CAMERA_CLASS_REASON",
        "CAMERA_CLASS_CONFLICT_STATUS",
        "CAMERA_CLASS_CONFLICT_REASON",
        "CAMERA_CLASS_RESOLUTION",
        "CHOSEN_CAMERA_CLASS",
        "CAMERA_CLASS_VISUAL_TRANSLATION",
        "BLACK_MASS_MAP",
        "NEGATIVE_SPACE_BALANCE",
        "FLOW_DIRECTION_MAP",
        "COMPOSITION_OBJECT_ROLE_SUMMARY",
        "USER_CHECKPOINT_A_DIRECTION",
        "GATE_STATUS",
    ],
    "## Step 2.1 Perspective Rig": [
        "CAMERA_POSITION",
        "SCALE_CRITICAL_SHOT_CLASS",
        "FULL_CONTAINER_VISIBILITY_REQUIREMENT",
        "SCALE_WITNESS_MIN_COUNT",
        "HERO_TO_MODULE_VISUAL_RATIO",
        "CLOSEUP_BLOCKED_UNTIL_SCALE_PASS",
        "FACE_FOCAL_DEMOTION_FOR_SCALE",
        "PERSPECTIVE_SCALE_TRANSFER_MODE",
        "HERO_FOOTPOINT_PLANE",
        "BASELINE_OBJECT",
        "PROJECTED_BASELINE_TO_HERO_POSITION",
        "SCREEN_OCCUPANCY_IS_DERIVED",
        "SCREEN_OCCUPANCY_MUST_NOT_OVERRIDE_WORLD_SCALE",
        "CAMERA_CUT_SCALE_RECONCILIATION",
        "SCALE_PROXY_DUMMY_REQUIRED",
        "SCALE_PROXY_DUMMY_HEIGHT",
        "SCALE_PROXY_DUMMY_BASELINE_OBJECT",
        "SCALE_PROXY_DUMMY_PLACEMENT_PLAN",
        "SCALE_PROXY_DUMMY_TO_HERO_PROJECTION",
        "HORIZON_LINE",
        "VANISHING_POINTS",
        "PRIMARY_DEPTH_AXIS",
        "SUPPORT_PLANES",
        "VERTICAL_PLANE_LOCKS",
        "SCALE_ANCHOR_OBJECTS",
        "SCALE_ANCHOR_CANDIDATES",
        "SCALE_BASELINE_SELECTION",
        "SCALE_ANCHOR_RANKING",
        "SCALE_RATIO_JUDGMENT_METHOD",
        "NEAR_PLANE_ANCHOR_CHECK",
        "DEPTH_PLANE_SCALE_TRANSFER",
        "FUNCTIONAL_SIZE_TESTS",
        "SCALE_ANCHOR_FAIL_CONDITIONS",
        "SCALE_ANCHOR_VERDICT_HANDOFF",
        "HERO_OBJECT_SCALE_RELATIONSHIP_CHECK",
        "HERO_BACKGROUND_HUMANOID_SCALE_COMPARISON_TABLE",
        "HERO_HUMANOID_SCALE_COMPARISON_PLAN",
        "PERSPECTIVE_ONLY_SCALE_LOCK",
        "IRREVERSIBLE_STRUCTURE_REGISTRY",
        "CONTACT_PLANES",
        "PERSPECTIVE_FAIL_CONDITIONS",
        "GATE_STATUS",
    ],
    "## Step 2.2 Object Inventory from Perspective": [
        "SOURCE_IMAGE_OBJECTS_PRESENT",
        "PRIMARY_RETAINED_OBJECTS",
        "STRUCTURALLY_CLEAR_SOURCE_OBJECTS",
        "STRUCTURALLY_UNCERTAIN_SOURCE_OBJECTS",
        "FOREGROUND_FRAME_OBJECTS",
        "SUPPORT_PLANE_OBJECTS",
        "LEFT_VERTICAL_PLANE_OBJECTS",
        "RIGHT_VERTICAL_PLANE_OBJECTS",
        "OVERHEAD_PLANE_OBJECTS",
        "BACKGROUND_DEPTH_OBJECTS",
        "EFFECT_OBJECTS",
        "TEXT_OR_GLYPH_OBJECTS",
        "UNKNOWN_OBJECT_TRIAGE",
        "VISIBLE_HUMANOID_OBJECT_CANDIDATES",
        "OBJECT_DISTORTION_RISK_INVENTORY",
        "OCCLUDER_MASS_INVENTORY",
        "OBJECT_DENSITY_EDGE_CASE",
        "HUMAN_PRIORITY_DENSITY_REDUCTION_PLAN",
        "GATE_STATUS",
    ],
    "## Step 2.2M Merge Gate: Normalized Scene Graph": [
        "MERGED_FROM_ROUTE",
        "SCENE_CONTRACT_VERSION",
        "SCENE_INTENT_LOCK",
        "COMPOSITION_LOCK",
        "PERSPECTIVE_LOCK",
        "OBJECT_REGISTRY",
        "RELATIONSHIP_CONTRACT",
        "ACTION_CONTACT_CONTRACT",
        "POST_ACTION_OBJECT_STATE_CONTRACT",
        "TARGET_CUT_PLANE_VISIBILITY_CONTRACT",
        "SCALE_PARITY_CONTRACT",
        "PROTECTED_ANATOMY_CHAINS",
        "GARMENT_ATTACHMENT_CONTRACT",
        "OBJECT_REGISTRY_BY_PLANE",
        "ANATOMY_CANDIDATE_REGISTRY",
        "SOURCE_PRESERVATION_LOCK",
        "PROMPT_ONLY_ASSUMPTION_LOCK",
        "OBJECT_RESEARCH_TRIGGER_SUMMARY",
        "MERGE_CONFLICTS",
        "SCENE_CONTRACT_GATE_STATUS",
        "MERGE_GATE_STATUS",
        "GATE_STATUS",
    ],
    "## Step 2.3 Anatomy Structure Gate": [
        "ANATOMY_GATE_REQUIRED",
        "ANATOMY_PRIMARY_OBJECT",
        "ANATOMY_SUB_OBJECTS",
        "ANATOMY_CONTACT_OBJECTS",
        "ALL_HUMANOID_ANATOMY_INVENTORY",
        "SECONDARY_HUMANOID_ANATOMY_OBJECTS",
        "HUMANOID_ANATOMY_TRANSFER_TABLE",
        "HUMANOID_DEPTH_PLANE_MAP",
        "HERO_SECONDARY_HUMANOID_SCALE_PARITY_LOCK",
        "NO_STYLIZED_SCALE_EXAGGERATION_LOCK",
        "AGE_BAND",
        "SEX_CLASSIFICATION",
        "BODY_TYPE_BASELINE",
        "BODY_ANATOMY_BASE_CARD",
        "SEX_OVERLAY_CARD",
        "HAND_ANATOMY_SUBMODULE_CARD",
        "STYLIZATION_LEVEL",
        "HEAD_TO_BODY_RATIO",
        "RIBCAGE_PELVIS_RELATION",
        "SHOULDER_WIDTH_NOTE",
        "HIP_WIDTH_NOTE",
        "LIMB_PROPORTION_NOTE",
        "ELBOW_WRIST_CHAIN_NOTE",
        "HIP_KNEE_ANKLE_CHAIN_NOTE",
        "HAND_SIZE_RELATIVE_NOTE",
        "FOOT_SIZE_RELATIVE_NOTE",
        "LOWER_BODY_SILHOUETTE_LOCK",
        "PROTECTED_ANATOMY_CHAIN_VISIBILITY",
        "VISIBLE_HANDS_AND_POSES",
        "HAND_SILHOUETTE_NOTE",
        "FINGER_GROUPING_NOTE",
        "HAND_DETAIL_BUDGET",
        "FINGER_TOPOLOGY_CHAIN_LOCK",
        "FINGER_TOPOLOGY_FAIL_CONDITIONS",
        "SUPPORTING_LEG_NOTE",
        "BALANCE_LINE_NOTE",
        "SHOULDER_PELVIS_TILT_NOTE",
        "ANATOMY_PRIMITIVE_BLOCKOUT",
        "HEAD_PRIMITIVE",
        "RIBCAGE_PRIMITIVE",
        "PELVIS_PRIMITIVE",
        "LIMB_CYLINDER_CHAIN",
        "JOINT_SPHERE_MAP",
        "HAND_FOOT_PRIMITIVES",
        "ANATOMY_PRIMITIVE_FAIL_CONDITIONS",
        "ANATOMY_RESEARCH_DECISION_NOTE",
        "GATE_STATUS",
    ],
    "## Step 2.4 Object Knowledge Query Plan": [
        "RESEARCH_LANES",
        "LOCAL_CARD_LOOKUP_PLAN",
        "EXISTING_MATCHED_CARDS",
        "MISSING_OR_WEAK_CARDS",
        "RESEARCH_REQUIRED_OBJECTS",
        "QUERY_TERMS",
        "CONFIDENCE_BY_OBJECT",
        "DRAW_READY_LOCKS_NEEDED",
        "CONTAINER_CAPACITY_RESEARCH_NEEDED",
        "HUMAN_ENTERABLE_COMPOSITE_SCALE_PLAN",
        "USER_CHECKPOINT_B_OBJECT_DIRECTION",
        "GATE_STATUS",
    ],
    "## Step 2.5 Object Research Handoff": [
        "HANDOFF_REQUIRED",
        "OBJECT_RESEARCH_ARTIFACT_PATH",
        "OBJECT_RESEARCH_INVOCATION_LOG_PATH",
        "SCENE_TYPE",
        "REQUIRED_OBJECTS",
        "RESEARCH_LANES_USED",
        "PASSENGER_INSTANCE_REGISTRY",
        "ANATOMY_REFERENCES_RESEARCHED",
        "SOURCE_IMAGE_OBJECTS_RESEARCHED",
        "SOURCE_IMAGE_RESEARCH_DECISION_NOTE",
        "HANDS_OR_FINGER_POSES_RESEARCHED",
        "HAND_RESEARCH_DECISION_NOTE",
        "BACKGROUND_OBJECTS_RESEARCHED",
        "SCALE_ANCHOR_OBJECTS_RESEARCHED",
        "CONTAINER_CAPACITY_OBJECTS_RESEARCHED",
        "CONTAINER_CAPACITY_RESEARCH_APPLIED",
        "HUMAN_ENTERABLE_COMPOSITE_SCALE_TABLE",
        "ENTRY_FIT_CHECK_APPLIED",
        "XYZ_VOLUME_CHECK_APPLIED",
        "CAPACITY_CLASS_CHECK_APPLIED",
        "OCCUPANT_ANCHOR_CHECK_APPLIED",
        "MODULE_REPETITION_CHECK_APPLIED",
        "HUMAN_ENTERABLE_SCALE_VERDICT_APPLIED",
        "STRUCTURALLY_UNCERTAIN_OBJECTS",
        "UNKNOWN_OBJECTS_RESOLUTION",
        "LOOKUP_RESULT",
        "RESEARCH_ACTION",
        "RETURNED_CARDS_OR_RECIPES",
        "GATE_STATUS",
    ],
    "## Step 2.6 Object Relationship Check": [
        "APPLY_STATUS",
        "SCALE_RELATION_TABLE",
        "OCCLUSION_ORDER",
        "OCCLUSION_LAYER_GRAPH",
        "PROTECTED_CHAIN_EXPOSURE_RULES",
        "SEPARATION_CUE_PLAN",
        "FINGER_OCCLUSION_SEPARATION_RULE",
        "CONTACT_AND_SUPPORT",
        "OBJECT_ANATOMY_SEPARATION_LOCKS",
        "IRREVERSIBLE_OBJECT_ANATOMY_LOCKS",
        "MATERIAL_LIGHT_INTERACTION",
        "RIGID_OBJECT_GEOMETRY_LOCKS",
        "ALL_OBJECT_DISTORTION_LOCK",
        "TEXT_RENDERING_POLICY",
        "GATE_STATUS",
    ],
    "## Step 2.7 Anatomy-on-Object Relationship Check": [
        "BODY_SUPPORT_LOGIC",
        "ANATOMY_STRUCTURE_APPLY_NOTE",
        "HAND_PROP_RELATION",
        "HAND_STRUCTURE_APPLY_NOTE",
        "FUNCTIONAL_GRIP_MECHANICS_CONTRACT",
        "WRIST_FORCE_PATH_CHECK",
        "FOOT_OBJECT_RELATION",
        "TORSO_ACTION_RELATION",
        "ANATOMY_OBJECT_FAIL_CONDITIONS",
        "GATE_STATUS",
    ],
    "## Step 2.8 3D Blockout / Modeling Contract": [
        "PRIMITIVE_BLOCKS",
        "ENVIRONMENT_PRIMITIVE_BLOCKOUT",
        "SHARED_PERSPECTIVE_GRID",
        "METER_SCALE_LOCK",
        "ABSOLUTE_SCALE_LADDER",
        "OBJECT_ANATOMY_SCALE_INVARIANTS",
        "HUMANOID_SCALE_PARITY_BLOCKOUT_CHECK",
        "OBJECT_DISTORTION_BLOCKOUT_CHECK",
        "IRREVERSIBLE_STRUCTURE_INVARIANTS",
        "ANATOMY_TO_ARCHITECTURE_SCALE_CHECK",
        "WINDOW_TO_HEAD_SIZE_CHECK",
        "PARAPET_TO_BODY_HEIGHT_CHECK",
        "DOOR_VEHICLE_FUNCTIONAL_SCALE_CHECK",
        "PASSENGER_CAPACITY_SCALE_CHECK",
        "XYZ_VOLUME_BLOCKOUT_CHECK",
        "CAPACITY_CLASS_BLOCKOUT_CHECK",
        "MODULE_REPETITION_BLOCKOUT_CHECK",
        "HUMAN_ENTERABLE_COMPOSITE_BLOCKOUT_VERDICT",
        "FOOTPRINT_ON_SUPPORT_PLANE_CHECK",
        "DETAIL_AFTER_BLOCKOUT_LOCK",
        "INSTANCE_MASK_SEPARATION_PLAN",
        "PROTECTED_CHAIN_MASK_REVIEW",
        "CAMERA_BLOCKOUT",
        "DEPTH_LAYER_ORDER",
        "CONTACT_POINTS",
        "SCALE_CHECK",
        "CAMERA_CLASS_BLOCKOUT_LOCK",
        "FULL_CONTAINER_VISIBILITY_BLOCKOUT_CHECK",
        "SCALE_WITNESS_VISIBILITY_COUNT_CHECK",
        "PERSPECTIVE_CALCULATION_BLOCKOUT_TRANSFER",
        "PROJECTED_BASELINE_BLOCKOUT_CHECK",
        "SCREEN_OCCUPANCY_BLOCKOUT_RECONCILIATION",
        "SCALE_PROXY_DUMMY_BLOCKOUT_PLACEMENT",
        "SCALE_PROXY_DUMMY_BLOCKOUT_CHECK",
        "SCALE_PROXY_DUMMY_REMOVAL_POLICY",
        "SCALE_PROXY_TRACE_OVERLAY",
        "SCALE_PROXY_TO_HERO_BLOCKOUT_VERDICT",
        "OPTIONAL_3D_REFERENCE_PLAN",
        "BLENDER_BLOCKOUT_REQUIRED",
        "BLENDER_SCENE_PATH",
        "BLENDER_RENDER_SCRIPT_PATH",
        "BLENDER_PASS_OUTPUTS",
        "BLENDER_BLOCKOUT_REVIEW",
        "BLENDER_GUIDE_STRENGTH",
        "BLOCKOUT_CORE_OBJECT_VISIBILITY",
        "BLOCKOUT_TARGET_CONTACT_VISIBILITY",
        "BLOCKOUT_CAMERA_OCCLUSION_CHECK",
        "BLENDER_VISIBILITY_REPORT_PATH",
        "BLENDER_VISIBILITY_REPORT_REVIEW",
        "VISUAL_GUIDE_COMPOSITE_REQUIRED",
        "VISUAL_GUIDE_COMPOSITE_PATH",
        "VISUAL_GUIDE_COMPOSITE_SOURCE_PASSES",
        "VISUAL_GUIDE_COMPOSITE_OVERLAYS",
        "VISUAL_GUIDE_COMPOSITE_REVIEW",
        "VISUAL_GUIDE_COMPOSITE_CONDITIONING_ROLE",
        "SCALE_COMPOSITE_HARD_LOCK",
        "USER_VISUAL_GUIDE_CHECKPOINT_REQUIRED",
        "USER_VISUAL_GUIDE_FEEDBACK",
        "USER_VISUAL_GUIDE_FEEDBACK_APPLIED",
        "USER_VISUAL_GUIDE_APPROVAL_STATUS",
        "SCALE_VISUAL_GUIDE_PACKAGE",
        "CUT_PLANE_VISUAL_GUIDE_PACKAGE",
        "GRIP_MECHANICS_VISUAL_GUIDE_PACKAGE",
        "STRUCTURAL_INVARIANTS_TO_PRESERVE",
        "PAINTERLY_FREEDOMS_ALLOWED",
        "STRUCTURE_OVER_PAINTERLY_LOCK",
        "NO_STRUCTURAL_SACRIFICE_RULE",
        "CONTROLNET_CONDITIONING_PLAN",
        "BLOCKOUT_REVIEW_STATUS",
        "USER_CHECKPOINT_C_BLOCKOUT_DIRECTION",
        "GATE_STATUS",
    ],
    "## Step 2.9 Image Translation Lock": [
        "GENERATION_PRIORITY_ORDER",
        "NON_NEGOTIABLE_LOCKS",
        "STYLE_ALLOWED_AFTER_STRUCTURE",
        "ANATOMY_OVER_DENSITY_LOCK",
        "SCENE_CONTRACT_PROMPT_LOCK",
        "ACTION_CONTACT_PROMPT_LOCK",
        "CAMERA_CLASS_PROMPT_OPENING",
        "BLENDER_GUIDE_STRENGTH",
        "TEXT_ONLY_LOCKS_REJECTION",
        "VISUAL_GUIDE_COMPOSITE_PROMPT_LOCK",
        "IMAGE_INPUT_STACK_PLAN",
        "PRE_COMPOSITE_EVIDENCE_STACK_LOCK",
        "SCALE_PROXY_TRACE_PROMPT_LOCK",
        "COMPOSITE_IS_REFERENCE_NOT_SOLE_AUTHORITY",
        "SCALE_MUST_FOLLOW_COMPOSITE_PROMPT_LOCK",
        "IMAGE_GEN_STRUCTURE_CONDITIONING_MODE",
        "IMAGE_GEN_STRUCTURE_CONDITIONING_STRENGTH",
        "IMAGE_GEN_STRUCTURE_CONDITIONING_INPUTS",
        "IMAGE_GEN_STRUCTURE_CONDITIONING_LIMITS",
        "IMAGE_GEN_HANDOFF_PACKAGE_PATH",
        "SCALE_VISUAL_GUIDE_PROMPT_LOCK",
        "CUT_PLANE_VISIBILITY_PROMPT_LOCK",
        "GRIP_MECHANICS_PROMPT_LOCK",
        "SCALE_OVER_STYLE_LOCK",
        "HUMANOID_SCALE_PARITY_PROMPT_LOCK",
        "HUMAN_ENTERABLE_OCCUPANT_PROMPT_LOCK",
        "SCALE_CRITICAL_PROMPT_OPENING",
        "SCALE_CRITICAL_SHOT_CLASS_PROMPT_LOCK",
        "FACE_FOCAL_DEMOTION_PROMPT_LOCK",
        "PERSPECTIVE_CALCULATION_PROMPT_LOCK",
        "SCREEN_OCCUPANCY_DERIVED_PROMPT_LOCK",
        "PROMPT_ATTENTION_BUDGET_LOCK",
        "TIERED_IMAGE_PROMPT_LOCKS",
        "OCCLUSION_TRANSLATION_LOCK",
        "ALL_OBJECTS_ANATOMY_IRREVERSIBLE_LOCK",
        "OBJECT_DISTORTION_PROMPT_LOCK",
        "PROMPT_FINGER_TOPOLOGY_LOCK",
        "PAINTERLY_COMPRESSION_ALLOWANCE",
        "NO_HIERATIC_SCALE_DISTORTION",
        "VERDICT_SCALE_AND_MIXING_FAILS",
        "VERDICT_IRREVERSIBLE_STRUCTURE_FAILS",
        "PROMPT_COMPRESSION_RULE",
        "UNKNOWN_OBJECT_POLICY_LOCK",
        "USER_CHECKPOINT_D_PRE_RENDER_DIRECTION",
        "GATE_STATUS",
    ],
    "## Step 3 Value": [
        "LIGHTING_PLAN",
        "VALUE_COUNT_DECISION",
        "GRAYSCALE_VALUE_MAP",
        "FOCAL_CONTRAST_ZONE",
        "OUTER_AREA_SUPPRESSION_PLAN",
        "MATERIAL_EDGE_PLAN",
        "GATE_STATUS",
    ],
    "## Step 4 Face": [
        "SURFACE_INNER_EMOTION",
        "MAIN_SUPPORT_EMOTION",
        "INTENSITY",
        "EYE_RENDER_PLAN",
        "FACE_STRUCTURE_QUALITY_LOCK",
        "FACE_FOCAL_MAP",
        "NATURAL_ACTING_LOCK",
        "ANTI_DIRECT_EXPRESSION_LOCK",
        "GATE_STATUS",
    ],
    "## Step 5 Line & Shape": [
        "LINE_HIERARCHY",
        "LINE_WEIGHT_MAP",
        "SHAPE_DECOMPOSITION_PLAN",
        "GAZE_GUIDANCE_MOTIF_MAP",
        "HAND_LINE_PRIORITY_NOTE",
        "LOWER_BODY_LINE_PRIORITY_NOTE",
        "PROTECTED_CHAIN_EDGE_SEPARATION_PLAN",
        "GATE_STATUS",
    ],
    "## Step 6 Color & Accent": [
        "PALETTE_SELECTION",
        "ACCENT_PLACEMENT_MAP",
        "NON_PLASTIC_SKIN_TONE_LOCK",
        "GATE_STATUS",
    ],
    "## Step 7 Texture": [
        "TEXTURE_DENSITY_MAP",
        "ROUGH_SMOOTH_SEPARATION_PLAN",
        "SECONDARY_SYMBOL_PLACEMENT",
        "GATE_STATUS",
    ],
    "## Step 8 Final Check": [
        "SCALE_ANCHOR_VERDICT_CHECK",
        "HERO_OBJECT_SCALE_VERDICT_CHECK",
        "HUMANOID_SCALE_PARITY_VERDICT_CHECK",
        "PASSENGER_CAPACITY_VERDICT_CHECK",
        "ENTRY_FIT_VERDICT_CHECK",
        "XYZ_VOLUME_VERDICT_CHECK",
        "CAPACITY_CLASS_VERDICT_CHECK",
        "OCCUPANT_ANCHOR_VERDICT_CHECK",
        "MODULE_REPETITION_VERDICT_CHECK",
        "HUMAN_ENTERABLE_SCALE_VERDICT",
        "ACTION_CONTACT_VERDICT_CHECK",
        "SCALE_VISUAL_GUIDE_VERDICT_CHECK",
        "CAMERA_CLASS_VERDICT_CHECK",
        "SCALE_CRITICAL_SHOT_CLASS_VERDICT_CHECK",
        "PERSPECTIVE_CALCULATION_VERDICT_CHECK",
        "SCREEN_OCCUPANCY_WORLD_SCALE_VERDICT_CHECK",
        "VISUAL_GUIDE_COMPOSITE_VERDICT_CHECK",
        "USER_VISUAL_GUIDE_APPROVAL_VERDICT_CHECK",
        "SCALE_PROXY_TRACE_VERDICT_CHECK",
        "PRE_COMPOSITE_EVIDENCE_STACK_VERDICT_CHECK",
        "SCALE_COMPOSITE_HARD_LOCK_VERDICT_CHECK",
        "CUT_PLANE_VISIBILITY_VERDICT_CHECK",
        "CUT_RESULT_UNKNOWN_FORM_VERDICT_CHECK",
        "WEAPON_GRIP_MECHANICS_VERDICT_CHECK",
        "WRIST_FORCE_PATH_VERDICT_CHECK",
        "POST_IMAGE_FAILURE_KEY_ROUTING",
        "POST_IMAGE_REPAIR_ARTIFACT_PATH",
        "POST_IMAGE_REPAIR_COMPILER_STATUS",
        "POST_IMAGE_NEXT_DRAFT_PROMPT",
        "POST_IMAGE_SCALE_FAILURE_SHOT_CLASS_ESCALATION",
        "REGENERATION_GATE_STATUS",
        "OBJECT_ANATOMY_MIXING_CHECK",
        "OBJECT_DISTORTION_VERDICT_CHECK",
        "PROTECTED_CHAIN_TRACE_VERDICT",
        "GARMENT_ATTACHMENT_VERDICT_CHECK",
        "FACE_AND_LOWER_BODY_VERDICT_CHECK",
        "IRREVERSIBLE_STRUCTURE_CHECK",
        "HAND_READABILITY_CHECK",
        "FINGER_TOPOLOGY_VERDICT_CHECK",
        "FINAL_CORRECTION_LIST",
        "USER_COMMAND_COMPLIANCE_CHECK",
        "AESTHETIC_RECOVERY_CHECK",
        "STRUCTURE_LOCK_SUMMARY",
        "AESTHETIC_RENDER_BRIEF",
        "NEGATIVE_PROMPT_LIMITED",
        "FINAL_IMAGE_PROMPT_COMPILED",
        "FINAL_PROMPT_COMPILER_STATUS",
        "AESTHETIC_RECOVERY_GATE_STATUS",
        "FINAL_GATE_STATUS",
    ],
}

THEORY_STEP_FIELDS = {
    "## Step 1 Intent": "STEP_1_FILES_READ",
    "## Step 2 Composition": "STEP_2_FILES_READ",
    "## Step 2.1 Perspective Rig": "STEP_2_FILES_READ",
    "## Step 2.2 Object Inventory from Perspective": "STEP_2_FILES_READ",
    "## Step 2.3 Anatomy Structure Gate": "STEP_2_FILES_READ",
    "## Step 2.4 Object Knowledge Query Plan": "STEP_2_FILES_READ",
    "## Step 2.5 Object Research Handoff": "STEP_2_FILES_READ",
    "## Step 2.6 Object Relationship Check": "STEP_2_FILES_READ",
    "## Step 2.7 Anatomy-on-Object Relationship Check": "STEP_2_FILES_READ",
    "## Step 2.8 3D Blockout / Modeling Contract": "STEP_2_FILES_READ",
    "## Step 2.9 Image Translation Lock": "STEP_2_FILES_READ",
    "## Step 3 Value": "STEP_3_FILES_READ",
    "## Step 4 Face": "STEP_4_FILES_READ",
    "## Step 5 Line & Shape": "STEP_5_FILES_READ",
    "## Step 6 Color & Accent": "STEP_6_FILES_READ",
    "## Step 7 Texture": "STEP_7_FILES_READ",
    "## Step 8 Final Check": "STEP_8_FILES_READ",
}

STATUS_FIELDS = {
    "GATE_STATUS": {"pass", "needs_revision", "not_applicable"},
    "ROUTE_GATE_STATUS": {"pass", "needs_revision"},
    "MERGE_GATE_STATUS": {"pass", "needs_revision"},
    "SCENE_CONTRACT_GATE_STATUS": {"pass", "needs_revision"},
    "FINAL_GATE_STATUS": {"pass", "needs_revision"},
    "BLOCKOUT_REVIEW_STATUS": {"pass", "needs_revision", "not_applicable"},
    "POST_IMAGE_REPAIR_COMPILER_STATUS": {"pass", "needs_revision", "not_applicable"},
    "REGENERATION_GATE_STATUS": {"pass", "blocked", "not_applicable"},
    "FINAL_PROMPT_COMPILER_STATUS": {"pass", "needs_revision", "not_applicable"},
    "AESTHETIC_RECOVERY_GATE_STATUS": {"pass", "needs_revision", "not_applicable"},
    "VISUAL_GUIDE_COMPOSITE_REVIEW": {"pass", "needs_revision", "not_applicable"},
    "USER_VISUAL_GUIDE_FEEDBACK_APPLIED": {"pass", "needs_revision", "not_applicable"},
}

BOOLEAN_FIELDS = {
    "SOURCE_IMAGE_UPGRADE": {"yes", "no"},
    "EXISTING_IMAGE_INPUT": {"yes", "no"},
    "PROMPT_ONLY_GENERATION": {"yes", "no"},
    "OBJECT_RESEARCH_REQUIRED": {"yes", "no"},
    "SCALE_CRITICAL_MODE": {"yes", "no"},
    "IMAGE_GEN_READY": {"yes", "no"},
    "PRE_IMAGE_HANDOFF_READY": {"yes", "no"},
    "POST_IMAGE_VERDICT_REQUIRED": {"yes", "no"},
    "ANATOMY_GATE_REQUIRED": {"yes", "no"},
    "HANDOFF_REQUIRED": {"yes", "no"},
    "BLENDER_BLOCKOUT_REQUIRED": {"yes", "no"},
    "VISUAL_GUIDE_COMPOSITE_REQUIRED": {"yes", "no"},
    "SCALE_COMPOSITE_HARD_LOCK": {"yes", "no"},
    "USER_VISUAL_GUIDE_CHECKPOINT_REQUIRED": {"yes", "no"},
    "SCALE_PROXY_DUMMY_REQUIRED": {"yes", "no"},
}

ENUM_FIELDS = {
    "INPUT_ROUTE": {"image_development", "prompt_only"},
    "ACTIVE_INTAKE_BRANCH": {"step_0a_existing_image_development", "step_0b_prompt_only"},
    "SOURCE_IMAGE_ACTUAL_CONDITIONING": {"yes", "no", "not_applicable"},
    "IMAGE_DEVELOPMENT_ALLOWED": {"yes", "blocked", "prompt_only_fallback", "not_applicable"},
    "POST_IMAGE_ACCEPTED": {"yes", "no", "not_applicable"},
    "USER_CAMERA_CLASS_LOCK_LEVEL": {"soft", "hard", "adaptive", "not_applicable"},
    "CAMERA_CLASS_CONFLICT_STATUS": {"none", "conflict", "resolved", "not_applicable"},
    "CLOSEUP_BLOCKED_UNTIL_SCALE_PASS": {"yes", "no", "not_applicable"},
    "PERSPECTIVE_SCALE_TRANSFER_MODE": {
        "projected_measurement",
        "depth_plane_projection",
        "blockout_projection",
        "not_applicable",
    },
    "SCREEN_OCCUPANCY_IS_DERIVED": {"yes", "no", "not_applicable"},
    "SCREEN_OCCUPANCY_MUST_NOT_OVERRIDE_WORLD_SCALE": {"yes", "no", "not_applicable"},
    "USER_VISUAL_GUIDE_APPROVAL_STATUS": {"pending", "approved", "needs_revision", "not_applicable"},
    "IMAGE_GEN_STRUCTURE_CONDITIONING_MODE": {
        "openai_high_fidelity_image_inputs",
        "external_controlnet",
        "direct_text_prompt",
        "blocked_text_only",
        "not_applicable",
    },
    "IMAGE_GEN_STRUCTURE_CONDITIONING_STRENGTH": {
        "strict_structure",
        "medium_structure",
        "loose_reference",
        "not_applicable",
    },
}

IMAGE_DEVELOPMENT_BRANCH_FIELDS = [
    "SOURCE_IMAGE_REFERENCE",
    "PREVIOUS_IMAGE_VISUAL_VERDICT_SUMMARY",
    "SOURCE_IMAGE_OBJECTS_PRESENT",
    "PRESERVE_OBJECTS",
    "CHANGE_OBJECTS",
    "REMOVE_OBJECTS",
    "FAILURE_CAUSE_MAP",
    "PREVIOUS_IMAGE_LESSONS",
    "ROUTE_A_OUTPUT_TO_STEP_1_2_2",
    "GATE_STATUS",
]

PROMPT_ONLY_BRANCH_FIELDS = [
    "PROMPT_OBJECT_CANDIDATES",
    "PROMPT_IMPLIED_ENVIRONMENT",
    "PROMPT_IMPLIED_ANATOMY",
    "PROMPT_AMBIGUITY_ASSUMPTIONS",
    "ROUTE_B_OUTPUT_TO_STEP_1_2_2",
    "GATE_STATUS",
]

APPLY_STATUS_VALUES = {"applied", "not_applicable", "needs_revision"}

BLENDER_STEP_FIELDS = {
    "BLENDER_BLOCKOUT_REQUIRED",
    "BLENDER_SCENE_PATH",
    "BLENDER_RENDER_SCRIPT_PATH",
    "BLENDER_PASS_OUTPUTS",
    "BLENDER_BLOCKOUT_REVIEW",
    "BLENDER_GUIDE_STRENGTH",
    "BLOCKOUT_CORE_OBJECT_VISIBILITY",
    "BLOCKOUT_TARGET_CONTACT_VISIBILITY",
    "BLOCKOUT_CAMERA_OCCLUSION_CHECK",
    "BLENDER_VISIBILITY_REPORT_PATH",
    "BLENDER_VISIBILITY_REPORT_REVIEW",
    "STRUCTURAL_INVARIANTS_TO_PRESERVE",
    "PAINTERLY_FREEDOMS_ALLOWED",
    "STRUCTURE_OVER_PAINTERLY_LOCK",
    "NO_STRUCTURAL_SACRIFICE_RULE",
    "CONTROLNET_CONDITIONING_PLAN",
    "BLOCKOUT_REVIEW_STATUS",
}

RENDER_BOUND_DELIVERABLE_KEYWORDS = [
    "image generation",
    "image render",
    "final render",
    "render",
    "generated image",
    "final illustration",
    "spec + image",
    "이미지",
    "렌더",
    "그림",
    "일러스트",
    "생성",
]

OBJECT_RESEARCH_KEYWORDS = [
    "alley",
    "streetlamp",
    "street",
    "city",
    "hong kong",
    "neon",
    "sign",
    "signage",
    "rain",
    "puddle",
    "katana",
    "sword",
    "weapon",
    "boot",
    "chain",
    "pipe",
    "cable",
    "building",
    "facade",
    "perspective",
    "vanishing",
    "horizon",
    "scale",
    "tram",
    "train",
    "rail",
    "track",
    "glyph",
    "text",
    "typography",
    "structure",
    "architecture",
    "vehicle",
    "motorcycle",
    "car",
    "window",
    "door",
    "exit",
    "emergency",
    "stair",
    "stairs",
    "bridge",
    "gate",
    "prop",
    "furniture",
    "lab",
    "laboratory",
    "machinery",
    "machine",
    "mech",
    "robot",
    "scaffold",
    "helmet",
    "gun",
    "rifle",
    "blade",
    "hand",
    "hands",
    "finger",
    "fingers",
    "grip",
    "gesture",
    "thumb",
    "palm",
    "골목",
    "거리",
    "도시",
    "홍콩",
    "네온",
    "비",
    "카타나",
    "검",
    "무기",
    "부츠",
    "체인",
    "배관",
    "배선",
    "차량",
    "건물",
    "구조물",
    "건축",
    "창문",
    "문",
    "출구",
    "비상구",
    "계단",
    "기계",
    "소품",
    "간판",
    "투시",
    "소실점",
    "수평선",
    "스케일",
    "전차",
    "철로",
    "레일",
    "글자",
    "손",
    "손가락",
    "파지",
    "제스처",
    "엄지",
]

HAND_KEYWORDS = [
    "hand",
    "hands",
    "finger",
    "fingers",
    "thumb",
    "palm",
    "grip",
    "gesture",
    "hold",
    "holding",
    "pointing",
    "touch",
    "resting hand",
    "손",
    "손들",
    "손가락",
    "엄지",
    "손바닥",
    "파지",
    "제스처",
    "쥐",
    "잡",
    "짚",
]

HAND_PROP_INTERACTION_KEYWORDS = [
    "cigarette",
    "pipe",
    "sword",
    "katana",
    "gun",
    "rifle",
    "blade",
    "cup",
    "glass",
    "phone",
    "rail",
    "guardrail",
    "담배",
    "파이프",
    "검",
    "카타나",
    "총",
    "칼",
    "잔",
    "폰",
    "난간",
    "가드레일",
]

HAND_ACTION_HINTS = [
    "hold",
    "holding",
    "grip",
    "gripping",
    "point",
    "pointing",
    "smoke",
    "smoking",
    "rest",
    "resting",
    "touch",
    "touching",
    "쥐",
    "잡",
    "파지",
    "가리키",
    "담배",
    "기대",
    "짚",
]

GROUNDED_POSE_KEYWORDS = [
    "full-body",
    "full body",
    "standing",
    "stand",
    "pose",
    "runway",
    "weight on",
    "support leg",
    "contrapposto",
    "balanced",
    "전신",
    "서 있는",
    "서서",
    "포즈",
    "체중",
]

EXAGGERATED_PROPORTION_KEYWORDS = [
    "stylized",
    "exaggerated",
    "very slim",
    "extremely slim",
    "tiny waist",
    "hourglass",
    "k-cup",
    "k cup",
    "very full bust",
    "과장",
    "매우 마른",
    "잘록한",
    "볼륨",
]

ANATOMY_GATE_KEYWORDS = [
    "body",
    "torso",
    "ribcage",
    "pelvis",
    "waist",
    "hip",
    "hips",
    "leg",
    "legs",
    "arm",
    "arms",
    "shoulder",
    "shoulders",
    "thigh",
    "thigh-up",
    "thigh up",
    "full-body",
    "full body",
    "half-body",
    "half body",
    "three-quarter body",
    "3/4 body",
    "figure",
    "character",
    "girl",
    "boy",
    "woman",
    "man",
    "female",
    "male",
    "school uniform",
    "pose",
    "seated",
    "sitting",
    "leaning",
    "jump",
    "jumping",
    "lunge",
    "lunging",
    "twist",
    "twisting",
    "foreshortened arm",
    "foreshortened hand",
    "인물",
    "캐릭터",
    "전신",
    "반신",
    "허벅지",
    "몸통",
    "흉곽",
    "골반",
    "허리",
    "엉덩이",
    "다리",
    "팔",
    "어깨",
    "손",
    "손가락",
    "소녀",
    "소년",
    "여성",
    "남성",
    "미녀",
    "미소녀",
    "미남",
    "교복",
    "앉",
    "기대",
    "점프",
    "런지",
    "비틀",
]

OBJECT_DENSITY_EDGE_KEYWORDS = [
    "many objects",
    "dense",
    "density",
    "crowd",
    "crowds",
    "particles",
    "blood",
    "smoke",
    "fire",
    "water",
    "shards",
    "petals",
    "debris",
    "city",
    "buildings",
    "architecture",
    "vehicle",
    "vehicles",
    "tram",
    "train",
    "rail",
    "machinery",
    "weapon",
    "weapons",
    "creature",
    "dragon",
    "signage",
    "background detail",
    "오브젝트",
    "구성요소",
    "밀도",
    "복잡",
    "군중",
    "입자",
    "피",
    "혈흔",
    "연기",
    "불",
    "파편",
    "꽃잎",
    "도시",
    "건물",
    "건축",
    "차량",
    "전차",
    "기차",
    "레일",
    "기계",
    "무기",
    "크리처",
    "드래곤",
    "간판",
    "배경",
]

HUMAN_PRIORITY_LOCK_KEYWORDS = [
    "human anatomy",
    "anatomy",
    "body",
    "proportion",
    "limb",
    "hands",
    "fingers",
    "feet",
    "grip",
    "contact",
    "인체",
    "해부",
    "몸",
    "비례",
    "팔다리",
    "손",
    "손가락",
    "발",
    "파지",
    "접촉",
]

DENSITY_REDUCTION_KEYWORDS = [
    "reduce",
    "suppress",
    "simplify",
    "before",
    "density",
    "clutter",
    "non-human",
    "background",
    "particles",
    "effects",
    "blood",
    "smoke",
    "costume noise",
    "signage",
    "texture",
    "줄",
    "감소",
    "억제",
    "단순",
    "먼저",
    "밀도",
    "클러터",
    "비인체",
    "배경",
    "입자",
    "효과",
    "피",
    "혈흔",
    "연기",
    "의상",
    "간판",
    "텍스처",
]

IRREVERSIBLE_STRUCTURE_KEYWORDS = [
    "irreversible",
    "mandatory",
    "non-negotiable",
    "registered",
    "structural instance",
    "separate instance",
    "preserve",
    "survive",
    "cannot sacrifice",
    "must not omit",
    "must not delete",
    "must not merge",
    "must not fuse",
    "must not absorb",
    "must not resize",
    "must not reinterpret",
    "no structural sacrifice",
    "비가역",
    "필수",
    "구조 인스턴스",
    "분리",
    "보존",
    "유지",
    "희생",
    "삭제",
    "누락",
    "병합",
    "융합",
    "흡수",
    "축소",
    "확대",
    "재해석",
]

STRUCTURE_OVER_STYLE_KEYWORDS = [
    "structure over",
    "before style",
    "before painterly",
    "style only",
    "painterly may not",
    "override painterly",
    "line/color/texture",
    "detail only",
    "구조 우선",
    "스타일보다",
    "회화적",
    "선",
    "색",
    "질감",
    "디테일",
]

OBJECT_DISTORTION_KEYWORDS = [
    "distortion",
    "no distortion",
    "warp",
    "warped",
    "bend",
    "bent",
    "melt",
    "melted",
    "rubbery",
    "noodle",
    "stretch",
    "squeezed",
    "resize",
    "fuse",
    "absorb",
    "texture replacement",
    "functional geometry",
    "axis",
    "axis continuity",
    "silhouette",
    "material boundary",
    "왜곡",
    "금지",
    "휘",
    "휘어",
    "녹",
    "고무",
    "늘어",
    "찌그러",
    "크기",
    "융합",
    "흡수",
    "텍스처 대체",
    "축",
    "실루엣",
    "기능",
]

HERO_OBJECT_SCALE_KEYWORDS = [
    "hero",
    "protagonist",
    "main character",
    "object scale",
    "scale parity",
    "scale witness",
    "passenger",
    "visible human",
    "door",
    "window",
    "vehicle",
    "prop",
    "architecture",
    "creature",
    "module",
    "depth plane",
    "perspective transfer",
    "주인공",
    "오브젝트",
    "스케일",
    "크기",
    "승객",
    "사람",
    "인간",
    "문",
    "창문",
    "차량",
    "소품",
    "건축",
    "크리처",
    "투시",
]

HUMANOID_OBJECT_KEYWORDS = [
    "human",
    "humans",
    "person",
    "people",
    "passenger",
    "passengers",
    "crowd",
    "driver",
    "humanoid",
    "humanoid monster",
    "android",
    "demon",
    "werewolf",
    "beast-man",
    "background human",
    "visible human",
    "인간",
    "사람",
    "인물",
    "승객",
    "군중",
    "운전자",
    "인간형",
    "인간형 몬스터",
    "몬스터",
    "괴물",
    "안드로이드",
    "마족",
    "늑대인간",
]

HUMANOID_SCALE_PARITY_KEYWORDS = [
    "protagonist",
    "hero",
    "main character",
    "humanoid",
    "human",
    "passenger",
    "crowd",
    "background human",
    "anatomy",
    "depth plane",
    "perspective",
    "scale parity",
    "same scale",
    "head",
    "body",
    "comparison",
    "not texture",
    "miniature",
    "doll",
    "giant",
    "no exaggeration",
    "주인공",
    "인간형",
    "인간",
    "사람",
    "승객",
    "군중",
    "배경 인물",
    "아나토미",
    "투시",
    "깊이",
    "동일 스케일",
    "스케일 비교",
    "머리",
    "몸",
    "텍스처",
    "미니어처",
    "인형",
    "거인",
    "과장 금지",
]

PERSPECTIVE_ONLY_SCALE_KEYWORDS = [
    "perspective",
    "depth",
    "depth plane",
    "lens",
    "actual size",
    "real size",
    "same scale",
    "scale parity",
    "no drama",
    "no style",
    "no focal",
    "no exaggeration",
    "no shrink",
    "no enlarge",
    "투시",
    "깊이",
    "렌즈",
    "실제 크기",
    "동일 스케일",
    "과장 금지",
    "축소 금지",
    "확대 금지",
    "드라마",
    "스타일",
    "초점",
]

COMMAND_COMPLIANCE_KEYWORDS = [
    "command",
    "instruction",
    "user",
    "checklist",
    "each",
    "every",
    "audit",
    "satisfied",
    "partial",
    "failed",
    "not applicable",
    "rerender",
    "명령",
    "지시",
    "사용자",
    "체크",
    "점검",
    "각각",
    "모든",
    "충족",
    "부분",
    "실패",
    "해당없음",
    "재생성",
]

PIVA_TRANSFER_KEYWORDS = [
    "transfer", "mapped", "map", "step", "prompt", "verify", "audit", "lock", "verdict",
    "research", "object", "scale", "style", "이전", "전달", "매핑", "단계", "프롬프트", "검증", "감사", "락", "판정", "조사", "오브젝트", "스케일", "스타일",
]

PIVA_RERENDER_KEYWORDS = [
    "fail", "failed", "failure", "rerender", "revise", "trigger", "blocked", "scale", "distortion",
    "실패", "재생성", "수정", "트리거", "차단", "스케일", "왜곡",
]

FINAL_PROMPT_SCHEMA_JARGON_RE = re.compile(r"\b[A-Z][A-Z0-9]+(?:_[A-Z0-9]+)+\b")

FINAL_PROMPT_BANNED_JARGON = [
    "tier 0",
    "tier 1",
    "tier 2",
    "tier 3",
    "step 0",
    "step 2",
    "step 8",
    "gate status",
    "verdict",
    "field",
    "schema",
    "visual guide package",
    "prompt lock",
    "scale_visual",
    "cut_plane",
    "grip_mechanics",
    "object_registry",
    "scene_contract",
    "non_negotiable",
    "validator",
    "검증 필드",
    "게이트",
    "판정",
    "스키마",
]

AESTHETIC_RECOVERY_KEYWORDS = [
    "composition",
    "pressure",
    "frame",
    "background",
    "value",
    "lighting",
    "light",
    "shadow",
    "line",
    "texture",
    "palette",
    "accent",
    "focal",
    "focus",
    "anti-generic",
    "generic",
    "mass",
    "구도",
    "압력",
    "프레임",
    "배경",
    "명암",
    "빛",
    "그림자",
    "선",
    "질감",
    "팔레트",
    "악센트",
    "초점",
    "미감",
    "제네릭",
    "덩어리",
]

FINAL_PROMPT_NATURAL_LANGUAGE_KEYWORDS = [
    "face",
    "eyes",
    "gaze",
    "composition",
    "background",
    "lighting",
    "shadow",
    "line",
    "texture",
    "palette",
    "accent",
    "얼굴",
    "눈",
    "시선",
    "구도",
    "배경",
    "조명",
    "그림자",
    "선",
    "질감",
    "색",
]

SCALE_FUNCTION_KEYWORDS = [
    "adult",
    "human",
    "door",
    "exit",
    "emergency",
    "tram",
    "vehicle",
    "passenger",
    "window",
    "parapet",
    "head",
    "body",
    "fit",
    "usable",
    "functional",
    "scale ladder",
    "ratio",
    "사람",
    "인간",
    "성인",
    "문",
    "출구",
    "비상구",
    "전차",
    "차량",
    "승객",
    "창문",
    "파라펫",
    "머리",
    "몸",
    "스케일",
    "비율",
    "크기",
]

ALLOWED_AGE_BANDS = {
    "초등학생",
    "중학생",
    "고등학생",
    "20대초반",
    "20대후반",
    "30대초반",
    "30대후반",
    "40대초반",
    "40대후반",
    "50대초반",
    "50대후반",
}

ANATOMY_CARD_FIELDS = [
    "BODY_ANATOMY_BASE_CARD",
    "SEX_OVERLAY_CARD",
    "HAND_ANATOMY_SUBMODULE_CARD",
]

DIRECTION_KEYWORDS = [
    "left",
    "right",
    "front",
    "back",
    "upper",
    "lower",
    "top",
    "side",
    "rim",
    "45-degree",
    "45 degree",
    "좌",
    "우",
    "정면",
    "후면",
    "상부",
    "하부",
    "측광",
    "역광",
]

FACE_FOCUS_KEYWORDS = [
    "face",
    "eye",
    "eyes",
    "iris",
    "brow",
    "gaze",
    "얼굴",
    "눈",
    "시선",
]

GARMENT_FOCUS_KEYWORDS = [
    "garment",
    "shirt",
    "bust",
    "torso",
    "chest",
    "neckline",
    "shorts",
    "hip",
    "garment tension",
    "옷",
    "상의",
    "가슴",
    "넥라인",
    "하의",
]

PERSPECTIVE_SCENE_KEYWORDS = [
    "perspective",
    "vanishing",
    "horizon",
    "depth",
    "rail",
    "track",
    "tram",
    "train",
    "street",
    "city",
    "building",
    "corridor",
    "architecture",
    "투시",
    "소실점",
    "수평선",
    "깊이",
    "레일",
    "철로",
    "전차",
    "기차",
    "거리",
    "도시",
    "건물",
    "건축",
]

GEOMETRIC_BLOCKOUT_KEYWORDS = [
    "full-body",
    "full body",
    "half-body",
    "thigh-up",
    "humanoid",
    "creature",
    "werewolf",
    "rooftop",
    "roof",
    "street",
    "city",
    "building",
    "architecture",
    "facade",
    "window",
    "parapet",
    "door",
    "exit",
    "emergency",
    "railing",
    "vehicle",
    "tram",
    "train",
    "weapon",
    "sword",
    "katana",
    "perspective",
    "scale",
    "전신",
    "반신",
    "허벅지",
    "인간형",
    "크리처",
    "늑대인간",
    "옥상",
    "지붕",
    "거리",
    "도시",
    "건물",
    "건축",
    "파사드",
    "창문",
    "파라펫",
    "문",
    "출구",
    "비상구",
    "난간",
    "차량",
    "전차",
    "기차",
    "무기",
    "검",
    "카타나",
    "투시",
    "스케일",
]

VEHICLE_SCALE_KEYWORDS = [
    "tram",
    "train",
    "vehicle",
    "car",
    "railcar",
    "bus",
    "전차",
    "기차",
    "차량",
]

PASSENGER_CAPACITY_KEYWORDS = [
    "passenger",
    "passengers",
    "capacity",
    "cabin",
    "car length",
    "door bay",
    "window bay",
    "many adult",
    "80",
    "100",
    "120",
    "승객",
    "수용",
    "객실",
    "열차 한 칸",
    "한 칸",
    "100명",
    "문",
    "창문",
]


TIERED_PROMPT_KEYWORDS = [
    "tier",
    "tier 0",
    "tier 1",
    "tier 2",
    "macro",
    "capacity",
    "face",
    "limb",
    "contact",
    "reduce",
    "티어",
    "매크로",
    "수용",
    "얼굴",
    "팔다리",
    "접촉",
    "축소",
]

FACE_STRUCTURE_PROMPT_KEYWORDS = [
    "face plane",
    "jaw",
    "chin",
    "cheek",
    "eye spacing",
    "adult",
    "not flattened",
    "얼굴면",
    "턱",
    "광대",
    "눈 간격",
    "성인",
    "납작",
]

LOWER_BODY_PROMPT_KEYWORDS = [
    "thigh",
    "knee",
    "shin",
    "ankle",
    "boot",
    "leg silhouette",
    "pants",
    "lower body",
    "허벅지",
    "무릎",
    "정강이",
    "발목",
    "부츠",
    "다리",
    "바지",
]

CONTAINER_OBJECT_KEYWORDS = [
    "container",
    "occupancy",
    "tram",
    "train",
    "bus",
    "railcar",
    "vehicle",
    "car",
    "elevator",
    "room",
    "corridor",
    "cabin",
    "interior",
    "compartment",
    "passenger",
    "building",
    "office",
    "house",
    "apartment",
    "tower",
    "전차",
    "기차",
    "버스",
    "차량",
    "엘리베이터",
    "방",
    "복도",
    "객실",
    "실내",
    "칸",
    "승객",
    "건물",
    "빌딩",
    "아파트",
    "타워",
]

CONTAINER_CAPACITY_RESEARCH_KEYWORDS = PASSENGER_CAPACITY_KEYWORDS + [
    "seat",
    "seats",
    "standing",
    "occupancy",
    "interior volume",
    "internal volume",
    "module",
    "modules",
    "aisle",
    "entry",
    "exit",
    "adult",
    "좌석",
    "입석",
    "정원",
    "수용량",
    "내부",
    "체적",
    "모듈",
    "통로",
    "출입",
    "성인",
]

ENTRY_FIT_KEYWORDS = [
    "entry",
    "door",
    "aisle",
    "clearance",
    "fit",
    "height",
    "width",
    "pass",
    "입구",
    "문",
    "통로",
    "여유",
    "높이",
    "폭",
]

XYZ_VOLUME_KEYWORDS = [
    "x",
    "y",
    "z",
    "width",
    "height",
    "length",
    "depth",
    "volume",
    "internal volume",
    "usable cabin",
    "interior",
    "폭",
    "높이",
    "길이",
    "깊이",
    "체적",
    "내부",
]

CAPACITY_CLASS_KEYWORDS = [
    "capacity class",
    "occupancy class",
    "expected occupancy",
    "passenger",
    "passengers",
    "100_plus",
    "100+",
    "many adult",
    "mass transit",
    "수용",
    "정원",
    "승객",
    "100명",
    "대중교통",
]

MODULE_REPETITION_KEYWORDS = [
    "module",
    "modules",
    "repetition",
    "repeated",
    "door bay",
    "window bay",
    "seat",
    "aisle",
    "floor module",
    "bay",
    "모듈",
    "반복",
    "문",
    "창문",
    "좌석",
    "통로",
]

COMPOSITE_SCALE_VERDICT_KEYWORDS = [
    "entry",
    "xyz",
    "volume",
    "capacity",
    "occupant",
    "module",
    "composite",
    "pass",
    "입구",
    "체적",
    "수용",
    "승객",
    "모듈",
    "종합",
]

SCALE_CRITICAL_CONTAINER_KEYWORDS = CONTAINER_OBJECT_KEYWORDS + [
    "human-enterable",
    "enterable",
    "occupant anchor",
    "occupant anatomy",
    "usable cabin",
    "container scale",
    "human enterable",
    "사람이 들어",
    "탑승",
    "내부 인체",
]

SCALE_CRITICAL_RATIO_KEYWORDS = [
    "ratio",
    "threshold",
    "percent",
    "percentage",
    "fraction",
    "height",
    "width",
    "length",
    "screen occupancy",
    "door",
    "entry",
    "occupant",
    "passenger",
    "container",
    "비율",
    "기준",
    "퍼센트",
    "%",
    "높이",
    "폭",
    "너비",
    "길이",
    "화면",
    "문",
    "출입",
    "승객",
    "탑승자",
]

CAMERA_CLASS_SCALE_PROVING_KEYWORDS = [
    "extreme wide",
    "extreme-wide",
    "wide",
    "wide shot",
    "scale shot",
    "long shot",
    "establishing",
    "full container",
    "full vehicle",
    "full tram",
    "multi-car",
    "multi car",
    "long passenger",
    "distant camera",
    "small figure",
    "작은 인물",
    "와이드",
    "롱샷",
    "익스트림 와이드",
    "전체 전차",
    "차량 전체",
    "전경",
    "스케일 샷",
]

CAMERA_CLASS_CLOSEUP_RISK_KEYWORDS = [
    "close-up",
    "close up",
    "portrait",
    "medium shot",
    "medium action",
    "hero shot",
    "low angle hero",
    "face-first",
    "face first",
    "upper body",
    "bust",
    "클로즈업",
    "인물 클로즈",
    "초상",
    "반신",
    "상반신",
    "히어로 샷",
    "얼굴 우선",
]

SCALE_WITNESS_VISIBILITY_KEYWORDS = (
    CAMERA_CLASS_SCALE_PROVING_KEYWORDS
    + PASSENGER_CAPACITY_KEYWORDS
    + MODULE_REPETITION_KEYWORDS
    + [
        "door",
        "doors",
        "window",
        "windows",
        "roof rail",
        "adult-height",
        "one adult",
        "5%",
        "under",
        "less than",
        "visible length",
        "문",
        "창문",
        "승객",
        "성인",
        "지붕 난간",
        "5%",
        "이하",
        "전체 길이",
    ]
)

FACE_FOCAL_DEMOTION_KEYWORDS = [
    "small accent",
    "tiny accent",
    "bright accent",
    "not close-up",
    "no close-up",
    "not portrait",
    "not a portrait",
    "face demoted",
    "eyes are small",
    "small bright eyes",
    "작은 악센트",
    "작은 초점",
    "클로즈업 아님",
    "초상 아님",
    "얼굴 축소",
    "눈은 작은",
]

PERSPECTIVE_CALCULATION_KEYWORDS = [
    "projected",
    "projection",
    "project",
    "perspective",
    "perspective grid",
    "vanishing",
    "horizon",
    "footpoint",
    "foot point",
    "support plane",
    "depth plane",
    "baseline",
    "measurement",
    "ratio",
    "same plane",
    "same depth",
    "투시",
    "투영",
    "소실점",
    "수평선",
    "발 위치",
    "지지 평면",
    "깊이 평면",
    "기준선",
    "기준 길이",
    "같은 평면",
    "같은 깊이",
]

PERSPECTIVE_BLOCKOUT_GUIDE_KEYWORDS = [
    "blockout",
    "blender",
    "guide",
    "visual guide",
    "overlay",
    "mask",
    "lineart",
    "depth",
    "clay",
    "render",
    "camera",
    "블록아웃",
    "블렌더",
    "가이드",
    "오버레이",
    "마스크",
    "라인아트",
    "깊이",
    "렌더",
]

SCREEN_OCCUPANCY_WORLD_SCALE_KEYWORDS = [
    "screen occupancy",
    "screen share",
    "image height",
    "frame share",
    "crop",
    "camera crop",
    "world scale",
    "actual size",
    "real size",
    "physical scale",
    "must not override",
    "not override",
    "derived",
    "does not resize",
    "화면 점유",
    "화면 비율",
    "프레임",
    "크롭",
    "세계 스케일",
    "실제 크기",
    "실제 스케일",
    "물리 스케일",
    "덮어쓰지",
    "파생",
    "리사이즈",
]

PERSPECTIVE_PROMPT_TRANSFER_KEYWORDS = [
    "projected baseline",
    "projected door",
    "projected height",
    "foot position",
    "footpoint",
    "same perspective plane",
    "same depth plane",
    "camera crop",
    "world scale",
    "actual size",
    "physical scale",
    "perspective projection",
    "투영된",
    "발 위치",
    "같은 투시",
    "같은 깊이",
    "카메라 크롭",
    "세계 스케일",
    "실제 크기",
]

SCALE_FAILURE_VERDICT_KEYS = {
    "container_scale_pass",
    "hero_fits_inside_object",
    "occupant_anchor_valid",
    "protagonist_to_occupant_ratio_pass",
    "scale_visual_guide_pass",
}

SCALE_CRITICAL_SPEC_NUMERIC_FIELDS = (
    ("global", None, "SCALE_CRITICAL_REASON", False),
    ("Step 2.1", "## Step 2.1 Perspective Rig", "SCALE_CRITICAL_RATIO_TARGETS", True),
    ("Step 2.1", "## Step 2.1 Perspective Rig", "MAX_PROTAGONIST_SCREEN_OCCUPANCY", True),
    ("Step 2.1", "## Step 2.1 Perspective Rig", "PROTAGONIST_ENTRY_FIT_TEST", True),
    ("Step 2.1", "## Step 2.1 Perspective Rig", "PROJECTED_BASELINE_TO_HERO_POSITION", True),
    ("Step 2.4", "## Step 2.4 Object Knowledge Query Plan", "CONTAINER_SCALE_RATIO_TABLE_NEEDED", False),
    ("Step 2.5", "## Step 2.5 Object Research Handoff", "CONTAINER_SCALE_RATIO_TABLE_APPLIED", True),
    ("Step 2.5", "## Step 2.5 Object Research Handoff", "PROTAGONIST_TO_ENTRY_RATIO_APPLIED", True),
    ("Step 2.5", "## Step 2.5 Object Research Handoff", "PROTAGONIST_TO_OCCUPANT_RATIO_APPLIED", True),
    ("Step 2.5", "## Step 2.5 Object Research Handoff", "PROTAGONIST_TO_CONTAINER_WIDTH_RATIO_APPLIED", True),
    ("Step 2.5", "## Step 2.5 Object Research Handoff", "PROTAGONIST_TO_CONTAINER_LENGTH_RATIO_APPLIED", True),
    ("Step 2.5", "## Step 2.5 Object Research Handoff", "SCALE_CRITICAL_FAIL_NUMBERS_APPLIED", True),
    ("Step 2.8", "## Step 2.8 3D Blockout / Modeling Contract", "STRICT_SCALE_BLOCKOUT_RATIO_REVIEW", True),
    ("Step 2.9", "## Step 2.9 Image Translation Lock", "SCALE_CRITICAL_PROMPT_OPENING", False),
    ("Step 8", "## Step 8 Final Check", "SCALE_VISUAL_GUIDE_VERDICT_CHECK", True),
)

SCALE_CRITICAL_OBJECT_RATIO_FIELDS = (
    "CONTAINER_SCALE_RATIO_TABLE",
    "PROTAGONIST_TO_ENTRY_RATIO",
    "PROTAGONIST_TO_OCCUPANT_RATIO",
    "PROTAGONIST_TO_CONTAINER_WIDTH_RATIO",
    "PROTAGONIST_TO_CONTAINER_LENGTH_RATIO",
    "MAX_PROTAGONIST_SCREEN_OCCUPANCY",
    "SCALE_CRITICAL_FAIL_NUMBERS",
)

BLOCKOUT_PROXY_KEYWORDS = [
    "placeholder",
    "proxy",
    "svg proxy",
    "svg-only",
    "manifest",
    "blender unavailable",
    "no_blender",
    "blocked_no_blender",
    "blocked_proxy_only",
    "pseudo",
    "unreviewed",
    "대체",
    "프록시",
    "블렌더 없음",
]

INTERNAL_HUMAN_ANCHOR_KEYWORDS = HUMANOID_SCALE_PARITY_KEYWORDS + [
    "occupant",
    "occupants",
    "driver",
    "conductor",
    "mannequin",
    "silhouette",
    "inside",
    "internal human",
    "human anatomy anchor",
    "door",
    "window",
    "seat",
    "standing",
    "seated",
    "head",
    "body",
    "same-depth",
    "same depth",
    "same plane",
    "adult",
    "탑승자",
    "운전사",
    "차장",
    "실루엣",
    "내부",
    "안에",
    "문",
    "창문",
    "좌석",
    "입석",
    "머리",
    "몸",
    "성인",
]

SOURCE_STRUCTURE_ONLY_KEYWORDS = [
    "structure only",
    "object reference only",
    "composition reference only",
    "object identity",
    "relationships",
    "pose/action",
    "perspective",
    "scale witness",
    "failure clues",
    "source evidence",
    "구조",
    "오브젝트",
    "객체",
    "관계",
    "포즈",
    "동작",
    "투시",
    "스케일",
    "근거",
]

SOURCE_STYLE_DESIGN_FORBID_KEYWORDS = [
    "do not copy source style",
    "do not preserve source style",
    "no source style",
    "forbid source style",
    "style/design firewall",
    "style design firewall",
    "source style/design",
    "style and design",
    "palette",
    "linework",
    "line style",
    "brush",
    "medium texture",
    "rendering style",
    "costume design",
    "creature design",
    "prop design",
    "decorative motifs",
    "explicit opt-in",
    "원본 스타일",
    "원본 디자인",
    "스타일/디자인",
    "가져오지",
    "복사하지",
    "금지",
    "방화벽",
    "색감",
    "팔레트",
    "선화",
    "선 스타일",
    "붓터치",
    "질감",
    "렌더링",
    "의상 디자인",
    "크리처 디자인",
    "소품 디자인",
    "모티프",
]

SCALE_EMPHASIS_OVERRIDE_KEYWORDS = PERSPECTIVE_ONLY_SCALE_KEYWORDS + [
    "ignore",
    "override",
    "do not enlarge",
    "do not shrink",
    "no enlargement",
    "no shrinking",
    "emphasis",
    "importance",
    "beauty",
    "action",
    "drama",
    "focal",
    "value",
    "framing",
    "무시",
    "무효",
    "크게",
    "작게",
    "강조",
    "중요",
    "미형",
    "액션",
    "드라마",
    "프레이밍",
]

HAND_FAILURE_CAUSE_KEYWORDS = [
    "attention",
    "prompt overload",
    "overload",
    "small",
    "screen size",
    "occlusion",
    "prop",
    "guard",
    "sleeve",
    "blood",
    "cloak",
    "dark texture",
    "absorb",
    "generic",
    "원인",
    "과부하",
    "작",
    "화면",
    "가림",
    "소품",
    "소매",
    "피",
    "망토",
    "흡수",
]


PROTECTED_CHAIN_KEYWORDS = [
    "chain", "landmark", "shoulder", "upper arm", "elbow", "forearm", "wrist", "hand",
    "hip", "thigh", "knee", "shin", "ankle", "boot", "finger", "thumb", "hilt", "blade",
    "체인", "랜드마크", "어깨", "상완", "팔꿈치", "전완", "손목", "손",
    "골반", "허벅지", "무릎", "정강이", "발목", "부츠", "손가락", "엄지", "검",
]

OCCLUDER_KEYWORDS = [
    "occluder", "occlusion", "cloak", "cape", "hood", "hair", "smoke", "blood", "glow",
    "effect", "background", "shadow", "black", "texture", "wing", "tail", "behind", "in front",
    "가림", "오클루전", "망토", "후드", "머리", "연기", "피", "이펙트", "배경", "그림자", "검은", "텍스처", "뒤", "앞",
]

SEPARATION_CUE_KEYWORDS = [
    "rim", "rim light", "negative space", "slit", "gap", "value", "hue", "color", "edge",
    "cast shadow", "contour", "notch", "mask", "outline", "highlight", "separate", "separation",
    "림", "림라이트", "네거티브", "틈", "간격", "명도", "색", "에지", "윤곽", "마스크", "하이라이트", "분리",
]

FINGER_TOPOLOGY_KEYWORDS = [
    "palm",
    "palm block",
    "thumb",
    "thumb wedge",
    "index",
    "middle",
    "ring",
    "little",
    "finger",
    "fingers",
    "knuckle",
    "start",
    "direction",
    "end",
    "overlap",
    "contact cue",
    "손바닥",
    "엄지",
    "검지",
    "중지",
    "약지",
    "새끼",
    "손가락",
    "마디",
    "시작점",
    "방향",
    "끝점",
    "겹침",
    "접촉",
]

FINGER_FAILURE_KEYWORDS = [
    "fail",
    "rerender",
    "revise",
    "fused",
    "claw",
    "lump",
    "melted",
    "mitten",
    "glove mass",
    "noise",
    "smear",
    "unreadable",
    "sacrifice",
    "실패",
    "재생성",
    "수정",
    "융합",
    "뭉개",
    "덩어리",
    "발톱",
    "장갑덩어리",
    "노이즈",
    "읽히지",
    "희생",
]

SWORD_KEYWORDS = ["sword", "blade", "katana", "검", "칼", "블레이드"]

ACTION_CONTACT_KEYWORDS = [
    "cut",
    "slice",
    "sever",
    "stab",
    "strike",
    "hit",
    "shoot",
    "grip",
    "hold",
    "bite",
    "contact",
    "attack",
    "벤",
    "베",
    "자르",
    "절단",
    "찌르",
    "치",
    "때리",
    "쏘",
    "잡",
    "접촉",
    "공격",
]

ACTION_CONTACT_CONTRACT_KEYWORDS = [
    "actor",
    "tool",
    "target",
    "forbidden",
    "contact",
    "landmark",
    "not",
    "행위자",
    "도구",
    "대상",
    "타겟",
    "금지",
    "접촉",
    "랜드마크",
    "아님",
]

VISUAL_GUIDE_EXECUTION_KEYWORDS = [
    "visual guide",
    "guide package",
    "annotated",
    "mask",
    "overlay",
    "blockout",
    "lineart",
    "depth",
    "normal",
    "controlnet",
    "img2img",
    "color pass",
    "visibility report",
    "시각",
    "가이드",
    "마스크",
    "오버레이",
    "블록아웃",
    "라인",
    "깊이",
]

VISUAL_GUIDE_COMPOSITE_KEYWORDS = [
    "visual guide composite",
    "composite",
    "clay",
    "lineart",
    "wire",
    "wireframe",
    "depth",
    "perspective line",
    "vanishing",
    "scale line",
    "baseline",
    "footpoint",
    "door height",
    "passenger height",
    "protagonist",
    "reference input",
    "image input",
    "conditioning",
    "참조 이미지",
    "복합",
    "합성",
    "투시선",
    "소실점",
    "기준선",
    "발 위치",
    "문 높이",
    "승객",
]

VISUAL_GUIDE_APPROVAL_KEYWORDS = [
    "approved",
    "approval",
    "user approved",
    "confirmed",
    "accepted",
    "final feedback",
    "피드백",
    "승인",
    "확인",
    "최종",
]

ASSUMED_VISUAL_GUIDE_APPROVAL_KEYWORDS = [
    "assumed",
    "workflow assumption",
    "auto-approved",
    "auto approved",
    "autonomous approval",
    "approved by workflow",
    "implicit approval",
    "no user review",
    "without user review",
    "가정",
    "추정",
    "자동 승인",
    "임의 승인",
    "사용자 검토 없이",
    "컨펌 없이",
]

SCALE_PROXY_DUMMY_KEYWORDS = [
    "scale proxy",
    "scale dummy",
    "proxy dummy",
    "dummy",
    "mannequin",
    "adult dummy",
    "adult mannequin",
    "adult scale",
    "door-side",
    "door side",
    "beside door",
    "height marker",
    "height line",
    "measurement trace",
    "projected",
    "projection",
    "baseline",
    "footpoint",
    "foot point",
    "same depth plane",
    "same perspective grid",
    "hide",
    "hidden",
    "delete",
    "remove",
    "removed",
    "overlay",
    "trace overlay",
    "더미",
    "마네킹",
    "성인",
    "문 옆",
    "키 기준",
    "키 선",
    "측정선",
    "측정",
    "투영",
    "기준선",
    "발 위치",
    "같은 깊이",
    "같은 투시",
    "숨김",
    "삭제",
    "제거",
    "오버레이",
]

PRE_COMPOSITE_EVIDENCE_STACK_KEYWORDS = [
    "pre-composite",
    "pre composite",
    "evidence stack",
    "full stack",
    "source image",
    "user commands",
    "immutable user commands",
    "object research",
    "perspective math",
    "perspective calculation",
    "scale proxy",
    "dummy projection",
    "blender blockout",
    "blender passes",
    "visibility report",
    "final prompt",
    "not sole authority",
    "not only composite",
    "not composite only",
    "one reference",
    "reference image",
    "conditioning input",
    "composite is one",
    "composite is not",
    "composite alone",
    "이전 단계",
    "근거 스택",
    "전체 스택",
    "원본 이미지",
    "사용자 명령",
    "오브젝트 리서치",
    "투시 계산",
    "더미 투영",
    "블록아웃",
    "가시성 리포트",
    "최종 프롬프트",
    "유일한 근거",
    "하나의 참고",
    "참조 중 하나",
    "단독",
]

SCALE_COMPOSITE_HARD_LOCK_KEYWORDS = [
    "scale follows composite",
    "follow composite scale",
    "composite scale wins",
    "approved composite scale",
    "binding scale",
    "hard scale lock",
    "hard-lock",
    "scale hard lock",
    "must follow",
    "exact scale",
    "scale markers",
    "height marker",
    "footpoint",
    "projected baseline",
    "door ratio",
    "passenger ratio",
    "container ratio",
    "screen occupancy",
    "no scale drift",
    "fail if scale drifts",
    "rerender if scale",
    "composite 기준",
    "composite 스케일",
    "컴포지트 기준",
    "컴포지트 스케일",
    "반드시 따라",
    "하드락",
    "강제",
    "스케일 마커",
    "키 마커",
    "발 위치",
    "투영 기준선",
    "문 비율",
    "승객 비율",
    "전차 비율",
    "컨테이너 비율",
    "화면 점유",
    "스케일 이탈",
    "리렌더",
]

IMAGE_GEN_STRUCTURE_CONDITIONING_KEYWORDS = [
    "image input",
    "image inputs",
    "reference image",
    "visual guide composite",
    "input fidelity",
    "high fidelity",
    "structure conditioning",
    "strict structure",
    "controlnet",
    "controlnet-like",
    "lineart",
    "depth",
    "clay",
    "source image",
    "not text-only",
    "not prompt-only",
    "attached image",
    "conditioning manifest",
    "이미지 입력",
    "참조 이미지",
    "구조 조건",
    "강한 구조",
    "고충실도",
    "컨트롤넷",
    "텍스트만 아님",
    "프롬프트만 아님",
]

TEXT_ONLY_REJECTION_KEYWORDS = [
    "text-only",
    "prompt alone",
    "prompt-only",
    "not enough",
    "insufficient",
    "must use visual",
    "must use mask",
    "must use blockout",
    "텍스트만",
    "프롬프트만",
    "부족",
    "불충분",
    "시각 가이드",
    "마스크",
    "블록아웃",
]

SCALE_VISUAL_GUIDE_KEYWORDS = VISUAL_GUIDE_EXECUTION_KEYWORDS + [
    "scale",
    "ratio",
    "occupant",
    "passenger",
    "door",
    "window",
    "tram",
    "container",
    "height",
    "length",
    "screen occupancy",
    "스케일",
    "비율",
    "승객",
    "탑승자",
    "문",
    "창문",
    "전차",
    "길이",
    "화면",
]

CUT_PLANE_VISIBILITY_KEYWORDS = [
    "cut plane",
    "cross-section",
    "neck",
    "head-side",
    "body-side",
    "near side",
    "far side",
    "visible",
    "not hidden",
    "not occluded",
    "protrusion",
    "unknown form",
    "stump",
    "edge silhouette",
    "절단면",
    "단면",
    "목",
    "머리쪽",
    "몸통쪽",
    "보임",
    "가리지",
    "숨기지",
    "돌출",
    "형체불명",
    "실루엣",
]
CUT_PLANE_VISUAL_GUIDE_KEYWORDS = VISUAL_GUIDE_EXECUTION_KEYWORDS + CUT_PLANE_VISIBILITY_KEYWORDS

GRIP_MECHANICS_KEYWORDS = [
    "functional grip",
    "grip",
    "hilt",
    "handle",
    "thumb opposition",
    "knuckle",
    "wrist",
    "forearm",
    "force path",
    "neutral wrist",
    "aligned wrist",
    "not bent",
    "not broken",
    "쥐",
    "손잡이",
    "그립",
    "엄지",
    "마디",
    "손목",
    "전완",
    "힘",
    "축",
    "꺾",
    "부러",
]
GRIP_MECHANICS_VISUAL_GUIDE_KEYWORDS = VISUAL_GUIDE_EXECUTION_KEYWORDS + GRIP_MECHANICS_KEYWORDS

GARMENT_ATTACHMENT_KEYWORDS = [
    "cloak",
    "cape",
    "hood",
    "mantle",
    "coat",
    "scarf",
    "veil",
    "망토",
    "케이프",
    "후드",
    "외투",
    "코트",
    "스카프",
    "베일",
]

GARMENT_ATTACHMENT_CONTRACT_KEYWORDS = [
    "attach",
    "attached",
    "attachment",
    "anchor",
    "shoulder",
    "collar",
    "neck",
    "back",
    "clasp",
    "origin",
    "부착",
    "고정",
    "앵커",
    "어깨",
    "목깃",
    "목",
    "등",
    "클래스프",
    "시작점",
]

TEXT_SIGN_KEYWORDS = [
    "sign",
    "signage",
    "text",
    "typography",
    "glyph",
    "label",
    "간판",
    "글자",
    "문자",
    "라벨",
]

UNKNOWN_UNRESOLVED_KEYWORDS = [
    "unresolved",
    "unknown unresolved",
    "allow random",
    "replace with random",
    "fake as",
    "fake pattern allowed",
    "unidentified noise",
    "대충",
    "알수없는 무늬로",
    "알 수 없는 무늬로",
    "랜덤 패턴으로",
]

ACTIONABLE_CORRECTION_KEYWORDS = [
    "increase",
    "reduce",
    "simplify",
    "darken",
    "lighten",
    "raise",
    "lower",
    "shift",
    "move",
    "widen",
    "narrow",
    "suppress",
    "deepen",
    "adjust",
    "revise",
    "tighten",
    "soften",
    "clarify",
    "rebalance",
    "boost",
    "trim",
    "clean up",
    "높",
    "낮",
    "줄",
    "늘",
    "단순",
    "어둡",
    "밝",
    "이동",
    "넓",
    "좁",
    "억제",
    "깊",
    "조정",
    "수정",
    "정리",
]

THEORY_PROOF_FIELDS = [
    "PARENT_SPEC_PATH",
    "WORKSPACE_STYLE_MODE",
    "STYLE_GUIDE_REQUIRED",
    "STEP_1_FILES_READ",
    "STEP_2_FILES_READ",
    "STEP_3_FILES_READ",
    "STEP_4_FILES_READ",
    "STEP_5_FILES_READ",
    "STEP_6_FILES_READ",
    "STEP_7_FILES_READ",
    "STEP_8_FILES_READ",
    "STYLE_GUIDE_FILES_READ",
    "READ_EVENTS",
    "PROOF_READY",
]

OBJECT_ARTIFACT_FIELDS = [
    "SOURCE_REQUEST",
    "PARENT_SPEC_PATH",
    "SCENE_INTENT",
    "SCENE_TYPE",
    "STYLE_MODE",
    "PRIORITY",
    "REQUIRED_OBJECTS",
    "RESEARCH_LANES",
    "MATCHED_CARDS_BY_LANE",
    "NEW_OR_UPDATED_CARDS",
    "MISSING_OR_WEAK_CARDS_BY_LANE",
    "OBJECT_CONTAINMENT_CLASSIFICATION",
    "HUMAN_ENTERABLE_OBJECTS",
    "NON_ENTERABLE_OBJECTS",
    "HUMAN_ENTERABLE_CAPACITY_RESEARCH",
    "INTERNAL_HUMAN_ANATOMY_ANCHORS",
    "OCCUPANT_BLEND_SCALE_PLAN",
    "PROTAGONIST_MAIN_FIGURE_SCALE_LOCK",
    "SCALE_EMPHASIS_OVERRIDE_POLICY",
    "HUMAN_ENTERABLE_COMPOSITE_SCALE_TABLE",
    "ENTRY_FIT_CHECK",
    "XYZ_VOLUME_CHECK",
    "CAPACITY_CLASS_CHECK",
    "OCCUPANT_ANCHOR_CHECK",
    "MODULE_REPETITION_CHECK",
    "HUMAN_ENTERABLE_SCALE_VERDICT",
    "UNKNOWN_OBJECT_TRIAGE_RESULT",
    "SCENE_RECIPE_UPDATES",
    "PER_OBJECT_DRAW_LOCKS",
    "SCALE_PERSPECTIVE_LOCKS",
    "CONTAINER_OBJECTS",
    "CONTAINER_CAPACITY_RESEARCH",
    "CONTAINER_DIMENSION_RESEARCH",
    "CONTAINER_HUMAN_SCALE_ANCHORS",
    "CONTAINER_PROMPT_LOCKS",
    "HAND_FAILURE_CAUSE_ANALYSIS",
    "HAND_TOPOLOGY_RESCUE_PLAN",
    "RELATIONSHIP_CHECK_NOTES",
    "GENERATION_PROMPT_LOCKS",
    "DO_NOT_FAKE_POLICY",
    "LOOKUP_SUMMARY",
    "RESEARCH_SUMMARY",
    "INVOCATION_LOG_PATH",
    "ARTIFACT_READY",
]

OBJECT_INVOCATION_FIELDS = [
    "PARENT_SPEC_PATH",
    "PARENT_OBJECT_ARTIFACT_PATH",
    "MODE",
    "SCENE_INTENT",
    "SCENE_TYPE",
    "STYLE_MODE",
    "PRIORITY",
    "REQUIRED_OBJECTS",
    "LOOKUP_FIRST",
    "LOCAL_LIBRARY_CHECK",
    "WEB_RESEARCH_USED",
    "OUTPUT_ARTIFACT_PATH",
    "RETURN_SHAPE",
    "INVOCATION_EVENTS",
    "INVOCATION_READY",
]

PLACEHOLDER_RE = re.compile(
    r"^\s*(?:<[^>]+>|todo|tbd|n/?a|yes/no|pass\|needs_revision|pass\|not_applicable\|needs_revision|applied\|not_applicable\|needs_revision)?\s*$",
    re.IGNORECASE,
)


@dataclass
class ValidationResult:
    path: Path
    text: str
    errors: list[str]
    warnings: list[str]
    sections: dict[str, str] | None = None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate an illustrate spec markdown file.")
    parser.add_argument("spec_path", type=Path, help="Path to the filled illustrate spec markdown file")
    parser.add_argument(
        "--strict-object-research",
        action="store_true",
        help="Treat likely-missing object research as an error instead of a warning.",
    )
    return parser.parse_args()


def normalize_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8").replace("\r\n", "\n")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8-sig").replace("\r\n", "\n")


def resolve_reference_path(reference: str, origin_path: Path) -> Path:
    candidate = Path(reference).expanduser()
    if candidate.is_absolute():
        return candidate

    cwd_candidate = Path.cwd() / candidate
    if cwd_candidate.exists():
        return cwd_candidate.resolve()

    origin_candidate = origin_path.parent / candidate
    if origin_candidate.exists():
        return origin_candidate.resolve()

    return cwd_candidate.resolve()


def section_blocks(text: str) -> dict[str, str]:
    sections: dict[str, str] = {}
    positions: list[tuple[str, int]] = []
    for heading in SECTION_ORDER:
        idx = text.find(heading)
        if idx == -1:
            continue
        positions.append((heading, idx))

    positions.sort(key=lambda item: item[1])
    for i, (heading, start) in enumerate(positions):
        end = positions[i + 1][1] if i + 1 < len(positions) else len(text)
        sections[heading] = text[start:end]
    return sections


def extract_field(block: str, field_name: str) -> str | None:
    pattern = re.compile(rf"(?m)^{re.escape(field_name)}:[ \t]*(.*)$")
    match = pattern.search(block)
    if not match:
        return None
    return match.group(1).strip()


def is_placeholder(value: str | None) -> bool:
    if value is None:
        return True
    return bool(PLACEHOLDER_RE.match(value))


def lower_value(value: str | None) -> str:
    return (value or "").strip().lower()


def extract_image_generation_prompt(block: str) -> str | None:
    """Return the prompt that should be sent to image generation.

    New specs must use FINAL_IMAGE_PROMPT_COMPILED so schema/validator prose
    stays inside the spec. IMAGE_GEN_HANDOFF_PROMPT remains a legacy fallback
    for older artifacts and post-image repair comparisons.
    """
    compiled = extract_field(block, "FINAL_IMAGE_PROMPT_COMPILED")
    if compiled and not is_placeholder(compiled) and lower_value(compiled) != "not_applicable":
        return compiled
    return extract_field(block, "IMAGE_GEN_HANDOFF_PROMPT")


def final_prompt_jargon_hits(value: str | None) -> list[str]:
    """Find internal schema/process words that should not reach image models."""
    if not value:
        return []
    hits: set[str] = set()
    lowered = lower_value(value)
    for term in FINAL_PROMPT_BANNED_JARGON:
        if term in lowered:
            hits.add(term)
    hits.update(FINAL_PROMPT_SCHEMA_JARGON_RE.findall(value))
    return sorted(hits)


def value_is_none_like(value: str | None) -> bool:
    normalized = lower_value(value)
    return normalized in {"", "none", "not_applicable", "n/a", "na", "no", "없음", "해당없음"}


def value_indicates_pass(value: str | None) -> bool:
    normalized = lower_value(value)
    return any(token in normalized for token in ("pass", "passed", "yes", "ok", "통과", "합격"))


def normalize_pipe_list(value: str | None) -> list[str]:
    if not value:
        return []
    # Older generated artifacts used semicolons while newer templates prefer
    # pipes. Accept both separators so proof artifacts remain readable without
    # weakening required-file matching.
    return [part.strip() for part in re.split(r"\s*(?:\| |;|\|)\s*", value) if part.strip()]


def _ascii_keyword_matches(text: str, keyword: str) -> bool:
    """Match English keyword tokens without substring false positives.

    The validator uses short structural keywords such as ``car`` and ``train``.
    A raw substring check makes unrelated prose like ``restrained`` look like a
    train scene, which incorrectly activates vehicle/scale-critical gates.
    Keep phrase keywords permissive, but require token boundaries for single
    English words.
    """
    kw = keyword.lower().strip()
    if not kw:
        return False
    if re.fullmatch(r"[a-z0-9]+", kw):
        plural = r"(?:s|es)?" if len(kw) > 2 else r""
        return re.search(rf"(?<![a-z0-9]){re.escape(kw)}{plural}(?![a-z0-9])", text) is not None
    return kw in text


def _keyword_matches(text: str, keyword: str) -> bool:
    if not keyword:
        return False
    if _HANGUL_RE.search(keyword):
        return keyword in text
    return _ascii_keyword_matches(text, keyword)


def contains_keyword(value: str | None, keywords: list[str]) -> bool:
    text = lower_value(value)
    return any(_keyword_matches(text, keyword) for keyword in keywords)


def normalize_camera_class(value: str | None) -> str:
    """Normalize camera-class preset/user prose for conflict checks."""
    return re.sub(r"[\s\-]+", "_", lower_value(value))


def camera_class_is_scale_proving(value: str | None) -> bool:
    """Return True when the camera class can visually prove protagonist/container scale."""
    if not value:
        return False
    normalized = normalize_camera_class(value)
    if any(token in normalized for token in ("extreme_wide", "wide", "long_shot", "establishing", "scale_shot")):
        return True
    return contains_keyword_korean_tolerant(value, CAMERA_CLASS_SCALE_PROVING_KEYWORDS)


def camera_class_is_closeup_risk(value: str | None) -> bool:
    """Return True when the camera class tends to enlarge the protagonist/focal face."""
    if not value:
        return False
    if camera_class_is_scale_proving(value):
        return False
    normalized = normalize_camera_class(value)
    if any(token in normalized for token in ("close", "portrait", "medium", "hero_shot", "upper_body", "bust")):
        return True
    return contains_keyword_korean_tolerant(value, CAMERA_CLASS_CLOSEUP_RISK_KEYWORDS)


def count_keyword_hits(value: str | None, keywords: list[str]) -> int:
    text = lower_value(value)
    return sum(1 for keyword in set(keywords) if keyword in text)


def has_numeric_scale(value: str | None) -> bool:
    if not value:
        return False
    return bool(re.search(r"\d", value))


def contains_proxy_blockout_evidence(value: str | None) -> bool:
    return contains_keyword(value, BLOCKOUT_PROXY_KEYWORDS)


def indicates_explicit_skip(value: str | None) -> bool:
    return contains_keyword(
        value,
        [
            "skip",
            "skipped",
            "no blender",
            "not_applicable",
            "direct_text_prompt",
            "backgroundless",
            "no background",
            "simple background",
            "plain background",
            "character-only",
            "skip_blender",
            "패스",
            "스킵",
            "생략",
            "배경 없음",
            "단순 배경",
            "캐릭터만",
        ],
    )


def is_render_bound_spec(text: str) -> bool:
    deliverable = extract_field(text, "DELIVERABLE")
    return is_pre_image_handoff_ready(text) or contains_keyword(deliverable, RENDER_BOUND_DELIVERABLE_KEYWORDS)


def is_pre_image_handoff_ready(text: str) -> bool:
    """True when the spec is claiming it is ready for the first image handoff.

    `IMAGE_GEN_READY` remains supported as a legacy alias, but new specs should
    use `PRE_IMAGE_HANDOFF_READY` so post-image acceptance can be gated
    separately.
    """
    return (
        lower_value(extract_field(text, "PRE_IMAGE_HANDOFF_READY")) == "yes"
        or lower_value(extract_field(text, "IMAGE_GEN_READY")) == "yes"
    )


def is_post_image_verdict_required(text: str) -> bool:
    """True when a generated/previous output is being accepted or rejected."""
    return (
        lower_value(extract_field(text, "POST_IMAGE_VERDICT_REQUIRED")) == "yes"
        or lower_value(extract_field(text, "POST_IMAGE_ACCEPTED")) in {"yes", "no"}
    )


def contains_object_research_signal(value: str | None) -> bool:
    text = lower_value(value)
    for keyword in OBJECT_RESEARCH_KEYWORDS:
        if re.search(r"[가-힣]", keyword):
            if keyword in text:
                return True
            continue

        if " " in keyword or "-" in keyword:
            if keyword in text:
                return True
            continue

        if re.search(rf"\b{re.escape(keyword)}s?\b", text):
            return True
    return False


def extract_first_ratio(text: str | None) -> float | None:
    """Best-effort numeric ratio extraction from operator-written text.

    Recognizes "60%" / "0.6" / "1.0" / "1:0.5" plus common filled-spec
    forms such as "1.55m / 2.0m = 0.78" and "ratio 0.78". Returns None if
    no plausible numeric value is found. Conservative on purpose — used only
    for flagging extreme contradictions, not for precise calculation.
    """
    if not text:
        return None
    # Prefer explicit computed/result ratios over raw dimensions or threshold
    # ranges. This avoids reading "1.55m / 2.0m = 0.78" as "1.55".
    m = re.search(r"=\s*(\d+(?:\.\d+)?)\s*%", text)
    if m:
        return float(m.group(1)) / 100.0
    m = re.search(r"=\s*(\d+(?:\.\d+)?)\b", text)
    if m:
        return float(m.group(1))
    m = re.search(
        r"(?:ratio|fraction|occupancy|screen\s*share|screen\s*occupancy|비율|점유율?)\D{0,24}(\d+(?:\.\d+)?)\s*%",
        text,
        re.IGNORECASE,
    )
    if m:
        return float(m.group(1)) / 100.0
    m = re.search(
        r"(?:ratio|fraction|occupancy|screen\s*share|screen\s*occupancy|비율|점유율?)\D{0,24}(\d+(?:\.\d+)?)\b",
        text,
        re.IGNORECASE,
    )
    if m:
        return float(m.group(1))
    m = re.search(r"(\d+(?:\.\d+)?)\s*%", text)
    if m:
        return float(m.group(1)) / 100.0
    m = re.search(r"\b(\d+(?:\.\d+)?)\s*:\s*(\d+(?:\.\d+)?)\b", text)
    if m:
        denom = float(m.group(1))
        numer = float(m.group(2))
        if denom > 0:
            return numer / denom
    m = re.search(
        r"\b(\d+(?:\.\d+)?)\s*(?:m|cm|px)?\s*/\s*(\d+(?:\.\d+)?)\s*(?:m|cm|px)?\b",
        text,
        re.IGNORECASE,
    )
    if m:
        numer = float(m.group(1))
        denom = float(m.group(2))
        if denom > 0:
            return numer / denom
    m = re.search(r"\b\d+(?:\.\d+)?\b", text)
    if m:
        return float(m.group(0))
    return None


def count_meaningful_tokens(value: str | None) -> int:
    if not value:
        return 0
    return len(re.findall(r"[A-Za-z0-9가-힣]+", value))


SECTION_HEADING_RE = re.compile(r"(?m)^## ")


def extract_named_section(text: str, heading: str) -> str:
    """Return the section starting at `heading` until the next `## ` heading. Empty if not found."""
    idx = text.find(heading)
    if idx == -1:
        return ""
    rest = text[idx + len(heading):]
    next_match = SECTION_HEADING_RE.search(rest)
    end = idx + len(heading) + (next_match.start() if next_match else len(rest))
    return text[idx:end]


def extract_block_list(block: str, field_name: str) -> list[str]:
    """Read consecutive `- ...` bullet lines following `FIELD_NAME:` with no inline value."""
    pattern = re.compile(rf"(?m)^{re.escape(field_name)}:[ \t]*$")
    match = pattern.search(block)
    if not match:
        return []
    items: list[str] = []
    for line in block[match.end():].splitlines():
        stripped = line.strip()
        if not stripped:
            if items:
                break
            continue
        if stripped.startswith("- "):
            items.append(stripped[2:].strip())
            continue
        if stripped.startswith("-"):
            items.append(stripped[1:].strip())
            continue
        break
    return items


def normalize_for_inheritance(value: str | None) -> str:
    if not value:
        return ""
    return re.sub(r"\s+", " ", value).strip().lower()


def find_missing_inheritance(commands: list[str], target: str | None) -> list[str]:
    """Return commands whose normalized form is not a substring of the normalized target text."""
    if not commands:
        return []
    target_norm = normalize_for_inheritance(target)
    if not target_norm:
        return list(commands)
    missing: list[str] = []
    for cmd in commands:
        cmd_norm = normalize_for_inheritance(cmd)
        if not cmd_norm:
            continue
        if cmd_norm not in target_norm:
            missing.append(cmd)
    return missing


def extract_yaml_literal_block(block: str, field_name: str) -> str:
    """Read a `FIELD: |` YAML-style literal block: indented lines until dedent."""
    pattern = re.compile(rf"(?m)^{re.escape(field_name)}:[ \t]*\|[ \t]*$")
    match = pattern.search(block)
    if not match:
        return ""
    lines = block[match.end():].splitlines()
    captured: list[str] = []
    for line in lines:
        if not line.strip():
            captured.append("")
            continue
        if line.startswith("  ") or line.startswith("\t"):
            captured.append(line.lstrip())
            continue
        break
    while captured and not captured[-1]:
        captured.pop()
    return "\n".join(captured)


def parse_visual_verdict_json(block: str, field_name: str = "POST_IMAGE_VISUAL_VERDICT_JSON") -> tuple[dict | None, str]:
    """Return (parsed_dict_or_None, error_message). Tries inline literal block first.

    `field_name` lets callers parse the same JSON shape from artifacts that use
    a different field label (e.g. VERDICT_JSON inside the verdict artifact).
    """
    import json
    raw = extract_yaml_literal_block(block, field_name)
    if not raw:
        single = extract_field(block, field_name)
        if not single or is_placeholder(single):
            return None, "missing"
        raw = single.strip()
    try:
        return json.loads(raw), ""
    except json.JSONDecodeError as exc:
        return None, f"invalid JSON: {exc.msg} at line {exc.lineno} col {exc.colno}"


def validate_post_image_visual_verdict_artifact(
    artifact_path: Path,
    spec_path: Path,
    spec_inline_verdict: dict | None,
) -> ValidationResult:
    if not artifact_path.exists():
        return ValidationResult(
            path=artifact_path,
            text="",
            errors=[f"Visual verdict artifact not found: {artifact_path}"],
            warnings=[],
        )

    text = normalize_text(artifact_path)
    errors: list[str] = []
    warnings: list[str] = []

    if (
        "[POST_IMAGE_VISUAL_VERDICT_ARTIFACT]" not in text
        or "[/POST_IMAGE_VISUAL_VERDICT_ARTIFACT]" not in text
    ):
        errors.append("Missing [POST_IMAGE_VISUAL_VERDICT_ARTIFACT] wrapper block.")

    artifact_ready = lower_value(extract_field(text, "ARTIFACT_READY"))
    if artifact_ready not in {"yes", "no"}:
        errors.append("Visual verdict artifact ARTIFACT_READY must be 'yes' or 'no'.")
    elif artifact_ready == "no":
        errors.append("Visual verdict artifact exists but ARTIFACT_READY is 'no'.")

    parent_field = extract_field(text, "PARENT_SPEC_PATH")
    if not is_placeholder(parent_field):
        resolved_parent = resolve_reference_path(parent_field or "", artifact_path)
        if resolved_parent != spec_path.resolve():
            warnings.append(
                f"Visual verdict artifact PARENT_SPEC_PATH points to {resolved_parent}, expected {spec_path.resolve()}."
            )

    artifact_verdict, parse_err = parse_visual_verdict_json(text, "VERDICT_JSON")
    if artifact_verdict is None:
        if parse_err == "missing":
            errors.append("Visual verdict artifact is missing VERDICT_JSON block.")
        else:
            errors.append(f"Visual verdict artifact VERDICT_JSON parse failure: {parse_err}")
    else:
        missing_keys = [k for k in VISUAL_VERDICT_REQUIRED_KEYS if k not in artifact_verdict]
        if missing_keys:
            errors.append(
                f"Visual verdict artifact VERDICT_JSON missing required keys: {', '.join(missing_keys)}."
            )

    if artifact_verdict is not None and spec_inline_verdict is not None:
        # Cross-check: each pass key must agree between artifact and spec inline.
        for key in VISUAL_VERDICT_REQUIRED_KEYS:
            if key not in artifact_verdict or key not in spec_inline_verdict:
                continue
            if artifact_verdict[key] != spec_inline_verdict[key]:
                errors.append(
                    f"Visual verdict artifact VERDICT_JSON.{key}={artifact_verdict[key]!r} disagrees with "
                    f"SPEC POST_IMAGE_VISUAL_VERDICT_JSON.{key}={spec_inline_verdict[key]!r}."
                )

    return ValidationResult(path=artifact_path, text=text, errors=errors, warnings=warnings)


POST_IMAGE_REPAIR_ARTIFACT_FIELDS = (
    "PARENT_SPEC_PATH",
    "SOURCE_VERDICT_ARTIFACT_PATH",
    "FAILED_KEYS",
    "FAILURE_KEY_ROUTING",
    "SCENE_CONTRACT_PATCH",
    "PROMPT_PATCH_TIER_0_TO_3",
    "SCALE_FAILURE_SHOT_CLASS_ESCALATION",
    "VISUAL_GUIDE_ESCALATION",
    "NEXT_DRAFT_PROMPT",
    "REPAIR_READY",
)


def split_failure_keys(value: str | None) -> list[str]:
    if not value:
        return []
    found = re.findall(
        r"\b([a-z_]+(?:_pass|_valid|_object|_inside_object|_accepted))\b",
        value,
    )
    if found:
        return sorted(set(found))
    return [part.strip() for part in re.split(r"\s*(?:\||,|\n|;)\s*", value) if part.strip()]


def failed_visual_verdict_keys(verdict: dict | None) -> list[str]:
    if not isinstance(verdict, dict):
        return []
    failed = [
        key for key in VISUAL_VERDICT_REQUIRED_KEYS
        if key.endswith("_pass") and verdict.get(key) is False
    ]
    for key in ("hero_fits_inside_object", "occupant_anchor_valid"):
        if verdict.get(key) is False:
            failed.append(key)
    return sorted(set(failed))


def validate_post_image_repair_artifact(
    artifact_path: Path,
    spec_path: Path,
    expected_failed_keys: list[str] | tuple[str, ...] | None = None,
    expected_next_prompt: str | None = None,
) -> ValidationResult:
    """Validate the repair compiler artifact for a failed generated image.

    A visual verdict says what failed. This artifact is the required bridge from
    those failed keys to a patched Scene Contract / prompt for the next draft,
    so the pipeline does not simply rerun the same failing prompt.
    """
    if not artifact_path.exists():
        return ValidationResult(
            path=artifact_path,
            text="",
            errors=[f"Post-image repair artifact not found: {artifact_path}"],
            warnings=[],
        )

    text = normalize_text(artifact_path)
    errors: list[str] = []
    warnings: list[str] = []

    if "[POST_IMAGE_REPAIR_ARTIFACT]" not in text or "[/POST_IMAGE_REPAIR_ARTIFACT]" not in text:
        errors.append("Missing [POST_IMAGE_REPAIR_ARTIFACT] wrapper block.")

    for field_name in POST_IMAGE_REPAIR_ARTIFACT_FIELDS:
        value = extract_field(text, field_name)
        if is_placeholder(value):
            errors.append(f"Missing or placeholder repair artifact field: {field_name}")

    repair_ready = lower_value(extract_field(text, "REPAIR_READY"))
    if repair_ready not in {"yes", "no"}:
        errors.append("Post-image repair artifact REPAIR_READY must be 'yes' or 'no'.")
    elif repair_ready == "no":
        errors.append("Post-image repair artifact exists but REPAIR_READY is 'no'.")

    parent_field = extract_field(text, "PARENT_SPEC_PATH")
    if not is_placeholder(parent_field):
        resolved_parent = resolve_reference_path(parent_field or "", artifact_path)
        if resolved_parent != spec_path.resolve():
            warnings.append(
                f"Post-image repair artifact PARENT_SPEC_PATH points to {resolved_parent}, expected {spec_path.resolve()}."
            )

    failed_keys = split_failure_keys(extract_field(text, "FAILED_KEYS"))
    expected = sorted(set(expected_failed_keys or []))
    missing_expected = [key for key in expected if key not in failed_keys]
    if missing_expected:
        errors.append(
            f"Post-image repair artifact FAILED_KEYS missing expected failed keys: {', '.join(missing_expected)}."
        )

    routing = extract_field(text, "FAILURE_KEY_ROUTING")
    scene_patch = extract_field(text, "SCENE_CONTRACT_PATCH")
    prompt_patch = extract_field(text, "PROMPT_PATCH_TIER_0_TO_3")
    scale_shot_escalation = extract_field(text, "SCALE_FAILURE_SHOT_CLASS_ESCALATION")
    guide_escalation = extract_field(text, "VISUAL_GUIDE_ESCALATION")
    next_prompt = extract_field(text, "NEXT_DRAFT_PROMPT")

    for label, value in (
        ("FAILURE_KEY_ROUTING", routing),
        ("SCENE_CONTRACT_PATCH", scene_patch),
        ("PROMPT_PATCH_TIER_0_TO_3", prompt_patch),
        ("VISUAL_GUIDE_ESCALATION", guide_escalation),
        ("NEXT_DRAFT_PROMPT", next_prompt),
    ):
        if value_is_none_like(value) or count_meaningful_tokens(value) < 6:
            errors.append(f"Post-image repair artifact {label} must contain actionable repair content.")

    combined = " ".join(
        filter(None, [routing, scene_patch, prompt_patch, scale_shot_escalation, guide_escalation, next_prompt])
    )
    if "target_contact_pass" in expected and not contains_keyword_korean_tolerant(
        combined,
        ["target", "contact", "forbidden", "not", "neck", "body", "wing", "대상", "접촉", "금지", "아님", "목", "몸통", "날개"],
    ):
        errors.append(
            "target_contact_pass repair must promote target/contact/forbidden-target wording into the repair patch and next prompt."
        )
    if "garment_attachment_pass" in expected and not contains_keyword_korean_tolerant(
        combined,
        GARMENT_ATTACHMENT_CONTRACT_KEYWORDS,
    ):
        errors.append(
            "garment_attachment_pass repair must name garment attachment/origin landmarks such as shoulders/collar/neck/back/clasp."
        )
    if any(
        key in expected
        for key in SCALE_FAILURE_VERDICT_KEYS
    ) and not contains_keyword(
        combined,
        HUMANOID_SCALE_PARITY_KEYWORDS
        + PASSENGER_CAPACITY_KEYWORDS
        + SCALE_CRITICAL_RATIO_KEYWORDS
        + SCALE_VISUAL_GUIDE_KEYWORDS,
    ):
        errors.append(
            "scale/occupant repair must carry scale parity, occupant/capacity, numeric ratio, or scale visual-guide wording into the repair patch."
        )
    if any(key in expected for key in SCALE_FAILURE_VERDICT_KEYS):
        if value_is_none_like(scale_shot_escalation) or count_meaningful_tokens(scale_shot_escalation) < 8:
            errors.append(
                "scale repair artifacts require SCALE_FAILURE_SHOT_CLASS_ESCALATION: camera/framing must be patched, not only ratio prose."
            )
        else:
            scale_repair_text = " ".join(filter(None, [scale_shot_escalation, prompt_patch, next_prompt]))
            if not contains_keyword_korean_tolerant(
                scale_repair_text,
                CAMERA_CLASS_SCALE_PROVING_KEYWORDS + SCALE_WITNESS_VISIBILITY_KEYWORDS,
            ):
                errors.append(
                    "scale repair must escalate to a scale-proving wide/long shot with visible doors/windows/passengers/modules/full container witnesses."
                )
            if not contains_keyword_korean_tolerant(scale_repair_text, FACE_FOCAL_DEMOTION_KEYWORDS):
                errors.append(
                    "scale repair must demote face/eye focal to a small accent until vehicle/container scale passes."
                )
    if "scale_visual_guide_pass" in expected and not contains_keyword_korean_tolerant(
        combined,
        VISUAL_GUIDE_EXECUTION_KEYWORDS,
    ):
        errors.append(
            "scale_visual_guide_pass repair must escalate beyond text-only prompt repair into visual guide evidence such as mask/overlay/blockout/lineart/depth."
        )
    if any(key in expected for key in ("cut_plane_visibility_pass", "unknown_cut_form_pass")) and not contains_keyword_korean_tolerant(
        combined,
        CUT_PLANE_VISIBILITY_KEYWORDS + CUT_PLANE_VISUAL_GUIDE_KEYWORDS,
    ):
        errors.append(
            "cut-plane repair must carry visible cut-plane/cross-section, head-side/body-side continuity, no-hidden-cut, and no-unknown-protrusion wording into the repair patch."
        )
    if any(key in expected for key in ("hand_topology_pass", "finger_separation_pass", "both_arms_present_pass")) and not contains_keyword(
        combined,
        PROTECTED_CHAIN_KEYWORDS + FINGER_TOPOLOGY_KEYWORDS,
    ):
        errors.append(
            "hand/finger/arm repair must carry protected-chain or finger-topology wording into the repair patch."
        )
    if any(key in expected for key in ("weapon_grip_mechanics_pass", "wrist_force_path_pass")) and not contains_keyword_korean_tolerant(
        combined,
        GRIP_MECHANICS_KEYWORDS + GRIP_MECHANICS_VISUAL_GUIDE_KEYWORDS,
    ):
        errors.append(
            "weapon-grip repair must carry functional grip mechanics and wrist/forearm force-path wording into the repair patch, not only finger topology."
        )

    if expected_next_prompt and next_prompt and next_prompt.strip() != expected_next_prompt.strip():
        errors.append("Post-image repair artifact NEXT_DRAFT_PROMPT disagrees with SPEC POST_IMAGE_NEXT_DRAFT_PROMPT.")

    return ValidationResult(path=artifact_path, text=text, errors=errors, warnings=warnings)


def _required_visibility_entries(entries: object) -> dict[str, dict]:
    if not isinstance(entries, dict):
        return {}
    required: dict[str, dict] = {}
    for key, value in entries.items():
        if not isinstance(value, dict):
            continue
        if value.get("required", True) is not False:
            required[str(key)] = value
    return required


def validate_blender_visibility_report(
    report_path: Path,
    spec_path: Path,
    *,
    require_target_contact: bool = False,
) -> ValidationResult:
    """Validate machine-readable visibility evidence from the Blender pass.

    The report is intentionally small JSON so the validator can distinguish a
    real reviewed blockout from a mere `.blend`/PNG existence check. It does not
    replace human/vision review, but it catches the failure mode where the
    camera/render sees mostly occluding buildings while the spec still claims a
    strict blockout pass.
    """
    if not report_path.exists():
        return ValidationResult(
            path=report_path,
            text="",
            errors=[f"Blender visibility report not found: {report_path}"],
            warnings=[],
        )

    raw = report_path.read_text(encoding="utf-8").replace("\r\n", "\n")
    errors: list[str] = []
    warnings: list[str] = []
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        return ValidationResult(
            path=report_path,
            text=raw,
            errors=[f"Blender visibility report invalid JSON: {exc.msg} at line {exc.lineno} col {exc.colno}"],
            warnings=[],
        )

    if not isinstance(data, dict):
        return ValidationResult(
            path=report_path,
            text=raw,
            errors=["Blender visibility report root must be a JSON object."],
            warnings=[],
        )

    parent_value = data.get("parent_spec_path")
    if isinstance(parent_value, str) and parent_value.strip():
        resolved_parent = resolve_reference_path(parent_value, report_path)
        if resolved_parent != spec_path.resolve():
            warnings.append(
                f"Blender visibility report parent_spec_path points to {resolved_parent}, expected {spec_path.resolve()}."
            )

    if data.get("report_ready") is not True:
        errors.append("Blender visibility report report_ready must be true.")

    if data.get("camera_not_occluded_by_buildings") is not True:
        errors.append("Blender visibility report camera_not_occluded_by_buildings must be true.")

    core_required = _required_visibility_entries(data.get("core_objects"))
    if len(core_required) < 3:
        errors.append("Blender visibility report must list at least three required core_objects.")
    for object_id, item in core_required.items():
        if item.get("visible") is not True:
            errors.append(f"Blender visibility report core object {object_id} must be visible.")

    target_required = _required_visibility_entries(data.get("target_contacts"))
    if require_target_contact and not target_required:
        errors.append("Blender visibility report requires at least one target_contacts entry for action/contact scenes.")
    for contact_id, item in target_required.items():
        if item.get("visible") is not True:
            errors.append(f"Blender visibility report target contact {contact_id} must be visible.")
        if item.get("forbidden_target_hit") is True:
            errors.append(f"Blender visibility report target contact {contact_id} has forbidden_target_hit=true.")
        if not str(item.get("target_id", "")).strip():
            errors.append(f"Blender visibility report target contact {contact_id} must name target_id.")

    scale_required = _required_visibility_entries(data.get("scale_anchors"))
    for anchor_id, item in scale_required.items():
        if item.get("visible") is not True:
            errors.append(f"Blender visibility report scale anchor {anchor_id} must be visible.")

    return ValidationResult(path=report_path, text=raw, errors=errors, warnings=warnings)


VISUAL_VERDICT_REQUIRED_KEYS = (
    "container_scale_pass",
    "hero_fits_inside_object",
    "occupant_anchor_valid",
    "protagonist_to_occupant_ratio_pass",
    "scale_visual_guide_pass",
    "target_contact_pass",
    "cut_plane_visibility_pass",
    "unknown_cut_form_pass",
    "dense_environment_pass",
    "hand_topology_pass",
    "finger_separation_pass",
    "weapon_grip_mechanics_pass",
    "wrist_force_path_pass",
    "both_arms_present_pass",
    "garment_attachment_pass",
    "named_object_distortion_pass",
    "command_inheritance_pass",
    "style_target_pass",
    "rerender_required",
)


_KOREAN_PARTICLE_RE = re.compile(
    r"([가-힣]{2,})("
    # case markers (intentionally excluding 은/는: ambiguous with verb endings)
    r"이|가|을|를|도|만|의|에"
    # locative / dative
    r"|에서|에게|에게서|한테|께서"
    # instrumental / comparative / connective
    r"|으로|로|와|과|랑|이랑|보다|처럼|같이"
    r")(\s|$|[,.;:!?\)\]\}])"
)
# Known limitation: stems ending in particle chars (e.g., 어린이 + space) may be
# over-stripped to 어린 + space. Acceptable trade-off for SCALE_CRITICAL matching.

_HANGUL_RE = re.compile(r"[가-힣]")


def normalize_korean(text: str | None) -> str:
    """Strip common Korean postpositional particles + collapse whitespace.

    Conservative: only strips when the noun is at least 2 syllables and the
    particle is followed by whitespace, line end, or punctuation.
    Words like 어린이/사람들 stay intact when no particle follows.
    """
    if not text:
        return ""
    s = text
    if _HANGUL_RE.search(s):
        s = _KOREAN_PARTICLE_RE.sub(r"\1\3", s)
    s = re.sub(r"\s+", " ", s).strip().lower()
    return s


def contains_keyword_korean_tolerant(value: str | None, keywords: list[str]) -> bool:
    """Keyword check that ignores Korean particles and avoids English substring false positives."""
    if not value:
        return False
    text_norm = normalize_korean(value)
    if not text_norm:
        return False
    for keyword in keywords:
        if not keyword:
            continue
        kw_norm = normalize_korean(keyword) if _HANGUL_RE.search(keyword) else keyword.lower().strip()
        if not kw_norm:
            continue
        if _HANGUL_RE.search(keyword):
            if kw_norm in text_norm:
                return True
        elif _ascii_keyword_matches(text_norm, kw_norm):
            return True
    return False


def prompt_starts_with_substring(prompt: str | None, opening: str | None, max_start_offset: int = 30) -> bool:
    """Return True if `opening` head appears within the first `max_start_offset` chars of `prompt`.

    Stricter than substring-anywhere: enforces the opening as the prompt's first
    sentence (with a small allowance for a brief leading framing phrase).
    """
    if not prompt or not opening:
        return False
    p_norm = normalize_for_inheritance(prompt)
    o_norm = normalize_for_inheritance(opening)
    if not o_norm or not p_norm:
        return False
    o_head = o_norm[:60]
    if not o_head:
        return False
    pos = p_norm.find(o_head)
    return 0 <= pos <= max_start_offset


def split_emotion_axis(value: str | None) -> list[str]:
    if not value:
        return []
    normalized = re.sub(r"\s+(and|및)\s+", " + ", value, flags=re.IGNORECASE)
    parts = re.split(r"\s*(?:\+|/|,|;|&|\|)\s*", normalized)
    return [part.strip() for part in parts if part.strip()]


def has_directional_detail(value: str | None) -> bool:
    return contains_keyword(value, DIRECTION_KEYWORDS)


def likely_visible_hands(*values: str | None) -> bool:
    combined = " ".join(filter(None, [lower_value(value) for value in values]))
    return contains_keyword(combined, HAND_KEYWORDS) or (
        contains_keyword(combined, HAND_PROP_INTERACTION_KEYWORDS)
        and contains_keyword(combined, HAND_ACTION_HINTS)
        and not value_is_none_like(combined)
    )


def normalize_age_band(value: str | None) -> str:
    return re.sub(r"\s+", "", (value or "").strip())


def likely_requires_anatomy_gate(*values: str | None) -> bool:
    combined = " ".join(filter(None, [lower_value(value) for value in values]))
    return contains_keyword(combined, ANATOMY_GATE_KEYWORDS)


def likely_requires_geometric_blockout(*values: str | None) -> bool:
    combined = " ".join(filter(None, [lower_value(value) for value in values]))
    return contains_keyword(combined, GEOMETRIC_BLOCKOUT_KEYWORDS)


def validate_card_path(value: str | None, origin_path: Path, field_name: str, errors: list[str]) -> None:
    if value_is_none_like(value):
        return
    resolved = resolve_reference_path(value or "", origin_path)
    if not resolved.exists():
        errors.append(f"{field_name} points to a missing card file: {resolved}")


def is_actionable_correction(value: str | None) -> bool:
    if not value:
        return False
    has_action = contains_keyword(value, ACTIONABLE_CORRECTION_KEYWORDS)
    has_condition = "if " in lower_value(value) or "면" in lower_value(value)
    return has_action or has_condition


def extract_theory_files(section_block: str) -> list[str]:
    files: list[str] = []
    lines = section_block.splitlines()
    in_theory_block = False
    for raw_line in lines:
        line = raw_line.rstrip()
        stripped = line.strip()
        if stripped == "THEORY_FILES:":
            in_theory_block = True
            continue
        if in_theory_block:
            if stripped.startswith("- "):
                files.append(stripped[2:].strip())
                continue
            if stripped == "":
                break
            break
    return files


def validate_theory_read_proof(proof_path: Path, spec_path: Path, spec_text: str, sections: dict[str, str]) -> ValidationResult:
    if not proof_path.exists():
        return ValidationResult(path=proof_path, text="", errors=[f"Theory-read proof file not found: {proof_path}"], warnings=[])

    text = normalize_text(proof_path)
    errors: list[str] = []
    warnings: list[str] = []

    if "[THEORY_READ_PROOF]" not in text or "[/THEORY_READ_PROOF]" not in text:
        errors.append("Missing [THEORY_READ_PROOF] wrapper block.")

    for field_name in THEORY_PROOF_FIELDS:
        value = extract_field(text, field_name)
        if is_placeholder(value):
            errors.append(f"Missing or placeholder theory-proof field: {field_name}")

    style_guide_required = lower_value(extract_field(text, "STYLE_GUIDE_REQUIRED"))
    if style_guide_required not in {"yes", "no"}:
        errors.append("STYLE_GUIDE_REQUIRED must be 'yes' or 'no'.")

    proof_ready = lower_value(extract_field(text, "PROOF_READY"))
    if proof_ready not in {"yes", "no"}:
        errors.append("PROOF_READY must be 'yes' or 'no'.")
    elif proof_ready == "no":
        errors.append("Theory-read proof exists but PROOF_READY is 'no'.")

    parent_field = extract_field(text, "PARENT_SPEC_PATH")
    if not is_placeholder(parent_field):
        resolved_parent = resolve_reference_path(parent_field or "", proof_path)
        if resolved_parent != spec_path.resolve():
            warnings.append(
                f"Theory proof PARENT_SPEC_PATH points to {resolved_parent}, expected {spec_path.resolve()}."
            )

    for heading, field_name in THEORY_STEP_FIELDS.items():
        required_files = extract_theory_files(sections[heading])
        logged_files = normalize_pipe_list(extract_field(text, field_name))
        missing = [file for file in required_files if file not in logged_files]
        if missing:
            errors.append(f"Theory proof missing required reads for {heading}: {missing}")

    workspace_style_mode = lower_value(extract_field(spec_text, "WORKSPACE_STYLE_MODE"))
    style_logged = normalize_pipe_list(extract_field(text, "STYLE_GUIDE_FILES_READ"))
    style_guide_path = "illustrate-skill/references/style-guide.md"
    if "workspace reference style" in workspace_style_mode:
        if style_guide_required != "yes":
            errors.append("Theory proof must mark STYLE_GUIDE_REQUIRED: yes for workspace reference style runs.")
        if style_guide_path not in style_logged:
            errors.append("Theory proof missing style-guide read for workspace reference style run.")

    if lower_value(extract_field(spec_text, "PIVA_MODE")) == "enabled":
        all_logged = []
        for proof_field in (
            "STEP_1_FILES_READ",
            "STEP_2_FILES_READ",
            "STEP_3_FILES_READ",
            "STEP_4_FILES_READ",
            "STEP_5_FILES_READ",
            "STEP_6_FILES_READ",
            "STEP_7_FILES_READ",
            "STEP_8_FILES_READ",
        ):
            all_logged.extend(normalize_pipe_list(extract_field(text, proof_field)))
        if PIVA_THEORY_FILE not in all_logged:
            errors.append(f"Theory proof missing PIVA lifecycle read: {PIVA_THEORY_FILE}")

    return ValidationResult(path=proof_path, text=text, errors=errors, warnings=warnings)


def validate_object_research_invocation_log(log_path: Path, spec_path: Path, artifact_path: Path) -> ValidationResult:
    if not log_path.exists():
        return ValidationResult(path=log_path, text="", errors=[f"Object research invocation log file not found: {log_path}"], warnings=[])

    text = normalize_text(log_path)
    errors: list[str] = []
    warnings: list[str] = []

    if "[OBJECT_RESEARCH_INVOCATION]" not in text or "[/OBJECT_RESEARCH_INVOCATION]" not in text:
        errors.append("Missing [OBJECT_RESEARCH_INVOCATION] wrapper block.")

    for field_name in OBJECT_INVOCATION_FIELDS:
        value = extract_field(text, field_name)
        if is_placeholder(value):
            errors.append(f"Missing or placeholder object-invocation field: {field_name}")

    lookup_first = lower_value(extract_field(text, "LOOKUP_FIRST"))
    if lookup_first not in {"yes", "no"}:
        errors.append("LOOKUP_FIRST must be 'yes' or 'no'.")
    elif lookup_first != "yes":
        errors.append("LOOKUP_FIRST must be 'yes' for object-research handoffs in this project.")

    web_research_used = lower_value(extract_field(text, "WEB_RESEARCH_USED"))
    if web_research_used not in {"yes", "no"}:
        errors.append("WEB_RESEARCH_USED must be 'yes' or 'no'.")

    invocation_ready = lower_value(extract_field(text, "INVOCATION_READY"))
    if invocation_ready not in {"yes", "no"}:
        errors.append("INVOCATION_READY must be 'yes' or 'no'.")
    elif invocation_ready == "no":
        errors.append("Object research invocation log exists but INVOCATION_READY is 'no'.")

    parent_spec_field = extract_field(text, "PARENT_SPEC_PATH")
    if not is_placeholder(parent_spec_field):
        resolved_parent_spec = resolve_reference_path(parent_spec_field or "", log_path)
        if resolved_parent_spec != spec_path.resolve():
            warnings.append(
                f"Object invocation log PARENT_SPEC_PATH points to {resolved_parent_spec}, expected {spec_path.resolve()}."
            )

    parent_artifact_field = extract_field(text, "PARENT_OBJECT_ARTIFACT_PATH")
    if not is_placeholder(parent_artifact_field):
        resolved_parent_artifact = resolve_reference_path(parent_artifact_field or "", log_path)
        if resolved_parent_artifact != artifact_path.resolve():
            warnings.append(
                f"Object invocation log PARENT_OBJECT_ARTIFACT_PATH points to {resolved_parent_artifact}, expected {artifact_path.resolve()}."
            )

    output_artifact_field = extract_field(text, "OUTPUT_ARTIFACT_PATH")
    if not is_placeholder(output_artifact_field):
        resolved_output_artifact = resolve_reference_path(output_artifact_field or "", log_path)
        if resolved_output_artifact != artifact_path.resolve():
            warnings.append(
                f"Object invocation log OUTPUT_ARTIFACT_PATH points to {resolved_output_artifact}, expected {artifact_path.resolve()}."
            )

    return ValidationResult(path=log_path, text=text, errors=errors, warnings=warnings)


def validate_object_research_artifact(artifact_path: Path, expected_parent_spec_path: Path | None = None) -> ValidationResult:
    if not artifact_path.exists():
        return ValidationResult(path=artifact_path, text="", errors=[f"Object research artifact file not found: {artifact_path}"], warnings=[])

    text = normalize_text(artifact_path)
    errors: list[str] = []
    warnings: list[str] = []

    if "[OBJECT_RESEARCH_ARTIFACT]" not in text or "[/OBJECT_RESEARCH_ARTIFACT]" not in text:
        errors.append("Missing [OBJECT_RESEARCH_ARTIFACT] wrapper block.")

    for field_name in OBJECT_ARTIFACT_FIELDS:
        value = extract_field(text, field_name)
        if is_placeholder(value):
            errors.append(f"Missing or placeholder object-artifact field: {field_name}")

    artifact_ready = lower_value(extract_field(text, "ARTIFACT_READY"))
    if artifact_ready and artifact_ready not in {"yes", "no"}:
        errors.append(f"Invalid value for ARTIFACT_READY: {artifact_ready!r}. Allowed: ['no', 'yes']")
    elif artifact_ready == "no":
        errors.append("Object research artifact exists but ARTIFACT_READY is 'no'.")

    if artifact_ready == "yes":
        for field_name in (
            "PER_OBJECT_DRAW_LOCKS",
            "SCALE_PERSPECTIVE_LOCKS",
            "RELATIONSHIP_CHECK_NOTES",
            "GENERATION_PROMPT_LOCKS",
            "DO_NOT_FAKE_POLICY",
        ):
            if count_meaningful_tokens(extract_field(text, field_name)) < 4:
                errors.append(f"Ready object artifact requires draw-ready structural content in {field_name}.")
        if contains_keyword(extract_field(text, "DO_NOT_FAKE_POLICY"), UNKNOWN_UNRESOLVED_KEYWORDS):
            errors.append("DO_NOT_FAKE_POLICY cannot permit unresolved unknown objects, random patterns, or fake detail.")

    container_expected = any(
        contains_keyword(field, CONTAINER_OBJECT_KEYWORDS)
        for field in (
            extract_field(text, "SOURCE_REQUEST"),
            extract_field(text, "SCENE_TYPE"),
            extract_field(text, "REQUIRED_OBJECTS"),
            extract_field(text, "RESEARCH_LANES"),
            extract_field(text, "PER_OBJECT_DRAW_LOCKS"),
            extract_field(text, "SCALE_PERSPECTIVE_LOCKS"),
        )
    )
    if container_expected:
        for field_name in (
            "OBJECT_CONTAINMENT_CLASSIFICATION",
            "HUMAN_ENTERABLE_OBJECTS",
            "HUMAN_ENTERABLE_CAPACITY_RESEARCH",
            "INTERNAL_HUMAN_ANATOMY_ANCHORS",
            "OCCUPANT_BLEND_SCALE_PLAN",
            "PROTAGONIST_MAIN_FIGURE_SCALE_LOCK",
            "SCALE_EMPHASIS_OVERRIDE_POLICY",
            "HUMAN_ENTERABLE_COMPOSITE_SCALE_TABLE",
            "ENTRY_FIT_CHECK",
            "XYZ_VOLUME_CHECK",
            "CAPACITY_CLASS_CHECK",
            "OCCUPANT_ANCHOR_CHECK",
            "MODULE_REPETITION_CHECK",
            "HUMAN_ENTERABLE_SCALE_VERDICT",
            "CONTAINER_OBJECTS",
            "CONTAINER_CAPACITY_RESEARCH",
            "CONTAINER_DIMENSION_RESEARCH",
            "CONTAINER_HUMAN_SCALE_ANCHORS",
            "CONTAINER_PROMPT_LOCKS",
        ):
            field_value = extract_field(text, field_name)
            if value_is_none_like(field_value) or count_meaningful_tokens(field_value) < 6:
                errors.append(f"Container-object research requires object-artifact {field_name} with occupancy/capacity scale information.")
        container_text = " ".join(
            filter(
                None,
                [
                    extract_field(text, "CONTAINER_CAPACITY_RESEARCH"),
                    extract_field(text, "CONTAINER_DIMENSION_RESEARCH"),
                    extract_field(text, "CONTAINER_HUMAN_SCALE_ANCHORS"),
                    extract_field(text, "CONTAINER_PROMPT_LOCKS"),
                    extract_field(text, "GENERATION_PROMPT_LOCKS"),
                ],
            )
        )
        if not contains_keyword(container_text, CONTAINER_CAPACITY_RESEARCH_KEYWORDS):
            errors.append("Container-object research must mention capacity/occupancy, seats/standing adults, cabin/interior volume, modules, doors/windows/aisles, or equivalent human-scale anchors.")
        internal_anchor_text = " ".join(
            filter(
                None,
                [
                    extract_field(text, "INTERNAL_HUMAN_ANATOMY_ANCHORS"),
                    extract_field(text, "OCCUPANT_BLEND_SCALE_PLAN"),
                    extract_field(text, "PROTAGONIST_MAIN_FIGURE_SCALE_LOCK"),
                    extract_field(text, "CONTAINER_HUMAN_SCALE_ANCHORS"),
                    extract_field(text, "GENERATION_PROMPT_LOCKS"),
                ],
            )
        )
        if not contains_keyword(internal_anchor_text, INTERNAL_HUMAN_ANCHOR_KEYWORDS):
            errors.append(
                "Human-enterable object research must define at least one internal human anatomy anchor "
                "(occupant/passenger/driver/mannequin/silhouette) and compare protagonist/main figures against it."
            )
        if not contains_keyword(extract_field(text, "PROTAGONIST_MAIN_FIGURE_SCALE_LOCK"), HUMANOID_SCALE_PARITY_KEYWORDS):
            errors.append("PROTAGONIST_MAIN_FIGURE_SCALE_LOCK must compare protagonist/main humans/humanoids against occupant anatomy and depth-plane perspective.")
        if not contains_keyword(extract_field(text, "SCALE_EMPHASIS_OVERRIDE_POLICY"), SCALE_EMPHASIS_OVERRIDE_KEYWORDS):
            errors.append("SCALE_EMPHASIS_OVERRIDE_POLICY must reject emphasis/drama/beauty/action scale changes and defer size to perspective/actual object size.")
        composite_checks = (
            ("ENTRY_FIT_CHECK", ENTRY_FIT_KEYWORDS),
            ("XYZ_VOLUME_CHECK", XYZ_VOLUME_KEYWORDS),
            ("CAPACITY_CLASS_CHECK", CAPACITY_CLASS_KEYWORDS),
            ("OCCUPANT_ANCHOR_CHECK", INTERNAL_HUMAN_ANCHOR_KEYWORDS),
            ("MODULE_REPETITION_CHECK", MODULE_REPETITION_KEYWORDS),
            ("HUMAN_ENTERABLE_SCALE_VERDICT", COMPOSITE_SCALE_VERDICT_KEYWORDS),
        )
        for field_name, keywords in composite_checks:
            field_value = extract_field(text, field_name)
            if value_is_none_like(field_value) or count_meaningful_tokens(field_value) < 4:
                errors.append(
                    f"Human-enterable object research requires object-artifact {field_name}; entry height alone cannot pass a container/tram/room."
                )
            elif not contains_keyword_korean_tolerant(field_value, keywords):
                errors.append(
                    f"Human-enterable object research {field_name} must include the relevant composite scale evidence, not generic prose."
                )
        composite_table = extract_field(text, "HUMAN_ENTERABLE_COMPOSITE_SCALE_TABLE")
        if not contains_keyword_korean_tolerant(
            composite_table,
            ENTRY_FIT_KEYWORDS + XYZ_VOLUME_KEYWORDS + CAPACITY_CLASS_KEYWORDS + INTERNAL_HUMAN_ANCHOR_KEYWORDS + MODULE_REPETITION_KEYWORDS,
        ):
            errors.append(
                "HUMAN_ENTERABLE_COMPOSITE_SCALE_TABLE must combine entry fit, XYZ volume, capacity class, occupant anchor, and module repetition in one row/table."
            )
        verdict_value = extract_field(text, "HUMAN_ENTERABLE_SCALE_VERDICT")
        if not value_indicates_pass(verdict_value):
            errors.append("HUMAN_ENTERABLE_SCALE_VERDICT must explicitly pass only after all composite subchecks pass.")
        for field_name in SCALE_CRITICAL_OBJECT_RATIO_FIELDS:
            field_value = extract_field(text, field_name)
            if value_is_none_like(field_value) or count_meaningful_tokens(field_value) < 4:
                errors.append(
                    f"Scale-critical container research requires object-artifact {field_name} with numeric ratio/threshold content."
                )
            elif not has_numeric_scale(field_value):
                errors.append(
                    f"Scale-critical container research requires object-artifact {field_name} to include a number, unit, ratio, percentage, or threshold."
                )
        ratio_text = " ".join(filter(None, [extract_field(text, field_name) for field_name in SCALE_CRITICAL_OBJECT_RATIO_FIELDS]))
        if not contains_keyword_korean_tolerant(ratio_text, SCALE_CRITICAL_RATIO_KEYWORDS):
            errors.append(
                "Scale-critical container ratio fields must mention ratio/threshold/height/width/length/screen occupancy/door/occupant/capacity logic, not prose-only scale language."
            )

    hand_expected = any(
        contains_keyword(field, HAND_KEYWORDS + FINGER_TOPOLOGY_KEYWORDS + HAND_PROP_INTERACTION_KEYWORDS)
        for field in (
            extract_field(text, "SOURCE_REQUEST"),
            extract_field(text, "REQUIRED_OBJECTS"),
            extract_field(text, "PER_OBJECT_DRAW_LOCKS"),
            extract_field(text, "GENERATION_PROMPT_LOCKS"),
        )
    )
    if hand_expected:
        cause = extract_field(text, "HAND_FAILURE_CAUSE_ANALYSIS")
        rescue = extract_field(text, "HAND_TOPOLOGY_RESCUE_PLAN")
        if value_is_none_like(cause) or count_meaningful_tokens(cause) < 8:
            errors.append("Visible/prop-holding hands require HAND_FAILURE_CAUSE_ANALYSIS in the object artifact.")
        elif not contains_keyword(cause, HAND_FAILURE_CAUSE_KEYWORDS):
            errors.append("HAND_FAILURE_CAUSE_ANALYSIS must name concrete causes such as prompt overload, small screen size, occlusion, prop/sleeve/blood/cloak absorption, or generic hand wording.")
        if value_is_none_like(rescue) or count_meaningful_tokens(rescue) < 8:
            errors.append("Visible/prop-holding hands require HAND_TOPOLOGY_RESCUE_PLAN in the object artifact.")
        elif not contains_keyword(rescue, FINGER_TOPOLOGY_KEYWORDS + SEPARATION_CUE_KEYWORDS):
            errors.append("HAND_TOPOLOGY_RESCUE_PLAN must name palm/thumb/finger topology plus concrete separation cues.")

    if expected_parent_spec_path is not None:
        parent_field = extract_field(text, "PARENT_SPEC_PATH")
        if not is_placeholder(parent_field):
            resolved_parent = resolve_reference_path(parent_field or "", artifact_path)
            if resolved_parent != expected_parent_spec_path.resolve():
                warnings.append(
                    f"Object artifact PARENT_SPEC_PATH points to {resolved_parent}, expected {expected_parent_spec_path.resolve()}."
                )

    invocation_log_field = extract_field(text, "INVOCATION_LOG_PATH")
    if not is_placeholder(invocation_log_field):
        invocation_log_path = resolve_reference_path(invocation_log_field or "", artifact_path)
        invocation_result = validate_object_research_invocation_log(
            invocation_log_path,
            spec_path=expected_parent_spec_path or artifact_path,
            artifact_path=artifact_path,
        )
        errors.extend(f"Object invocation log: {item}" for item in invocation_result.errors)
        warnings.extend(f"Object invocation log: {item}" for item in invocation_result.warnings)

    return ValidationResult(path=artifact_path, text=text, errors=errors, warnings=warnings)


def validate_piva_gates(text: str, render_bound_spec: bool, pre_image_handoff_ready: bool) -> list[str]:
    errors: list[str] = []
    if not render_bound_spec:
        return errors

    for field_name in PIVA_FIELDS:
        value = extract_field(text, field_name)
        if is_placeholder(value):
            errors.append(f"Missing or placeholder PIVA field: {field_name}")

    piva_mode = lower_value(extract_field(text, "PIVA_MODE"))
    if piva_mode != "enabled":
        errors.append("Render-bound specs require PIVA_MODE: enabled.")

    for field_name, allowed in PIVA_STATUS_FIELDS.items():
        value = lower_value(extract_field(text, field_name))
        if value and value not in allowed:
            errors.append(f"Invalid PIVA status in {field_name}: {value!r}. Allowed: {sorted(allowed)}")
        if pre_image_handoff_ready and field_name == "IMAGE_HANDOFF_GATE_STATUS" and value != "pass":
            errors.append("PRE_IMAGE_HANDOFF_READY/IMAGE_GEN_READY: yes requires IMAGE_HANDOFF_GATE_STATUS: pass.")
        elif pre_image_handoff_ready and field_name != "IMAGE_HANDOFF_GATE_STATUS" and value != "pass":
            errors.append(f"PRE_IMAGE_HANDOFF_READY/IMAGE_GEN_READY: yes requires {field_name}: pass.")

    plan_text = " ".join(
        filter(
            None,
            [
                extract_field(text, "USER_COMMAND_CHECKLIST"),
                extract_field(text, "PLAN_USER_COMMAND_SOURCE"),
                extract_field(text, "PLAN_NON_NEGOTIABLES"),
                extract_field(text, "PLAN_OBJECT_ANATOMY_SCALE_WITNESSES"),
                extract_field(text, "PLAN_HUMANOID_ANATOMY_SCALE_PARITY"),
            ],
        )
    )
    if count_meaningful_tokens(plan_text) < 20:
        errors.append("PIVA PLAN must capture user commands, non-negotiables, object/anatomy requirements, and scale witnesses in enough detail.")
    if not contains_keyword(plan_text, COMMAND_COMPLIANCE_KEYWORDS):
        errors.append("PIVA PLAN must use command/checklist/audit language tied to explicit user instructions.")
    if not contains_keyword(plan_text, HERO_OBJECT_SCALE_KEYWORDS):
        errors.append("PIVA PLAN must name protagonist/object scale witnesses such as passengers, humans, doors, windows, vehicles, props, architecture, or depth-plane transfer.")
    if not contains_keyword(plan_text, HUMANOID_SCALE_PARITY_KEYWORDS):
        errors.append("PIVA PLAN must define all visible humans/humanoids/humanoid monsters as anatomy scale-parity witnesses when present.")

    implement_text = " ".join(
        filter(
            None,
            [
                extract_field(text, "IMPLEMENT_STEP_MAP"),
                extract_field(text, "IMPLEMENT_OBJECT_RESEARCH_TRANSFER"),
                extract_field(text, "IMPLEMENT_SCALE_TRANSFER"),
                extract_field(text, "IMPLEMENT_HUMANOID_SCALE_TRANSFER"),
                extract_field(text, "IMPLEMENT_STYLE_TRANSFER"),
                extract_field(text, "IMPLEMENT_PROMPT_DRAFT_TRANSFER"),
            ],
        )
    )
    if count_meaningful_tokens(implement_text) < 25:
        errors.append("PIVA IMPLEMENT must map PLAN requirements through Step 0-8, object research, scale transfer, style transfer, and prompt drafting.")
    if not contains_keyword(implement_text, PIVA_TRANSFER_KEYWORDS):
        errors.append("PIVA IMPLEMENT must explicitly describe transfer/mapping into steps, prompt locks, verify tests, or audit verdicts.")

    verify_text = " ".join(
        filter(
            None,
            [
                extract_field(text, "VERIFY_OBJECT_DISTORTION_TEST"),
                extract_field(text, "VERIFY_HERO_OBJECT_SCALE_TEST"),
                extract_field(text, "VERIFY_HUMANOID_SCALE_PARITY_TEST"),
                extract_field(text, "VERIFY_OBJECT_RESEARCH_TRANSFER_TEST"),
                extract_field(text, "VERIFY_STYLE_TARGET_TEST"),
                extract_field(text, "VERIFY_PROMPT_CONFLICT_TEST"),
            ],
        )
    )
    if count_meaningful_tokens(verify_text) < 25:
        errors.append("PIVA VERIFY must define pre-image tests for object distortion, hero/object scale, research transfer, style target, and prompt conflicts.")
    if not contains_keyword(verify_text, OBJECT_DISTORTION_KEYWORDS):
        errors.append("PIVA VERIFY must include an object distortion/no-warp/no-melt/no-resize test.")
    if not contains_keyword(verify_text, HERO_OBJECT_SCALE_KEYWORDS):
        errors.append("PIVA VERIFY must include a protagonist-to-object scale test.")
    if not contains_keyword(verify_text, HUMANOID_SCALE_PARITY_KEYWORDS):
        errors.append("PIVA VERIFY must include a protagonist-to-secondary-humanoid scale parity test.")

    audit_text = " ".join(
        filter(
            None,
            [
                extract_field(text, "AUDIT_PRE_IMAGE_COMMAND_AUDIT"),
                extract_field(text, "AUDIT_PRE_IMAGE_NON_NEGOTIABLE_AUDIT"),
                extract_field(text, "AUDIT_HUMANOID_SCALE_PARITY_TRIGGER"),
                extract_field(text, "AUDIT_POST_IMAGE_VISUAL_AUDIT_PLAN"),
                extract_field(text, "AUDIT_RERENDER_TRIGGERS"),
            ],
        )
    )
    if count_meaningful_tokens(audit_text) < 25:
        errors.append("PIVA AUDIT must define command audit, non-negotiable audit, post-image visual audit plan, and rerender triggers.")
    if not contains_keyword(audit_text, COMMAND_COMPLIANCE_KEYWORDS):
        errors.append("PIVA AUDIT must audit every command/non-negotiable with explicit compliance language.")
    if not contains_keyword(audit_text, PIVA_RERENDER_KEYWORDS):
        errors.append("PIVA AUDIT must define concrete fail/rerender/revision triggers.")
    if not contains_keyword(audit_text, HUMANOID_SCALE_PARITY_KEYWORDS):
        errors.append("PIVA AUDIT must include humanoid scale-parity fail/rerender triggers.")

    return errors


def validate_render_style_baseline_gate(text: str, render_bound_spec: bool, pre_image_handoff_ready: bool) -> list[str]:
    """Validate the up-front render-family decision gate.

    This gate prevents prompts from silently mixing 2D anime, semi-real
    concept art, 3D render, live-action/cosplay photo, and game-CG key visual
    signals. Render-bound specs must record the user's chosen primary axis and
    the permitted mix before any image handoff.
    """
    errors: list[str] = []
    if not render_bound_spec:
        return errors

    question = extract_field(text, "RENDER_STYLE_BASELINE_QUESTION")
    user_decision = extract_field(text, "RENDER_STYLE_USER_DECISION")
    primary_axis = lower_value(extract_field(text, "RENDER_STYLE_PRIMARY_AXIS"))
    secondary_axes = lower_value(extract_field(text, "RENDER_STYLE_SECONDARY_AXES"))
    mixing_policy = extract_field(text, "RENDER_STYLE_MIXING_POLICY")
    drift_guard = extract_field(text, "RENDER_STYLE_DRIFT_GUARD")
    prompt_anchor = extract_field(text, "RENDER_STYLE_PROMPT_ANCHOR")

    question_lower = lower_value(question)
    missing_axes = [axis for axis in sorted(RENDER_STYLE_AXES) if axis not in question_lower]
    if missing_axes:
        errors.append(
            "RENDER_STYLE_BASELINE_QUESTION must ask the user using all five render-style axes: "
            + ", ".join(sorted(RENDER_STYLE_AXES))
            + "."
        )
    if not contains_keyword_korean_tolerant(question, RENDER_STYLE_MIX_KEYWORDS):
        errors.append("RENDER_STYLE_BASELINE_QUESTION must include recommended/allowed mix guidance, not only five isolated labels.")

    if primary_axis not in RENDER_STYLE_PRIMARY_ALLOWED:
        errors.append(
            f"RENDER_STYLE_PRIMARY_AXIS must be one of {sorted(RENDER_STYLE_PRIMARY_ALLOWED)}, got {primary_axis!r}."
        )
    if secondary_axes and secondary_axes != "none":
        secondary_tokens = [
            token.strip()
            for token in re.split(r"[,|/]+|\s+\+\s+|\s+and\s+", secondary_axes)
            if token.strip()
        ]
        invalid_secondary = [
            token
            for token in secondary_tokens
            if token not in RENDER_STYLE_AXES and token != "custom_mix"
        ]
        if invalid_secondary:
            errors.append(
                "RENDER_STYLE_SECONDARY_AXES may only list approved axes, custom_mix, or none; invalid: "
                + ", ".join(invalid_secondary)
            )

    if contains_keyword_korean_tolerant(user_decision, RENDER_STYLE_PENDING_MARKERS):
        errors.append("RENDER_STYLE_USER_DECISION is pending/assumed; ask the user which render-style axis/mix to use before proceeding.")
    elif count_meaningful_tokens(user_decision) < 2:
        errors.append("RENDER_STYLE_USER_DECISION must quote or summarize the user's render-style choice.")

    if not contains_keyword_korean_tolerant(mixing_policy, RENDER_STYLE_MIX_KEYWORDS):
        errors.append("RENDER_STYLE_MIXING_POLICY must state an allowed/recommended or forbidden mix combination.")
    if not contains_keyword_korean_tolerant(drift_guard, RENDER_STYLE_DRIFT_KEYWORDS):
        errors.append("RENDER_STYLE_DRIFT_GUARD must explicitly name render-family drift to forbid or avoid.")
    if count_meaningful_tokens(prompt_anchor) < 5:
        errors.append("RENDER_STYLE_PROMPT_ANCHOR must provide a concrete first-sentence render-family anchor for the final prompt.")
    if pre_image_handoff_ready and contains_keyword_korean_tolerant(
        " ".join(filter(None, [user_decision, primary_axis, mixing_policy, prompt_anchor])),
        RENDER_STYLE_PENDING_MARKERS,
    ):
        errors.append("PRE_IMAGE_HANDOFF_READY: yes requires the render-style baseline gate to be resolved, not pending/assumed.")

    return errors


def validate_spec_path(path: Path, strict_object_research: bool = False) -> ValidationResult:
    if not path.exists():
        return ValidationResult(path=path, text="", errors=[f"file not found: {path}"], warnings=[])

    text = normalize_text(path)
    errors: list[str] = []
    warnings: list[str] = []

    if "[ILLUSTRATE_SPEC]" not in text or "[/ILLUSTRATE_SPEC]" not in text:
        errors.append("Missing [ILLUSTRATE_SPEC] wrapper block.")

    sections = section_blocks(text)
    for heading in SECTION_ORDER:
        if heading not in sections:
            errors.append(f"Missing section heading: {heading}")

    if errors:
        return ValidationResult(path=path, text=text, errors=errors, warnings=warnings, sections=sections)

    for field_name in GLOBAL_FIELDS:
        value = extract_field(text, field_name)
        if is_placeholder(value):
            errors.append(f"Missing or placeholder global field: {field_name}")

    for field_name, allowed in BOOLEAN_FIELDS.items():
        value = extract_field(text, field_name)
        if value is not None and not is_placeholder(value):
            if lower_value(value) not in allowed:
                errors.append(f"Invalid value for {field_name}: {value!r}. Allowed: {sorted(allowed)}")

    for field_name, allowed in ENUM_FIELDS.items():
        value = extract_field(text, field_name)
        if value is not None and not is_placeholder(value):
            if lower_value(value) not in allowed:
                errors.append(f"Invalid value for {field_name}: {value!r}. Allowed: {sorted(allowed)}")

    render_bound_spec = is_render_bound_spec(text)
    pre_image_handoff_ready = is_pre_image_handoff_ready(text)
    errors.extend(validate_piva_gates(text, render_bound_spec, pre_image_handoff_ready))
    errors.extend(validate_render_style_baseline_gate(text, render_bound_spec, pre_image_handoff_ready))

    for heading, field_names in SECTION_FIELDS.items():
        block = sections[heading]
        legacy_missing_blender_fields = (
            heading == "## Step 2.8 3D Blockout / Modeling Contract"
            and extract_field(block, "BLENDER_BLOCKOUT_REQUIRED") is None
        )
        if legacy_missing_blender_fields:
            if render_bound_spec:
                errors.append("Render-bound specs must include the Step 2.8 Blender hard-route fields.")
            else:
                warnings.append(
                    "Step 2.8 is using the pre-Blender-route schema; add Blender blockout fields for new render-bound specs."
                )
        for field_name in field_names:
            value = extract_field(block, field_name)
            if legacy_missing_blender_fields and not render_bound_spec and field_name in BLENDER_STEP_FIELDS:
                continue
            if is_placeholder(value):
                errors.append(f"Missing or placeholder field in {heading}: {field_name}")

            if field_name in STATUS_FIELDS and value and not is_placeholder(value):
                if lower_value(value) not in STATUS_FIELDS[field_name]:
                    errors.append(
                        f"Invalid status in {heading} for {field_name}: {value!r}. "
                        f"Allowed: {sorted(STATUS_FIELDS[field_name])}"
                    )

        if heading == "## Step 2.6 Object Relationship Check":
            apply_status = extract_field(block, "APPLY_STATUS")
            if apply_status and not is_placeholder(apply_status):
                if lower_value(apply_status) not in APPLY_STATUS_VALUES:
                    errors.append(
                        f"Invalid APPLY_STATUS in {heading}: {apply_status!r}. "
                        f"Allowed: {sorted(APPLY_STATUS_VALUES)}"
                    )

    step0_block = sections["## Step 0 Route Gate"]
    step1_block = sections["## Step 1 Intent"]
    step2_block = sections["## Step 2 Composition"]
    step2_1_block = sections["## Step 2.1 Perspective Rig"]
    step2_2_block = sections["## Step 2.2 Object Inventory from Perspective"]
    step2_2m_block = sections["## Step 2.2M Merge Gate: Normalized Scene Graph"]
    step2_3_block = sections["## Step 2.3 Anatomy Structure Gate"]
    step2_4_block = sections["## Step 2.4 Object Knowledge Query Plan"]
    step2_5_block = sections["## Step 2.5 Object Research Handoff"]
    step2_6_block = sections["## Step 2.6 Object Relationship Check"]
    step2_7_block = sections["## Step 2.7 Anatomy-on-Object Relationship Check"]
    step2_8_block = sections["## Step 2.8 3D Blockout / Modeling Contract"]
    step2_9_block = sections["## Step 2.9 Image Translation Lock"]
    step3_block = sections["## Step 3 Value"]
    step4_block = sections["## Step 4 Face"]
    step5_block = sections["## Step 5 Line & Shape"]
    step6_block = sections["## Step 6 Color & Accent"]
    step8_block = sections["## Step 8 Final Check"]

    emotion_axis = extract_field(step1_block, "EMOTION_AXIS")
    emotion_parts = split_emotion_axis(emotion_axis)
    if emotion_parts and not (1 <= len(emotion_parts) <= 2):
        errors.append(
            f"EMOTION_AXIS should contain 1-2 emotion axes, but found {len(emotion_parts)}: {emotion_parts}"
        )

    request_summary = extract_field(text, "REQUEST_SUMMARY")
    user_command_checklist = extract_field(text, "USER_COMMAND_CHECKLIST")
    scale_critical_mode = lower_value(extract_field(text, "SCALE_CRITICAL_MODE"))
    scale_critical_reason = extract_field(text, "SCALE_CRITICAL_REASON")
    image_ready_value = "yes" if pre_image_handoff_ready else "no"
    post_image_verdict_required = is_post_image_verdict_required(text)
    post_image_accepted_value = lower_value(extract_field(text, "POST_IMAGE_ACCEPTED"))
    action_field = extract_field(step1_block, "ACTION")
    camera_angle = extract_field(step2_block, "CAMERA_ANGLE")
    user_camera_class_preset_global = extract_field(text, "USER_CAMERA_CLASS_PRESET")
    user_camera_class_lock_global = lower_value(extract_field(text, "USER_CAMERA_CLASS_LOCK_LEVEL"))
    user_camera_class_reason_global = extract_field(text, "USER_CAMERA_CLASS_REASON")
    user_camera_class_preset_step = extract_field(step2_block, "USER_CAMERA_CLASS_PRESET")
    user_camera_class_lock_step = lower_value(extract_field(step2_block, "USER_CAMERA_CLASS_LOCK_LEVEL"))
    camera_class_conflict_status = lower_value(extract_field(step2_block, "CAMERA_CLASS_CONFLICT_STATUS"))
    camera_class_conflict_reason = extract_field(step2_block, "CAMERA_CLASS_CONFLICT_REASON")
    camera_class_resolution = extract_field(step2_block, "CAMERA_CLASS_RESOLUTION")
    chosen_camera_class = extract_field(step2_block, "CHOSEN_CAMERA_CLASS")
    camera_class_visual_translation = extract_field(step2_block, "CAMERA_CLASS_VISUAL_TRANSLATION")

    input_route_global = lower_value(extract_field(text, "INPUT_ROUTE"))
    input_route_step = lower_value(extract_field(step0_block, "INPUT_ROUTE"))
    existing_image_input = lower_value(extract_field(step0_block, "EXISTING_IMAGE_INPUT"))
    prompt_only_generation = lower_value(extract_field(step0_block, "PROMPT_ONLY_GENERATION"))
    source_image_actual_conditioning_global = lower_value(extract_field(text, "SOURCE_IMAGE_ACTUAL_CONDITIONING"))
    source_image_actual_conditioning_step = lower_value(extract_field(step0_block, "SOURCE_IMAGE_ACTUAL_CONDITIONING"))
    image_development_allowed_global = lower_value(extract_field(text, "IMAGE_DEVELOPMENT_ALLOWED"))
    image_development_allowed_step = lower_value(extract_field(step0_block, "IMAGE_DEVELOPMENT_ALLOWED"))
    image_development_conditioning_note = extract_field(step0_block, "IMAGE_DEVELOPMENT_CONDITIONING_NOTE")
    active_intake_branch = lower_value(extract_field(step0_block, "ACTIVE_INTAKE_BRANCH"))
    merged_from_route = lower_value(extract_field(step2_2m_block, "MERGED_FROM_ROUTE"))
    route_a_block = extract_named_section(text, "## Step 0A Existing Image Development Intake")
    route_b_block = extract_named_section(text, "## Step 0B Prompt-Only Intake")

    if input_route_global != input_route_step:
        errors.append("Global INPUT_ROUTE and Step 0 INPUT_ROUTE must match exactly.")
    if source_image_actual_conditioning_global != source_image_actual_conditioning_step:
        errors.append("Global SOURCE_IMAGE_ACTUAL_CONDITIONING and Step 0 SOURCE_IMAGE_ACTUAL_CONDITIONING must match exactly.")
    if image_development_allowed_global != image_development_allowed_step:
        errors.append("Global IMAGE_DEVELOPMENT_ALLOWED and Step 0 IMAGE_DEVELOPMENT_ALLOWED must match exactly.")
    if input_route_global == "image_development":
        if existing_image_input != "yes" or prompt_only_generation != "no":
            errors.append("INPUT_ROUTE: image_development requires EXISTING_IMAGE_INPUT: yes and PROMPT_ONLY_GENERATION: no.")
        if source_image_actual_conditioning_global not in {"yes", "no"}:
            errors.append(
                "INPUT_ROUTE: image_development requires SOURCE_IMAGE_ACTUAL_CONDITIONING: yes or no "
                "so the run distinguishes real image conditioning from text-only reinterpretation."
            )
        if image_development_allowed_global not in {"yes", "blocked", "prompt_only_fallback"}:
            errors.append(
                "INPUT_ROUTE: image_development requires IMAGE_DEVELOPMENT_ALLOWED: yes, blocked, or prompt_only_fallback."
            )
        if count_meaningful_tokens(image_development_conditioning_note) < 4:
            errors.append(
                "INPUT_ROUTE: image_development requires IMAGE_DEVELOPMENT_CONDITIONING_NOTE explaining whether the source image is actually conditionable."
            )
        if source_image_actual_conditioning_global == "yes" and image_development_allowed_global not in {"yes", "blocked"}:
            errors.append(
                "SOURCE_IMAGE_ACTUAL_CONDITIONING: yes should set IMAGE_DEVELOPMENT_ALLOWED: yes unless the run is explicitly blocked."
            )
        if source_image_actual_conditioning_global == "no":
            if image_development_allowed_global == "yes":
                errors.append(
                    "IMAGE_DEVELOPMENT_ALLOWED cannot be yes when SOURCE_IMAGE_ACTUAL_CONDITIONING is no; "
                    "mark prompt_only_fallback or blocked instead."
                )
            if image_development_allowed_global == "prompt_only_fallback" and not contains_keyword(
                image_development_conditioning_note,
                ["fallback", "reinterpret", "descriptive", "text-only", "prompt-only", "재해석", "텍스트", "프롬프트", "참조"],
            ):
                errors.append(
                    "prompt_only_fallback image-development runs must state that generation is a descriptive reinterpretation, not true source-image conditioning."
                )
        if pre_image_handoff_ready and image_development_allowed_global == "blocked":
            errors.append(
                "PRE_IMAGE_HANDOFF_READY cannot be yes while IMAGE_DEVELOPMENT_ALLOWED is blocked."
            )
        if active_intake_branch != "step_0a_existing_image_development":
            errors.append("INPUT_ROUTE: image_development requires ACTIVE_INTAKE_BRANCH: step_0a_existing_image_development.")
        if lower_value(extract_field(text, "SOURCE_IMAGE_UPGRADE")) != "yes":
            errors.append("INPUT_ROUTE: image_development must set SOURCE_IMAGE_UPGRADE: yes.")
        if not route_a_block:
            errors.append("INPUT_ROUTE: image_development requires ## Step 0A Existing Image Development Intake.")
        else:
            for field_name in IMAGE_DEVELOPMENT_BRANCH_FIELDS:
                value = extract_field(route_a_block, field_name)
                if is_placeholder(value):
                    errors.append(f"Active image-development branch is missing field: {field_name}")
            if lower_value(extract_field(route_a_block, "GATE_STATUS")) != "pass":
                errors.append("Active image-development branch requires GATE_STATUS: pass.")
        if route_b_block and lower_value(extract_field(route_b_block, "GATE_STATUS")) not in {"not_applicable", ""}:
            errors.append("Inactive prompt-only branch should use GATE_STATUS: not_applicable.")
    elif input_route_global == "prompt_only":
        if existing_image_input != "no" or prompt_only_generation != "yes":
            errors.append("INPUT_ROUTE: prompt_only requires EXISTING_IMAGE_INPUT: no and PROMPT_ONLY_GENERATION: yes.")
        if source_image_actual_conditioning_global != "not_applicable":
            errors.append("INPUT_ROUTE: prompt_only requires SOURCE_IMAGE_ACTUAL_CONDITIONING: not_applicable.")
        if image_development_allowed_global != "not_applicable":
            errors.append("INPUT_ROUTE: prompt_only requires IMAGE_DEVELOPMENT_ALLOWED: not_applicable.")
        if active_intake_branch != "step_0b_prompt_only":
            errors.append("INPUT_ROUTE: prompt_only requires ACTIVE_INTAKE_BRANCH: step_0b_prompt_only.")
        if lower_value(extract_field(text, "SOURCE_IMAGE_UPGRADE")) != "no":
            errors.append("INPUT_ROUTE: prompt_only must set SOURCE_IMAGE_UPGRADE: no.")
        if not route_b_block:
            errors.append("INPUT_ROUTE: prompt_only requires ## Step 0B Prompt-Only Intake.")
        else:
            for field_name in PROMPT_ONLY_BRANCH_FIELDS:
                value = extract_field(route_b_block, field_name)
                if is_placeholder(value):
                    errors.append(f"Active prompt-only branch is missing field: {field_name}")
            if lower_value(extract_field(route_b_block, "GATE_STATUS")) != "pass":
                errors.append("Active prompt-only branch requires GATE_STATUS: pass.")
        if route_a_block and lower_value(extract_field(route_a_block, "GATE_STATUS")) not in {"not_applicable", ""}:
            errors.append("Inactive image-development branch should use GATE_STATUS: not_applicable.")

    if merged_from_route != input_route_global:
        errors.append("Step 2.2M MERGED_FROM_ROUTE must match INPUT_ROUTE so both intake paths merge into one canonical scene graph.")

    action_contact_expected = any(
        contains_keyword_korean_tolerant(field, ACTION_CONTACT_KEYWORDS)
        for field in (
            request_summary,
            user_command_checklist,
            action_field,
            extract_field(step2_block, "COMPOSITION_OBJECT_ROLE_SUMMARY"),
            extract_field(step2_2_block, "SOURCE_IMAGE_OBJECTS_PRESENT"),
            extract_field(step2_5_block, "REQUIRED_OBJECTS"),
        )
    )
    garment_attachment_expected = any(
        contains_keyword_korean_tolerant(field, GARMENT_ATTACHMENT_KEYWORDS)
        for field in (
            request_summary,
            user_command_checklist,
            extract_field(step2_2_block, "SOURCE_IMAGE_OBJECTS_PRESENT"),
            extract_field(step2_2_block, "OCCLUDER_MASS_INVENTORY"),
            extract_field(step2_5_block, "REQUIRED_OBJECTS"),
        )
    )

    grounded_pose_expected = any(
        contains_keyword(field, GROUNDED_POSE_KEYWORDS)
        for field in (request_summary, action_field, camera_angle)
    )
    exaggerated_pose_expected = any(
        contains_keyword(field, EXAGGERATED_PROPORTION_KEYWORDS)
        for field in (request_summary, action_field, camera_angle)
    )

    if grounded_pose_expected or exaggerated_pose_expected:
        support_note = extract_field(step2_3_block, "SUPPORTING_LEG_NOTE")
        balance_note = extract_field(step2_3_block, "BALANCE_LINE_NOTE")
        tilt_note = extract_field(step2_3_block, "SHOULDER_PELVIS_TILT_NOTE")
        if count_meaningful_tokens(support_note) < 4:
            errors.append(
                "Grounded or exaggerated full-body poses need a meaningful SUPPORTING_LEG_NOTE in Step 2."
            )
        if count_meaningful_tokens(balance_note) < 4:
            errors.append(
                "Grounded or exaggerated full-body poses need a meaningful BALANCE_LINE_NOTE in Step 2."
            )
        if count_meaningful_tokens(tilt_note) < 4:
            errors.append(
                "Grounded or exaggerated full-body poses need a meaningful SHOULDER_PELVIS_TILT_NOTE in Step 2."
            )

    visible_hands_and_poses = extract_field(step2_3_block, "VISIBLE_HANDS_AND_POSES")
    hand_silhouette_note = extract_field(step2_3_block, "HAND_SILHOUETTE_NOTE")
    finger_grouping_note = extract_field(step2_3_block, "FINGER_GROUPING_NOTE")
    hands_visible_expected = likely_visible_hands(
        request_summary,
        action_field,
        extract_field(step2_2_block, "SOURCE_IMAGE_OBJECTS_PRESENT"),
        visible_hands_and_poses,
    )
    weapon_grip_expected = hands_visible_expected and any(
        contains_keyword(field, SWORD_KEYWORDS + ["weapon", "hilt", "handle", "grip", "무기", "손잡이", "쥐"])
        for field in (
            request_summary,
            user_command_checklist,
            action_field,
            extract_field(step2_2_block, "SOURCE_IMAGE_OBJECTS_PRESENT"),
            extract_field(step2_5_block, "REQUIRED_OBJECTS"),
            visible_hands_and_poses,
        )
    )

    if hands_visible_expected:
        if value_is_none_like(visible_hands_and_poses):
            errors.append(
                "Visible, gripping, or gesture-critical hands are implied, so Step 2.3 must fill VISIBLE_HANDS_AND_POSES."
            )
        if count_meaningful_tokens(hand_silhouette_note) < 4:
            errors.append(
                "Visible hands require a meaningful HAND_SILHOUETTE_NOTE in Step 2.3."
            )
        if count_meaningful_tokens(finger_grouping_note) < 4:
            errors.append(
                "Visible hands require a meaningful FINGER_GROUPING_NOTE in Step 2.3; despite the legacy field name, fill it with individual finger-chain modeling rather than finger grouping/fusion."
            )

    anatomy_required_expected = likely_requires_anatomy_gate(
        request_summary,
        action_field,
        camera_angle,
        extract_field(step2_block, "CHARACTER_POSITION"),
        visible_hands_and_poses,
    ) or hands_visible_expected

    scene_contract_required = render_bound_spec or pre_image_handoff_ready
    if scene_contract_required:
        scene_contract_fields = (
            ("SCENE_CONTRACT_VERSION", extract_field(step2_2m_block, "SCENE_CONTRACT_VERSION")),
            ("OBJECT_REGISTRY", extract_field(step2_2m_block, "OBJECT_REGISTRY")),
            ("RELATIONSHIP_CONTRACT", extract_field(step2_2m_block, "RELATIONSHIP_CONTRACT")),
            ("SCALE_PARITY_CONTRACT", extract_field(step2_2m_block, "SCALE_PARITY_CONTRACT")),
            ("PROTECTED_ANATOMY_CHAINS", extract_field(step2_2m_block, "PROTECTED_ANATOMY_CHAINS")),
        )
        for field_name, field_value in scene_contract_fields:
            if value_is_none_like(field_value) or count_meaningful_tokens(field_value) < 4:
                errors.append(
                    f"Render-bound specs require Step 2.2M {field_name} as part of the canonical Scene Contract before prompt translation."
                )

        object_registry = extract_field(step2_2m_block, "OBJECT_REGISTRY")
        if object_registry and not re.search(r"\b[A-Z][A-Z0-9_]*\d+\b", object_registry):
            errors.append(
                "Step 2.2M OBJECT_REGISTRY must assign stable object ids such as H1, T1, D2, or K1; prose-only object lists are not enough."
            )

        relationship_contract = extract_field(step2_2m_block, "RELATIONSHIP_CONTRACT")
        if relationship_contract and not contains_keyword(
            relationship_contract,
            ["stands_on", "attached_to", "cuts", "contacts", "inside", "contains", "scale", "on", "in", "support", "부착", "접촉", "안", "위", "스케일"],
        ):
            errors.append(
                "Step 2.2M RELATIONSHIP_CONTRACT must use explicit relationship verbs such as stands_on, attached_to, cuts/contacts, inside/contains, or scale parity."
            )

        protected_chains = extract_field(step2_2m_block, "PROTECTED_ANATOMY_CHAINS")
        if anatomy_required_expected and not contains_keyword(protected_chains, PROTECTED_CHAIN_KEYWORDS):
            errors.append(
                "Step 2.2M PROTECTED_ANATOMY_CHAINS must name visible anatomy chains/landmarks that may not be absorbed by objects or effects."
            )
        if hands_visible_expected and not contains_keyword(
            protected_chains,
            ["left", "right", "both", "off hand", "sword hand", "왼", "오른", "양팔", "양손", "보조손", "검손"],
        ):
            errors.append(
                "Hand/weapon scenes require Step 2.2M PROTECTED_ANATOMY_CHAINS to distinguish both sides or named hand roles so one arm cannot vanish or sprout extra hands."
            )

        scale_parity_contract = extract_field(step2_2m_block, "SCALE_PARITY_CONTRACT")
        if scale_parity_contract and contains_keyword(
            " ".join(filter(None, [request_summary, extract_field(step2_5_block, "REQUIRED_OBJECTS")])),
            HUMANOID_OBJECT_KEYWORDS + VEHICLE_SCALE_KEYWORDS,
        ) and not contains_keyword(scale_parity_contract, HUMANOID_SCALE_PARITY_KEYWORDS + PERSPECTIVE_ONLY_SCALE_KEYWORDS):
            errors.append(
                "Step 2.2M SCALE_PARITY_CONTRACT must name the protagonist/secondary humanoid scale relationship and reject miniature/doll/giant/texture humans."
            )

        if lower_value(extract_field(step2_2m_block, "SCENE_CONTRACT_GATE_STATUS")) != "pass":
            errors.append("Render-bound specs require Step 2.2M SCENE_CONTRACT_GATE_STATUS: pass before downstream steps.")

    if action_contact_expected:
        action_contact_contract = extract_field(step2_2m_block, "ACTION_CONTACT_CONTRACT")
        if value_is_none_like(action_contact_contract) or count_meaningful_tokens(action_contact_contract) < 8:
            errors.append(
                "Action/contact scenes require Step 2.2M ACTION_CONTACT_CONTRACT with actor, tool/body part, target object/subpart, contact landmarks, and forbidden targets."
            )
        elif not contains_keyword_korean_tolerant(action_contact_contract, ACTION_CONTACT_CONTRACT_KEYWORDS):
            errors.append(
                "Step 2.2M ACTION_CONTACT_CONTRACT must explicitly name actor/tool/target/contact/forbidden-target roles."
            )
        post_action_state_contract = extract_field(step2_2m_block, "POST_ACTION_OBJECT_STATE_CONTRACT")
        target_cut_plane_contract = extract_field(step2_2m_block, "TARGET_CUT_PLANE_VISIBILITY_CONTRACT")
        for field_name, field_value in (
            ("POST_ACTION_OBJECT_STATE_CONTRACT", post_action_state_contract),
            ("TARGET_CUT_PLANE_VISIBILITY_CONTRACT", target_cut_plane_contract),
        ):
            if value_is_none_like(field_value) or count_meaningful_tokens(field_value) < 8:
                errors.append(
                    f"Action/cut scenes require Step 2.2M {field_name} so the post-action object state and target cut plane cannot be hidden or improvised."
                )
            elif not contains_keyword_korean_tolerant(field_value, CUT_PLANE_VISIBILITY_KEYWORDS):
                errors.append(
                    f"{field_name} must name the visible cut plane/cross-section, head-side/body-side continuity, and unknown-form/occlusion failure triggers."
                )

    if garment_attachment_expected:
        garment_attachment_contract = extract_field(step2_2m_block, "GARMENT_ATTACHMENT_CONTRACT")
        if value_is_none_like(garment_attachment_contract) or count_meaningful_tokens(garment_attachment_contract) < 8:
            errors.append(
                "Cloak/cape/hood/large-garment scenes require Step 2.2M GARMENT_ATTACHMENT_CONTRACT before the garment can enter prompt/style stages."
            )
        elif not contains_keyword_korean_tolerant(garment_attachment_contract, GARMENT_ATTACHMENT_CONTRACT_KEYWORDS):
            errors.append(
                "GARMENT_ATTACHMENT_CONTRACT must name attachment/origin landmarks such as shoulders, collar, neck, back, clasp, or anchor points."
            )

    if render_bound_spec:
        if user_camera_class_lock_global != user_camera_class_lock_step:
            errors.append("Global USER_CAMERA_CLASS_LOCK_LEVEL and Step 2 USER_CAMERA_CLASS_LOCK_LEVEL must match exactly.")
        if normalize_camera_class(user_camera_class_preset_global) != normalize_camera_class(user_camera_class_preset_step):
            errors.append("Global USER_CAMERA_CLASS_PRESET and Step 2 USER_CAMERA_CLASS_PRESET must match exactly.")
        for label, value in (
            ("USER_CAMERA_CLASS_REASON", user_camera_class_reason_global),
            ("Step 2 USER_CAMERA_CLASS_REASON", extract_field(step2_block, "USER_CAMERA_CLASS_REASON")),
            ("CHOSEN_CAMERA_CLASS", chosen_camera_class),
            ("CAMERA_CLASS_VISUAL_TRANSLATION", camera_class_visual_translation),
        ):
            if value_is_none_like(value) or count_meaningful_tokens(value) < 2:
                errors.append(
                    f"Render-bound specs require {label} so camera class is a first-class composition input, not an implicit prompt adjective."
                )
        if user_camera_class_lock_global == "hard" and not value_is_none_like(user_camera_class_preset_global):
            if normalize_camera_class(chosen_camera_class) != normalize_camera_class(user_camera_class_preset_global):
                errors.append(
                    "USER_CAMERA_CLASS_LOCK_LEVEL: hard requires CHOSEN_CAMERA_CLASS to preserve the user preset unless the user explicitly changes it."
                )
        if camera_class_conflict_status in {"conflict", "resolved"}:
            if count_meaningful_tokens(camera_class_conflict_reason) < 4:
                errors.append("CAMERA_CLASS_CONFLICT_STATUS requires a concrete CAMERA_CLASS_CONFLICT_REASON.")
            if count_meaningful_tokens(camera_class_resolution) < 4:
                errors.append("CAMERA_CLASS_CONFLICT_STATUS requires a concrete CAMERA_CLASS_RESOLUTION.")

    perspective_expected = any(
        contains_keyword(field, PERSPECTIVE_SCENE_KEYWORDS)
        for field in (
            request_summary,
            extract_field(step1_block, "ENVIRONMENT"),
            camera_angle,
            extract_field(step2_2_block, "SUPPORT_PLANE_OBJECTS"),
            extract_field(step2_2_block, "BACKGROUND_DEPTH_OBJECTS"),
        )
    )
    if perspective_expected:
        for field_name in (
            "HORIZON_LINE",
            "VANISHING_POINTS",
            "PRIMARY_DEPTH_AXIS",
            "SUPPORT_PLANES",
            "SCALE_ANCHOR_OBJECTS",
            "SCALE_ANCHOR_CANDIDATES",
            "SCALE_BASELINE_SELECTION",
            "SCALE_ANCHOR_RANKING",
            "SCALE_RATIO_JUDGMENT_METHOD",
            "NEAR_PLANE_ANCHOR_CHECK",
            "DEPTH_PLANE_SCALE_TRANSFER",
            "FUNCTIONAL_SIZE_TESTS",
            "SCALE_ANCHOR_FAIL_CONDITIONS",
            "SCALE_ANCHOR_VERDICT_HANDOFF",
            "CONTACT_PLANES",
            "PERSPECTIVE_FAIL_CONDITIONS",
        ):
            if count_meaningful_tokens(extract_field(step2_1_block, field_name)) < 4:
                errors.append(f"Perspective-heavy scenes require a meaningful Step 2.1 {field_name}.")

    scale_anchor_expected = perspective_expected or any(
        contains_keyword(field, SCALE_FUNCTION_KEYWORDS)
        for field in (
            request_summary,
            extract_field(step1_block, "ENVIRONMENT"),
            action_field,
            camera_angle,
            extract_field(step2_1_block, "SCALE_ANCHOR_OBJECTS"),
            extract_field(step2_2_block, "SOURCE_IMAGE_OBJECTS_PRESENT"),
            extract_field(step2_2_block, "SUPPORT_PLANE_OBJECTS"),
            extract_field(step2_5_block, "REQUIRED_OBJECTS"),
        )
    )
    if scale_anchor_expected:
        for field_name in (
            "SCALE_ANCHOR_CANDIDATES",
            "SCALE_BASELINE_SELECTION",
            "SCALE_ANCHOR_RANKING",
            "SCALE_RATIO_JUDGMENT_METHOD",
            "FUNCTIONAL_SIZE_TESTS",
            "SCALE_ANCHOR_FAIL_CONDITIONS",
            "SCALE_ANCHOR_VERDICT_HANDOFF",
        ):
            value = extract_field(step2_1_block, field_name)
            if count_meaningful_tokens(value) < 6:
                errors.append(f"Scale-anchor scenes require Step 2.1 {field_name} to document the scale judgment process.")
        scale_process_text = " ".join(
            filter(
                None,
                [
                    extract_field(step2_1_block, "SCALE_BASELINE_SELECTION"),
                    extract_field(step2_1_block, "SCALE_RATIO_JUDGMENT_METHOD"),
                    extract_field(step2_1_block, "FUNCTIONAL_SIZE_TESTS"),
                    extract_field(step2_1_block, "SCALE_ANCHOR_VERDICT_HANDOFF"),
                ],
            )
        )
        if not contains_keyword(scale_process_text, SCALE_FUNCTION_KEYWORDS):
            errors.append(
                "Scale-anchor judgment must reference functional size/ratio checks such as human/adult, door/window, vehicle/tram, head/body, or usable object scale."
            )

    humanoid_signal_text = " ".join(
        filter(
            None,
            [
                request_summary,
                action_field,
                extract_field(step1_block, "ENVIRONMENT"),
                extract_field(step2_block, "COMPOSITION_OBJECT_ROLE_SUMMARY"),
                extract_field(step2_1_block, "HERO_OBJECT_SCALE_RELATIONSHIP_CHECK"),
                extract_field(step2_1_block, "HERO_BACKGROUND_HUMANOID_SCALE_COMPARISON_TABLE"),
                extract_field(step2_2_block, "SOURCE_IMAGE_OBJECTS_PRESENT"),
                extract_field(step2_2_block, "VISIBLE_HUMANOID_OBJECT_CANDIDATES"),
                extract_field(step2_2_block, "BACKGROUND_DEPTH_OBJECTS"),
                extract_field(step2_3_block, "ALL_HUMANOID_ANATOMY_INVENTORY"),
                extract_field(step2_3_block, "SECONDARY_HUMANOID_ANATOMY_OBJECTS"),
                extract_field(step2_5_block, "REQUIRED_OBJECTS"),
            ],
        )
    )
    humanoid_scale_expected = contains_keyword(humanoid_signal_text, HUMANOID_OBJECT_KEYWORDS) or anatomy_required_expected
    if humanoid_scale_expected:
        humanoid_fields = (
            ("Step 2.1", step2_1_block, "HERO_BACKGROUND_HUMANOID_SCALE_COMPARISON_TABLE"),
            ("Step 2.1", step2_1_block, "HERO_HUMANOID_SCALE_COMPARISON_PLAN"),
            ("Step 2.1", step2_1_block, "PERSPECTIVE_ONLY_SCALE_LOCK"),
            ("Step 2.2", step2_2_block, "VISIBLE_HUMANOID_OBJECT_CANDIDATES"),
            ("Step 2.3", step2_3_block, "ALL_HUMANOID_ANATOMY_INVENTORY"),
            ("Step 2.3", step2_3_block, "SECONDARY_HUMANOID_ANATOMY_OBJECTS"),
            ("Step 2.3", step2_3_block, "HUMANOID_ANATOMY_TRANSFER_TABLE"),
            ("Step 2.3", step2_3_block, "HUMANOID_DEPTH_PLANE_MAP"),
            ("Step 2.3", step2_3_block, "HERO_SECONDARY_HUMANOID_SCALE_PARITY_LOCK"),
            ("Step 2.3", step2_3_block, "NO_STYLIZED_SCALE_EXAGGERATION_LOCK"),
            ("Step 2.8", step2_8_block, "HUMANOID_SCALE_PARITY_BLOCKOUT_CHECK"),
            ("Step 2.9", step2_9_block, "HUMANOID_SCALE_PARITY_PROMPT_LOCK"),
            ("Step 8", step8_block, "HUMANOID_SCALE_PARITY_VERDICT_CHECK"),
        )
        for section_label, block, field_name in humanoid_fields:
            value = extract_field(block, field_name)
            if count_meaningful_tokens(value) < 6:
                errors.append(
                    f"{section_label} {field_name} must compare the protagonist against every visible human/humanoid/humanoid monster as anatomy scale objects."
                )
        humanoid_scale_text = " ".join(
            filter(None, [extract_field(block, field_name) for _, block, field_name in humanoid_fields])
        )
        if not contains_keyword(humanoid_scale_text, HUMANOID_SCALE_PARITY_KEYWORDS):
            errors.append(
                "Humanoid scale-parity fields must mention protagonist/background humans or humanoids, anatomy, depth-plane/perspective scale, and fail miniature/doll/giant/texture humanoids."
            )
        if not contains_keyword(
            " ".join(
                filter(
                    None,
                    [
                        extract_field(step2_1_block, "PERSPECTIVE_ONLY_SCALE_LOCK"),
                        extract_field(step2_3_block, "NO_STYLIZED_SCALE_EXAGGERATION_LOCK"),
                        extract_field(step2_9_block, "SCALE_OVER_STYLE_LOCK"),
                        extract_field(step2_9_block, "HUMANOID_SCALE_PARITY_PROMPT_LOCK"),
                    ],
                )
            ),
            PERSPECTIVE_ONLY_SCALE_KEYWORDS,
        ):
            errors.append(
                "Humanoid/person/object scale locks must state that size changes are allowed only by real size, perspective/depth/lens, or explicit symbolic opt-in, never by style/drama/focal importance."
            )
        image_prompt = extract_image_generation_prompt(text)
        if image_ready_value == "yes" and not contains_keyword(image_prompt, HUMANOID_SCALE_PARITY_KEYWORDS):
            errors.append(
                "IMAGE_GEN_HANDOFF_PROMPT must carry protagonist-to-background-humanoid scale parity language when humans/passengers/humanoids are present."
            )

    long_vehicle_scale_expected = any(
        contains_keyword_korean_tolerant(field, VEHICLE_SCALE_KEYWORDS)
        for field in (
            request_summary,
            extract_field(step2_2_block, "SUPPORT_PLANE_OBJECTS"),
            extract_field(step2_2_block, "BACKGROUND_DEPTH_OBJECTS"),
            extract_field(step2_1_block, "SCALE_ANCHOR_OBJECTS"),
            extract_field(step2_1_block, "FUNCTIONAL_SIZE_TESTS"),
            extract_field(step2_5_block, "REQUIRED_OBJECTS"),
        )
    )
    vehicle_or_scale_expected = any(
        contains_keyword_korean_tolerant(field, VEHICLE_SCALE_KEYWORDS + SCALE_CRITICAL_CONTAINER_KEYWORDS)
        for field in (
            request_summary,
            extract_field(step2_2_block, "SUPPORT_PLANE_OBJECTS"),
            extract_field(step2_2_block, "BACKGROUND_DEPTH_OBJECTS"),
            extract_field(step2_1_block, "SCALE_ANCHOR_OBJECTS"),
            extract_field(step2_1_block, "FUNCTIONAL_SIZE_TESTS"),
            extract_field(step2_5_block, "REQUIRED_OBJECTS"),
        )
    )
    if vehicle_or_scale_expected:
        container_research_needed = extract_field(step2_4_block, "CONTAINER_CAPACITY_RESEARCH_NEEDED")
        container_objects_researched = extract_field(step2_5_block, "CONTAINER_CAPACITY_OBJECTS_RESEARCHED")
        container_research_applied = extract_field(step2_5_block, "CONTAINER_CAPACITY_RESEARCH_APPLIED")
        for section_label, field_value in (
            ("Step 2.4 CONTAINER_CAPACITY_RESEARCH_NEEDED", container_research_needed),
            ("Step 2.5 CONTAINER_CAPACITY_OBJECTS_RESEARCHED", container_objects_researched),
            ("Step 2.5 CONTAINER_CAPACITY_RESEARCH_APPLIED", container_research_applied),
        ):
            if value_is_none_like(field_value) or count_meaningful_tokens(field_value) < 6:
                errors.append(f"Vehicle / container scenes require {section_label} so object research checks occupancy/capacity scale, not just exterior shape.")
        container_handoff_text = " ".join(filter(None, [container_research_needed, container_objects_researched, container_research_applied]))
        if not contains_keyword(container_handoff_text, CONTAINER_CAPACITY_RESEARCH_KEYWORDS):
            errors.append("Vehicle / container object research handoff must mention capacity/occupancy, seats/standing adults, cabin/interior volume, modules, doors/windows/aisles, or equivalent human-scale anchors.")
        if not contains_keyword(container_handoff_text, INTERNAL_HUMAN_ANCHOR_KEYWORDS):
            errors.append("Vehicle / human-enterable object handoff must mention internal occupant/passenger/driver human anatomy anchors, not only exterior capacity.")
        scale_relation_table = extract_field(step2_6_block, "SCALE_RELATION_TABLE")
        if count_meaningful_tokens(scale_relation_table) < 6:
            errors.append("Vehicle / scale-anchor scenes require Step 2.6 SCALE_RELATION_TABLE to lock object scale relationships.")
        if count_meaningful_tokens(extract_field(step2_8_block, "SCALE_CHECK")) < 6:
            errors.append("Vehicle / scale-anchor scenes require Step 2.8 SCALE_CHECK to explicitly address scale or ratio.")
        if count_meaningful_tokens(extract_field(step2_8_block, "DOOR_VEHICLE_FUNCTIONAL_SCALE_CHECK")) < 6:
            errors.append("Vehicle / door / scale-anchor scenes require Step 2.8 DOOR_VEHICLE_FUNCTIONAL_SCALE_CHECK to prevent toy vehicles or tiny exits.")
        passenger_capacity_check = extract_field(step2_8_block, "PASSENGER_CAPACITY_SCALE_CHECK")
        passenger_capacity_verdict = extract_field(step8_block, "PASSENGER_CAPACITY_VERDICT_CHECK")
        if count_meaningful_tokens(passenger_capacity_check) < 8:
            errors.append("Vehicle / tram / train scenes require Step 2.8 PASSENGER_CAPACITY_SCALE_CHECK to prove full cabin scale, not just roof width.")
        if not contains_keyword(passenger_capacity_check, PASSENGER_CAPACITY_KEYWORDS):
            errors.append("PASSENGER_CAPACITY_SCALE_CHECK must reference passengers/cabin/capacity/window-door bays or equivalent human-occupancy scale anchors.")
        if count_meaningful_tokens(passenger_capacity_verdict) < 8:
            errors.append("Vehicle / tram / train scenes require Step 8 PASSENGER_CAPACITY_VERDICT_CHECK to fail protagonist-sized vehicles.")
        image_prompt = extract_image_generation_prompt(text)
        if image_ready_value == "yes" and not contains_keyword(image_prompt, PASSENGER_CAPACITY_KEYWORDS):
            errors.append("Vehicle / tram / train IMAGE_GEN_HANDOFF_PROMPT must carry passenger/cabin/capacity/window-door-bay scale language, not leave it only in the spec.")
        if image_ready_value == "yes" and not contains_keyword(image_prompt, INTERNAL_HUMAN_ANCHOR_KEYWORDS):
            errors.append("Vehicle / human-enterable IMAGE_GEN_HANDOFF_PROMPT must carry internal occupant/passenger/driver anatomy scale anchors.")
        if image_ready_value == "yes" and not contains_keyword(image_prompt, SCALE_EMPHASIS_OVERRIDE_KEYWORDS):
            errors.append("Vehicle / human-enterable IMAGE_GEN_HANDOFF_PROMPT must reject drama/beauty/action/focal scale enlargement and defer size to perspective/actual object size.")

    scale_critical_expected = vehicle_or_scale_expected and humanoid_scale_expected
    scale_critical_active = scale_critical_expected or scale_critical_mode == "yes"
    if scale_critical_expected and scale_critical_mode != "yes":
        errors.append(
            "Human-enterable object plus protagonist/main humanoid requires SCALE_CRITICAL_MODE: yes so scale proof becomes a hard gate."
        )
    if scale_critical_active:
        if scale_critical_mode != "yes":
            errors.append("Scale-critical fields are required only after declaring SCALE_CRITICAL_MODE: yes.")

        scale_critical_shot_class = extract_field(step2_1_block, "SCALE_CRITICAL_SHOT_CLASS")
        full_container_visibility_requirement = extract_field(step2_1_block, "FULL_CONTAINER_VISIBILITY_REQUIREMENT")
        scale_witness_min_count = extract_field(step2_1_block, "SCALE_WITNESS_MIN_COUNT")
        hero_to_module_visual_ratio = extract_field(step2_1_block, "HERO_TO_MODULE_VISUAL_RATIO")
        closeup_blocked_until_scale_pass = lower_value(extract_field(step2_1_block, "CLOSEUP_BLOCKED_UNTIL_SCALE_PASS"))
        face_focal_demotion_for_scale = extract_field(step2_1_block, "FACE_FOCAL_DEMOTION_FOR_SCALE")
        camera_class_blockout_lock = extract_field(step2_8_block, "CAMERA_CLASS_BLOCKOUT_LOCK")
        full_container_visibility_blockout_check = extract_field(step2_8_block, "FULL_CONTAINER_VISIBILITY_BLOCKOUT_CHECK")
        scale_witness_visibility_count_check = extract_field(step2_8_block, "SCALE_WITNESS_VISIBILITY_COUNT_CHECK")
        camera_class_prompt_opening = extract_field(step2_9_block, "CAMERA_CLASS_PROMPT_OPENING")
        scale_critical_shot_class_prompt_lock = extract_field(step2_9_block, "SCALE_CRITICAL_SHOT_CLASS_PROMPT_LOCK")
        face_focal_demotion_prompt_lock = extract_field(step2_9_block, "FACE_FOCAL_DEMOTION_PROMPT_LOCK")
        camera_class_verdict_check = extract_field(step8_block, "CAMERA_CLASS_VERDICT_CHECK")
        scale_critical_shot_class_verdict_check = extract_field(step8_block, "SCALE_CRITICAL_SHOT_CLASS_VERDICT_CHECK")

        requested_or_chosen_camera = " ".join(
            filter(None, [user_camera_class_preset_global, chosen_camera_class, scale_critical_shot_class])
        )
        if user_camera_class_lock_global == "hard" and camera_class_is_closeup_risk(user_camera_class_preset_global):
            errors.append(
                "Hard-locked close/portrait/medium camera class conflicts with SCALE_CRITICAL_MODE. "
                "Resolve with the user before image handoff, or change the user camera preset to a scale-proving wide/long shot."
            )
        elif camera_class_is_closeup_risk(requested_or_chosen_camera) and camera_class_conflict_status not in {"conflict", "resolved"}:
            errors.append(
                "Scale-critical camera conflict must be recorded in CAMERA_CLASS_CONFLICT_STATUS when a close/medium/hero camera risks enlarging the protagonist."
            )

        for label, field_value in (
            ("Step 2 CHOSEN_CAMERA_CLASS", chosen_camera_class),
            ("Step 2 CAMERA_CLASS_VISUAL_TRANSLATION", camera_class_visual_translation),
            ("Step 2.1 SCALE_CRITICAL_SHOT_CLASS", scale_critical_shot_class),
            ("Step 2.8 CAMERA_CLASS_BLOCKOUT_LOCK", camera_class_blockout_lock),
            ("Step 2.9 CAMERA_CLASS_PROMPT_OPENING", camera_class_prompt_opening),
            ("Step 2.9 SCALE_CRITICAL_SHOT_CLASS_PROMPT_LOCK", scale_critical_shot_class_prompt_lock),
            ("Step 8 CAMERA_CLASS_VERDICT_CHECK", camera_class_verdict_check),
            ("Step 8 SCALE_CRITICAL_SHOT_CLASS_VERDICT_CHECK", scale_critical_shot_class_verdict_check),
        ):
            if value_is_none_like(field_value) or count_meaningful_tokens(field_value) < 4:
                errors.append(f"Scale-critical scenes require {label} to lock a scale-proving camera class.")
            elif not contains_keyword_korean_tolerant(field_value, CAMERA_CLASS_SCALE_PROVING_KEYWORDS):
                errors.append(
                    f"{label} must translate to a scale-proving wide/long/establishing camera class, not a face-first or medium hero shot."
                )

        for label, field_value, numeric_required in (
            ("Step 2.1 FULL_CONTAINER_VISIBILITY_REQUIREMENT", full_container_visibility_requirement, True),
            ("Step 2.1 SCALE_WITNESS_MIN_COUNT", scale_witness_min_count, True),
            ("Step 2.1 HERO_TO_MODULE_VISUAL_RATIO", hero_to_module_visual_ratio, True),
            ("Step 2.8 FULL_CONTAINER_VISIBILITY_BLOCKOUT_CHECK", full_container_visibility_blockout_check, False),
            ("Step 2.8 SCALE_WITNESS_VISIBILITY_COUNT_CHECK", scale_witness_visibility_count_check, True),
        ):
            if value_is_none_like(field_value) or count_meaningful_tokens(field_value) < 4:
                errors.append(f"Scale-critical shot-class gate requires {label}.")
            elif numeric_required and not has_numeric_scale(field_value):
                errors.append(f"{label} must include numeric screen/module/witness thresholds.")
            elif not contains_keyword_korean_tolerant(field_value, SCALE_WITNESS_VISIBILITY_KEYWORDS):
                errors.append(
                    f"{label} must name visible doors/windows/passengers/modules/full container witnesses, not only abstract scale."
                )

        if closeup_blocked_until_scale_pass != "yes":
            errors.append("Scale-critical scenes require CLOSEUP_BLOCKED_UNTIL_SCALE_PASS: yes until the post-image scale verdict passes.")

        face_demotion_text = " ".join(
            filter(None, [face_focal_demotion_for_scale, face_focal_demotion_prompt_lock])
        )
        if value_is_none_like(face_demotion_text) or not contains_keyword_korean_tolerant(
            face_demotion_text,
            FACE_FOCAL_DEMOTION_KEYWORDS,
        ):
            errors.append(
                "Scale-critical scenes must demote face/eye focal to a small accent until scale passes; close portrait language cannot lead the prompt."
            )

        scale_critical_values: list[str] = []
        for section_label, heading, field_name, numeric_required in SCALE_CRITICAL_SPEC_NUMERIC_FIELDS:
            block = text if heading is None else sections[heading]
            field_value = extract_field(block, field_name)
            scale_critical_values.append(field_value or "")
            if numeric_required:
                if value_is_none_like(field_value) or not has_numeric_scale(field_value):
                    errors.append(
                        f"Scale-critical scenes require {section_label} {field_name} with numeric ratio/threshold evidence."
                    )
            elif value_is_none_like(field_value) or count_meaningful_tokens(field_value) < 4:
                errors.append(f"Scale-critical scenes require {section_label} {field_name} with actionable scale-proof content.")
        scale_critical_ratio_text = " ".join(scale_critical_values)
        if not contains_keyword_korean_tolerant(scale_critical_ratio_text, SCALE_CRITICAL_RATIO_KEYWORDS):
            errors.append(
                "Scale-critical fields must carry ratio/threshold/height/width/length/screen-occupancy/door/occupant language, not only narrative scale claims."
            )

        strict_scale_blockout_required = lower_value(
            extract_field(step2_8_block, "STRICT_SCALE_BLOCKOUT_REQUIRED")
        )
        if strict_scale_blockout_required != "yes":
            errors.append("Scale-critical scenes require Step 2.8 STRICT_SCALE_BLOCKOUT_REQUIRED: yes.")

        scale_proxy_dummy_required = lower_value(extract_field(step2_1_block, "SCALE_PROXY_DUMMY_REQUIRED"))
        scale_proxy_step21_fields = (
            ("Step 2.1 SCALE_PROXY_DUMMY_HEIGHT", step2_1_block, "SCALE_PROXY_DUMMY_HEIGHT", True),
            ("Step 2.1 SCALE_PROXY_DUMMY_BASELINE_OBJECT", step2_1_block, "SCALE_PROXY_DUMMY_BASELINE_OBJECT", False),
            ("Step 2.1 SCALE_PROXY_DUMMY_PLACEMENT_PLAN", step2_1_block, "SCALE_PROXY_DUMMY_PLACEMENT_PLAN", False),
            ("Step 2.1 SCALE_PROXY_DUMMY_TO_HERO_PROJECTION", step2_1_block, "SCALE_PROXY_DUMMY_TO_HERO_PROJECTION", True),
        )
        scale_proxy_step28_fields = (
            ("Step 2.8 SCALE_PROXY_DUMMY_BLOCKOUT_PLACEMENT", step2_8_block, "SCALE_PROXY_DUMMY_BLOCKOUT_PLACEMENT", True),
            ("Step 2.8 SCALE_PROXY_DUMMY_BLOCKOUT_CHECK", step2_8_block, "SCALE_PROXY_DUMMY_BLOCKOUT_CHECK", True),
            ("Step 2.8 SCALE_PROXY_DUMMY_REMOVAL_POLICY", step2_8_block, "SCALE_PROXY_DUMMY_REMOVAL_POLICY", False),
            ("Step 2.8 SCALE_PROXY_TRACE_OVERLAY", step2_8_block, "SCALE_PROXY_TRACE_OVERLAY", True),
            ("Step 2.8 SCALE_PROXY_TO_HERO_BLOCKOUT_VERDICT", step2_8_block, "SCALE_PROXY_TO_HERO_BLOCKOUT_VERDICT", True),
        )
        if scale_proxy_dummy_required != "yes":
            errors.append(
                "Scale-critical human-enterable scenes require SCALE_PROXY_DUMMY_REQUIRED: yes so an adult dummy/mannequin is used as a temporary door-side scale witness before the composite."
            )
        scale_proxy_text_parts: list[str] = []
        for label, block, field_name, numeric_required in scale_proxy_step21_fields + scale_proxy_step28_fields:
            field_value = extract_field(block, field_name)
            scale_proxy_text_parts.append(field_value or "")
            if value_is_none_like(field_value) or count_meaningful_tokens(field_value) < 4:
                errors.append(
                    f"Scale-critical scenes require {label}: place a temporary adult dummy/mannequin by the door/baseline, project it to the hero, then remove the dummy but retain measurement traces."
                )
                continue
            if numeric_required and not has_numeric_scale(field_value):
                errors.append(f"{label} must include numeric height/ratio/projection evidence.")
        scale_proxy_text = " ".join(scale_proxy_text_parts)
        if not contains_keyword_korean_tolerant(scale_proxy_text, SCALE_PROXY_DUMMY_KEYWORDS):
            errors.append(
                "Scale proxy fields must mention the temporary adult dummy/mannequin, door-side baseline, projection, footpoint/depth plane, removal, and retained measurement overlay."
            )
        removal_policy_text = " ".join(
            filter(
                None,
                [
                    extract_field(step2_8_block, "SCALE_PROXY_DUMMY_REMOVAL_POLICY"),
                    extract_field(step2_8_block, "SCALE_PROXY_TRACE_OVERLAY"),
                ],
            )
        )
        if not (
            contains_keyword_korean_tolerant(
                removal_policy_text,
                ["hide", "hidden", "delete", "remove", "removed", "숨김", "삭제", "제거"],
            )
            and contains_keyword_korean_tolerant(
                removal_policy_text,
                ["trace", "overlay", "height line", "measurement", "baseline", "오버레이", "측정선", "기준선"],
            )
        ):
            errors.append(
                "Scale proxy removal policy must hide/delete the temporary dummy before the composite/final image while retaining the measurement trace/height-line/baseline overlay."
            )
        scale_proxy_blockout_verdict = extract_field(step2_8_block, "SCALE_PROXY_TO_HERO_BLOCKOUT_VERDICT")
        if not value_indicates_pass(scale_proxy_blockout_verdict):
            errors.append("SCALE_PROXY_TO_HERO_BLOCKOUT_VERDICT must explicitly pass before a scale-critical visual guide composite can be approved.")

        real_blockout_evidence_status = lower_value(
            extract_field(step2_8_block, "REAL_BLOCKOUT_EVIDENCE_STATUS")
        )
        proxy_or_blocked_evidence = real_blockout_evidence_status in {
            "blocked_no_blender",
            "blocked_proxy_only",
        } or contains_proxy_blockout_evidence(
            " ".join(
                filter(
                    None,
                    [
                        extract_field(step2_8_block, "REAL_BLOCKOUT_EVIDENCE_STATUS"),
                        extract_field(step2_8_block, "BLENDER_BLOCKOUT_REVIEW"),
                        extract_field(step2_8_block, "VISUAL_GUIDE_COMPOSITE_SOURCE_PASSES"),
                        extract_field(step2_8_block, "VISUAL_GUIDE_COMPOSITE_OVERLAYS"),
                        extract_field(step2_8_block, "SCALE_VISUAL_GUIDE_PACKAGE"),
                    ],
                )
            )
        )
        if proxy_or_blocked_evidence:
            proxy_disclosure_text = " ".join(
                filter(
                    None,
                    [
                        extract_field(step2_8_block, "REAL_BLOCKOUT_EVIDENCE_STATUS"),
                        extract_field(step2_8_block, "BLENDER_BLOCKOUT_REVIEW"),
                        extract_field(step2_8_block, "VISUAL_GUIDE_COMPOSITE_SOURCE_PASSES"),
                        extract_field(step2_8_block, "VISUAL_GUIDE_COMPOSITE_OVERLAYS"),
                        extract_field(step2_8_block, "SCALE_VISUAL_GUIDE_PACKAGE"),
                    ],
                )
            )
            if not contains_keyword_korean_tolerant(
                proxy_disclosure_text,
                ["proxy", "placeholder", "blocked", "not true", "not real", "not a true", "not claimed", "not blender", "no blender", "블렌더 아님", "프록시", "대체"],
            ):
                errors.append(
                    "Proxy/no-Blender blockout evidence must be disclosed honestly in Step 2.8; do not imply proxy images are true Blender render passes."
                )
            if not contains_keyword_korean_tolerant(
                proxy_disclosure_text,
                ["distinct", "separate", "different", "clay", "lineart", "wire", "depth", "composite", "구분", "분리", "별도"],
            ):
                errors.append(
                    "Proxy visual-guide packages must state that clay/lineart/depth/composite outputs are visually/functionally distinct, not duplicate saves."
                )
        if image_ready_value == "yes" and real_blockout_evidence_status != "real_blender_pass":
            errors.append(
                "Scale-critical IMAGE_GEN_READY: yes requires REAL_BLOCKOUT_EVIDENCE_STATUS: real_blender_pass; "
                "blocked_no_blender/proxy-only evidence cannot unlock image generation."
            )

        scale_critical_prompt_opening = extract_field(step2_9_block, "SCALE_CRITICAL_PROMPT_OPENING")
        image_prompt = extract_image_generation_prompt(text)
        prompt_scale_text = " ".join(filter(None, [scale_critical_prompt_opening, image_prompt]))
        if image_ready_value == "yes":
            if not contains_keyword_korean_tolerant(prompt_scale_text, SCALE_CRITICAL_RATIO_KEYWORDS):
                errors.append(
                    "Scale-critical image handoff must carry the numeric scale proof in the prompt opening, not only in earlier spec fields."
                )
            if not contains_keyword(prompt_scale_text, INTERNAL_HUMAN_ANCHOR_KEYWORDS + PASSENGER_CAPACITY_KEYWORDS):
                errors.append(
                    "Scale-critical image handoff must foreground occupant/passenger/driver and door/window/cabin anchors before face/action/style detail."
                )
            if not contains_keyword(prompt_scale_text, SCALE_EMPHASIS_OVERRIDE_KEYWORDS):
                errors.append(
                    "Scale-critical image handoff must explicitly reject drama/style/action/focal size enlargement."
                )
            if not contains_keyword_korean_tolerant(prompt_scale_text, CAMERA_CLASS_SCALE_PROVING_KEYWORDS):
                errors.append(
                    "Scale-critical image handoff must open with a scale-proving camera class such as extreme wide / wide / long shot."
                )
            if not contains_keyword_korean_tolerant(prompt_scale_text, SCALE_WITNESS_VISIBILITY_KEYWORDS):
                errors.append(
                    "Scale-critical image handoff must mention full container visibility and repeated doors/windows/passengers/modules."
                )
            if not contains_keyword_korean_tolerant(prompt_scale_text, FACE_FOCAL_DEMOTION_KEYWORDS):
                errors.append(
                    "Scale-critical image handoff must state that face/eyes are small accents, not a close-up portrait focus."
                )

        # PASSENGER_INSTANCE_REGISTRY: every passenger is an individual anatomy instance
        passenger_registry = extract_field(step2_5_block, "PASSENGER_INSTANCE_REGISTRY")
        if value_is_none_like(passenger_registry):
            errors.append(
                "Scale-critical scenes require Step 2.5 PASSENGER_INSTANCE_REGISTRY with at least one filled entry per human-enterable container; not_applicable is rejected."
            )
        else:
            entry_count = passenger_registry.count("passenger_id:") - passenger_registry.count("<P1>")
            if entry_count < 1:
                errors.append(
                    "PASSENGER_INSTANCE_REGISTRY must contain at least one filled entry (placeholder <P1> rows do not count)."
                )
            for required_subkey in ("container:", "depth_plane:", "visible_landmarks:", "pass_or_fail:"):
                if required_subkey not in passenger_registry:
                    errors.append(
                        f"PASSENGER_INSTANCE_REGISTRY entries require '{required_subkey}' so each passenger is treated as an individual anatomy instance, not background texture."
                    )

        composite_spec_checks = (
            ("Step 2.4 HUMAN_ENTERABLE_COMPOSITE_SCALE_PLAN", step2_4_block, "HUMAN_ENTERABLE_COMPOSITE_SCALE_PLAN", COMPOSITE_SCALE_VERDICT_KEYWORDS, False),
            ("Step 2.5 HUMAN_ENTERABLE_COMPOSITE_SCALE_TABLE", step2_5_block, "HUMAN_ENTERABLE_COMPOSITE_SCALE_TABLE", ENTRY_FIT_KEYWORDS + XYZ_VOLUME_KEYWORDS + CAPACITY_CLASS_KEYWORDS + INTERNAL_HUMAN_ANCHOR_KEYWORDS + MODULE_REPETITION_KEYWORDS, False),
            ("Step 2.5 ENTRY_FIT_CHECK_APPLIED", step2_5_block, "ENTRY_FIT_CHECK_APPLIED", ENTRY_FIT_KEYWORDS, True),
            ("Step 2.5 XYZ_VOLUME_CHECK_APPLIED", step2_5_block, "XYZ_VOLUME_CHECK_APPLIED", XYZ_VOLUME_KEYWORDS, True),
            ("Step 2.5 CAPACITY_CLASS_CHECK_APPLIED", step2_5_block, "CAPACITY_CLASS_CHECK_APPLIED", CAPACITY_CLASS_KEYWORDS, True),
            ("Step 2.5 OCCUPANT_ANCHOR_CHECK_APPLIED", step2_5_block, "OCCUPANT_ANCHOR_CHECK_APPLIED", INTERNAL_HUMAN_ANCHOR_KEYWORDS, True),
            ("Step 2.5 MODULE_REPETITION_CHECK_APPLIED", step2_5_block, "MODULE_REPETITION_CHECK_APPLIED", MODULE_REPETITION_KEYWORDS, True),
            ("Step 2.5 HUMAN_ENTERABLE_SCALE_VERDICT_APPLIED", step2_5_block, "HUMAN_ENTERABLE_SCALE_VERDICT_APPLIED", COMPOSITE_SCALE_VERDICT_KEYWORDS, True),
            ("Step 2.8 XYZ_VOLUME_BLOCKOUT_CHECK", step2_8_block, "XYZ_VOLUME_BLOCKOUT_CHECK", XYZ_VOLUME_KEYWORDS, True),
            ("Step 2.8 CAPACITY_CLASS_BLOCKOUT_CHECK", step2_8_block, "CAPACITY_CLASS_BLOCKOUT_CHECK", CAPACITY_CLASS_KEYWORDS, True),
            ("Step 2.8 MODULE_REPETITION_BLOCKOUT_CHECK", step2_8_block, "MODULE_REPETITION_BLOCKOUT_CHECK", MODULE_REPETITION_KEYWORDS, True),
            ("Step 2.8 HUMAN_ENTERABLE_COMPOSITE_BLOCKOUT_VERDICT", step2_8_block, "HUMAN_ENTERABLE_COMPOSITE_BLOCKOUT_VERDICT", COMPOSITE_SCALE_VERDICT_KEYWORDS, True),
            ("Step 8 ENTRY_FIT_VERDICT_CHECK", step8_block, "ENTRY_FIT_VERDICT_CHECK", ENTRY_FIT_KEYWORDS, True),
            ("Step 8 XYZ_VOLUME_VERDICT_CHECK", step8_block, "XYZ_VOLUME_VERDICT_CHECK", XYZ_VOLUME_KEYWORDS, True),
            ("Step 8 CAPACITY_CLASS_VERDICT_CHECK", step8_block, "CAPACITY_CLASS_VERDICT_CHECK", CAPACITY_CLASS_KEYWORDS, True),
            ("Step 8 OCCUPANT_ANCHOR_VERDICT_CHECK", step8_block, "OCCUPANT_ANCHOR_VERDICT_CHECK", INTERNAL_HUMAN_ANCHOR_KEYWORDS, True),
            ("Step 8 MODULE_REPETITION_VERDICT_CHECK", step8_block, "MODULE_REPETITION_VERDICT_CHECK", MODULE_REPETITION_KEYWORDS, True),
            ("Step 8 HUMAN_ENTERABLE_SCALE_VERDICT", step8_block, "HUMAN_ENTERABLE_SCALE_VERDICT", COMPOSITE_SCALE_VERDICT_KEYWORDS, True),
        )
        for label, block, field_name, keywords, must_pass in composite_spec_checks:
            field_value = extract_field(block, field_name)
            if value_is_none_like(field_value) or count_meaningful_tokens(field_value) < 4:
                errors.append(
                    f"Scale-critical human-enterable scenes require {label}; entry height alone is not a container/tram scale proof."
                )
                continue
            if not contains_keyword_korean_tolerant(field_value, keywords):
                errors.append(
                    f"{label} must contain its specific composite scale evidence, not generic scale prose."
                )
            if must_pass and not value_indicates_pass(field_value):
                errors.append(
                    f"{label} must explicitly pass before the human-enterable composite scale verdict can pass."
                )

        # SCALE_EMPHASIS_OVERRIDE_* wire-up: must be filled when SCALE_CRITICAL_MODE: yes
        emphasis_policy = extract_field(step2_5_block, "SCALE_EMPHASIS_OVERRIDE_POLICY_APPLIED")
        emphasis_prompt_lock = extract_field(step2_9_block, "SCALE_EMPHASIS_OVERRIDE_PROMPT_LOCK")
        if value_is_none_like(emphasis_policy) or count_meaningful_tokens(emphasis_policy) < 4:
            errors.append(
                "Scale-critical scenes require Step 2.5 SCALE_EMPHASIS_OVERRIDE_POLICY_APPLIED to spell out how emphasis-size commands are ignored."
            )
        if value_is_none_like(emphasis_prompt_lock) or count_meaningful_tokens(emphasis_prompt_lock) < 4:
            errors.append(
                "Scale-critical scenes require Step 2.9 SCALE_EMPHASIS_OVERRIDE_PROMPT_LOCK with concrete prompt-side override wording."
            )

        # INTERNAL_OCCUPANT_* / HUMAN_ENTERABLE_OCCUPANT_PROMPT_LOCK wire-up:
        # these survive in template after PASSENGER_INSTANCE_REGISTRY refactor and must reference it.
        occupant_blockout_check = extract_field(step2_8_block, "INTERNAL_OCCUPANT_ANATOMY_SCALE_CHECK")
        occupant_prompt_lock = extract_field(step2_9_block, "HUMAN_ENTERABLE_OCCUPANT_PROMPT_LOCK")
        occupant_verdict_check = extract_field(text, "INTERNAL_OCCUPANT_SCALE_VERDICT_CHECK")
        for label, value in (
            ("Step 2.8 INTERNAL_OCCUPANT_ANATOMY_SCALE_CHECK", occupant_blockout_check),
            ("Step 2.9 HUMAN_ENTERABLE_OCCUPANT_PROMPT_LOCK", occupant_prompt_lock),
            ("Step 8 INTERNAL_OCCUPANT_SCALE_VERDICT_CHECK", occupant_verdict_check),
        ):
            if value_is_none_like(value) or count_meaningful_tokens(value) < 4:
                errors.append(
                    f"Scale-critical scenes require {label} to apply the PASSENGER_INSTANCE_REGISTRY per-instance scale check, not placeholder."
                )

        # Numeric ratio consistency check (원인 4): catch self-contradicting numbers
        # before they reach the prompt. Conservative thresholds — flag only clearly
        # impossible configurations.
        max_occupancy_text = extract_field(step2_1_block, "MAX_PROTAGONIST_SCREEN_OCCUPANCY")
        max_occupancy = extract_first_ratio(max_occupancy_text)
        if long_vehicle_scale_expected and max_occupancy is not None and max_occupancy > 0.15:
            errors.append(
                f"MAX_PROTAGONIST_SCREEN_OCCUPANCY ({max_occupancy_text!r}) exceeds 15% for a scale-critical shot-class gate. "
                "Use a wide/long shot and keep the protagonist small enough that full vehicle/container scale remains legible; long vehicles should normally target <= 5% of visible length."
            )
        if max_occupancy is not None and max_occupancy > 0.50:
            errors.append(
                f"MAX_PROTAGONIST_SCREEN_OCCUPANCY ({max_occupancy_text!r}) exceeds 50% — protagonist this large in a scale-critical scene contradicts occupant anchor parity. Reduce to <= 30% or widen the camera."
            )

        protag_entry_ratio_text = extract_field(step2_5_block, "PROTAGONIST_TO_ENTRY_RATIO_APPLIED")
        protag_entry_ratio = extract_first_ratio(protag_entry_ratio_text)
        if protag_entry_ratio is not None and protag_entry_ratio >= 1.0:
            errors.append(
                f"PROTAGONIST_TO_ENTRY_RATIO_APPLIED ({protag_entry_ratio_text!r}) >= 1.0 means protagonist is at least as tall as the door/entry — this is the F-002 'protagonist-sized container' failure. Door/entry must exceed protagonist height."
            )

        protag_occupant_ratio_text = extract_field(step2_5_block, "PROTAGONIST_TO_OCCUPANT_RATIO_APPLIED")
        protag_occupant_ratio = extract_first_ratio(protag_occupant_ratio_text)
        if protag_occupant_ratio is not None and protag_occupant_ratio > 1.5:
            errors.append(
                f"PROTAGONIST_TO_OCCUPANT_RATIO_APPLIED ({protag_occupant_ratio_text!r}) > 1.5 means protagonist is much larger than fellow occupants — hieratic distortion is not allowed without explicit user opt-in."
            )

        # Cross-field contradiction: large screen share + adult-equal occupant ratio = impossible
        if (
            max_occupancy is not None
            and protag_occupant_ratio is not None
            and max_occupancy > 0.40
            and abs(protag_occupant_ratio - 1.0) < 0.20
        ):
            errors.append(
                f"Numeric inconsistency: MAX_PROTAGONIST_SCREEN_OCCUPANCY ~{max_occupancy:.0%} says protagonist dominates the frame, "
                f"but PROTAGONIST_TO_OCCUPANT_RATIO_APPLIED ~{protag_occupant_ratio:.2f} says same scale as occupants. Both cannot be true unless occupants also dominate the frame."
            )

    camera_cut_or_scale_signal_text = " ".join(
        filter(
            None,
            [
                request_summary,
                user_command_checklist,
                camera_angle,
                user_camera_class_preset_global,
                user_camera_class_reason_global,
                chosen_camera_class,
                camera_class_visual_translation,
                extract_field(step2_1_block, "SCALE_RATIO_JUDGMENT_METHOD"),
                extract_field(step2_1_block, "MAX_PROTAGONIST_SCREEN_OCCUPANCY"),
            ],
        )
    )
    camera_cut_or_scale_adjustment_expected = render_bound_spec and (
        scale_critical_active
        or not value_is_none_like(user_camera_class_preset_global)
        or contains_keyword_korean_tolerant(
            camera_cut_or_scale_signal_text,
            [
                "camera",
                "shot",
                "angle",
                "crop",
                "full body",
                "knee shot",
                "low angle",
                "scale",
                "screen occupancy",
                "size",
                "카메라",
                "컷",
                "샷",
                "앵글",
                "풀샷",
                "니샷",
                "로우앵글",
                "스케일",
                "크기",
                "화면 점유",
            ],
        )
    )
    if camera_cut_or_scale_adjustment_expected:
        perspective_transfer_mode = lower_value(extract_field(step2_1_block, "PERSPECTIVE_SCALE_TRANSFER_MODE"))
        screen_occupancy_is_derived = lower_value(extract_field(step2_1_block, "SCREEN_OCCUPANCY_IS_DERIVED"))
        screen_occupancy_must_not_override = lower_value(
            extract_field(step2_1_block, "SCREEN_OCCUPANCY_MUST_NOT_OVERRIDE_WORLD_SCALE")
        )
        perspective_calculation_fields = (
            ("Step 2.1 PERSPECTIVE_SCALE_TRANSFER_MODE", step2_1_block, "PERSPECTIVE_SCALE_TRANSFER_MODE"),
            ("Step 2.1 HERO_FOOTPOINT_PLANE", step2_1_block, "HERO_FOOTPOINT_PLANE"),
            ("Step 2.1 BASELINE_OBJECT", step2_1_block, "BASELINE_OBJECT"),
            ("Step 2.1 PROJECTED_BASELINE_TO_HERO_POSITION", step2_1_block, "PROJECTED_BASELINE_TO_HERO_POSITION"),
            ("Step 2.1 CAMERA_CUT_SCALE_RECONCILIATION", step2_1_block, "CAMERA_CUT_SCALE_RECONCILIATION"),
            ("Step 2.8 PERSPECTIVE_CALCULATION_BLOCKOUT_TRANSFER", step2_8_block, "PERSPECTIVE_CALCULATION_BLOCKOUT_TRANSFER"),
            ("Step 2.8 PROJECTED_BASELINE_BLOCKOUT_CHECK", step2_8_block, "PROJECTED_BASELINE_BLOCKOUT_CHECK"),
            ("Step 2.8 SCREEN_OCCUPANCY_BLOCKOUT_RECONCILIATION", step2_8_block, "SCREEN_OCCUPANCY_BLOCKOUT_RECONCILIATION"),
            ("Step 2.9 PERSPECTIVE_CALCULATION_PROMPT_LOCK", step2_9_block, "PERSPECTIVE_CALCULATION_PROMPT_LOCK"),
            ("Step 2.9 SCREEN_OCCUPANCY_DERIVED_PROMPT_LOCK", step2_9_block, "SCREEN_OCCUPANCY_DERIVED_PROMPT_LOCK"),
            ("Step 8 PERSPECTIVE_CALCULATION_VERDICT_CHECK", step8_block, "PERSPECTIVE_CALCULATION_VERDICT_CHECK"),
            ("Step 8 SCREEN_OCCUPANCY_WORLD_SCALE_VERDICT_CHECK", step8_block, "SCREEN_OCCUPANCY_WORLD_SCALE_VERDICT_CHECK"),
        )
        for label, block, field_name in perspective_calculation_fields:
            value = extract_field(block, field_name)
            if field_name == "PERSPECTIVE_SCALE_TRANSFER_MODE":
                if value_is_none_like(value):
                    errors.append(
                        f"Camera cut / scale adjustment requires {label}; follow perspective calculation -> blockout/guide -> final prompt."
                    )
                continue
            if value_is_none_like(value) or count_meaningful_tokens(value) < 4:
                errors.append(
                    f"Camera cut / scale adjustment requires {label}; follow perspective calculation -> blockout/guide -> final prompt."
                )
        if perspective_transfer_mode not in {"projected_measurement", "depth_plane_projection", "blockout_projection"}:
            errors.append(
                "Camera cut / scale adjustment requires PERSPECTIVE_SCALE_TRANSFER_MODE to be projected_measurement, depth_plane_projection, or blockout_projection."
            )
        if screen_occupancy_is_derived != "yes":
            errors.append("Camera cut / scale adjustment requires SCREEN_OCCUPANCY_IS_DERIVED: yes.")
        if screen_occupancy_must_not_override != "yes":
            errors.append("Camera cut / scale adjustment requires SCREEN_OCCUPANCY_MUST_NOT_OVERRIDE_WORLD_SCALE: yes.")

        perspective_calc_text = " ".join(
            filter(
                None,
                [
                    extract_field(step2_1_block, "HERO_FOOTPOINT_PLANE"),
                    extract_field(step2_1_block, "BASELINE_OBJECT"),
                    extract_field(step2_1_block, "PROJECTED_BASELINE_TO_HERO_POSITION"),
                    extract_field(step2_1_block, "CAMERA_CUT_SCALE_RECONCILIATION"),
                    extract_field(step2_1_block, "SCALE_PROXY_DUMMY_TO_HERO_PROJECTION"),
                ],
            )
        )
        if not contains_keyword_korean_tolerant(perspective_calc_text, PERSPECTIVE_CALCULATION_KEYWORDS):
            errors.append(
                "Perspective calculation must name the footpoint/support/depth plane, baseline object, projection, vanishing/perspective grid, or equivalent 투시 계산."
            )
        if not has_numeric_scale(perspective_calc_text):
            errors.append(
                "Perspective calculation must include numeric projected-scale evidence, e.g. protagonist 1.58m vs projected 1.95m door or occupant ratio."
            )

        blockout_transfer_text = " ".join(
            filter(
                None,
                [
                    extract_field(step2_8_block, "PERSPECTIVE_CALCULATION_BLOCKOUT_TRANSFER"),
                    extract_field(step2_8_block, "PROJECTED_BASELINE_BLOCKOUT_CHECK"),
                    extract_field(step2_8_block, "SCREEN_OCCUPANCY_BLOCKOUT_RECONCILIATION"),
                    extract_field(step2_8_block, "SCALE_PROXY_DUMMY_BLOCKOUT_CHECK"),
                    extract_field(step2_8_block, "SCALE_PROXY_TRACE_OVERLAY"),
                    extract_field(step2_8_block, "SCALE_VISUAL_GUIDE_PACKAGE"),
                ],
            )
        )
        if not contains_keyword_korean_tolerant(blockout_transfer_text, PERSPECTIVE_CALCULATION_KEYWORDS):
            errors.append("Blockout/guide transfer must carry the perspective projection calculation, not only prose scale claims.")
        if not contains_keyword_korean_tolerant(blockout_transfer_text, PERSPECTIVE_BLOCKOUT_GUIDE_KEYWORDS):
            errors.append("Blockout/guide transfer must name concrete guide evidence such as Blender/blockout/overlay/mask/lineart/depth.")

        prompt_transfer_text = " ".join(
            filter(
                None,
                [
                    extract_field(step2_9_block, "PERSPECTIVE_CALCULATION_PROMPT_LOCK"),
                    extract_field(step2_9_block, "SCREEN_OCCUPANCY_DERIVED_PROMPT_LOCK"),
                    extract_image_generation_prompt(text),
                ],
            )
        )
        if image_ready_value == "yes" and not contains_keyword_korean_tolerant(
            prompt_transfer_text,
            PERSPECTIVE_PROMPT_TRANSFER_KEYWORDS,
        ):
            errors.append(
                "Final image prompt must carry natural-language perspective transfer: projected baseline/foot position/same depth/camera crop vs world scale."
            )
        if image_ready_value == "yes" and not contains_keyword_korean_tolerant(
            prompt_transfer_text,
            SCREEN_OCCUPANCY_WORLD_SCALE_KEYWORDS,
        ):
            errors.append(
                "Final image prompt must state screen occupancy is camera/crop-derived and must not override actual/world scale."
            )

        verdict_transfer_text = " ".join(
            filter(
                None,
                [
                    extract_field(step8_block, "PERSPECTIVE_CALCULATION_VERDICT_CHECK"),
                    extract_field(step8_block, "SCREEN_OCCUPANCY_WORLD_SCALE_VERDICT_CHECK"),
                ],
            )
        )
        if not contains_keyword_korean_tolerant(verdict_transfer_text, PERSPECTIVE_CALCULATION_KEYWORDS):
            errors.append("Step 8 verdict must check the projected perspective calculation, not only the final picture's apparent size.")
        if not contains_keyword_korean_tolerant(verdict_transfer_text, SCREEN_OCCUPANCY_WORLD_SCALE_KEYWORDS):
            errors.append("Step 8 verdict must check that screen occupancy/crop did not override world/physical scale.")

    irreversible_structure_expected = render_bound_spec or perspective_expected or anatomy_required_expected or any(
        contains_keyword(field, OBJECT_DENSITY_EDGE_KEYWORDS + GEOMETRIC_BLOCKOUT_KEYWORDS)
        for field in (
            request_summary,
            action_field,
            extract_field(step1_block, "ENVIRONMENT"),
            extract_field(step2_block, "COMPOSITION_OBJECT_ROLE_SUMMARY"),
            extract_field(step2_2_block, "SOURCE_IMAGE_OBJECTS_PRESENT"),
            extract_field(step2_2_block, "PRIMARY_RETAINED_OBJECTS"),
            extract_field(step2_5_block, "REQUIRED_OBJECTS"),
        )
    )
    if irreversible_structure_expected:
        irreversible_fields = (
            ("Step 2.1", step2_1_block, "IRREVERSIBLE_STRUCTURE_REGISTRY"),
            ("Step 2.6", step2_6_block, "OBJECT_ANATOMY_SEPARATION_LOCKS"),
            ("Step 2.6", step2_6_block, "IRREVERSIBLE_OBJECT_ANATOMY_LOCKS"),
            ("Step 2.6", step2_6_block, "ALL_OBJECT_DISTORTION_LOCK"),
            ("Step 2.8", step2_8_block, "OBJECT_ANATOMY_SCALE_INVARIANTS"),
            ("Step 2.8", step2_8_block, "OBJECT_DISTORTION_BLOCKOUT_CHECK"),
            ("Step 2.8", step2_8_block, "IRREVERSIBLE_STRUCTURE_INVARIANTS"),
            ("Step 2.8", step2_8_block, "STRUCTURE_OVER_PAINTERLY_LOCK"),
            ("Step 2.8", step2_8_block, "NO_STRUCTURAL_SACRIFICE_RULE"),
            ("Step 2.9", step2_9_block, "ALL_OBJECTS_ANATOMY_IRREVERSIBLE_LOCK"),
            ("Step 2.9", step2_9_block, "OBJECT_DISTORTION_PROMPT_LOCK"),
            ("Step 2.9", step2_9_block, "VERDICT_IRREVERSIBLE_STRUCTURE_FAILS"),
            ("Step 8", step8_block, "OBJECT_DISTORTION_VERDICT_CHECK"),
            ("Step 8", step8_block, "IRREVERSIBLE_STRUCTURE_CHECK"),
        )
        for section_label, block, field_name in irreversible_fields:
            value = extract_field(block, field_name)
            if count_meaningful_tokens(value) < 6:
                errors.append(f"{section_label} {field_name} must define irreversible object/anatomy structure preservation.")

        irreversible_text = " ".join(
            filter(None, [extract_field(block, field_name) for _, block, field_name in irreversible_fields])
        )
        if not contains_keyword(irreversible_text, IRREVERSIBLE_STRUCTURE_KEYWORDS):
            errors.append(
                "Irreversible structure fields must explicitly forbid omission, deletion, fusion, absorption, resizing, reinterpretation, or sacrifice of registered object/anatomy instances."
            )
        if not contains_keyword(irreversible_text, STRUCTURE_OVER_STYLE_KEYWORDS):
            errors.append(
                "Irreversible structure fields must state that structure is preserved before painterly/style/detail compression."
            )
        if not contains_keyword(irreversible_text, OBJECT_DISTORTION_KEYWORDS):
            errors.append(
                "Irreversible structure fields must explicitly ban object distortion: bending, warping, melting, resizing, fusing, absorption, texture replacement, broken axis/silhouette/function, or similar failures."
            )

    occlusion_signal_text = " ".join(
        filter(
            None,
            [
                request_summary,
                action_field,
                extract_field(step1_block, "ENVIRONMENT"),
                extract_field(step2_block, "COMPOSITION_OBJECT_ROLE_SUMMARY"),
                extract_field(step2_2_block, "SOURCE_IMAGE_OBJECTS_PRESENT"),
                extract_field(step2_2_block, "FOREGROUND_FRAME_OBJECTS"),
                extract_field(step2_2_block, "SUPPORT_PLANE_OBJECTS"),
                extract_field(step2_2_block, "LEFT_VERTICAL_PLANE_OBJECTS"),
                extract_field(step2_2_block, "RIGHT_VERTICAL_PLANE_OBJECTS"),
                extract_field(step2_2_block, "OVERHEAD_PLANE_OBJECTS"),
                extract_field(step2_2_block, "BACKGROUND_DEPTH_OBJECTS"),
                extract_field(step2_2_block, "EFFECT_OBJECTS"),
                extract_field(step2_2_block, "OCCLUDER_MASS_INVENTORY"),
                extract_field(step2_3_block, "PROTECTED_ANATOMY_CHAIN_VISIBILITY"),
                extract_field(step2_5_block, "REQUIRED_OBJECTS"),
            ],
        )
    )
    occlusion_separation_expected = (
        anatomy_required_expected
        or hands_visible_expected
        or contains_keyword(occlusion_signal_text, OCCLUDER_KEYWORDS)
    ) and contains_keyword(occlusion_signal_text, OCCLUDER_KEYWORDS + PROTECTED_CHAIN_KEYWORDS)
    if occlusion_separation_expected:
        occlusion_fields = (
            ("Step 2.2", step2_2_block, "OCCLUDER_MASS_INVENTORY"),
            ("Step 2.3", step2_3_block, "PROTECTED_ANATOMY_CHAIN_VISIBILITY"),
            ("Step 2.6", step2_6_block, "OCCLUSION_ORDER"),
            ("Step 2.6", step2_6_block, "OCCLUSION_LAYER_GRAPH"),
            ("Step 2.6", step2_6_block, "PROTECTED_CHAIN_EXPOSURE_RULES"),
            ("Step 2.6", step2_6_block, "SEPARATION_CUE_PLAN"),
            ("Step 2.8", step2_8_block, "INSTANCE_MASK_SEPARATION_PLAN"),
            ("Step 2.8", step2_8_block, "PROTECTED_CHAIN_MASK_REVIEW"),
            ("Step 2.9", step2_9_block, "OCCLUSION_TRANSLATION_LOCK"),
            ("Step 5", step5_block, "PROTECTED_CHAIN_EDGE_SEPARATION_PLAN"),
            ("Step 8", step8_block, "PROTECTED_CHAIN_TRACE_VERDICT"),
        )
        for section_label, block, field_name in occlusion_fields:
            value = extract_field(block, field_name)
            if count_meaningful_tokens(value) < 6:
                errors.append(
                    f"{section_label} {field_name} must define occluder/protected-chain separation so anatomy, props, or objects are not absorbed by style density."
                )

        occlusion_text = " ".join(
            filter(None, [extract_field(block, field_name) for _, block, field_name in occlusion_fields])
        )
        if not contains_keyword(occlusion_text, OCCLUDER_KEYWORDS):
            errors.append(
                "Occlusion separation fields must explicitly name occluder masses such as cloak, hood, hair, smoke, blood, glow, shadows, background, or black texture."
            )
        if not contains_keyword(occlusion_text, PROTECTED_CHAIN_KEYWORDS):
            errors.append(
                "Occlusion separation fields must explicitly name protected chain landmarks such as shoulder/elbow/wrist/hand, hip/knee/ankle/boot, fingers, hilt, or blade."
            )
        if not contains_keyword(occlusion_text, SEPARATION_CUE_KEYWORDS):
            errors.append(
                "Occlusion separation fields must specify concrete separation cues such as rim light, negative-space gap, value/color edge, cast shadow, contour notch, outline, or mask boundary."
            )
        if image_ready_value == "yes":
            image_prompt = extract_image_generation_prompt(text)
            if not contains_keyword(image_prompt, PROTECTED_CHAIN_KEYWORDS):
                errors.append(
                    "Occlusion-risk IMAGE_GEN_HANDOFF_PROMPT must carry protected-chain landmark language, not leave limb/prop separation only in the spec."
                )
            if not contains_keyword(image_prompt, SEPARATION_CUE_KEYWORDS):
                errors.append(
                    "Occlusion-risk IMAGE_GEN_HANDOFF_PROMPT must carry a concrete separation cue such as rim light, gap, value/color edge, cast shadow, contour notch, outline, or mask boundary."
                )

    if any(
        contains_keyword(field, SWORD_KEYWORDS)
        for field in (request_summary, action_field, extract_field(step2_5_block, "REQUIRED_OBJECTS"))
    ):
        rigid_locks = extract_field(step2_6_block, "RIGID_OBJECT_GEOMETRY_LOCKS")
        if not contains_keyword(rigid_locks, ["straight", "rigid", "blade", "separate", "직선", "강체", "검", "분리"]):
            errors.append("Sword / blade scenes require Step 2.6 RIGID_OBJECT_GEOMETRY_LOCKS to separate rigid blade geometry from effects.")

    if any(
        contains_keyword(field, TEXT_SIGN_KEYWORDS)
        for field in (
            request_summary,
            extract_field(step2_2_block, "TEXT_OR_GLYPH_OBJECTS"),
            extract_field(step2_5_block, "REQUIRED_OBJECTS"),
        )
    ):
        text_policy = extract_field(step2_6_block, "TEXT_RENDERING_POLICY")
        if count_meaningful_tokens(text_policy) < 4:
            errors.append("Signage / text scenes require Step 2.6 TEXT_RENDERING_POLICY.")

    unknown_triage = extract_field(step2_2_block, "UNKNOWN_OBJECT_TRIAGE")
    unknown_policy_lock = extract_field(step2_9_block, "UNKNOWN_OBJECT_POLICY_LOCK")
    unknown_combined = f"{unknown_triage or ''} {unknown_policy_lock or ''}"
    unknown_combined_lower = lower_value(unknown_combined)
    bad_unknown_policy = contains_keyword(unknown_combined, UNKNOWN_UNRESOLVED_KEYWORDS) and "no unresolved" not in unknown_combined_lower
    if image_ready_value == "yes" and bad_unknown_policy:
        errors.append("IMAGE_GEN_READY cannot be 'yes' while unknown objects are unresolved or being replaced with fake/random patterns.")

    if count_meaningful_tokens(extract_field(step2_8_block, "PRIMITIVE_BLOCKS")) < 6:
        errors.append("Step 2.8 PRIMITIVE_BLOCKS must describe 3D/blockout primitives before image translation.")

    geometric_blockout_expected = perspective_expected or likely_requires_geometric_blockout(
        request_summary,
        action_field,
        camera_angle,
        extract_field(step1_block, "ENVIRONMENT"),
        extract_field(step2_block, "CHARACTER_POSITION"),
        extract_field(step2_2_block, "SUPPORT_PLANE_OBJECTS"),
        extract_field(step2_2_block, "LEFT_VERTICAL_PLANE_OBJECTS"),
        extract_field(step2_2_block, "RIGHT_VERTICAL_PLANE_OBJECTS"),
        extract_field(step2_2_block, "BACKGROUND_DEPTH_OBJECTS"),
        extract_field(step2_5_block, "REQUIRED_OBJECTS"),
    )
    if geometric_blockout_expected:
        for field_name in (
            "ENVIRONMENT_PRIMITIVE_BLOCKOUT",
            "SHARED_PERSPECTIVE_GRID",
            "METER_SCALE_LOCK",
            "ABSOLUTE_SCALE_LADDER",
            "OBJECT_ANATOMY_SCALE_INVARIANTS",
            "OBJECT_DISTORTION_BLOCKOUT_CHECK",
            "IRREVERSIBLE_STRUCTURE_INVARIANTS",
            "ANATOMY_TO_ARCHITECTURE_SCALE_CHECK",
            "FOOTPRINT_ON_SUPPORT_PLANE_CHECK",
            "DETAIL_AFTER_BLOCKOUT_LOCK",
            "STRUCTURE_OVER_PAINTERLY_LOCK",
            "NO_STRUCTURAL_SACRIFICE_RULE",
        ):
            if count_meaningful_tokens(extract_field(step2_8_block, field_name)) < 6:
                errors.append(f"Geometric blockout scenes require Step 2.8 {field_name} to lock structure before detail.")
        detail_lock = extract_field(step2_8_block, "DETAIL_AFTER_BLOCKOUT_LOCK")
        if not contains_keyword(detail_lock, ["detail", "after", "blockout", "structure", "디테일", "도형", "구조", "이후"]):
            errors.append("Step 2.8 DETAIL_AFTER_BLOCKOUT_LOCK must say detail follows the locked primitive structure.")

    architecture_scale_expected = any(
        contains_keyword(field, ["building", "architecture", "facade", "window", "parapet", "rooftop", "건물", "건축", "파사드", "창문", "파라펫", "옥상"])
        for field in (
            request_summary,
            extract_field(step1_block, "ENVIRONMENT"),
            extract_field(step2_1_block, "SCALE_ANCHOR_OBJECTS"),
            extract_field(step2_2_block, "SUPPORT_PLANE_OBJECTS"),
            extract_field(step2_2_block, "LEFT_VERTICAL_PLANE_OBJECTS"),
            extract_field(step2_2_block, "RIGHT_VERTICAL_PLANE_OBJECTS"),
            extract_field(step2_2_block, "BACKGROUND_DEPTH_OBJECTS"),
        )
    )
    if architecture_scale_expected:
        for field_name in (
            "WINDOW_TO_HEAD_SIZE_CHECK",
            "PARAPET_TO_BODY_HEIGHT_CHECK",
            "DOOR_VEHICLE_FUNCTIONAL_SCALE_CHECK",
            "FOOTPRINT_ON_SUPPORT_PLANE_CHECK",
            "ANATOMY_TO_ARCHITECTURE_SCALE_CHECK",
        ):
            if count_meaningful_tokens(extract_field(step2_8_block, field_name)) < 5:
                errors.append(f"Architecture-scale figure scenes require Step 2.8 {field_name}.")

    blender_blockout_required = lower_value(extract_field(step2_8_block, "BLENDER_BLOCKOUT_REQUIRED"))
    blender_scene_path = extract_field(step2_8_block, "BLENDER_SCENE_PATH")
    blender_render_script_path = extract_field(step2_8_block, "BLENDER_RENDER_SCRIPT_PATH")
    blender_pass_outputs = extract_field(step2_8_block, "BLENDER_PASS_OUTPUTS")
    blender_blockout_review = extract_field(step2_8_block, "BLENDER_BLOCKOUT_REVIEW")
    blender_guide_strength = lower_value(extract_field(step2_8_block, "BLENDER_GUIDE_STRENGTH"))
    blockout_core_object_visibility = extract_field(step2_8_block, "BLOCKOUT_CORE_OBJECT_VISIBILITY")
    blockout_target_contact_visibility = extract_field(step2_8_block, "BLOCKOUT_TARGET_CONTACT_VISIBILITY")
    blockout_camera_occlusion_check = extract_field(step2_8_block, "BLOCKOUT_CAMERA_OCCLUSION_CHECK")
    blender_visibility_report_path = extract_field(step2_8_block, "BLENDER_VISIBILITY_REPORT_PATH")
    blender_visibility_report_review = extract_field(step2_8_block, "BLENDER_VISIBILITY_REPORT_REVIEW")
    visual_guide_composite_required = lower_value(extract_field(step2_8_block, "VISUAL_GUIDE_COMPOSITE_REQUIRED"))
    visual_guide_composite_path = extract_field(step2_8_block, "VISUAL_GUIDE_COMPOSITE_PATH")
    visual_guide_composite_source_passes = extract_field(step2_8_block, "VISUAL_GUIDE_COMPOSITE_SOURCE_PASSES")
    visual_guide_composite_overlays = extract_field(step2_8_block, "VISUAL_GUIDE_COMPOSITE_OVERLAYS")
    visual_guide_composite_review = lower_value(extract_field(step2_8_block, "VISUAL_GUIDE_COMPOSITE_REVIEW"))
    visual_guide_composite_conditioning_role = extract_field(step2_8_block, "VISUAL_GUIDE_COMPOSITE_CONDITIONING_ROLE")
    scale_composite_hard_lock = lower_value(extract_field(step2_8_block, "SCALE_COMPOSITE_HARD_LOCK"))
    user_visual_guide_checkpoint_required = lower_value(extract_field(step2_8_block, "USER_VISUAL_GUIDE_CHECKPOINT_REQUIRED"))
    user_visual_guide_feedback = extract_field(step2_8_block, "USER_VISUAL_GUIDE_FEEDBACK")
    user_visual_guide_feedback_applied = lower_value(extract_field(step2_8_block, "USER_VISUAL_GUIDE_FEEDBACK_APPLIED"))
    user_visual_guide_approval_status = lower_value(extract_field(step2_8_block, "USER_VISUAL_GUIDE_APPROVAL_STATUS"))
    scale_visual_guide_package = extract_field(step2_8_block, "SCALE_VISUAL_GUIDE_PACKAGE")
    cut_plane_visual_guide_package = extract_field(step2_8_block, "CUT_PLANE_VISUAL_GUIDE_PACKAGE")
    grip_mechanics_visual_guide_package = extract_field(step2_8_block, "GRIP_MECHANICS_VISUAL_GUIDE_PACKAGE")
    structural_invariants = extract_field(step2_8_block, "STRUCTURAL_INVARIANTS_TO_PRESERVE")
    painterly_freedoms = extract_field(step2_8_block, "PAINTERLY_FREEDOMS_ALLOWED")
    structure_over_painterly = extract_field(step2_8_block, "STRUCTURE_OVER_PAINTERLY_LOCK")
    no_structural_sacrifice_rule = extract_field(step2_8_block, "NO_STRUCTURAL_SACRIFICE_RULE")
    controlnet_conditioning_plan = extract_field(step2_8_block, "CONTROLNET_CONDITIONING_PLAN")
    blockout_review_status = lower_value(extract_field(step2_8_block, "BLOCKOUT_REVIEW_STATUS"))
    step2_9_blender_guide_strength = lower_value(extract_field(step2_9_block, "BLENDER_GUIDE_STRENGTH"))
    text_only_locks_rejection = extract_field(step2_9_block, "TEXT_ONLY_LOCKS_REJECTION")
    visual_guide_composite_prompt_lock = extract_field(step2_9_block, "VISUAL_GUIDE_COMPOSITE_PROMPT_LOCK")
    image_input_stack_plan = extract_field(step2_9_block, "IMAGE_INPUT_STACK_PLAN")
    pre_composite_evidence_stack_lock = extract_field(step2_9_block, "PRE_COMPOSITE_EVIDENCE_STACK_LOCK")
    scale_proxy_trace_prompt_lock = extract_field(step2_9_block, "SCALE_PROXY_TRACE_PROMPT_LOCK")
    composite_is_reference_not_sole_authority = extract_field(step2_9_block, "COMPOSITE_IS_REFERENCE_NOT_SOLE_AUTHORITY")
    scale_must_follow_composite_prompt_lock = extract_field(step2_9_block, "SCALE_MUST_FOLLOW_COMPOSITE_PROMPT_LOCK")
    image_gen_structure_conditioning_mode = lower_value(extract_field(step2_9_block, "IMAGE_GEN_STRUCTURE_CONDITIONING_MODE"))
    image_gen_structure_conditioning_strength = lower_value(extract_field(step2_9_block, "IMAGE_GEN_STRUCTURE_CONDITIONING_STRENGTH"))
    image_gen_structure_conditioning_inputs = extract_field(step2_9_block, "IMAGE_GEN_STRUCTURE_CONDITIONING_INPUTS")
    image_gen_structure_conditioning_limits = extract_field(step2_9_block, "IMAGE_GEN_STRUCTURE_CONDITIONING_LIMITS")
    image_gen_handoff_package_path = extract_field(step2_9_block, "IMAGE_GEN_HANDOFF_PACKAGE_PATH")
    scale_visual_guide_prompt_lock = extract_field(step2_9_block, "SCALE_VISUAL_GUIDE_PROMPT_LOCK")
    cut_plane_visibility_prompt_lock = extract_field(step2_9_block, "CUT_PLANE_VISIBILITY_PROMPT_LOCK")
    grip_mechanics_prompt_lock = extract_field(step2_9_block, "GRIP_MECHANICS_PROMPT_LOCK")
    scale_over_style_lock = extract_field(step2_9_block, "SCALE_OVER_STYLE_LOCK")
    prompt_attention_budget_lock = extract_field(step2_9_block, "PROMPT_ATTENTION_BUDGET_LOCK")
    tiered_image_prompt_locks = extract_field(step2_9_block, "TIERED_IMAGE_PROMPT_LOCKS")
    all_objects_anatomy_irreversible_lock = extract_field(step2_9_block, "ALL_OBJECTS_ANATOMY_IRREVERSIBLE_LOCK")
    painterly_compression_allowance = extract_field(step2_9_block, "PAINTERLY_COMPRESSION_ALLOWANCE")
    no_hieratic_scale_distortion = extract_field(step2_9_block, "NO_HIERATIC_SCALE_DISTORTION")
    verdict_scale_and_mixing_fails = extract_field(step2_9_block, "VERDICT_SCALE_AND_MIXING_FAILS")
    verdict_irreversible_structure_fails = extract_field(step2_9_block, "VERDICT_IRREVERSIBLE_STRUCTURE_FAILS")
    scale_visual_guide_verdict_check = extract_field(step8_block, "SCALE_VISUAL_GUIDE_VERDICT_CHECK")
    visual_guide_composite_verdict_check = extract_field(step8_block, "VISUAL_GUIDE_COMPOSITE_VERDICT_CHECK")
    user_visual_guide_approval_verdict_check = extract_field(step8_block, "USER_VISUAL_GUIDE_APPROVAL_VERDICT_CHECK")
    scale_proxy_trace_verdict_check = extract_field(step8_block, "SCALE_PROXY_TRACE_VERDICT_CHECK")
    pre_composite_evidence_stack_verdict_check = extract_field(step8_block, "PRE_COMPOSITE_EVIDENCE_STACK_VERDICT_CHECK")
    scale_composite_hard_lock_verdict_check = extract_field(step8_block, "SCALE_COMPOSITE_HARD_LOCK_VERDICT_CHECK")
    cut_plane_visibility_verdict_check = extract_field(step8_block, "CUT_PLANE_VISIBILITY_VERDICT_CHECK")
    cut_result_unknown_form_verdict_check = extract_field(step8_block, "CUT_RESULT_UNKNOWN_FORM_VERDICT_CHECK")
    weapon_grip_mechanics_verdict_check = extract_field(step8_block, "WEAPON_GRIP_MECHANICS_VERDICT_CHECK")
    wrist_force_path_verdict_check = extract_field(step8_block, "WRIST_FORCE_PATH_VERDICT_CHECK")
    allowed_guide_strengths = {"loose guide", "medium guide", "strict guide", "not_applicable"}

    blender_route_decision = lower_value(extract_field(step2_8_block, "BLENDER_ROUTE_DECISION"))
    blender_route_decision_reason = extract_field(step2_8_block, "BLENDER_ROUTE_DECISION_REASON")
    blender_skip_reason = extract_field(step2_8_block, "BLENDER_SKIP_REASON")
    optional_3d_reference_plan = extract_field(step2_8_block, "OPTIONAL_3D_REFERENCE_PLAN")

    if blender_route_decision and blender_route_decision not in {"use_blender", "skip_blender"}:
        errors.append("BLENDER_ROUTE_DECISION must be use_blender or skip_blender when present.")
    if render_bound_spec and blender_blockout_required == "no":
        skip_text = " ".join(filter(None, [blender_route_decision_reason, blender_skip_reason, optional_3d_reference_plan]))
        if blender_route_decision and blender_route_decision != "skip_blender":
            errors.append("BLENDER_BLOCKOUT_REQUIRED: no requires BLENDER_ROUTE_DECISION: skip_blender.")
        if count_meaningful_tokens(skip_text) < 10 or not indicates_explicit_skip(skip_text):
            errors.append(
                "Render-bound BLENDER_BLOCKOUT_REQUIRED: no requires a concrete skip reason: no/simple background or character-only scene, no scale-critical/hard-surface/contact/grip/source-structure risk, and direct_text_prompt route."
            )
        if scale_critical_active:
            errors.append("Scale-critical human-enterable scenes cannot skip Blender/blockout evidence.")
        if visual_guide_composite_required == "yes" or user_visual_guide_checkpoint_required == "yes":
            errors.append("BLENDER_BLOCKOUT_REQUIRED: no must also set VISUAL_GUIDE_COMPOSITE_REQUIRED: no and USER_VISUAL_GUIDE_CHECKPOINT_REQUIRED: no.")
        if image_ready_value == "yes" and image_gen_structure_conditioning_mode not in {"direct_text_prompt", "not_applicable"}:
            errors.append("No-Blender image handoff should use IMAGE_GEN_STRUCTURE_CONDITIONING_MODE: direct_text_prompt or not_applicable.")

    if any(
        contains_keyword(field, ["blender", "controlnet", "depth map", "normal map", "lineart", "3d-first", "3d first"])
        and not indicates_explicit_skip(field)
        for field in (request_summary, optional_3d_reference_plan)
    ) and blender_blockout_required != "yes":
        errors.append(
            "Spec mentions Blender/ControlNet-style conditioning but BLENDER_BLOCKOUT_REQUIRED is not 'yes'."
        )

    if blender_blockout_required == "yes":
        for field_name, field_value in (
            ("BLENDER_SCENE_PATH", blender_scene_path),
            ("BLENDER_RENDER_SCRIPT_PATH", blender_render_script_path),
            ("BLENDER_PASS_OUTPUTS", blender_pass_outputs),
            ("BLENDER_BLOCKOUT_REVIEW", blender_blockout_review),
                    ("BLENDER_GUIDE_STRENGTH", blender_guide_strength),
                    ("BLOCKOUT_CORE_OBJECT_VISIBILITY", blockout_core_object_visibility),
                    ("BLOCKOUT_CAMERA_OCCLUSION_CHECK", blockout_camera_occlusion_check),
                    ("BLENDER_VISIBILITY_REPORT_PATH", blender_visibility_report_path),
                    ("BLENDER_VISIBILITY_REPORT_REVIEW", blender_visibility_report_review),
                    ("STRUCTURAL_INVARIANTS_TO_PRESERVE", structural_invariants),
                    ("PAINTERLY_FREEDOMS_ALLOWED", painterly_freedoms),
                    ("STRUCTURE_OVER_PAINTERLY_LOCK", structure_over_painterly),
                    ("NO_STRUCTURAL_SACRIFICE_RULE", no_structural_sacrifice_rule),
                    ("CONTROLNET_CONDITIONING_PLAN", controlnet_conditioning_plan),
                ):
            if value_is_none_like(field_value) or count_meaningful_tokens(field_value) < 2:
                errors.append(f"BLENDER_BLOCKOUT_REQUIRED: yes requires Step 2.8 {field_name}.")

        if blender_guide_strength not in allowed_guide_strengths - {"not_applicable"}:
            errors.append(
                "BLENDER_BLOCKOUT_REQUIRED: yes requires BLENDER_GUIDE_STRENGTH to be one of "
                "'loose guide', 'medium guide', or 'strict guide'."
            )

        if step2_9_blender_guide_strength not in allowed_guide_strengths - {"not_applicable"}:
            errors.append(
                "Render-bound image translation requires Step 2.9 BLENDER_GUIDE_STRENGTH to be "
                "'loose guide', 'medium guide', or 'strict guide'."
            )
        elif step2_9_blender_guide_strength != blender_guide_strength:
            errors.append("Step 2.8 and Step 2.9 BLENDER_GUIDE_STRENGTH values must match.")

        if scale_critical_active:
            if blender_guide_strength != "strict guide" or step2_9_blender_guide_strength != "strict guide":
                errors.append(
                    "Scale-critical human-enterable scenes require BLENDER_GUIDE_STRENGTH: strict guide "
                    "in both Step 2.8 and Step 2.9; loose guide cannot police protagonist/container scale."
                )
            blockout_evidence_text = " ".join(
                value or ""
                for value in (
                    blender_scene_path,
                    blender_render_script_path,
                    blender_pass_outputs,
                    blender_blockout_review,
                    extract_field(step2_8_block, "REAL_BLOCKOUT_EVIDENCE_STATUS"),
                    extract_field(step2_8_block, "STRICT_SCALE_BLOCKOUT_RATIO_REVIEW"),
                    controlnet_conditioning_plan,
                )
            )
            if image_ready_value == "yes" and contains_proxy_blockout_evidence(blockout_evidence_text):
                errors.append(
                    "Scale-critical IMAGE_GEN_READY: yes cannot use placeholder/proxy/SVG-only/Blender-unavailable blockout evidence."
                )

            for label, field_value in (
                ("SCALE_VISUAL_GUIDE_PACKAGE", scale_visual_guide_package),
                ("SCALE_VISUAL_GUIDE_PROMPT_LOCK", scale_visual_guide_prompt_lock),
                ("SCALE_VISUAL_GUIDE_VERDICT_CHECK", scale_visual_guide_verdict_check),
            ):
                if value_is_none_like(field_value) or count_meaningful_tokens(field_value) < 8:
                    errors.append(
                        f"Scale-critical scenes require {label}: text-only scale locks are insufficient after repeated protagonist/tram scale failures."
                    )
                elif not (
                    contains_keyword_korean_tolerant(field_value, VISUAL_GUIDE_EXECUTION_KEYWORDS)
                    and contains_keyword_korean_tolerant(field_value, SCALE_CRITICAL_RATIO_KEYWORDS + SCALE_CRITICAL_CONTAINER_KEYWORDS)
                ):
                    errors.append(
                        f"{label} must name visual scale-guide evidence such as mask/overlay/blockout plus passenger/door/window/ratio anchors."
                    )

        if render_bound_spec:
            if value_is_none_like(text_only_locks_rejection) or count_meaningful_tokens(text_only_locks_rejection) < 8:
                errors.append(
                    "Render-bound image handoff requires TEXT_ONLY_LOCKS_REJECTION explaining that prompt text alone cannot pass high-risk scale/contact/grip gates."
                )
            elif not (
                contains_keyword_korean_tolerant(text_only_locks_rejection, TEXT_ONLY_REJECTION_KEYWORDS)
                and contains_keyword_korean_tolerant(text_only_locks_rejection, VISUAL_GUIDE_EXECUTION_KEYWORDS)
            ):
                errors.append(
                    "TEXT_ONLY_LOCKS_REJECTION must explicitly reject prompt/text-only locks and require visual guide/blockout/mask evidence."
                )

            composite_text = " ".join(
                filter(
                    None,
                    [
                        visual_guide_composite_path,
                        visual_guide_composite_source_passes,
                        visual_guide_composite_overlays,
                        visual_guide_composite_conditioning_role,
                        scale_composite_hard_lock,
                        visual_guide_composite_prompt_lock,
                        image_input_stack_plan,
                        pre_composite_evidence_stack_lock,
                        scale_proxy_trace_prompt_lock,
                        composite_is_reference_not_sole_authority,
                        scale_must_follow_composite_prompt_lock,
                        image_gen_structure_conditioning_mode,
                        image_gen_structure_conditioning_strength,
                        image_gen_structure_conditioning_inputs,
                        image_gen_structure_conditioning_limits,
                        image_gen_handoff_package_path,
                        visual_guide_composite_verdict_check,
                        scale_proxy_trace_verdict_check,
                        pre_composite_evidence_stack_verdict_check,
                        scale_composite_hard_lock_verdict_check,
                    ],
                )
            )
            if visual_guide_composite_required != "yes":
                errors.append(
                    "Render-bound image handoff requires VISUAL_GUIDE_COMPOSITE_REQUIRED: yes so blockout/line/depth evidence becomes a user-reviewed image input."
                )
            for field_name, field_value in (
                ("VISUAL_GUIDE_COMPOSITE_PATH", visual_guide_composite_path),
                ("VISUAL_GUIDE_COMPOSITE_SOURCE_PASSES", visual_guide_composite_source_passes),
                ("VISUAL_GUIDE_COMPOSITE_OVERLAYS", visual_guide_composite_overlays),
                ("VISUAL_GUIDE_COMPOSITE_CONDITIONING_ROLE", visual_guide_composite_conditioning_role),
                ("VISUAL_GUIDE_COMPOSITE_PROMPT_LOCK", visual_guide_composite_prompt_lock),
                ("IMAGE_INPUT_STACK_PLAN", image_input_stack_plan),
                ("PRE_COMPOSITE_EVIDENCE_STACK_LOCK", pre_composite_evidence_stack_lock),
                ("COMPOSITE_IS_REFERENCE_NOT_SOLE_AUTHORITY", composite_is_reference_not_sole_authority),
                ("SCALE_MUST_FOLLOW_COMPOSITE_PROMPT_LOCK", scale_must_follow_composite_prompt_lock),
                ("IMAGE_GEN_STRUCTURE_CONDITIONING_INPUTS", image_gen_structure_conditioning_inputs),
                ("IMAGE_GEN_STRUCTURE_CONDITIONING_LIMITS", image_gen_structure_conditioning_limits),
                ("IMAGE_GEN_HANDOFF_PACKAGE_PATH", image_gen_handoff_package_path),
                ("VISUAL_GUIDE_COMPOSITE_VERDICT_CHECK", visual_guide_composite_verdict_check),
                ("PRE_COMPOSITE_EVIDENCE_STACK_VERDICT_CHECK", pre_composite_evidence_stack_verdict_check),
                ("SCALE_COMPOSITE_HARD_LOCK_VERDICT_CHECK", scale_composite_hard_lock_verdict_check),
            ):
                if value_is_none_like(field_value) or count_meaningful_tokens(field_value) < 6:
                    errors.append(f"Render-bound visual-guide checkpoint requires {field_name}.")
            if not contains_keyword_korean_tolerant(composite_text, VISUAL_GUIDE_COMPOSITE_KEYWORDS):
                errors.append(
                    "Visual guide composite fields must mention a clay/lineart/depth composite with perspective lines, scale baselines, footpoint, door/passenger/protagonist markers, and image/reference conditioning role."
                )
            if not contains_keyword_korean_tolerant(composite_text, IMAGE_GEN_STRUCTURE_CONDITIONING_KEYWORDS):
                errors.append(
                    "Image generation handoff must use actual image-input conditioning language: high-fidelity image inputs/reference images, visual guide composite, lineart/depth/clay roles, and not text-only generation."
                )
            evidence_stack_text = " ".join(
                filter(
                    None,
                    [
                        pre_composite_evidence_stack_lock,
                        composite_is_reference_not_sole_authority,
                        pre_composite_evidence_stack_verdict_check,
                        image_input_stack_plan,
                        image_gen_structure_conditioning_inputs,
                        image_gen_handoff_package_path,
                    ],
                )
            )
            if not contains_keyword_korean_tolerant(evidence_stack_text, PRE_COMPOSITE_EVIDENCE_STACK_KEYWORDS):
                errors.append(
                    "Image generation handoff must state that the approved composite is one structure reference in the full pre-composite evidence stack, not the sole authority or a replacement for source/object/perspective/blockout/final-prompt locks."
                )
            if not (
                contains_keyword_korean_tolerant(
                    evidence_stack_text,
                    [
                        "source image",
                        "object research",
                        "perspective calculation",
                        "perspective math",
                        "blender blockout",
                        "visibility report",
                        "final prompt",
                        "원본 이미지",
                        "오브젝트 리서치",
                        "투시 계산",
                        "블록아웃",
                        "가시성 리포트",
                        "최종 프롬프트",
                    ],
                )
                and contains_keyword_korean_tolerant(
                    evidence_stack_text,
                    [
                        "not sole authority",
                        "not only composite",
                        "not composite only",
                        "one reference",
                        "not a replacement",
                        "composite is not",
                        "유일한 근거",
                        "하나의 참고",
                        "참조 중 하나",
                        "대체",
                        "단독",
                    ],
                )
            ):
                errors.append(
                    "PRE_COMPOSITE_EVIDENCE_STACK_LOCK / COMPOSITE_IS_REFERENCE_NOT_SOLE_AUTHORITY must include both (1) pre-composite sources such as source/object/perspective/blockout/final prompt and (2) an explicit not-composite-only / not-sole-authority statement."
                )
            if scale_critical_active:
                if scale_composite_hard_lock != "yes":
                    errors.append(
                        "Scale-critical render-bound handoff requires SCALE_COMPOSITE_HARD_LOCK: yes; scale must follow the approved visual guide composite even though the composite is not the sole authority for the whole image."
                    )
                scale_composite_hard_lock_text = " ".join(
                    filter(
                        None,
                        [
                            visual_guide_composite_overlays,
                            visual_guide_composite_conditioning_role,
                            visual_guide_composite_prompt_lock,
                            scale_must_follow_composite_prompt_lock,
                            scale_visual_guide_prompt_lock,
                            scale_visual_guide_verdict_check,
                            visual_guide_composite_verdict_check,
                            scale_composite_hard_lock_verdict_check,
                        ],
                    )
                )
                if not contains_keyword_korean_tolerant(
                    scale_composite_hard_lock_text,
                    SCALE_COMPOSITE_HARD_LOCK_KEYWORDS,
                ):
                    errors.append(
                        "Scale-critical scale handoff must explicitly say that protagonist/object scale follows the approved composite's scale markers/baselines/footpoints and fails/rerenders if scale drifts."
                    )
                for field_name, field_value in (
                    ("SCALE_PROXY_TRACE_PROMPT_LOCK", scale_proxy_trace_prompt_lock),
                    ("SCALE_PROXY_TRACE_VERDICT_CHECK", scale_proxy_trace_verdict_check),
                    ("SCALE_MUST_FOLLOW_COMPOSITE_PROMPT_LOCK", scale_must_follow_composite_prompt_lock),
                    ("SCALE_COMPOSITE_HARD_LOCK_VERDICT_CHECK", scale_composite_hard_lock_verdict_check),
                ):
                    if value_is_none_like(field_value) or count_meaningful_tokens(field_value) < 6:
                        errors.append(
                            f"Scale-critical render-bound handoff requires {field_name} so the approved composite's scale trace, not style/action/beauty pressure, carries scale into generation."
                        )
                    elif not (
                        contains_keyword_korean_tolerant(field_value, SCALE_PROXY_DUMMY_KEYWORDS)
                        or contains_keyword_korean_tolerant(field_value, SCALE_COMPOSITE_HARD_LOCK_KEYWORDS)
                    ):
                        errors.append(
                            f"{field_name} must mention the dummy/mannequin-derived height trace/baseline/projection and/or the approved composite scale hard-lock."
                        )
            if image_gen_structure_conditioning_mode in {"", "not_applicable", "blocked_text_only"}:
                errors.append(
                    "Render-bound image handoff requires IMAGE_GEN_STRUCTURE_CONDITIONING_MODE: openai_high_fidelity_image_inputs or external_controlnet; text-only image_gen is blocked."
                )
            if image_gen_structure_conditioning_strength in {"", "not_applicable", "loose_reference"}:
                errors.append(
                    "Render-bound image handoff requires IMAGE_GEN_STRUCTURE_CONDITIONING_STRENGTH: strict_structure or medium_structure, with strict_structure for scale/contact/cut/grip-critical scenes."
                )
            if image_ready_value == "yes":
                if visual_guide_composite_review != "pass":
                    errors.append("PRE_IMAGE_HANDOFF_READY: yes requires VISUAL_GUIDE_COMPOSITE_REVIEW: pass.")
                if user_visual_guide_checkpoint_required != "yes":
                    errors.append("PRE_IMAGE_HANDOFF_READY: yes requires USER_VISUAL_GUIDE_CHECKPOINT_REQUIRED: yes.")
                if user_visual_guide_approval_status != "approved":
                    errors.append("PRE_IMAGE_HANDOFF_READY: yes requires USER_VISUAL_GUIDE_APPROVAL_STATUS: approved after the user reviews the visual guide composite.")
                if user_visual_guide_feedback_applied != "pass":
                    errors.append("PRE_IMAGE_HANDOFF_READY: yes requires USER_VISUAL_GUIDE_FEEDBACK_APPLIED: pass, or PRE_IMAGE_HANDOFF_READY must remain no while revisions are pending.")
                if not contains_keyword_korean_tolerant(
                    " ".join(filter(None, [user_visual_guide_feedback, user_visual_guide_approval_verdict_check])),
                    VISUAL_GUIDE_APPROVAL_KEYWORDS,
                ):
                    errors.append("User visual guide feedback/approval fields must record the user's feedback or explicit approval before image handoff.")
                if contains_keyword_korean_tolerant(
                    user_visual_guide_feedback,
                    ASSUMED_VISUAL_GUIDE_APPROVAL_KEYWORDS,
                ):
                    errors.append(
                        "USER_VISUAL_GUIDE_FEEDBACK cannot be an assumed/auto approval. "
                        "Stop at the clay/visual-guide checkpoint and keep PRE_IMAGE_HANDOFF_READY: no "
                        "until the user explicitly reviews and approves the guide."
                    )
                if visual_guide_composite_path and not value_is_none_like(visual_guide_composite_path):
                    composite_path = resolve_reference_path(visual_guide_composite_path, path)
                    if not composite_path.exists():
                        errors.append(f"VISUAL_GUIDE_COMPOSITE_PATH points to a missing file: {visual_guide_composite_path}")
                if image_gen_structure_conditioning_mode not in {
                    "openai_high_fidelity_image_inputs",
                    "external_controlnet",
                }:
                    errors.append("PRE_IMAGE_HANDOFF_READY: yes requires an actual image-input conditioning mode, not blocked_text_only.")
                if scale_critical_active and image_gen_structure_conditioning_strength != "strict_structure":
                    errors.append("Scale-critical PRE_IMAGE_HANDOFF_READY: yes requires IMAGE_GEN_STRUCTURE_CONDITIONING_STRENGTH: strict_structure.")
                if image_gen_handoff_package_path and not value_is_none_like(image_gen_handoff_package_path):
                    handoff_package_path = resolve_reference_path(image_gen_handoff_package_path, path)
                    if not handoff_package_path.exists():
                        errors.append(f"IMAGE_GEN_HANDOFF_PACKAGE_PATH points to a missing file: {image_gen_handoff_package_path}")

        if count_meaningful_tokens(painterly_compression_allowance) < 4:
            errors.append(
                "Step 2.9 PAINTERLY_COMPRESSION_ALLOWANCE must state what compression/massing is allowed or disallowed."
            )

        for field_name, field_value in (
            ("SCALE_OVER_STYLE_LOCK", scale_over_style_lock),
            ("PROMPT_ATTENTION_BUDGET_LOCK", prompt_attention_budget_lock),
            ("TIERED_IMAGE_PROMPT_LOCKS", tiered_image_prompt_locks),
            ("ALL_OBJECTS_ANATOMY_IRREVERSIBLE_LOCK", all_objects_anatomy_irreversible_lock),
            ("OBJECT_DISTORTION_PROMPT_LOCK", extract_field(step2_9_block, "OBJECT_DISTORTION_PROMPT_LOCK")),
            ("VERDICT_SCALE_AND_MIXING_FAILS", verdict_scale_and_mixing_fails),
            ("VERDICT_IRREVERSIBLE_STRUCTURE_FAILS", verdict_irreversible_structure_fails),
        ):
            if count_meaningful_tokens(field_value) < 6:
                errors.append(f"Render-bound image translation requires Step 2.9 {field_name}.")

        tier_budget_text = " ".join(filter(None, [prompt_attention_budget_lock, tiered_image_prompt_locks, extract_field(step2_9_block, "PROMPT_COMPRESSION_RULE")]))
        if not contains_keyword(tier_budget_text, TIERED_PROMPT_KEYWORDS):
            errors.append("Step 2.9 prompt-budget fields must describe a tiered prompt hierarchy: macro scale/capacity, face/anatomy, contacts/props, then reducible style/detail.")

        if count_meaningful_tokens(no_hieratic_scale_distortion) < 6:
            errors.append(
                "Step 2.9 NO_HIERATIC_SCALE_DISTORTION must state that authority/power cannot be shown by impossible body-size scaling."
            )
        if contains_keyword(
            " ".join(
                value or ""
                for value in (
                    structural_invariants,
                    painterly_freedoms,
                    painterly_compression_allowance,
                    extract_field(step2_9_block, "PROMPT_COMPRESSION_RULE"),
                    extract_image_generation_prompt(text),
                )
            ),
            ["symbolic scale emphasis", "hieratic scale", "권력 스케일", "상징적 크기"],
        ) and not contains_keyword(no_hieratic_scale_distortion, ["explicitly requested", "user explicitly", "명시", "요청"]):
            errors.append(
                "Spec mentions symbolic/hieratic scale language without an explicit opt-in exception in NO_HIERATIC_SCALE_DISTORTION."
            )

        if blockout_review_status != "pass":
            errors.append("BLENDER_BLOCKOUT_REQUIRED: yes requires BLOCKOUT_REVIEW_STATUS: pass before Step 2.8 can pass.")

        if image_ready_value == "yes":
            for label, field_value in (
                ("BLOCKOUT_CORE_OBJECT_VISIBILITY", blockout_core_object_visibility),
                ("BLOCKOUT_CAMERA_OCCLUSION_CHECK", blockout_camera_occlusion_check),
                ("BLENDER_VISIBILITY_REPORT_REVIEW", blender_visibility_report_review),
            ):
                if value_is_none_like(field_value) or count_meaningful_tokens(field_value) < 6:
                    errors.append(
                        f"PRE_IMAGE_HANDOFF_READY: yes with Blender requires Step 2.8 {label} to prove the pass is visually usable, not merely present on disk."
                    )
                elif not value_indicates_pass(field_value):
                    errors.append(
                        f"PRE_IMAGE_HANDOFF_READY: yes with Blender requires Step 2.8 {label} to explicitly pass."
                    )

            if action_contact_expected:
                if value_is_none_like(blockout_target_contact_visibility) or count_meaningful_tokens(blockout_target_contact_visibility) < 6:
                    errors.append(
                        "Action/contact image handoff requires Step 2.8 BLOCKOUT_TARGET_CONTACT_VISIBILITY proving the named target/subpart is visible."
                    )
                elif not value_indicates_pass(blockout_target_contact_visibility):
                    errors.append("BLOCKOUT_TARGET_CONTACT_VISIBILITY must explicitly pass before image handoff.")
                elif not contains_keyword_korean_tolerant(
                    blockout_target_contact_visibility,
                    ["target", "forbidden", "contact", "neck", "subpart", "대상", "금지", "접촉", "목", "부위"],
                ):
                    errors.append(
                        "BLOCKOUT_TARGET_CONTACT_VISIBILITY must mention the visible target/subpart and forbidden-target exclusion."
                    )

            if is_placeholder(blender_visibility_report_path) or lower_value(blender_visibility_report_path) == "not_applicable":
                errors.append(
                    "PRE_IMAGE_HANDOFF_READY: yes with Blender requires BLENDER_VISIBILITY_REPORT_PATH to a JSON visibility report; pass PNG existence alone is insufficient."
                )
            else:
                visibility_report_path = resolve_reference_path(blender_visibility_report_path or "", path)
                visibility_result = validate_blender_visibility_report(
                    visibility_report_path,
                    spec_path=path,
                    require_target_contact=action_contact_expected,
                )
                errors.extend(f"Blender visibility report: {item}" for item in visibility_result.errors)
                warnings.extend(f"Blender visibility report: {item}" for item in visibility_result.warnings)

        for field_name, field_value in (
            ("BLENDER_SCENE_PATH", blender_scene_path),
            ("BLENDER_RENDER_SCRIPT_PATH", blender_render_script_path),
        ):
            if not value_is_none_like(field_value):
                artifact_path = resolve_reference_path(field_value or "", path)
                if not artifact_path.exists():
                    errors.append(f"{field_name} points to a missing file: {field_value}")

        pass_paths: list[tuple[str, str]] = []
        if blender_pass_outputs and not value_is_none_like(blender_pass_outputs):
            for item in re.split(r"\s*\|\s*", blender_pass_outputs):
                if not item.strip():
                    continue
                if "=" in item:
                    label, value = item.split("=", 1)
                    pass_paths.append((label.strip(), value.strip()))
                else:
                    pass_paths.append(("pass", item.strip()))
        if len(pass_paths) < 2:
            errors.append("BLENDER_BLOCKOUT_REQUIRED: yes requires at least two BLENDER_PASS_OUTPUTS entries, e.g. clay and lineart/depth.")
        for label, pass_path_value in pass_paths:
            if value_is_none_like(pass_path_value):
                errors.append(f"BLENDER_PASS_OUTPUTS entry {label!r} has no usable path.")
                continue
            pass_path = resolve_reference_path(pass_path_value, path)
            if not pass_path.exists():
                errors.append(f"BLENDER_PASS_OUTPUTS entry {label!r} points to a missing file: {pass_path_value}")
        existing_passes: list[tuple[str, Path]] = [
            (label, resolve_reference_path(pass_path_value, path))
            for label, pass_path_value in pass_paths
            if not value_is_none_like(pass_path_value)
            and resolve_reference_path(pass_path_value, path).exists()
        ]
        seen_pass_bytes: dict[bytes, str] = {}
        for label, pass_path in existing_passes:
            try:
                pass_bytes = pass_path.read_bytes()
            except OSError:
                continue
            previous_label = seen_pass_bytes.get(pass_bytes)
            if previous_label is not None:
                errors.append(
                    f"BLENDER_PASS_OUTPUTS entries {previous_label!r} and {label!r} are byte-identical; "
                    "clay/lineart/depth/mask outputs must be distinct passes, not duplicate saves."
                )
            else:
                seen_pass_bytes[pass_bytes] = label
    elif blender_blockout_required == "no":
        if blockout_review_status == "pass":
            warnings.append("BLOCKOUT_REVIEW_STATUS is 'pass' even though BLENDER_BLOCKOUT_REQUIRED is 'no'.")

    anatomy_gate_required_value = lower_value(extract_field(step2_3_block, "ANATOMY_GATE_REQUIRED"))
    age_band = extract_field(step2_3_block, "AGE_BAND")
    sex_classification = extract_field(step2_3_block, "SEX_CLASSIFICATION")
    body_type_baseline = extract_field(step2_3_block, "BODY_TYPE_BASELINE")
    stylization_level = extract_field(step2_3_block, "STYLIZATION_LEVEL")
    head_to_body_ratio = extract_field(step2_3_block, "HEAD_TO_BODY_RATIO")
    ribcage_pelvis_relation = extract_field(step2_3_block, "RIBCAGE_PELVIS_RELATION")
    shoulder_width_note = extract_field(step2_3_block, "SHOULDER_WIDTH_NOTE")
    hip_width_note = extract_field(step2_3_block, "HIP_WIDTH_NOTE")
    limb_proportion_note = extract_field(step2_3_block, "LIMB_PROPORTION_NOTE")
    elbow_wrist_chain_note = extract_field(step2_3_block, "ELBOW_WRIST_CHAIN_NOTE")
    hip_knee_ankle_chain_note = extract_field(step2_3_block, "HIP_KNEE_ANKLE_CHAIN_NOTE")
    hand_size_relative_note = extract_field(step2_3_block, "HAND_SIZE_RELATIVE_NOTE")
    foot_size_relative_note = extract_field(step2_3_block, "FOOT_SIZE_RELATIVE_NOTE")
    lower_body_silhouette_lock = extract_field(step2_3_block, "LOWER_BODY_SILHOUETTE_LOCK")
    protected_anatomy_chain_visibility = extract_field(step2_3_block, "PROTECTED_ANATOMY_CHAIN_VISIBILITY")
    hand_detail_budget = extract_field(step2_3_block, "HAND_DETAIL_BUDGET")
    finger_topology_chain_lock = extract_field(step2_3_block, "FINGER_TOPOLOGY_CHAIN_LOCK")
    finger_topology_fail_conditions = extract_field(step2_3_block, "FINGER_TOPOLOGY_FAIL_CONDITIONS")
    anatomy_primitive_blockout = extract_field(step2_3_block, "ANATOMY_PRIMITIVE_BLOCKOUT")
    head_primitive = extract_field(step2_3_block, "HEAD_PRIMITIVE")
    ribcage_primitive = extract_field(step2_3_block, "RIBCAGE_PRIMITIVE")
    pelvis_primitive = extract_field(step2_3_block, "PELVIS_PRIMITIVE")
    limb_cylinder_chain = extract_field(step2_3_block, "LIMB_CYLINDER_CHAIN")
    joint_sphere_map = extract_field(step2_3_block, "JOINT_SPHERE_MAP")
    hand_foot_primitives = extract_field(step2_3_block, "HAND_FOOT_PRIMITIVES")
    anatomy_primitive_fail_conditions = extract_field(step2_3_block, "ANATOMY_PRIMITIVE_FAIL_CONDITIONS")
    anatomy_research_decision_note = extract_field(step2_3_block, "ANATOMY_RESEARCH_DECISION_NOTE")
    hand_prop_relation = extract_field(step2_7_block, "HAND_PROP_RELATION")
    hand_structure_apply_note_step2_7 = extract_field(step2_7_block, "HAND_STRUCTURE_APPLY_NOTE")
    functional_grip_mechanics_contract = extract_field(step2_7_block, "FUNCTIONAL_GRIP_MECHANICS_CONTRACT")
    wrist_force_path_check = extract_field(step2_7_block, "WRIST_FORCE_PATH_CHECK")

    anatomy_required_expected = likely_requires_anatomy_gate(
        request_summary,
        action_field,
        camera_angle,
        extract_field(step2_block, "CHARACTER_POSITION"),
        visible_hands_and_poses,
    ) or hands_visible_expected

    if anatomy_required_expected and anatomy_gate_required_value != "yes":
        errors.append(
            "Human figure scenes with meaningful body read or visible hands require ANATOMY_GATE_REQUIRED: yes in Step 2.3."
        )

    object_density_signal_text = " ".join(
        filter(
            None,
            [
                request_summary,
                action_field,
                extract_field(step1_block, "ENVIRONMENT"),
                camera_angle,
                extract_field(step2_block, "COMPOSITION_OBJECT_ROLE_SUMMARY"),
                extract_field(step2_2_block, "SOURCE_IMAGE_OBJECTS_PRESENT"),
                extract_field(step2_2_block, "FOREGROUND_FRAME_OBJECTS"),
                extract_field(step2_2_block, "SUPPORT_PLANE_OBJECTS"),
                extract_field(step2_2_block, "LEFT_VERTICAL_PLANE_OBJECTS"),
                extract_field(step2_2_block, "RIGHT_VERTICAL_PLANE_OBJECTS"),
                extract_field(step2_2_block, "OVERHEAD_PLANE_OBJECTS"),
                extract_field(step2_2_block, "BACKGROUND_DEPTH_OBJECTS"),
                extract_field(step2_2_block, "EFFECT_OBJECTS"),
                extract_field(step2_5_block, "REQUIRED_OBJECTS"),
            ],
        )
    )
    object_density_edge_expected = (
        anatomy_required_expected
        and count_keyword_hits(object_density_signal_text, OBJECT_DENSITY_EDGE_KEYWORDS) >= 2
    )
    if object_density_edge_expected:
        density_priority_text = " ".join(
            filter(
                None,
                [
                    extract_field(step2_8_block, "DETAIL_AFTER_BLOCKOUT_LOCK"),
                    extract_field(step2_8_block, "STRUCTURAL_INVARIANTS_TO_PRESERVE"),
                    extract_field(step2_8_block, "PAINTERLY_FREEDOMS_ALLOWED"),
                    extract_field(step2_9_block, "GENERATION_PRIORITY_ORDER"),
                    extract_field(step2_9_block, "NON_NEGOTIABLE_LOCKS"),
                    extract_field(step2_9_block, "STYLE_ALLOWED_AFTER_STRUCTURE"),
                    extract_field(step2_9_block, "ANATOMY_OVER_DENSITY_LOCK"),
                    extract_field(step2_9_block, "PAINTERLY_COMPRESSION_ALLOWANCE"),
                    extract_field(step2_9_block, "PROMPT_COMPRESSION_RULE"),
                    extract_field(step8_block, "FINAL_CORRECTION_LIST"),
                    extract_image_generation_prompt(text),
                ],
            )
        )
        if not contains_keyword(density_priority_text, HUMAN_PRIORITY_LOCK_KEYWORDS):
            errors.append(
                "Object-dense human figure scenes must explicitly prioritize human anatomy/body/hands/fingers/feet/contact in Step 2.8/2.9 or the image prompt."
            )
        if not contains_keyword(density_priority_text, DENSITY_REDUCTION_KEYWORDS):
            errors.append(
                "Object-dense human figure scenes must explicitly name non-human density/clutter/background/effects that can be reduced before anatomy is sacrificed."
            )

    if anatomy_gate_required_value == "yes":
        normalized_age_band = normalize_age_band(age_band)
        if normalized_age_band not in ALLOWED_AGE_BANDS:
            errors.append(
                "AGE_BAND must use one of the project's canonical values when anatomy gating is active."
            )
        if count_meaningful_tokens(sex_classification) < 1:
            errors.append("Anatomy-gated scenes require SEX_CLASSIFICATION in Step 2.3.")
        if count_meaningful_tokens(body_type_baseline) < 4:
            errors.append("Anatomy-gated scenes require a meaningful BODY_TYPE_BASELINE note in Step 2.3.")
        if count_meaningful_tokens(stylization_level) < 2:
            errors.append("Anatomy-gated scenes require STYLIZATION_LEVEL in Step 2.3.")
        if count_meaningful_tokens(head_to_body_ratio) < 2:
            errors.append("Anatomy-gated scenes require HEAD_TO_BODY_RATIO in Step 2.3.")
        if count_meaningful_tokens(ribcage_pelvis_relation) < 4:
            errors.append("Anatomy-gated scenes require RIBCAGE_PELVIS_RELATION in Step 2.3.")
        if count_meaningful_tokens(shoulder_width_note) < 4:
            errors.append("Anatomy-gated scenes require SHOULDER_WIDTH_NOTE in Step 2.3.")
        if count_meaningful_tokens(hip_width_note) < 4:
            errors.append("Anatomy-gated scenes require HIP_WIDTH_NOTE in Step 2.3.")
        if count_meaningful_tokens(limb_proportion_note) < 4:
            errors.append("Anatomy-gated scenes require LIMB_PROPORTION_NOTE in Step 2.3.")
        if count_meaningful_tokens(elbow_wrist_chain_note) < 4:
            errors.append("Anatomy-gated scenes require ELBOW_WRIST_CHAIN_NOTE in Step 2.3.")
        if count_meaningful_tokens(hip_knee_ankle_chain_note) < 4:
            errors.append("Anatomy-gated scenes require HIP_KNEE_ANKLE_CHAIN_NOTE in Step 2.3.")
        if count_meaningful_tokens(hand_size_relative_note) < 4:
            errors.append("Anatomy-gated scenes require HAND_SIZE_RELATIVE_NOTE in Step 2.3.")
        if count_meaningful_tokens(foot_size_relative_note) < 4:
            errors.append("Anatomy-gated scenes require FOOT_SIZE_RELATIVE_NOTE in Step 2.3.")
        if count_meaningful_tokens(lower_body_silhouette_lock) < 6:
            errors.append("Anatomy-gated scenes require LOWER_BODY_SILHOUETTE_LOCK so pants/armor/black texture cannot absorb leg anatomy.")
        if count_meaningful_tokens(protected_anatomy_chain_visibility) < 8:
            errors.append("Anatomy-gated scenes require PROTECTED_ANATOMY_CHAIN_VISIBILITY to define traceable limb/hand/leg landmarks under occlusion.")
        if not contains_keyword(protected_anatomy_chain_visibility, PROTECTED_CHAIN_KEYWORDS):
            errors.append("PROTECTED_ANATOMY_CHAIN_VISIBILITY must name protected chain landmarks such as shoulder/elbow/wrist/hand or hip/knee/ankle/boot.")
        if hands_visible_expected:
            if count_meaningful_tokens(hand_detail_budget) < 8:
                errors.append("Visible hands require Step 2.3 HAND_DETAIL_BUDGET to assign per-hand readability/detail budget and nearby detail reductions.")
            if not contains_keyword(hand_detail_budget, ["focal", "support", "background", "detail", "reduce", "screen", "read", "초점", "보조", "배경", "디테일", "축소", "판독"]):
                errors.append("HAND_DETAIL_BUDGET must state each visible hand's role/readability target and what detail can be reduced first.")
            if count_meaningful_tokens(finger_topology_chain_lock) < 10:
                errors.append("Visible hands require Step 2.3 FINGER_TOPOLOGY_CHAIN_LOCK, not only a generic hand note.")
            if not contains_keyword(finger_topology_chain_lock, FINGER_TOPOLOGY_KEYWORDS):
                errors.append("FINGER_TOPOLOGY_CHAIN_LOCK must name palm/thumb/finger topology landmarks such as palm block, thumb wedge, index/middle/ring/little.")
            if count_meaningful_tokens(finger_topology_fail_conditions) < 6:
                errors.append("Visible hands require Step 2.3 FINGER_TOPOLOGY_FAIL_CONDITIONS so existence-only hand preservation cannot pass.")
            if not contains_keyword(finger_topology_fail_conditions, FINGER_FAILURE_KEYWORDS):
                errors.append("FINGER_TOPOLOGY_FAIL_CONDITIONS must fail fused/claw/lump/melted/unreadable hands, not only missing hands.")
        for field_name, field_value in (
            ("ANATOMY_PRIMITIVE_BLOCKOUT", anatomy_primitive_blockout),
            ("HEAD_PRIMITIVE", head_primitive),
            ("RIBCAGE_PRIMITIVE", ribcage_primitive),
            ("PELVIS_PRIMITIVE", pelvis_primitive),
            ("LIMB_CYLINDER_CHAIN", limb_cylinder_chain),
            ("JOINT_SPHERE_MAP", joint_sphere_map),
            ("HAND_FOOT_PRIMITIVES", hand_foot_primitives),
            ("ANATOMY_PRIMITIVE_FAIL_CONDITIONS", anatomy_primitive_fail_conditions),
        ):
            if count_meaningful_tokens(field_value) < 4:
                errors.append(f"Anatomy-gated scenes require primitive construction in Step 2.3 {field_name}.")
        if count_meaningful_tokens(anatomy_research_decision_note) < 4:
            errors.append("Anatomy-gated scenes require ANATOMY_RESEARCH_DECISION_NOTE in Step 2.3.")
        for field_name in ANATOMY_CARD_FIELDS:
            validate_card_path(extract_field(step2_3_block, field_name), path, field_name, errors)

    if hands_visible_expected and anatomy_gate_required_value != "yes":
        errors.append(
            "Visible hands now belong to the anatomy stack, so Step 2.3 must be active before hand rendering decisions."
        )

    lighting_plan = extract_field(step3_block, "LIGHTING_PLAN")
    value_count = extract_field(step3_block, "VALUE_COUNT_DECISION")
    focal_contrast_zone = extract_field(step3_block, "FOCAL_CONTRAST_ZONE")
    if not has_directional_detail(lighting_plan):
        errors.append("Step 3 LIGHTING_PLAN must describe a readable light direction.")
    value_numbers = [int(match) for match in re.findall(r"\b([0-9])\b", value_count or "")]
    if not any(3 <= number <= 5 for number in value_numbers):
        errors.append("Step 3 VALUE_COUNT_DECISION must explicitly keep value groups within 3-5.")
    if not contains_keyword(focal_contrast_zone, FACE_FOCUS_KEYWORDS):
        errors.append("Step 3 FOCAL_CONTRAST_ZONE must explicitly prioritize face or eyes.")

    eye_render_plan = extract_field(step4_block, "EYE_RENDER_PLAN")
    face_structure_quality_lock = extract_field(step4_block, "FACE_STRUCTURE_QUALITY_LOCK")
    face_focal_map = extract_field(step4_block, "FACE_FOCAL_MAP")
    if not contains_keyword(face_focal_map, FACE_FOCUS_KEYWORDS):
        errors.append("Step 4 FACE_FOCAL_MAP must explicitly describe face/eye-first focus.")
    if not contains_keyword(eye_render_plan, ["iris", "pupil", "highlight", "홍채", "동공", "하이라이트"]):
        errors.append("Step 4 EYE_RENDER_PLAN must describe eye-structure rendering, not just mood.")
    if count_meaningful_tokens(face_structure_quality_lock) < 6:
        errors.append("Step 4 FACE_STRUCTURE_QUALITY_LOCK must protect intended face planes/proportions from flattened or dumpling-wide drift.")

    hand_line_priority_note = extract_field(step5_block, "HAND_LINE_PRIORITY_NOTE")
    lower_body_line_priority_note = extract_field(step5_block, "LOWER_BODY_LINE_PRIORITY_NOTE")
    protected_chain_edge_separation_plan = extract_field(step5_block, "PROTECTED_CHAIN_EDGE_SEPARATION_PLAN")
    finger_occlusion_separation_rule = extract_field(step2_6_block, "FINGER_OCCLUSION_SEPARATION_RULE")
    prompt_finger_topology_lock = extract_field(step2_9_block, "PROMPT_FINGER_TOPOLOGY_LOCK")
    if hands_visible_expected:
        if not likely_visible_hands(hand_line_priority_note):
            errors.append(
                "Visible hands require Step 5 HAND_LINE_PRIORITY_NOTE to explicitly address hand/finger handling."
            )
        if count_meaningful_tokens(finger_occlusion_separation_rule) < 8:
            errors.append("Visible hands require Step 2.6 FINGER_OCCLUSION_SEPARATION_RULE so finger gaps are not sacrificed to cloak/blood/armor/background density.")
        if not contains_keyword(finger_occlusion_separation_rule, FINGER_TOPOLOGY_KEYWORDS):
            errors.append("FINGER_OCCLUSION_SEPARATION_RULE must name palm/thumb/finger topology, not only a generic hand silhouette.")
        if not contains_keyword(finger_occlusion_separation_rule, SEPARATION_CUE_KEYWORDS):
            errors.append("FINGER_OCCLUSION_SEPARATION_RULE must include concrete separation cues such as negative-space gaps, rim/value edges, contour notches, or masks.")
        if count_meaningful_tokens(prompt_finger_topology_lock) < 8:
            errors.append("Visible hands require Step 2.9 PROMPT_FINGER_TOPOLOGY_LOCK so the final prompt carries per-hand finger topology instructions.")
        if not contains_keyword(prompt_finger_topology_lock, FINGER_TOPOLOGY_KEYWORDS):
            errors.append("PROMPT_FINGER_TOPOLOGY_LOCK must name palm/thumb/finger topology landmarks.")
    if anatomy_required_expected and count_meaningful_tokens(lower_body_line_priority_note) < 6:
        errors.append("Anatomy-gated scenes require Step 5 LOWER_BODY_LINE_PRIORITY_NOTE for leg/pants silhouette before costume texture.")
    if anatomy_required_expected and count_meaningful_tokens(protected_chain_edge_separation_plan) < 6:
        errors.append("Anatomy-gated scenes require Step 5 PROTECTED_CHAIN_EDGE_SEPARATION_PLAN so limbs/props can be traced through occlusion and density.")
    if anatomy_required_expected and image_ready_value == "yes":
        image_prompt = extract_image_generation_prompt(text)
        if not contains_keyword(image_prompt, FACE_STRUCTURE_PROMPT_KEYWORDS):
            errors.append("Anatomy-gated IMAGE_GEN_HANDOFF_PROMPT must carry face-plane/proportion quality language before style density.")
        if not contains_keyword(image_prompt, LOWER_BODY_PROMPT_KEYWORDS):
            errors.append("Anatomy-gated IMAGE_GEN_HANDOFF_PROMPT must carry lower-body/leg/pants silhouette language before costume texture.")
        if hands_visible_expected:
            if not contains_keyword(image_prompt, FINGER_TOPOLOGY_KEYWORDS):
                errors.append("Visible-hand IMAGE_GEN_HANDOFF_PROMPT must carry palm/thumb/finger topology language, not only 'hands visible'.")
            if not contains_keyword(image_prompt, FINGER_FAILURE_KEYWORDS + SEPARATION_CUE_KEYWORDS):
                errors.append("Visible-hand IMAGE_GEN_HANDOFF_PROMPT must state a separation/failure solution so fused/claw/lump hands do not pass.")
        if weapon_grip_expected:
            for label, field_value in (
                ("Step 2.7 HAND_PROP_RELATION", hand_prop_relation),
                ("Step 2.7 HAND_STRUCTURE_APPLY_NOTE", hand_structure_apply_note_step2_7),
                ("Step 2.7 FUNCTIONAL_GRIP_MECHANICS_CONTRACT", functional_grip_mechanics_contract),
                ("Step 2.7 WRIST_FORCE_PATH_CHECK", wrist_force_path_check),
                ("Step 2.8 GRIP_MECHANICS_VISUAL_GUIDE_PACKAGE", grip_mechanics_visual_guide_package),
                ("Step 2.9 GRIP_MECHANICS_PROMPT_LOCK", grip_mechanics_prompt_lock),
                ("Step 8 WEAPON_GRIP_MECHANICS_VERDICT_CHECK", weapon_grip_mechanics_verdict_check),
                ("Step 8 WRIST_FORCE_PATH_VERDICT_CHECK", wrist_force_path_verdict_check),
            ):
                if value_is_none_like(field_value) or count_meaningful_tokens(field_value) < 8:
                    errors.append(
                        f"Weapon/prop-holding hands require {label} so correct fingers do not pass with an impossible grip or broken wrist."
                    )
                elif not contains_keyword_korean_tolerant(field_value, GRIP_MECHANICS_KEYWORDS + VISUAL_GUIDE_EXECUTION_KEYWORDS):
                    errors.append(
                        f"{label} must name functional grip mechanics: hilt/handle, thumb opposition or knuckles, wrist/forearm force path, and impossible-bend failures."
                    )
                elif "VISUAL_GUIDE_PACKAGE" in label and not contains_keyword_korean_tolerant(field_value, VISUAL_GUIDE_EXECUTION_KEYWORDS):
                    errors.append(
                        f"{label} must point to grip visual guide evidence such as annotated mask/overlay/blockout/lineart, not prose-only hand wording."
                    )
            if image_ready_value == "yes" and not contains_keyword_korean_tolerant(
                image_prompt,
                ["grip", "hilt", "thumb", "knuckle", "wrist", "forearm", "force path", "not bent", "쥐", "손잡이", "엄지", "손목", "전완", "힘", "꺾"],
            ):
                errors.append(
                    "Weapon-hand IMAGE_GEN_HANDOFF_PROMPT must carry functional grip/wrist-force wording, not only palm/finger topology."
                )

    accent_map = extract_field(step6_block, "ACCENT_PLACEMENT_MAP")
    if not contains_keyword(accent_map, FACE_FOCUS_KEYWORDS):
        errors.append("Step 6 ACCENT_PLACEMENT_MAP must explicitly place the strongest accents at face or eyes.")
    if contains_keyword(accent_map, GARMENT_FOCUS_KEYWORDS) and not contains_keyword(accent_map, FACE_FOCUS_KEYWORDS):
        errors.append("Step 6 ACCENT_PLACEMENT_MAP cannot prioritize garment accents without face/eye priority.")

    correction_list = extract_field(step8_block, "FINAL_CORRECTION_LIST")
    scale_anchor_verdict_check = extract_field(step8_block, "SCALE_ANCHOR_VERDICT_CHECK")
    hero_object_scale_verdict_check = extract_field(step8_block, "HERO_OBJECT_SCALE_VERDICT_CHECK")
    humanoid_scale_parity_verdict_check = extract_field(step8_block, "HUMANOID_SCALE_PARITY_VERDICT_CHECK")
    scale_visual_guide_verdict_check = extract_field(step8_block, "SCALE_VISUAL_GUIDE_VERDICT_CHECK")
    cut_plane_visibility_verdict_check = extract_field(step8_block, "CUT_PLANE_VISIBILITY_VERDICT_CHECK")
    cut_result_unknown_form_verdict_check = extract_field(step8_block, "CUT_RESULT_UNKNOWN_FORM_VERDICT_CHECK")
    weapon_grip_mechanics_verdict_check = extract_field(step8_block, "WEAPON_GRIP_MECHANICS_VERDICT_CHECK")
    wrist_force_path_verdict_check = extract_field(step8_block, "WRIST_FORCE_PATH_VERDICT_CHECK")
    camera_class_verdict_check = extract_field(step8_block, "CAMERA_CLASS_VERDICT_CHECK")
    scale_critical_shot_class_verdict_check = extract_field(step8_block, "SCALE_CRITICAL_SHOT_CLASS_VERDICT_CHECK")
    object_anatomy_mixing_check = extract_field(step8_block, "OBJECT_ANATOMY_MIXING_CHECK")
    object_distortion_verdict_check = extract_field(step8_block, "OBJECT_DISTORTION_VERDICT_CHECK")
    protected_chain_trace_verdict = extract_field(step8_block, "PROTECTED_CHAIN_TRACE_VERDICT")
    face_and_lower_body_verdict_check = extract_field(step8_block, "FACE_AND_LOWER_BODY_VERDICT_CHECK")
    irreversible_structure_check = extract_field(step8_block, "IRREVERSIBLE_STRUCTURE_CHECK")
    hand_readability_check = extract_field(step8_block, "HAND_READABILITY_CHECK")
    finger_topology_verdict_check = extract_field(step8_block, "FINGER_TOPOLOGY_VERDICT_CHECK")
    user_command_compliance_check = extract_field(step8_block, "USER_COMMAND_COMPLIANCE_CHECK")
    post_image_scale_failure_shot_class_escalation = extract_field(
        step8_block, "POST_IMAGE_SCALE_FAILURE_SHOT_CLASS_ESCALATION"
    )
    aesthetic_recovery_check = extract_field(step8_block, "AESTHETIC_RECOVERY_CHECK")
    structure_lock_summary = extract_field(step8_block, "STRUCTURE_LOCK_SUMMARY")
    aesthetic_render_brief = extract_field(step8_block, "AESTHETIC_RENDER_BRIEF")
    negative_prompt_limited = extract_field(step8_block, "NEGATIVE_PROMPT_LIMITED")
    final_image_prompt_compiled = extract_field(step8_block, "FINAL_IMAGE_PROMPT_COMPILED")
    final_prompt_compiler_status = lower_value(extract_field(step8_block, "FINAL_PROMPT_COMPILER_STATUS"))
    aesthetic_recovery_gate_status = lower_value(extract_field(step8_block, "AESTHETIC_RECOVERY_GATE_STATUS"))
    if not is_actionable_correction(correction_list):
        errors.append("Step 8 FINAL_CORRECTION_LIST must contain actionable corrections, not only summary praise.")
    if scale_anchor_expected and count_meaningful_tokens(scale_anchor_verdict_check) < 6:
        errors.append("Scale-anchor scenes require Step 8 SCALE_ANCHOR_VERDICT_CHECK to confirm generated scale anchors or list rerender triggers.")
    if scale_anchor_expected:
        if count_meaningful_tokens(hero_object_scale_verdict_check) < 8:
            errors.append("Scale-anchor scenes require Step 8 HERO_OBJECT_SCALE_VERDICT_CHECK comparing protagonist size against objects and visible scale witnesses.")
        if not contains_keyword(hero_object_scale_verdict_check, HERO_OBJECT_SCALE_KEYWORDS):
            errors.append("HERO_OBJECT_SCALE_VERDICT_CHECK must explicitly mention protagonist/object scale witnesses and perspective/depth transfer or failure triggers.")
    if humanoid_scale_expected:
        if count_meaningful_tokens(humanoid_scale_parity_verdict_check) < 8:
            errors.append("Humanoid scenes require Step 8 HUMANOID_SCALE_PARITY_VERDICT_CHECK comparing protagonist to visible background humans/humanoids/humanoid monsters.")
        if not contains_keyword(humanoid_scale_parity_verdict_check, HUMANOID_SCALE_PARITY_KEYWORDS):
            errors.append("HUMANOID_SCALE_PARITY_VERDICT_CHECK must explicitly fail miniature/doll/giant/background-texture humanoids and mention perspective/depth-plane scale parity.")
    if irreversible_structure_expected:
        if count_meaningful_tokens(object_anatomy_mixing_check) < 6:
            errors.append("Object/anatomy dense scenes require Step 8 OBJECT_ANATOMY_MIXING_CHECK.")
        if count_meaningful_tokens(object_distortion_verdict_check) < 8:
            errors.append("Object/anatomy dense scenes require Step 8 OBJECT_DISTORTION_VERDICT_CHECK to audit unintended bending/warping/melting/resizing/fusion/absorption/texture replacement.")
        if not contains_keyword(object_distortion_verdict_check, OBJECT_DISTORTION_KEYWORDS):
            errors.append("OBJECT_DISTORTION_VERDICT_CHECK must explicitly name distortion failures such as bend, warp, melt, resize, fuse, absorb, axis/silhouette/function break, or texture replacement.")
        if count_meaningful_tokens(protected_chain_trace_verdict) < 6:
            errors.append("Object/anatomy dense scenes require Step 8 PROTECTED_CHAIN_TRACE_VERDICT to trace protected chains by visible landmarks, not inference.")
        if count_meaningful_tokens(face_and_lower_body_verdict_check) < 6:
            errors.append("Object/anatomy dense scenes require Step 8 FACE_AND_LOWER_BODY_VERDICT_CHECK.")
        if count_meaningful_tokens(irreversible_structure_check) < 6:
            errors.append("Object/anatomy dense scenes require Step 8 IRREVERSIBLE_STRUCTURE_CHECK.")
    if hands_visible_expected and count_meaningful_tokens(hand_readability_check) < 4:
        errors.append(
            "Visible hands require Step 8 HAND_READABILITY_CHECK to confirm the hand/finger read."
        )
    if hands_visible_expected:
        if count_meaningful_tokens(finger_topology_verdict_check) < 8:
            errors.append("Visible hands require Step 8 FINGER_TOPOLOGY_VERDICT_CHECK to fail existence-only or fused hand preservation.")
        if not contains_keyword(finger_topology_verdict_check, FINGER_TOPOLOGY_KEYWORDS):
            errors.append("FINGER_TOPOLOGY_VERDICT_CHECK must explicitly judge palm/thumb/finger topology.")
        if not contains_keyword(finger_topology_verdict_check, FINGER_FAILURE_KEYWORDS):
            errors.append("FINGER_TOPOLOGY_VERDICT_CHECK must name fused/claw/lump/melted/unreadable hands as rerender/fail conditions.")

    if render_bound_spec or image_ready_value == "yes":
        for label, value in (
            ("AESTHETIC_RECOVERY_CHECK", aesthetic_recovery_check),
            ("STRUCTURE_LOCK_SUMMARY", structure_lock_summary),
            ("AESTHETIC_RENDER_BRIEF", aesthetic_render_brief),
            ("NEGATIVE_PROMPT_LIMITED", negative_prompt_limited),
        ):
            if value_is_none_like(value) or count_meaningful_tokens(value) < 6:
                errors.append(
                    f"Render-bound specs require Step 8 {label} so final prompts are compiled as image language instead of schema/verdict prose."
                )

        if not contains_keyword(aesthetic_recovery_check, AESTHETIC_RECOVERY_KEYWORDS):
            errors.append(
                "AESTHETIC_RECOVERY_CHECK must verify composition pressure, face/eye focal read, value/line/texture/color hierarchy, or anti-generic style recovery."
            )
        if not contains_keyword(aesthetic_render_brief, FACE_FOCUS_KEYWORDS):
            errors.append("AESTHETIC_RENDER_BRIEF must restore face/eye focal language before final prompt handoff.")
        if not contains_keyword(aesthetic_render_brief, AESTHETIC_RECOVERY_KEYWORDS):
            errors.append(
                "AESTHETIC_RENDER_BRIEF must contain production image-language for composition, background pressure, value, line, texture, palette, or accent handling."
            )
        if not contains_keyword(structure_lock_summary, STRUCTURE_OVER_STYLE_KEYWORDS + IRREVERSIBLE_STRUCTURE_KEYWORDS):
            errors.append(
                "STRUCTURE_LOCK_SUMMARY must summarize the surviving structure locks before aesthetic recovery, not replace them with style praise."
            )
        if image_ready_value == "yes":
            if final_prompt_compiler_status != "pass":
                errors.append("PRE_IMAGE_HANDOFF_READY: yes requires FINAL_PROMPT_COMPILER_STATUS: pass.")
            if aesthetic_recovery_gate_status != "pass":
                errors.append("PRE_IMAGE_HANDOFF_READY: yes requires AESTHETIC_RECOVERY_GATE_STATUS: pass.")
            if (
                is_placeholder(final_image_prompt_compiled)
                or value_is_none_like(final_image_prompt_compiled)
                or count_meaningful_tokens(final_image_prompt_compiled) < 12
            ):
                errors.append(
                    "PRE_IMAGE_HANDOFF_READY: yes requires FINAL_IMAGE_PROMPT_COMPILED with the production image prompt."
                )
            else:
                jargon_hits = final_prompt_jargon_hits(final_image_prompt_compiled)
                if jargon_hits:
                    errors.append(
                        "FINAL_IMAGE_PROMPT_COMPILED must not leak schema/validator jargon into the image model: "
                        + ", ".join(jargon_hits[:12])
                    )
                if not contains_keyword(final_image_prompt_compiled, FINAL_PROMPT_NATURAL_LANGUAGE_KEYWORDS):
                    errors.append(
                        "FINAL_IMAGE_PROMPT_COMPILED must be natural image language with visible focal/composition/light/line/texture wording, not only negative rules."
                    )

        if count_meaningful_tokens(user_command_checklist) < 4:
            errors.append("Render-bound specs require USER_COMMAND_CHECKLIST listing explicit user commands and non-negotiable requests.")
        if count_meaningful_tokens(user_command_compliance_check) < 8:
            errors.append("Step 8 USER_COMMAND_COMPLIANCE_CHECK must audit every user command/non-negotiable before final pass.")
        if not contains_keyword(user_command_compliance_check, COMMAND_COMPLIANCE_KEYWORDS):
            errors.append("USER_COMMAND_COMPLIANCE_CHECK must use checklist/audit language and state satisfied/partial/failed/not_applicable or rerender status for each command.")

        # PSE Command Immutability — verbatim inheritance through PLAN/IMPLEMENT/VERIFY/AUDIT/Step 8
        immutable_commands_raw = extract_block_list(text, "IMMUTABLE_USER_COMMANDS_VERBATIM")
        immutable_commands = [c for c in immutable_commands_raw if not is_placeholder(c) and not value_is_none_like(c)]
        dilution_policy = lower_value(extract_field(text, "COMMAND_DILUTION_POLICY"))
        if not immutable_commands:
            errors.append(
                "Render-bound specs require IMMUTABLE_USER_COMMANDS_VERBATIM as a bulleted list of verbatim user commands "
                "(no paraphrase) that downstream stages must inherit."
            )
        else:
            if dilution_policy != "forbid":
                errors.append('COMMAND_DILUTION_POLICY must be set to "forbid" so PLAN/IMPLEMENT/VERIFY/AUDIT cannot summarize user commands.')
            inheritance_targets = (
                ("PLAN", extract_named_section(text, "## PLAN Gate"), "PLAN_COMMAND_INHERITANCE"),
                ("IMPLEMENT", extract_named_section(text, "## IMPLEMENT Gate"), "IMPLEMENT_COMMAND_INHERITANCE"),
                ("VERIFY", extract_named_section(text, "## VERIFY Gate"), "VERIFY_COMMAND_INHERITANCE"),
                ("AUDIT", extract_named_section(text, "## AUDIT Gate"), "AUDIT_COMMAND_INHERITANCE"),
                ("Step 8", step8_block, "USER_COMMAND_COMPLIANCE_CHECK"),
            )
            for stage_label, stage_block, field_name in inheritance_targets:
                if not stage_block:
                    errors.append(
                        f"Command inheritance: missing {stage_label} section block; cannot verify command propagation."
                    )
                    continue
                inheritance_text = extract_field(stage_block, field_name)
                if value_is_none_like(inheritance_text) or is_placeholder(inheritance_text):
                    errors.append(
                        f"Command inheritance: {stage_label} {field_name} is empty/placeholder; must repeat each IMMUTABLE_USER_COMMANDS_VERBATIM line verbatim."
                    )
                    continue
                missing = find_missing_inheritance(immutable_commands, inheritance_text)
                if missing:
                    sample = "; ".join(missing[:3])
                    suffix = "" if len(missing) <= 3 else f" (+{len(missing) - 3} more)"
                    errors.append(
                        f"Command inheritance: {stage_label} {field_name} omits or paraphrases {len(missing)} immutable command(s): {sample}{suffix}. "
                        "Each IMMUTABLE_USER_COMMANDS_VERBATIM line must appear as a verbatim substring (whitespace/case insensitive)."
                    )

        # Failure-first loop — inherited failure lessons + negative prompt defenses
        inherited_lessons_raw = extract_block_list(text, "INHERITED_FAILURE_LESSONS")
        real_lessons: list[str] = []
        exemption_present = False
        for lesson in inherited_lessons_raw:
            if is_placeholder(lesson):
                continue
            if "none_with_reason" in normalize_for_inheritance(lesson):
                exemption_present = True
                continue
            if value_is_none_like(lesson):
                continue
            real_lessons.append(lesson)
        if not real_lessons and not exemption_present:
            errors.append(
                "Render-bound specs require INHERITED_FAILURE_LESSONS: at least one bullet quoting a prior FAILURE_CATALOG_PATH lesson, "
                "or a single bullet starting with 'none_with_reason:' explaining why no prior failures apply."
            )
        elif real_lessons:
            negative_defense_raw = extract_block_list(text, "NEGATIVE_PROMPT_DEFENSE")
            negative_defenses = [d for d in negative_defense_raw if not is_placeholder(d) and not value_is_none_like(d)]
            if not negative_defenses:
                errors.append(
                    "INHERITED_FAILURE_LESSONS requires matching NEGATIVE_PROMPT_DEFENSE entries (one specific negative-prompt phrase per lesson)."
                )
            elif len(negative_defenses) < len(real_lessons):
                errors.append(
                    f"NEGATIVE_PROMPT_DEFENSE has {len(negative_defenses)} entries but {len(real_lessons)} lessons; each lesson needs a defense."
                )

        # Scale-critical prompt opening must appear at the START of the handoff prompt
        if scale_critical_active and image_ready_value == "yes":
            opening_value = extract_field(step2_9_block, "SCALE_CRITICAL_PROMPT_OPENING")
            handoff_prompt_value = extract_image_generation_prompt(text)
            if (
                opening_value
                and not is_placeholder(opening_value)
                and handoff_prompt_value
                and not prompt_starts_with_substring(handoff_prompt_value, opening_value)
            ):
                errors.append(
                    "SCALE_CRITICAL_PROMPT_OPENING must appear within the first ~240 chars of IMAGE_GEN_HANDOFF_PROMPT; "
                    "scale proof cannot be buried after style/action/face wording."
                )

        if render_bound_spec:
            scene_contract_prompt_lock = extract_field(step2_9_block, "SCENE_CONTRACT_PROMPT_LOCK")
            if value_is_none_like(scene_contract_prompt_lock) or count_meaningful_tokens(scene_contract_prompt_lock) < 6:
                errors.append(
                    "Render-bound specs require Step 2.9 SCENE_CONTRACT_PROMPT_LOCK so the final prompt inherits the canonical object/relationship contract."
                )
            elif not contains_keyword(
                scene_contract_prompt_lock,
                ["object", "relationship", "contract", "registry", "target", "scale", "객체", "관계", "계약", "등록", "대상", "스케일"],
            ):
                errors.append(
                    "SCENE_CONTRACT_PROMPT_LOCK must reference object registry / relationship contract / target or scale locks, not generic prompt quality."
                )

        if action_contact_expected:
            handoff_prompt_value = extract_image_generation_prompt(text)
            for label, block, field_name in (
                ("Step 2.9", step2_9_block, "ACTION_CONTACT_PROMPT_LOCK"),
                ("Step 8", step8_block, "ACTION_CONTACT_VERDICT_CHECK"),
            ):
                field_value = extract_field(block, field_name)
                if value_is_none_like(field_value) or count_meaningful_tokens(field_value) < 6:
                    errors.append(
                        f"Action/contact scenes require {label} {field_name} with named actor/tool/target/subpart and forbidden-target fail triggers."
                    )
                elif not contains_keyword_korean_tolerant(field_value, ACTION_CONTACT_CONTRACT_KEYWORDS):
                    errors.append(f"{label} {field_name} must carry actor/tool/target/contact/forbidden-target language.")
            if image_ready_value == "yes" and not contains_keyword_korean_tolerant(
                handoff_prompt_value,
                ["target", "forbidden", "not", "neck", "body", "wing", "대상", "금지", "아님", "목", "몸통", "날개"],
            ):
                errors.append(
                    "IMAGE_GEN_HANDOFF_PROMPT must carry the action-contact target and forbidden-target wording, not leave it only in the Scene Contract."
                )
            for label, field_value in (
                ("CUT_PLANE_VISUAL_GUIDE_PACKAGE", cut_plane_visual_guide_package),
                ("CUT_PLANE_VISIBILITY_PROMPT_LOCK", cut_plane_visibility_prompt_lock),
                ("CUT_PLANE_VISIBILITY_VERDICT_CHECK", cut_plane_visibility_verdict_check),
                ("CUT_RESULT_UNKNOWN_FORM_VERDICT_CHECK", cut_result_unknown_form_verdict_check),
            ):
                if value_is_none_like(field_value) or count_meaningful_tokens(field_value) < 8:
                    errors.append(
                        f"Action/cut scenes require {label}: the cut plane and post-cut object state cannot be solved by hiding them behind the protagonist."
                    )
                elif not contains_keyword_korean_tolerant(field_value, CUT_PLANE_VISIBILITY_KEYWORDS):
                    errors.append(
                        f"{label} must name visible cut-plane/cross-section landmarks, head-side/body-side continuity, and unknown protrusion/occlusion failure triggers."
                    )
                elif "VISUAL_GUIDE_PACKAGE" in label and not contains_keyword_korean_tolerant(field_value, VISUAL_GUIDE_EXECUTION_KEYWORDS):
                    errors.append(
                        f"{label} must point to visual guide evidence such as mask/overlay/blockout/lineart/depth, not prose-only target wording."
                    )
            if image_ready_value == "yes" and not contains_keyword_korean_tolerant(
                handoff_prompt_value,
                ["cut plane", "cross-section", "visible", "not hidden", "not occluded", "unknown form", "protrusion", "절단면", "단면", "보임", "가리지", "형체불명", "돌출"],
            ):
                errors.append(
                    "IMAGE_GEN_HANDOFF_PROMPT must carry visible cut-plane / no-unknown-protrusion wording, not only 'cut the neck'."
                )

        if garment_attachment_expected:
            garment_attachment_verdict = extract_field(step8_block, "GARMENT_ATTACHMENT_VERDICT_CHECK")
            if value_is_none_like(garment_attachment_verdict) or count_meaningful_tokens(garment_attachment_verdict) < 6:
                errors.append(
                    "Cloak/cape/hood/large-garment scenes require Step 8 GARMENT_ATTACHMENT_VERDICT_CHECK before accepting output."
                )
            elif not contains_keyword_korean_tolerant(garment_attachment_verdict, GARMENT_ATTACHMENT_CONTRACT_KEYWORDS):
                errors.append(
                    "GARMENT_ATTACHMENT_VERDICT_CHECK must judge visible attachment/origin landmarks such as shoulder/collar/neck/back/clasp."
                )
            if image_ready_value == "yes" and not contains_keyword_korean_tolerant(
                extract_image_generation_prompt(text),
                GARMENT_ATTACHMENT_CONTRACT_KEYWORDS,
            ):
                errors.append(
                    "IMAGE_GEN_HANDOFF_PROMPT must carry cloak/cape/hood attachment-origin wording when garment attachment is in the Scene Contract."
                )

        # Structured POST_IMAGE_VISUAL_VERDICT_JSON parse + contradiction check.
        # This is a post-generation acceptance gate, not the first prompt handoff
        # gate. PRE_IMAGE_HANDOFF_READY/IMAGE_GEN_READY may pass without it.
        if post_image_verdict_required:
            verdict: dict | None = None
            post_image_failed_keys: list[str] = []
            post_image_rerender_required: bool | None = None

            if post_image_accepted_value not in {"yes", "no"}:
                errors.append("POST_IMAGE_VERDICT_REQUIRED: yes requires POST_IMAGE_ACCEPTED to be yes or no, not not_applicable.")
            verdict, verdict_err = parse_visual_verdict_json(step8_block)
            if verdict is None:
                if verdict_err == "missing":
                    errors.append(
                        "POST_IMAGE_VERDICT_REQUIRED: yes requires POST_IMAGE_VISUAL_VERDICT_JSON in Step 8 with the structured pass/fail keys."
                    )
                else:
                    errors.append(f"POST_IMAGE_VISUAL_VERDICT_JSON parse failure: {verdict_err}")
            else:
                missing_keys = [k for k in VISUAL_VERDICT_REQUIRED_KEYS if k not in verdict]
                if missing_keys:
                    errors.append(
                        f"POST_IMAGE_VISUAL_VERDICT_JSON missing required keys: {', '.join(missing_keys)}."
                    )
                else:
                    failed_pass_keys = [
                        k for k in VISUAL_VERDICT_REQUIRED_KEYS
                        if k.endswith("_pass") and verdict.get(k) is False
                    ]
                    if verdict.get("hero_fits_inside_object") is False:
                        failed_pass_keys.append("hero_fits_inside_object")
                    if verdict.get("occupant_anchor_valid") is False:
                        failed_pass_keys.append("occupant_anchor_valid")
                    rerender_required = verdict.get("rerender_required")
                    post_image_rerender_required = rerender_required if isinstance(rerender_required, bool) else None
                    post_image_failed_keys = failed_visual_verdict_keys(verdict)
                    fail_reasons = verdict.get("fail_reasons") or []
                    if failed_pass_keys and rerender_required is not True:
                        errors.append(
                            f"POST_IMAGE_VISUAL_VERDICT_JSON has failing checks ({', '.join(sorted(set(failed_pass_keys)))}) "
                            "but rerender_required is not true."
                        )
                    if failed_pass_keys and not fail_reasons:
                        errors.append(
                            "POST_IMAGE_VISUAL_VERDICT_JSON has failing checks but fail_reasons is empty."
                        )
                    if rerender_required is True and post_image_accepted_value == "yes":
                        errors.append(
                            "POST_IMAGE_VISUAL_VERDICT_JSON.rerender_required is true; POST_IMAGE_ACCEPTED must be no until the rerender resolves the failures."
                        )
                    if not failed_pass_keys and rerender_required is False and post_image_accepted_value == "no":
                        warnings.append(
                            "POST_IMAGE_ACCEPTED is no even though POST_IMAGE_VISUAL_VERDICT_JSON has no failing pass keys and rerender_required is false."
                        )

            # POST_IMAGE_VISUAL_VERDICT_ARTIFACT_PATH: file-based verdict + cross-check
            verdict_artifact_path_value = extract_field(text, "POST_IMAGE_VISUAL_VERDICT_ARTIFACT_PATH")
            verdict_artifact_lower = lower_value(verdict_artifact_path_value)
            if is_placeholder(verdict_artifact_path_value) or verdict_artifact_lower == "not_applicable":
                errors.append(
                    "POST_IMAGE_VERDICT_REQUIRED: yes requires POST_IMAGE_VISUAL_VERDICT_ARTIFACT_PATH to point to a "
                    "filled visual verdict artifact (templates/post-image-visual-verdict-artifact-template.md). "
                    "not_applicable is rejected when a generated image is being accepted/rejected."
                )
            else:
                verdict_artifact_path = resolve_reference_path(verdict_artifact_path_value or "", path)
                spec_inline_verdict = verdict if 'verdict' in locals() else None
                verdict_artifact_result = validate_post_image_visual_verdict_artifact(
                    verdict_artifact_path,
                    spec_path=path,
                    spec_inline_verdict=spec_inline_verdict,
                )
                errors.extend(f"Visual verdict artifact: {item}" for item in verdict_artifact_result.errors)
                warnings.extend(f"Visual verdict artifact: {item}" for item in verdict_artifact_result.warnings)

            # Failed generated images must be compiled into a repair plan before
            # the next image handoff. This prevents the pipeline from rerunning
            # the same prompt while merely hoping the model obeys next time.
            if post_image_rerender_required is True and post_image_accepted_value == "no":
                failure_routing = extract_field(step8_block, "POST_IMAGE_FAILURE_KEY_ROUTING")
                failure_routing_lower = lower_value(failure_routing)
                if (
                    is_placeholder(failure_routing)
                    or failure_routing_lower.startswith("not_applicable")
                    or value_is_none_like(failure_routing)
                    or count_meaningful_tokens(failure_routing) < 6
                ):
                    errors.append(
                        "Failed post-image verdict requires POST_IMAGE_FAILURE_KEY_ROUTING with a key-by-key route "
                        "from failed verdict keys to Scene Contract / prompt / guide fixes."
                    )
                else:
                    routed_keys = split_failure_keys(failure_routing)
                    missing_routed_keys = [key for key in post_image_failed_keys if key not in routed_keys]
                    if missing_routed_keys:
                        errors.append(
                            "POST_IMAGE_FAILURE_KEY_ROUTING missing failed verdict keys: "
                            + ", ".join(missing_routed_keys)
                        )
                    scale_failed_keys = [key for key in post_image_failed_keys if key in SCALE_FAILURE_VERDICT_KEYS]
                    if scale_failed_keys:
                        scale_repair_text = " ".join(
                            filter(
                                None,
                                [
                                    failure_routing,
                                    post_image_scale_failure_shot_class_escalation,
                                    extract_field(step8_block, "POST_IMAGE_NEXT_DRAFT_PROMPT"),
                                ],
                            )
                        )
                        if (
                            value_is_none_like(post_image_scale_failure_shot_class_escalation)
                            or count_meaningful_tokens(post_image_scale_failure_shot_class_escalation) < 8
                        ):
                            errors.append(
                                "Scale-related post-image failures require POST_IMAGE_SCALE_FAILURE_SHOT_CLASS_ESCALATION: "
                                "repair the camera/framing first, not only the ratio prose."
                            )
                        elif not contains_keyword_korean_tolerant(
                            scale_repair_text,
                            CAMERA_CLASS_SCALE_PROVING_KEYWORDS + SCALE_WITNESS_VISIBILITY_KEYWORDS,
                        ):
                            errors.append(
                                "Scale-related post-image repair must escalate to a wide/long scale shot with full container and door/window/passenger/module witnesses."
                            )
                        if not contains_keyword_korean_tolerant(scale_repair_text, FACE_FOCAL_DEMOTION_KEYWORDS):
                            errors.append(
                                "Scale-related post-image repair must demote face/eye focal to a small accent until vehicle/container scale passes."
                            )

                repair_status = lower_value(extract_field(step8_block, "POST_IMAGE_REPAIR_COMPILER_STATUS"))
                if repair_status != "pass":
                    errors.append(
                        "Failed post-image verdict requires POST_IMAGE_REPAIR_COMPILER_STATUS: pass before rerender."
                    )

                regeneration_gate = lower_value(extract_field(step8_block, "REGENERATION_GATE_STATUS"))
                if regeneration_gate != "pass":
                    errors.append(
                        "Failed post-image verdict requires REGENERATION_GATE_STATUS: pass before the next draft prompt is usable."
                    )

                next_draft_prompt = extract_field(step8_block, "POST_IMAGE_NEXT_DRAFT_PROMPT")
                next_draft_lower = lower_value(next_draft_prompt)
                if (
                    is_placeholder(next_draft_prompt)
                    or next_draft_lower.startswith("not_applicable")
                    or value_is_none_like(next_draft_prompt)
                    or count_meaningful_tokens(next_draft_prompt) < 8
                ):
                    errors.append(
                        "Failed post-image verdict requires POST_IMAGE_NEXT_DRAFT_PROMPT with the repaired next draft prompt."
                    )
                image_gen_prompt = extract_image_generation_prompt(text)
                if next_draft_prompt and image_gen_prompt and next_draft_prompt.strip() == image_gen_prompt.strip():
                    errors.append(
                        "POST_IMAGE_NEXT_DRAFT_PROMPT must not be identical to IMAGE_GEN_HANDOFF_PROMPT after a failed verdict; "
                        "compile a changed repair prompt instead of rerunning the same prompt."
                    )

                repair_artifact_path_value = extract_field(step8_block, "POST_IMAGE_REPAIR_ARTIFACT_PATH")
                repair_artifact_lower = lower_value(repair_artifact_path_value)
                if (
                    is_placeholder(repair_artifact_path_value)
                    or repair_artifact_lower.startswith("not_applicable")
                    or value_is_none_like(repair_artifact_path_value)
                ):
                    errors.append(
                        "Failed post-image verdict requires POST_IMAGE_REPAIR_ARTIFACT_PATH to point to a filled "
                        "templates/post-image-repair-artifact-template.md artifact."
                    )
                else:
                    repair_artifact_path = resolve_reference_path(repair_artifact_path_value or "", path)
                    repair_result = validate_post_image_repair_artifact(
                        repair_artifact_path,
                        spec_path=path,
                        expected_failed_keys=post_image_failed_keys,
                        expected_next_prompt=next_draft_prompt,
                    )
                    errors.extend(f"Post-image repair artifact: {item}" for item in repair_result.errors)
                    warnings.extend(f"Post-image repair artifact: {item}" for item in repair_result.warnings)

    theory_proof_path_value = extract_field(text, "THEORY_READ_PROOF_PATH")
    if not is_placeholder(theory_proof_path_value):
        theory_proof_path = resolve_reference_path(theory_proof_path_value or "", path)
        theory_result = validate_theory_read_proof(theory_proof_path, path, text, sections)
        errors.extend(f"Theory proof: {item}" for item in theory_result.errors)
        warnings.extend(f"Theory proof: {item}" for item in theory_result.warnings)

    object_required = lower_value(extract_field(text, "OBJECT_RESEARCH_REQUIRED"))
    source_image_upgrade = lower_value(extract_field(text, "SOURCE_IMAGE_UPGRADE"))
    object_inventory_block = sections["## Step 2.2 Object Inventory from Perspective"]
    handoff_block = sections["## Step 2.5 Object Research Handoff"]
    relationship_block = sections["## Step 2.6 Object Relationship Check"]
    anatomy_relation_block = sections["## Step 2.7 Anatomy-on-Object Relationship Check"]
    handoff_required = lower_value(extract_field(handoff_block, "HANDOFF_REQUIRED"))
    artifact_path_value = extract_field(handoff_block, "OBJECT_RESEARCH_ARTIFACT_PATH")
    apply_status = lower_value(extract_field(relationship_block, "APPLY_STATUS"))
    image_ready = image_ready_value

    source_image_objects_present = extract_field(object_inventory_block, "SOURCE_IMAGE_OBJECTS_PRESENT")
    primary_retained_objects = extract_field(object_inventory_block, "PRIMARY_RETAINED_OBJECTS")
    structurally_clear_source_objects = extract_field(object_inventory_block, "STRUCTURALLY_CLEAR_SOURCE_OBJECTS")
    structurally_uncertain_source_objects = extract_field(
        object_inventory_block, "STRUCTURALLY_UNCERTAIN_SOURCE_OBJECTS"
    )
    source_image_objects_researched = extract_field(handoff_block, "SOURCE_IMAGE_OBJECTS_RESEARCHED")
    anatomy_references_researched = extract_field(handoff_block, "ANATOMY_REFERENCES_RESEARCHED")
    source_image_research_decision_note = extract_field(
        handoff_block, "SOURCE_IMAGE_RESEARCH_DECISION_NOTE"
    )
    hands_or_finger_poses_researched = extract_field(
        handoff_block, "HANDS_OR_FINGER_POSES_RESEARCHED"
    )
    hand_research_decision_note = extract_field(
        handoff_block, "HAND_RESEARCH_DECISION_NOTE"
    )
    handoff_uncertain_objects = extract_field(handoff_block, "STRUCTURALLY_UNCERTAIN_OBJECTS")
    anatomy_structure_apply_note = extract_field(anatomy_relation_block, "ANATOMY_STRUCTURE_APPLY_NOTE")
    hand_structure_apply_note = extract_field(anatomy_relation_block, "HAND_STRUCTURE_APPLY_NOTE")

    if object_required and handoff_required and object_required != handoff_required:
        errors.append("OBJECT_RESEARCH_REQUIRED and Step 2.5 HANDOFF_REQUIRED must agree.")

    if source_image_upgrade == "yes":
        source_image_style_firewall_fields = {
            "SOURCE_IMAGE_TRANSFER_SCOPE": extract_field(text, "SOURCE_IMAGE_TRANSFER_SCOPE"),
            "SOURCE_IMAGE_STYLE_DESIGN_FIREWALL": extract_field(text, "SOURCE_IMAGE_STYLE_DESIGN_FIREWALL"),
            "SOURCE_IMAGE_ALLOWED_TRANSFER": extract_field(text, "SOURCE_IMAGE_ALLOWED_TRANSFER"),
            "SOURCE_IMAGE_FORBIDDEN_TRANSFER": extract_field(text, "SOURCE_IMAGE_FORBIDDEN_TRANSFER"),
            "SOURCE_IMAGE_REDESIGN_DIRECTIVE": extract_field(text, "SOURCE_IMAGE_REDESIGN_DIRECTIVE"),
            "SOURCE_IMAGE_PROMPT_FIREWALL": extract_field(text, "SOURCE_IMAGE_PROMPT_FIREWALL"),
        }
        source_image_required_fields = {
            "SOURCE_IMAGE_OBJECTS_PRESENT": source_image_objects_present,
            "PRIMARY_RETAINED_OBJECTS": primary_retained_objects,
            "STRUCTURALLY_CLEAR_SOURCE_OBJECTS": structurally_clear_source_objects,
            "STRUCTURALLY_UNCERTAIN_SOURCE_OBJECTS": structurally_uncertain_source_objects,
            "SOURCE_IMAGE_RESEARCH_DECISION_NOTE": source_image_research_decision_note,
            **source_image_style_firewall_fields,
        }
        for field_name, value in source_image_required_fields.items():
            if is_placeholder(value):
                errors.append(f"Source-image upgrade run is missing required field: {field_name}")

        if value_is_none_like(source_image_objects_present):
            errors.append("Source-image upgrade run must list recognized objects in SOURCE_IMAGE_OBJECTS_PRESENT.")

        source_image_style_firewall_text = " ".join(
            value or "" for value in source_image_style_firewall_fields.values()
        )
        if not contains_keyword_korean_tolerant(
            source_image_style_firewall_text, SOURCE_STRUCTURE_ONLY_KEYWORDS
        ):
            errors.append(
                "Source-image upgrade Step 0A must state that the source image transfers structure/object/pose/perspective evidence only, not full style/design."
            )
        if not contains_keyword_korean_tolerant(
            source_image_style_firewall_text, SOURCE_STYLE_DESIGN_FORBID_KEYWORDS
        ):
            errors.append(
                "Source-image upgrade Step 0A must explicitly forbid copying source style/design/palette/linework/medium/costume/creature/prop design unless explicitly opted in."
            )
        if image_ready == "yes":
            final_source_firewall_text = " ".join(
                filter(
                    None,
                    [
                        extract_image_generation_prompt(text),
                        extract_field(step2_9_block, "IMAGE_INPUT_STACK_PLAN"),
                        extract_field(step2_9_block, "IMAGE_GEN_STRUCTURE_CONDITIONING_LIMITS"),
                        extract_field(step2_9_block, "PRE_COMPOSITE_EVIDENCE_STACK_LOCK"),
                    ],
                )
            )
            if not (
                contains_keyword_korean_tolerant(final_source_firewall_text, SOURCE_STRUCTURE_ONLY_KEYWORDS)
                and contains_keyword_korean_tolerant(final_source_firewall_text, SOURCE_STYLE_DESIGN_FORBID_KEYWORDS)
            ):
                errors.append(
                    "PRE_IMAGE_HANDOFF_READY source-image upgrades must carry the source-image style/design firewall into the final prompt or image-input limits: source is structure/object reference only; source style/design/palette/linework/design motifs are not copied."
                )

        if handoff_required == "yes" and value_is_none_like(source_image_objects_researched):
            errors.append(
                "Source-image upgrade run with HANDOFF_REQUIRED: yes must list researched source objects "
                "in SOURCE_IMAGE_OBJECTS_RESEARCHED."
            )

        if handoff_required == "no":
            message = (
                "Source-image upgrade run should normally use Step 2.5 object research on recognized "
                "original-image objects, but HANDOFF_REQUIRED is 'no'."
            )
            if strict_object_research:
                errors.append(message)
            else:
                warnings.append(message)

        if (
            not value_is_none_like(structurally_uncertain_source_objects)
            and handoff_required != "yes"
        ):
            errors.append(
                "STRUCTURALLY_UNCERTAIN_SOURCE_OBJECTS is populated, so source-image upgrade runs must set "
                "HANDOFF_REQUIRED: yes."
            )

    if hands_visible_expected:
        if is_placeholder(hand_research_decision_note) or count_meaningful_tokens(hand_research_decision_note) < 4:
            errors.append(
                "Visible hands require a meaningful HAND_RESEARCH_DECISION_NOTE in Step 2.5."
            )
        if handoff_required != "yes":
            errors.append(
                "Visible, expressive, or prop-holding hands require HANDOFF_REQUIRED: yes so object research can lock hand/finger structure."
            )

    if anatomy_gate_required_value == "yes" and handoff_required != "yes":
        errors.append(
            "ANATOMY_GATE_REQUIRED: yes must flow into Step 2.5 with HANDOFF_REQUIRED: yes so the anatomy library is actually used."
        )

    if not value_is_none_like(handoff_uncertain_objects) and handoff_required != "yes":
        errors.append(
            "Step 2.5 STRUCTURALLY_UNCERTAIN_OBJECTS is populated, so HANDOFF_REQUIRED must be 'yes'."
        )

    if handoff_required == "yes":
        required_fields = [
            ("## Step 2.5 Object Research Handoff", "LOOKUP_RESULT"),
            ("## Step 2.5 Object Research Handoff", "RESEARCH_ACTION"),
            ("## Step 2.5 Object Research Handoff", "RETURNED_CARDS_OR_RECIPES"),
        ]
        for heading, field_name in required_fields:
            value = extract_field(sections[heading], field_name)
            if is_placeholder(value):
                errors.append(f"Object research is required, but {field_name} is missing.")

        if apply_status != "applied":
            errors.append("Object research handoff is required, so Step 2.6 APPLY_STATUS must be 'applied'.")

        if anatomy_gate_required_value == "yes":
            if count_meaningful_tokens(anatomy_references_researched) < 4:
                errors.append(
                    "Anatomy-gated scenes require ANATOMY_REFERENCES_RESEARCHED in Step 2.5."
                )
            if count_meaningful_tokens(anatomy_structure_apply_note) < 4:
                errors.append(
                    "Anatomy-gated scenes require a meaningful ANATOMY_STRUCTURE_APPLY_NOTE in Step 2.6."
                )
        if hands_visible_expected and value_is_none_like(hands_or_finger_poses_researched):
            errors.append(
                "Visible hands require HANDS_OR_FINGER_POSES_RESEARCHED to list the researched hand or finger pose coverage."
            )
        if hands_visible_expected and count_meaningful_tokens(hand_structure_apply_note) < 4:
            errors.append(
                "Visible hands require a meaningful HAND_STRUCTURE_APPLY_NOTE in Step 2.6."
            )

        if is_placeholder(artifact_path_value):
            errors.append("Object research handoff is required, but OBJECT_RESEARCH_ARTIFACT_PATH is missing.")
        else:
            artifact_path = resolve_reference_path(artifact_path_value or "", path)
            artifact_result = validate_object_research_artifact(artifact_path, expected_parent_spec_path=path)
            errors.extend(f"Object artifact: {item}" for item in artifact_result.errors)
            warnings.extend(f"Object artifact: {item}" for item in artifact_result.warnings)

            spec_log_value = extract_field(handoff_block, "OBJECT_RESEARCH_INVOCATION_LOG_PATH")
            spec_log_lower = lower_value(spec_log_value)
            if render_bound_spec and (is_placeholder(spec_log_value) or spec_log_lower == "not_applicable"):
                if spec_log_lower == "not_applicable":
                    errors.append(
                        "Render-bound SPEC with HANDOFF_REQUIRED: yes cannot mark "
                        "OBJECT_RESEARCH_INVOCATION_LOG_PATH as not_applicable; provide the invocation log path."
                    )
                else:
                    errors.append(
                        "Render-bound SPEC with HANDOFF_REQUIRED: yes requires "
                        "OBJECT_RESEARCH_INVOCATION_LOG_PATH (relative path to the invocation log)."
                    )
            elif spec_log_value and not is_placeholder(spec_log_value) and spec_log_lower != "not_applicable":
                spec_log_path = resolve_reference_path(spec_log_value, path)
                if artifact_path.exists():
                    artifact_text = normalize_text(artifact_path)
                    artifact_log_value = extract_field(artifact_text, "INVOCATION_LOG_PATH")
                    if artifact_log_value and not is_placeholder(artifact_log_value):
                        artifact_log_path = resolve_reference_path(artifact_log_value, artifact_path)
                        if spec_log_path != artifact_log_path:
                            errors.append(
                                "OBJECT_RESEARCH_INVOCATION_LOG_PATH in spec resolves to "
                                f"{spec_log_path}, but the object artifact's INVOCATION_LOG_PATH resolves to "
                                f"{artifact_log_path}. The spec, artifact, and log must agree on a single path."
                            )
    else:
        if handoff_required == "no" and apply_status == "applied":
            warnings.append("Step 2.6 APPLY_STATUS is 'applied' even though Step 2.5 says no handoff was required.")
        if artifact_path_value and not is_placeholder(artifact_path_value) and lower_value(artifact_path_value) != "not_applicable":
            warnings.append("OBJECT_RESEARCH_ARTIFACT_PATH is populated even though handoff is not required.")
        spec_log_value = extract_field(handoff_block, "OBJECT_RESEARCH_INVOCATION_LOG_PATH")
        if (
            spec_log_value
            and not is_placeholder(spec_log_value)
            and lower_value(spec_log_value) != "not_applicable"
        ):
            warnings.append(
                "OBJECT_RESEARCH_INVOCATION_LOG_PATH is populated even though HANDOFF_REQUIRED is not 'yes'."
            )

    request_summary = lower_value(extract_field(text, "REQUEST_SUMMARY"))
    object_research_signal_text = " ".join(
        filter(
            None,
            [
                request_summary,
                lower_value(extract_field(handoff_block, "SCENE_TYPE")),
                lower_value(extract_field(handoff_block, "REQUIRED_OBJECTS")),
                lower_value(extract_field(step2_2_block, "STRUCTURALLY_UNCERTAIN_SOURCE_OBJECTS")),
                lower_value(extract_field(step2_2_block, "UNKNOWN_OBJECT_TRIAGE")),
                lower_value(visible_hands_and_poses),
            ],
        )
    )
    likely_needs_object_research = contains_object_research_signal(object_research_signal_text)
    if likely_needs_object_research and handoff_required == "no":
        message = (
            "Spec text contains environment/prop keywords that often require Step 2.5 object research, "
            "but HANDOFF_REQUIRED is 'no'."
        )
        if strict_object_research:
            errors.append(message)
        else:
            warnings.append(message)

    final_gate = lower_value(extract_field(sections["## Step 8 Final Check"], "FINAL_GATE_STATUS"))
    if image_ready == "yes" and final_gate != "pass":
        errors.append("IMAGE_GEN_READY cannot be 'yes' unless FINAL_GATE_STATUS is 'pass'.")

    if final_gate == "pass":
        for heading in SECTION_ORDER[:-1]:
            value = lower_value(extract_field(sections[heading], "GATE_STATUS"))
            if heading == "## Step 2.3 Anatomy Structure Gate" and anatomy_gate_required_value == "no":
                if value not in {"pass", "not_applicable"}:
                    errors.append(f"{heading} must be 'pass' or 'not_applicable' when anatomy gating is not required.")
                continue
            if heading in {
                "## Step 2.5 Object Research Handoff",
                "## Step 2.6 Object Relationship Check",
            } and handoff_required == "no":
                if value not in {"pass", "not_applicable"}:
                    errors.append(f"{heading} must be 'pass' or 'not_applicable' when handoff is not required.")
                continue
            if value != "pass":
                errors.append(f"{heading} must have GATE_STATUS: pass before final completion.")

    return ValidationResult(path=path, text=text, errors=errors, warnings=warnings, sections=sections)


def print_results(errors: list[str], warnings: list[str]) -> None:
    if errors:
        print("VALIDATION FAILED")
        for item in errors:
            print(f"- ERROR: {item}")
    else:
        print("VALIDATION PASSED")

    if warnings:
        for item in warnings:
            print(f"- WARNING: {item}")


def main() -> int:
    args = parse_args()
    result = validate_spec_path(args.spec_path, strict_object_research=args.strict_object_research)
    print_results(result.errors, result.warnings)
    return 1 if result.errors else 0


if __name__ == "__main__":
    sys.exit(main())
