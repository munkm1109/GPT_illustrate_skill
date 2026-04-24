#!/usr/bin/env python3
"""Validate an illustrate-skill SPEC artifact and linked evidence."""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path


GLOBAL_FIELDS = [
    "REQUEST_SUMMARY",
    "DELIVERABLE",
    "WORKSPACE_STYLE_MODE",
    "SOURCE_IMAGE_UPGRADE",
    "OBJECT_RESEARCH_REQUIRED",
    "IMAGE_GEN_READY",
    "THEORY_READ_PROOF_PATH",
]

SECTION_ORDER = [
    "## Step 1 Intent",
    "## Step 2 Composition",
    "## Step 2.1 Perspective Rig",
    "## Step 2.2 Object Inventory from Perspective",
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
        "BLACK_MASS_MAP",
        "NEGATIVE_SPACE_BALANCE",
        "FLOW_DIRECTION_MAP",
        "COMPOSITION_OBJECT_ROLE_SUMMARY",
        "USER_CHECKPOINT_A_DIRECTION",
        "GATE_STATUS",
    ],
    "## Step 2.1 Perspective Rig": [
        "CAMERA_POSITION",
        "HORIZON_LINE",
        "VANISHING_POINTS",
        "PRIMARY_DEPTH_AXIS",
        "SUPPORT_PLANES",
        "VERTICAL_PLANE_LOCKS",
        "SCALE_ANCHOR_OBJECTS",
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
        "GATE_STATUS",
    ],
    "## Step 2.3 Anatomy Structure Gate": [
        "ANATOMY_GATE_REQUIRED",
        "ANATOMY_PRIMARY_OBJECT",
        "ANATOMY_SUB_OBJECTS",
        "ANATOMY_CONTACT_OBJECTS",
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
        "VISIBLE_HANDS_AND_POSES",
        "HAND_SILHOUETTE_NOTE",
        "FINGER_GROUPING_NOTE",
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
        "USER_CHECKPOINT_B_OBJECT_DIRECTION",
        "GATE_STATUS",
    ],
    "## Step 2.5 Object Research Handoff": [
        "HANDOFF_REQUIRED",
        "OBJECT_RESEARCH_ARTIFACT_PATH",
        "SCENE_TYPE",
        "REQUIRED_OBJECTS",
        "RESEARCH_LANES_USED",
        "ANATOMY_REFERENCES_RESEARCHED",
        "SOURCE_IMAGE_OBJECTS_RESEARCHED",
        "SOURCE_IMAGE_RESEARCH_DECISION_NOTE",
        "HANDS_OR_FINGER_POSES_RESEARCHED",
        "HAND_RESEARCH_DECISION_NOTE",
        "BACKGROUND_OBJECTS_RESEARCHED",
        "SCALE_ANCHOR_OBJECTS_RESEARCHED",
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
        "CONTACT_AND_SUPPORT",
        "COLLISION_CHECK",
        "MATERIAL_LIGHT_INTERACTION",
        "RIGID_OBJECT_GEOMETRY_LOCKS",
        "TEXT_RENDERING_POLICY",
        "GATE_STATUS",
    ],
    "## Step 2.7 Anatomy-on-Object Relationship Check": [
        "BODY_SUPPORT_LOGIC",
        "ANATOMY_STRUCTURE_APPLY_NOTE",
        "HAND_PROP_RELATION",
        "HAND_STRUCTURE_APPLY_NOTE",
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
        "ANATOMY_TO_ARCHITECTURE_SCALE_CHECK",
        "WINDOW_TO_HEAD_SIZE_CHECK",
        "PARAPET_TO_BODY_HEIGHT_CHECK",
        "FOOTPRINT_ON_SUPPORT_PLANE_CHECK",
        "DETAIL_AFTER_BLOCKOUT_LOCK",
        "CAMERA_BLOCKOUT",
        "DEPTH_LAYER_ORDER",
        "CONTACT_POINTS",
        "SCALE_CHECK",
        "PERSPECTIVE_CHECK",
        "OPTIONAL_3D_REFERENCE_PLAN",
        "BLENDER_BLOCKOUT_REQUIRED",
        "BLENDER_SCENE_PATH",
        "BLENDER_RENDER_SCRIPT_PATH",
        "BLENDER_PASS_OUTPUTS",
        "BLENDER_BLOCKOUT_REVIEW",
        "BLENDER_GUIDE_STRENGTH",
        "STRUCTURAL_INVARIANTS_TO_PRESERVE",
        "PAINTERLY_FREEDOMS_ALLOWED",
        "CONTROLNET_CONDITIONING_PLAN",
        "BLOCKOUT_REVIEW_STATUS",
        "USER_CHECKPOINT_C_BLOCKOUT_DIRECTION",
        "GATE_STATUS",
    ],
    "## Step 2.9 Image Translation Lock": [
        "GENERATION_PRIORITY_ORDER",
        "NON_NEGOTIABLE_LOCKS",
        "STYLE_ALLOWED_AFTER_STRUCTURE",
        "BLENDER_GUIDE_STRENGTH",
        "PAINTERLY_COMPRESSION_ALLOWANCE",
        "NO_HIERATIC_SCALE_DISTORTION",
        "PROMPT_COMPRESSION_RULE",
        "UNKNOWN_OBJECT_POLICY_LOCK",
        "USER_CHECKPOINT_D_PRE_RENDER_DIRECTION",
        "GATE_STATUS",
        "GATE_NOTE",
    ],
    "## Step 3 Value": [
        "LIGHTING_PLAN",
        "VALUE_COUNT_DECISION",
        "GRAYSCALE_VALUE_MAP",
        "FOCAL_CONTRAST_ZONE",
        "OUTER_AREA_SUPPRESSION_PLAN",
        "MATERIAL_EDGE_PLAN",
        "GRAYSCALE_REDUCTION_TEST",
        "GATE_STATUS",
    ],
    "## Step 4 Face": [
        "SURFACE_INNER_EMOTION",
        "MAIN_SUPPORT_EMOTION",
        "INTENSITY",
        "EYE_RENDER_PLAN",
        "EXPRESSION_NOTE",
        "FACE_FOCAL_MAP",
        "EYE_LIGHT_CONSISTENCY_NOTE",
        "ASYMMETRY_NOTE",
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
        "LINE_VS_SHAPE_ROLE_NOTE",
        "GATE_STATUS",
    ],
    "## Step 6 Color & Accent": [
        "PALETTE_SELECTION",
        "ACCENT_PLACEMENT_MAP",
        "BASE_SUPPORT_ACCENT_ROLE_NOTE",
        "PER_PART_COLOR_DISTRIBUTION_NOTE",
        "NON_PLASTIC_SKIN_TONE_LOCK",
        "VALUE_PRESERVATION_NOTE",
        "GATE_STATUS",
    ],
    "## Step 7 Texture": [
        "TEXTURE_DENSITY_MAP",
        "ROUGH_SMOOTH_SEPARATION_PLAN",
        "SECONDARY_SYMBOL_PLACEMENT",
        "GLOBAL_GRAIN_NOTE",
        "LOCAL_TEXTURE_EMPHASIS_NOTE",
        "NON_PLASTIC_SKIN_SURFACE_NOTE",
        "GATE_STATUS",
    ],
    "## Step 8 Final Check": [
        "NORMAL_VIEW_CHECK",
        "REDUCED_SIZE_CHECK",
        "GRAYSCALE_CHECK",
        "HAND_READABILITY_CHECK",
        "FINAL_CORRECTION_LIST",
        "OUTPUT_MEDIUM_NOTE",
        "SELF_FEEDBACK_NOTE",
        "ARCHIVE_NOTE",
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
    "## Step 2.7 Anatomy-on-Object Relationship Check": "STEP_2_FILES_READ",
    "## Step 2.8 3D Blockout / Modeling Contract": "STEP_2_FILES_READ",
    "## Step 2.9 Image Translation Lock": "STEP_8_FILES_READ",
    "## Step 3 Value": "STEP_3_FILES_READ",
    "## Step 4 Face": "STEP_4_FILES_READ",
    "## Step 5 Line & Shape": "STEP_5_FILES_READ",
    "## Step 6 Color & Accent": "STEP_6_FILES_READ",
    "## Step 7 Texture": "STEP_7_FILES_READ",
    "## Step 8 Final Check": "STEP_8_FILES_READ",
}

STATUS_FIELDS = {
    "GATE_STATUS": {"pass", "needs_revision", "not_applicable"},
    "FINAL_GATE_STATUS": {"pass", "needs_revision"},
    "BLOCKOUT_REVIEW_STATUS": {"pass", "needs_revision", "not_applicable"},
}

BOOLEAN_FIELDS = {
    "SOURCE_IMAGE_UPGRADE": {"yes", "no"},
    "OBJECT_RESEARCH_REQUIRED": {"yes", "no"},
    "IMAGE_GEN_READY": {"yes", "no"},
    "ANATOMY_GATE_REQUIRED": {"yes", "no"},
    "HANDOFF_REQUIRED": {"yes", "no"},
    "BLENDER_BLOCKOUT_REQUIRED": {"yes", "no"},
}

APPLY_STATUS_VALUES = {"applied", "not_applicable", "needs_revision"}

BLENDER_STEP_FIELDS = {
    "BLENDER_BLOCKOUT_REQUIRED",
    "BLENDER_SCENE_PATH",
    "BLENDER_RENDER_SCRIPT_PATH",
    "BLENDER_PASS_OUTPUTS",
    "BLENDER_BLOCKOUT_REVIEW",
    "BLENDER_GUIDE_STRENGTH",
    "STRUCTURAL_INVARIANTS_TO_PRESERVE",
    "PAINTERLY_FREEDOMS_ALLOWED",
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

SWORD_KEYWORDS = ["sword", "blade", "katana", "검", "칼", "블레이드"]

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
    "UNKNOWN_OBJECT_TRIAGE_RESULT",
    "SCENE_RECIPE_UPDATES",
    "PER_OBJECT_DRAW_LOCKS",
    "SCALE_PERSPECTIVE_LOCKS",
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


def value_is_none_like(value: str | None) -> bool:
    normalized = lower_value(value)
    return normalized in {"", "none", "not_applicable", "n/a", "na", "no", "없음", "해당없음"}


def normalize_pipe_list(value: str | None) -> list[str]:
    if not value:
        return []
    return [part.strip() for part in value.split(" | ") if part.strip()]


def contains_keyword(value: str | None, keywords: list[str]) -> bool:
    text = lower_value(value)
    return any(keyword in text for keyword in keywords)


def is_render_bound_spec(text: str) -> bool:
    deliverable = extract_field(text, "DELIVERABLE")
    image_ready = lower_value(extract_field(text, "IMAGE_GEN_READY"))
    return image_ready == "yes" or contains_keyword(deliverable, RENDER_BOUND_DELIVERABLE_KEYWORDS)


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


def count_meaningful_tokens(value: str | None) -> int:
    if not value:
        return 0
    return len(re.findall(r"[A-Za-z0-9가-힣]+", value))


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

    render_bound_spec = is_render_bound_spec(text)

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

    step1_block = sections["## Step 1 Intent"]
    step2_block = sections["## Step 2 Composition"]
    step2_1_block = sections["## Step 2.1 Perspective Rig"]
    step2_2_block = sections["## Step 2.2 Object Inventory from Perspective"]
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
    action_field = extract_field(step1_block, "ACTION")
    camera_angle = extract_field(step2_block, "CAMERA_ANGLE")
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
                "Visible hands require a meaningful FINGER_GROUPING_NOTE in Step 2.3."
            )

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
            "CONTACT_PLANES",
            "PERSPECTIVE_FAIL_CONDITIONS",
        ):
            if count_meaningful_tokens(extract_field(step2_1_block, field_name)) < 4:
                errors.append(f"Perspective-heavy scenes require a meaningful Step 2.1 {field_name}.")

    vehicle_or_scale_expected = any(
        contains_keyword(field, VEHICLE_SCALE_KEYWORDS)
        for field in (
            request_summary,
            extract_field(step2_2_block, "SUPPORT_PLANE_OBJECTS"),
            extract_field(step2_2_block, "SCALE_ANCHOR_OBJECTS"),
            extract_field(step2_5_block, "REQUIRED_OBJECTS"),
        )
    )
    if vehicle_or_scale_expected:
        scale_relation_table = extract_field(step2_6_block, "SCALE_RELATION_TABLE")
        if count_meaningful_tokens(scale_relation_table) < 6:
            errors.append("Vehicle / scale-anchor scenes require Step 2.6 SCALE_RELATION_TABLE to lock object scale relationships.")
        if count_meaningful_tokens(extract_field(step2_8_block, "SCALE_CHECK")) < 6:
            errors.append("Vehicle / scale-anchor scenes require Step 2.8 SCALE_CHECK to explicitly address scale or ratio.")

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
    if lower_value(extract_field(text, "IMAGE_GEN_READY")) == "yes" and bad_unknown_policy:
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
            "ANATOMY_TO_ARCHITECTURE_SCALE_CHECK",
            "FOOTPRINT_ON_SUPPORT_PLANE_CHECK",
            "DETAIL_AFTER_BLOCKOUT_LOCK",
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
    structural_invariants = extract_field(step2_8_block, "STRUCTURAL_INVARIANTS_TO_PRESERVE")
    painterly_freedoms = extract_field(step2_8_block, "PAINTERLY_FREEDOMS_ALLOWED")
    controlnet_conditioning_plan = extract_field(step2_8_block, "CONTROLNET_CONDITIONING_PLAN")
    blockout_review_status = lower_value(extract_field(step2_8_block, "BLOCKOUT_REVIEW_STATUS"))
    step2_9_blender_guide_strength = lower_value(extract_field(step2_9_block, "BLENDER_GUIDE_STRENGTH"))
    painterly_compression_allowance = extract_field(step2_9_block, "PAINTERLY_COMPRESSION_ALLOWANCE")
    no_hieratic_scale_distortion = extract_field(step2_9_block, "NO_HIERATIC_SCALE_DISTORTION")
    allowed_guide_strengths = {"loose guide", "medium guide", "strict guide", "not_applicable"}

    if render_bound_spec and blender_blockout_required != "yes":
        errors.append(
            "Render-bound SPEC runs must set BLENDER_BLOCKOUT_REQUIRED: yes; Blender is no longer optional."
        )

    if any(
        contains_keyword(field, ["blender", "controlnet", "depth map", "normal map", "lineart", "3d-first", "3d first"])
        for field in (request_summary, extract_field(step2_8_block, "OPTIONAL_3D_REFERENCE_PLAN"))
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
            ("STRUCTURAL_INVARIANTS_TO_PRESERVE", structural_invariants),
            ("PAINTERLY_FREEDOMS_ALLOWED", painterly_freedoms),
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

        if count_meaningful_tokens(painterly_compression_allowance) < 4:
            errors.append(
                "Step 2.9 PAINTERLY_COMPRESSION_ALLOWANCE must state what compression/massing is allowed or disallowed."
            )

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
                    extract_field(text, "IMAGE_GEN_HANDOFF_PROMPT"),
                )
            ),
            ["symbolic scale emphasis", "hieratic scale", "권력 스케일", "상징적 크기"],
        ) and not contains_keyword(no_hieratic_scale_distortion, ["explicitly requested", "user explicitly", "명시", "요청"]):
            errors.append(
                "Spec mentions symbolic/hieratic scale language without an explicit opt-in exception in NO_HIERATIC_SCALE_DISTORTION."
            )

        if blockout_review_status != "pass":
            errors.append("BLENDER_BLOCKOUT_REQUIRED: yes requires BLOCKOUT_REVIEW_STATUS: pass before Step 2.8 can pass.")

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
    anatomy_primitive_blockout = extract_field(step2_3_block, "ANATOMY_PRIMITIVE_BLOCKOUT")
    head_primitive = extract_field(step2_3_block, "HEAD_PRIMITIVE")
    ribcage_primitive = extract_field(step2_3_block, "RIBCAGE_PRIMITIVE")
    pelvis_primitive = extract_field(step2_3_block, "PELVIS_PRIMITIVE")
    limb_cylinder_chain = extract_field(step2_3_block, "LIMB_CYLINDER_CHAIN")
    joint_sphere_map = extract_field(step2_3_block, "JOINT_SPHERE_MAP")
    hand_foot_primitives = extract_field(step2_3_block, "HAND_FOOT_PRIMITIVES")
    anatomy_primitive_fail_conditions = extract_field(step2_3_block, "ANATOMY_PRIMITIVE_FAIL_CONDITIONS")
    anatomy_research_decision_note = extract_field(step2_3_block, "ANATOMY_RESEARCH_DECISION_NOTE")

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
    face_focal_map = extract_field(step4_block, "FACE_FOCAL_MAP")
    if not contains_keyword(face_focal_map, FACE_FOCUS_KEYWORDS):
        errors.append("Step 4 FACE_FOCAL_MAP must explicitly describe face/eye-first focus.")
    if not contains_keyword(eye_render_plan, ["iris", "pupil", "highlight", "홍채", "동공", "하이라이트"]):
        errors.append("Step 4 EYE_RENDER_PLAN must describe eye-structure rendering, not just mood.")

    hand_line_priority_note = extract_field(step5_block, "HAND_LINE_PRIORITY_NOTE")
    if hands_visible_expected:
        if not likely_visible_hands(hand_line_priority_note):
            errors.append(
                "Visible hands require Step 5 HAND_LINE_PRIORITY_NOTE to explicitly address hand/finger handling."
            )

    accent_map = extract_field(step6_block, "ACCENT_PLACEMENT_MAP")
    if not contains_keyword(accent_map, FACE_FOCUS_KEYWORDS):
        errors.append("Step 6 ACCENT_PLACEMENT_MAP must explicitly place the strongest accents at face or eyes.")
    if contains_keyword(accent_map, GARMENT_FOCUS_KEYWORDS) and not contains_keyword(accent_map, FACE_FOCUS_KEYWORDS):
        errors.append("Step 6 ACCENT_PLACEMENT_MAP cannot prioritize garment accents without face/eye priority.")

    correction_list = extract_field(step8_block, "FINAL_CORRECTION_LIST")
    hand_readability_check = extract_field(step8_block, "HAND_READABILITY_CHECK")
    if not is_actionable_correction(correction_list):
        errors.append("Step 8 FINAL_CORRECTION_LIST must contain actionable corrections, not only summary praise.")
    if hands_visible_expected and count_meaningful_tokens(hand_readability_check) < 4:
        errors.append(
            "Visible hands require Step 8 HAND_READABILITY_CHECK to confirm the hand/finger read."
        )

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
    image_ready = lower_value(extract_field(text, "IMAGE_GEN_READY"))

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
        source_image_required_fields = {
            "SOURCE_IMAGE_OBJECTS_PRESENT": source_image_objects_present,
            "PRIMARY_RETAINED_OBJECTS": primary_retained_objects,
            "STRUCTURALLY_CLEAR_SOURCE_OBJECTS": structurally_clear_source_objects,
            "STRUCTURALLY_UNCERTAIN_SOURCE_OBJECTS": structurally_uncertain_source_objects,
            "SOURCE_IMAGE_RESEARCH_DECISION_NOTE": source_image_research_decision_note,
        }
        for field_name, value in source_image_required_fields.items():
            if is_placeholder(value):
                errors.append(f"Source-image upgrade run is missing required field: {field_name}")

        if value_is_none_like(source_image_objects_present):
            errors.append("Source-image upgrade run must list recognized objects in SOURCE_IMAGE_OBJECTS_PRESENT.")

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
    else:
        if handoff_required == "no" and apply_status == "applied":
            warnings.append("Step 2.6 APPLY_STATUS is 'applied' even though Step 2.5 says no handoff was required.")
        if artifact_path_value and not is_placeholder(artifact_path_value) and lower_value(artifact_path_value) != "not_applicable":
            warnings.append("OBJECT_RESEARCH_ARTIFACT_PATH is populated even though handoff is not required.")

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
