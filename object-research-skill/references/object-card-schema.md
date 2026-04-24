# Object Card Schema

Summary: Use this schema to store one reusable object per file. The card should make the object easier to draw, simplify, restyle, and place into later scenes.

Summary: Keep cards compact and structured. Store only information that improves silhouette, structure, material read, or scene placement.

Anatomy note:

- This same schema can store anatomy cards.
- For layered anatomy work, prefer:
  - one age-band body base card
  - one sex overlay card
  - one current body-type baseline card
  - one hand submodule card
- The hand card should be treated as a submodule of the body choice, not as an isolated replacement for anatomy structure.

## File location

Store cards in:

`illustration-library/object_cards/<category>/<slug>.md`

## Required fields

```text
[OBJECT_CARD]

NAME:
ALIASES:
CATEGORY:

FUNCTION:

CORE_SILHOUETTE:

PRIMARY_FORMS:

DIMENSIONAL_ENVELOPE:

THICKNESS_NOTES:

PROPORTION_RULES:

HUMAN_SCALE_READ:

SUPPORT_LOGIC:

MATERIALS:

VISUAL_CUES:

ANGLE_NOTES:

DO_NOT_BREAK:

STYLE_VARIATION:

SCENE_USAGE:

SOURCE_NOTES:

CONFIDENCE:

LAST_UPDATED:

[/OBJECT_CARD]
```

## Field guidance

### NAME

Canonical object name.

### ALIASES

Alternate names, spellings, plural forms, Korean/English synonyms.

### CATEGORY

Example:

- laboratory / containment device
- gothic / lighting fixture
- industrial / piping
- anatomy / hand
- anatomy / body / age-band
- anatomy / body / sex-overlay
- anatomy / body / body-type-baseline

### FUNCTION

What the object does in-scene and what it implies narratively.

### CORE_SILHOUETTE

The fastest read of the object at thumbnail size.

### PRIMARY_FORMS

List the biggest forms first.
Ignore tiny decoration unless it affects identity.

### DIMENSIONAL_ENVELOPE

Record approximate X/Y/Z extent in a drawing-friendly way:

- width
- height
- depth

Use ranges when the object exists in multiple common sizes.
Prefer practical envelopes over fake precision.

### THICKNESS_NOTES

Store thickness cues that affect believable drawing:

- wall thickness
- bezel thickness
- lip height
- frame thickness
- bundle diameter

### PROPORTION_RULES

Store the internal ratio logic that keeps the object believable:

- tall vs wide
- shallow vs deep
- cap/base/body relation
- repeated-part spacing

### HUMAN_SCALE_READ

Explain how the object reads next to a person, hand, head, torso, or room module.
This helps scene blocking and scale comparison.

### SUPPORT_LOGIC

How the object stands, hangs, mounts, connects, opposes, or bears weight.
This field is mandatory for furniture, machinery, fixtures, architecture-adjacent objects, and anatomy cards that grip or support props.
For anatomy base / overlay cards, use this field to explain how the body mass, joints, or contact logic stay believable in pose construction.

### MATERIALS

Only list materials that affect rendering, edge behavior, reflection, or wear.

### VISUAL_CUES

The small details that make the object recognizable.

### ANGLE_NOTES

What matters in front, side, and 3/4 views.

### DO_NOT_BREAK

Critical proportions or logic that make the object believable.

### STYLE_VARIATION

How the object changes across modes such as:

- realistic
- anime simplified
- gothic
- neon sci-fi

### SCENE_USAGE

How the object supports framing, scale, focal hierarchy, lighting bounce, density, or worldbuilding.

### SOURCE_NOTES

Short source summary and what came from observation vs inference.
Do not paste long copyrighted text.

### CONFIDENCE

Use `high`, `medium`, or `low`.

### LAST_UPDATED

Use ISO-like date where practical.
