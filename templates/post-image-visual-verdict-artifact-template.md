# Post-Image Visual Verdict Artifact Template

Use this template to record an authoritative post-image visual verdict for a
SPEC run that produced a generated image. The artifact is filled by a
vision-capable reviewer (human or vision model) and is the file-based
counterpart of `POST_IMAGE_VISUAL_VERDICT_JSON` inside the SPEC.

The validator cross-checks the artifact against the SPEC's inline JSON and
blocks `IMAGE_GEN_READY: yes` if either side is missing or contradictory.

Recommended path:

    .omx/runs/<YYYYMMDD>-<scene-slug>-visual-verdict.md

[POST_IMAGE_VISUAL_VERDICT_ARTIFACT]

PARENT_SPEC_PATH: <relative path back to the SPEC artifact>
GENERATED_IMAGE_PATH: <relative path to the rendered image being judged>
REVIEWER: <human reviewer name | vision model id | "vision_loop">
REVIEW_TIMESTAMP: <ISO-8601>
ARTIFACT_READY: <yes|no>

VERDICT_JSON: |
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

VISIBLE_LANDMARK_EVIDENCE: <one bullet per landmark used to judge each *_pass field; cite where in the image (e.g. "passenger head silhouette in window 3 from left at z~5m"); evidence must be directly visible, not inferred from spec wording>

FAIL_DESCRIPTIONS: <free prose per failed *_pass; describe what was visible vs. what was required, with concrete pixel/region references when possible>

RERENDER_PLAN: <if rerender_required is true: tier-by-tier list of changes needed before next render; else "not_applicable">

NOTES_TO_NEXT_SPEC: <anything that should be inherited into FAILURE_CATALOG_PATH or future PASSENGER_INSTANCE_REGISTRY entries>

[/POST_IMAGE_VISUAL_VERDICT_ARTIFACT]
