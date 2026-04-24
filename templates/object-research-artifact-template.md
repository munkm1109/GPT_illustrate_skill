# Object Research Artifact Template

Use this template when `illustrate-skill` Step 2.5 hands off to `object-research-skill` for render-bound scene work.

Recommended workflow:

1. Copy this file to a working path such as `.omx/runs/<YYYYMMDD>-<scene-slug>-object-research.md`.
2. Fill every field with draw-ready object knowledge or explicit `none` / `not_applicable` style values where appropriate.
3. Split research by lane instead of mixing anatomy, scale anchors, hard-surface background, effects, and text in one flat list.
4. Create a matching invocation log from `templates/object-research-invocation-log-template.md` and record its path in `INVOCATION_LOG_PATH`.
5. Record the artifact path in the parent spec's `OBJECT_RESEARCH_ARTIFACT_PATH` field.
6. Do not mark `ARTIFACT_READY: yes` until the notes are usable for scale/perspective locks, relationship checks, 3D blockout, and image-generation prompt locks.
7. Unknown objects must be named, researched, removed, replaced with a known object, intentionally abstracted with a declared function, or escalated to the user. Do not fake unknown objects as random patterns.

[OBJECT_RESEARCH_ARTIFACT]

SOURCE_REQUEST:
PARENT_SPEC_PATH:
SCENE_INTENT:
SCENE_TYPE:
STYLE_MODE:
PRIORITY:
REQUIRED_OBJECTS:
RESEARCH_LANES:
MATCHED_CARDS_BY_LANE:
NEW_OR_UPDATED_CARDS:
MISSING_OR_WEAK_CARDS_BY_LANE:
UNKNOWN_OBJECT_TRIAGE_RESULT:
SCENE_RECIPE_UPDATES:
PER_OBJECT_DRAW_LOCKS:
SCALE_PERSPECTIVE_LOCKS:
RELATIONSHIP_CHECK_NOTES:
GENERATION_PROMPT_LOCKS:
DO_NOT_FAKE_POLICY:
LOOKUP_SUMMARY:
RESEARCH_SUMMARY:
INVOCATION_LOG_PATH:
ARTIFACT_READY: <yes|no>

[/OBJECT_RESEARCH_ARTIFACT]
