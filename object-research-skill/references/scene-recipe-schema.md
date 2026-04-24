# Scene Recipe Schema

Summary: Use a scene recipe when a set of objects repeatedly appears together in the same type of environment. Recipes prevent re-researching the same background ecosystem from scratch.

Summary: A recipe is not a fixed composition. It is a reusable environment knowledge pack.

## File location

Store recipes in:

`illustration-library/scene_recipes/<slug>.md`

## Required fields

```text
[SCENE_RECIPE]

NAME:
SCENE_TYPE:
MOOD_TAGS:

CORE_OBJECT_SET:

OPTIONAL_OBJECTS:

LAYOUT_PATTERNS:

FOCAL_SUPPORT:

DENSITY_RULES:

LIGHTING_IMPLICATIONS:

STYLE_VARIATIONS:

RELATED_OBJECT_CARDS:

SOURCE_NOTES:

CONFIDENCE:

LAST_UPDATED:

[/SCENE_RECIPE]
```

## Guidance

- `CORE_OBJECT_SET`: the minimum recognizable object combination
- `OPTIONAL_OBJECTS`: variations that add richness without breaking the scene type
- `LAYOUT_PATTERNS`: common placement logic, framing roles, and depth layering
- `FOCAL_SUPPORT`: how the objects support the main figure without stealing first read
- `DENSITY_RULES`: where clutter should gather and where breathing room should remain
- `LIGHTING_IMPLICATIONS`: typical bounce, glow, shadow, or reflective behavior from the environment
- `STYLE_VARIATIONS`: how the same recipe shifts across gothic, neon, industrial, anime, or simplified modes
