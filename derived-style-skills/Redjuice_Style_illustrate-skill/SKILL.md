---
name: Redjuice_Style_illustrate-skill
description: Wrap the base illustrate-skill with a Reference-Redjuice-derived style pack. Use when the user wants restrained luminous dark portraits, cyber-gothic editorial mood, crystalline focal design, ritual/greenhouse/architectural pressure, or information-rich environment-heavy character illustrations while keeping the base staged illustration process intact.
---

# Reference-Redjuice Derived Illustrate Skill

Use this skill as a thin style wrapper over `illustrate-skill`.
Do not replace the base process.
Preserve the base process and bend each stage through the local reference-derived style pack.

## Scope and safety

- This wrapper is **reference-derived**, not a direct living-artist imitation protocol.
- The folder name stays as-is for local organization, but the usable output should remain at the level of:
  - recurring visual traits
  - composition pressure
  - line / plane grammar
  - palette logic
  - environment density rules
- Treat the goal as: **extract what repeatedly appears in the local reference set and make it operational**, while avoiding generic model-default anime polish.

## Priority rule

Treat **Reference-Redjuice-derived fidelity as the top visual priority**.

This means:

1. keep the reference-derived line / plane / focal / environment-pressure logic first
2. forbid drift into other dominant style families even when the prompt asks for secondary treatment
3. treat secondary asks such as medium, setting material, or background treatment as subordinate overlays unless they break the reference-derived read

If a request contains another strong style pull, do **not** average them evenly.
Instead:

- preserve the reference-derived character/mount/render logic
- allow the secondary condition only in the limited area it explicitly owns
- reject any result where the secondary style takes over the whole image

## Default load order

1. Read the base skill context from the first path that exists:
   - workspace layout: `../../illustrate-skill/references/domain_context.md`
   - Codex installed-skill layout: `../illustrate-skill/references/domain_context.md`
2. Read the base process from the first path that exists:
   - workspace layout: `../../illustrate-skill/references/main-process.md`
   - Codex installed-skill layout: `../illustrate-skill/references/main-process.md`
3. Read `references/domain_context.md`.
4. Read `references/style-pack.md`.
5. Read `references/reference-index.md` when you need evidence or a reference-to-rule trace.
6. Read `references/line-plane-intent-analysis.md` when the user asks for deeper line grammar, plane grammar, composition pressure, or anti-generic rendering logic.

## Modes

Keep the base mode structure:

- `SPEC`
- `CRITIQUE`
- `EXTEND`

Use the same gate order and artifact requirements as `illustrate-skill`.

## Core rule

Execute the base illustration process exactly as defined in `illustrate-skill`, then apply the reference-derived biases below:

1. **Step 1 intent** must bias toward sealed emotion, theatrical stillness, engineered beauty under pressure, ritual framing, synthetic ecology, or elegant fracture.
2. **Step 2 composition** must prioritize a strong black/bright mass structure, silhouette clarity, and a pressure frame built from architecture, panes, shards, cables, foliage, thorns, signs, halos, or ceremonial props.
3. **Step 3 value** must reserve the sharpest contrast around the face and especially the eyes, while letting large dark or overexposed planes shape the surrounding pressure.
4. **Step 4 face** must keep emotion restrained and let gaze, iris structure, and tiny mouth shifts carry most of the psychology.
5. **Step 5 line and shape** must separate delicate facial / hair line logic from harder costume / frame / prop logic.
6. **Step 6 color** must stay narrow, with one dominant family and one decisive accent family, never a scattered rainbow.
7. **Step 7 texture** must keep skin quieter than costume/background while allowing grit, bloom, labels, reflection, glass haze, and environmental density elsewhere.
8. **Step 8 final check** must reject outputs that feel pastel-soft, uniformly outlined, background-empty, focal-blurry, or “default polished anime” with no pressure system.
9. If the prompt contains a secondary style instruction, it must be contained rather than allowed to replace the wrapper's core style identity.

## Anti-generic override

This wrapper exists partly to suppress common model-default drift.

Reject or revise when the image starts doing any of the following:

- single isolated character on an underdesigned blur background
- evenly soft rendering across skin, costume, and environment
- highlight bloom everywhere with no focal discipline
- default center crop with no secondary framing pressure
- generic “pretty anime face” without iris structure, lash hierarchy, or restrained expression logic
- random decorative clutter that does not reinforce composition
- accent colors spread evenly instead of gathering around focal triggers
- smooth cloth blobs with no wedge / petal / facet segmentation
- clean empty space where the references repeatedly use architecture, signage, plants, glass, shards, or symbolic framing
- secondary style takeover where the whole image starts reading as some other genre first and the reference-derived pressure system second

## Source-image upgrade handling

For source-image upgrade tasks, treat the original image's existing objects as mandatory style-translation inputs:

- identify them before finalizing Step 2
- prefer researching those recognized source-image objects through Step 2.5 / 2.6 when their structure, material logic, or motif importance affects the upgrade
- preserve the source object's identity while upgrading its line, plane, value, texture, and atmosphere treatment
- do not hide weak object understanding behind glow, blur, or decorative noise

## Working rules

- For render-bound tasks, obey all base-skill artifact and pipeline requirements before any image-generation handoff.
- When a prompt mixes the wrapper with another style/material request, explicitly mark which parts stay reference-derived and which parts may take the secondary treatment.
- For background-bearing scenes, explicitly decide what the background is doing:
  - pressure frame
  - narrative machinery
  - symbolic field
  - atmosphere support
  Empty wallpaper or blur-only backdrop should be treated as failure states for this wrapper.
- If the scene includes believable structures, props, machinery, weapons, vehicles, signage, greenhouse architecture, throne forms, window framing, parasols, cages, aquarium glass, or complex interiors, use `object-research-skill` through the base Step 2.5 / 2.6 handoff.
- For source-image upgrade tasks, do not limit object research only to newly added background elements; first inspect the original image and research the already-present source objects that materially define the upgrade.
- Treat `references/style-pack.md` as the style authority and `references/reference-index.md` as the evidence trail.
- Keep this wrapper style-focused. Do not mutate `illustrate-skill`.

## CRITIQUE focus

In addition to the base critique flow, check these failure modes first:

- face is no longer the emotional anchor
- background is too empty to carry pressure or story
- line weight has collapsed into one uniform treatment
- color accents are too evenly distributed
- the scene reads as generic polished anime rather than a controlled pressure system
- environment details exist but do not reinforce the main figure
- costume and background planes are too soft / rounded / blob-like
- another style family has become the primary read ahead of the reference-derived wrapper

## Outputs

Prefer compact, production-usable outputs that remain base-process compatible:

- one-line reference-derived scene intent
- composition pressure note
- value hierarchy note
- facial psychology note
- line/shape grammar note
- palette/accent note
- texture-density note
- anti-generic conformity verdict
