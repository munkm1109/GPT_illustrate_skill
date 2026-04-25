# Invocation Routing

Use `reference-copy-skill` when the user is not trying to plan one picture, but instead wants to **manufacture a new reusable style wrapper** from references.

## Route here when

- the user provides a reference folder and asks for a new style skill
- the user wants a new derivative `illustrate-skill` variant
- the user wants to strengthen an existing wrapper using added references
- `illustrate-skill` receives a request that is actually about style-wrapper generation rather than scene design

## Do not route here when

- the user only wants one scene designed
- the user only wants object research
- the user wants to critique one generated image without creating a new wrapper

## Handoff note

If `illustrate-skill` detects that the request is fundamentally:

> “Analyze these references and make me a new style-specific illustration skill.”

then `illustrate-skill` should stop trying to treat the job as `SPEC` and hand off to `reference-copy-skill`.
