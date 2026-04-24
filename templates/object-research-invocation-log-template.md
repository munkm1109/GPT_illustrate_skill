# Object Research Invocation Log Template

Use this template when `object-research-skill` is called as part of an `illustrate-skill` Step 2.5 handoff for a render-bound scene.

Recommended workflow:

1. Copy this file to a working path such as `.omx/runs/<YYYYMMDD>-<scene-slug>-object-research-log.md`.
2. Record its path in the parent object-research artifact's `INVOCATION_LOG_PATH`.
3. Update the log before handing control back to `illustrate-skill`, preferably via `python scripts/log_object_research_invocation.py ...`.
4. Do not mark `INVOCATION_READY: yes` until the lookup-first result and output artifact path are recorded.

[OBJECT_RESEARCH_INVOCATION]

PARENT_SPEC_PATH:
PARENT_OBJECT_ARTIFACT_PATH:
MODE:
SCENE_INTENT:
SCENE_TYPE:
STYLE_MODE:
PRIORITY:
REQUIRED_OBJECTS:
LOOKUP_FIRST: <yes|no>
LOCAL_LIBRARY_CHECK:
WEB_RESEARCH_USED: <yes|no>
OUTPUT_ARTIFACT_PATH:
RETURN_SHAPE:
INVOCATION_EVENTS:
INVOCATION_READY: <yes|no>

[/OBJECT_RESEARCH_INVOCATION]
