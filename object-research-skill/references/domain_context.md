# Domain Context

Summary: This skill exists to support illustration planning, not industrial design or engineering documentation. The output should help Codex draw objects believably inside scenes, especially for background structures, props, furniture, lab devices, machinery, and architectural elements.

Summary: The user is Korean-speaking and wants reusable object knowledge that can be recalled in later illustration sessions. Library lookup should be preferred over repeated web search.

## Storage roots

- Object cards: `illustration-library/object_cards/`
- Scene recipes: `illustration-library/scene_recipes/`

## User expectations

- Research should produce draw-ready structure, not generic encyclopedia summaries.
- Object knowledge should be reusable across future scenes.
- The same object type should be retrieved from the library before new browsing happens.
- The card should support silhouette blocking, structural plausibility, materials, and style variation.

## Quality priorities

1. silhouette readability
2. believable structure / support logic
3. major form breakdown
4. useful angle notes
5. style adaptation for the current scene

## Language rule

- Procedural content may remain English.
- User-facing labels and examples may include Korean if it improves retrieval or clarity.

## Integration rule

This skill is typically called from `illustrate-skill` after composition blocking and before lighting/value design, then the result is used to refine structural blocking and material planning.
