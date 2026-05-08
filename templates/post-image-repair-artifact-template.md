[POST_IMAGE_REPAIR_ARTIFACT]

PARENT_SPEC_PATH: <relative path to the SPEC whose generated image failed>
SOURCE_VERDICT_ARTIFACT_PATH: <relative path to the POST_IMAGE_VISUAL_VERDICT_ARTIFACT that found the failure>
FAILED_KEYS: <pipe-separated failed verdict keys, e.g. target_contact_pass | scale_visual_guide_pass | cut_plane_visibility_pass | weapon_grip_mechanics_pass>
FAILURE_KEY_ROUTING: <for each FAILED_KEYS item: failed key -> Scene Contract field / prompt-lock field / visual-guide escalation to change; scale/cut-plane/grip failures must route to visual guide evidence, not prose-only prompt patches>
SCENE_CONTRACT_PATCH: <specific contract edits that prevent the failure from recurring; name object IDs, target IDs, forbidden targets, scale witnesses, anatomy chains, or garment anchors>
PROMPT_PATCH_TIER_0_TO_3: <ordered prompt patch: Tier 0 non-negotiable repair first, Tier 1 structure/anatomy/scale, Tier 2 style-safe simplification, Tier 3 optional polish>
SCALE_FAILURE_SHOT_CLASS_ESCALATION: <required when any scale-related key failed: escalate camera/framing first, e.g. extreme wide / wide scale shot, no close-up, smaller protagonist screen share, full container visibility, repeated doors/windows/passengers/modules, face/eyes as small accents; otherwise not_applicable with reason>
VISUAL_GUIDE_ESCALATION: <state the required annotated mask / blockout overlay / crop guide / lineart-depth pass when a failed key is scale_visual_guide_pass, cut_plane_visibility_pass, unknown_cut_form_pass, weapon_grip_mechanics_pass, or wrist_force_path_pass; use not_applicable only when no visual-guide-sensitive key failed and explain why>
NEXT_DRAFT_PROMPT: <the repaired prompt for the next draft; must differ from the failed IMAGE_GEN_HANDOFF_PROMPT and explicitly carry each failed-key repair>
REPAIR_READY: <yes|no>

[/POST_IMAGE_REPAIR_ARTIFACT]
