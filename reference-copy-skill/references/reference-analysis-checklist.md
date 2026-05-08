# Reference Analysis Checklist

Summary: Use this checklist to turn a reference set into a coherent style pack rather than a pile of disconnected observations.

## Analyze the set in this order

1. What is the provenance note? For this project, assume user-provided AI style-study outputs unless stated otherwise.
2. Has pixel-plane analysis been run at source resolution? If there are more than 10 images, were 10-image batches measured and merged?
3. What do the pixel-plane reports say about value planes, bloom, dark anchors, palette pools, edge density, and 3x3 composition pressure?
4. What emotion does the set repeatedly aim for?
5. How does the set handle composition, pressure framing, silhouette, and focal placement?
6. What value, light grouping, and dark/light mass patterns recur?
7. How are faces, eyes, and expression intensity handled?
8. What line, edge, and shape language dominates?
9. How is color restricted, released, or accented?
10. How is texture and density controlled?
11. What motifs repeat often enough to count as style grammar?
12. Which repeated measured and visual observations become production rules?
13. What should never appear if this wrapper is being respected?
14. What generic model-default habits would weaken this reference set?
15. What one-off details, metric outliers, or AI artifacts must be filtered out instead of learned?
16. What is the final compact `AESTHETIC_RENDER_BRIEF`?
17. What structure locks must the style wrapper never override?

## Evidence rule

When extracting style rules:

- one-off detail = weak evidence
- repeated trait across multiple references = strong evidence
- repeated trait that appears across different subjects/scenes = strongest evidence
- repeated trait supported by pixel-plane measurement and manual visual inspection = production-grade evidence
- metric outlier in one image = exemplar lane, not a global rule

## Pixel-plane rule

Pixel-plane analysis is mandatory for reference-derived style analysis unless the reference files are unavailable or unreadable. If unavailable, mark the style analysis as provisional.

Use the report as evidence for:

- value and bloom hierarchy
- compact versus broad dark-anchor behavior
- palette pool and accent release
- edge density and local line hardness
- 3x3 composition pressure

Do not paste raw metric names or numeric tables into image prompts.

## Separation rule

Always separate:

- direct observation
- inferred preference
- production rule
- anti-generic / anti-overfit rule

## Boundary rule

Style applies after the base scene structure is understood. It must not override:

- scene requirements
- source-image identity
- object research
- camera class
- perspective calculation
- scale-critical measurements
- Blender/blockout guide
- approved visual guide composite scale markers

## Output rule

The final style pack should read like:

- a reusable drawing behavior system
- a prompt-ready aesthetic render brief

not like:

- a review essay
- a fan description
- an image caption list
- raw validator/schema prose
