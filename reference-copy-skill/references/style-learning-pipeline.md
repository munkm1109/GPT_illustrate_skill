# Style Learning Pipeline

Summary: Turn a reference set into reusable drawing behavior, then into compact production prompt language, without replacing the base illustration process.

## Project provenance assumption

Unless the user says otherwise, project reference sets are treated as user-provided AI-generated style-study outputs rather than original artist source images. Under that assumption, direct source imitation is not the primary concern. The main risk is quality drift: overfitting to one image, copying accidental artifacts, or using a style name instead of extracting the visual grammar.

## Pipeline

```text
references
  -> AI_REFERENCE_PROVENANCE_NOTE
  -> PIXEL_PLANE_ANALYSIS_REPORT / PIXEL_PLANE_ANALYSIS_JSON
  -> PIXEL_PLANE_VISUAL_GRAMMAR_SYNTHESIS
  -> REFERENCE_STYLE_OBSERVATION_MATRIX
  -> STYLE_GRAMMAR_EXTRACTION
  -> COPY_RISK_FILTER / anti-overfit transform
  -> STYLE_APPLICATION_BOUNDARY
  -> style-pack.md
  -> AESTHETIC_RENDER_BRIEF
  -> final prompt compiler / aesthetic recovery
```

## 1. AI_REFERENCE_PROVENANCE_NOTE

Record what the reference set is believed to be:

- `user-provided AI style-study outputs`
- `mixed provenance`
- `unknown provenance`
- `original artist/source images` when explicitly stated

This note controls tone and risk handling. For the project default, do not stall on direct-imitation worries; still avoid one-image overfit and exact reference replication.

## 2. PIXEL_PLANE_ANALYSIS_REPORT

Run `pixel-plane-reference-analysis.md` before writing style rules.

Required defaults:

- measure source resolution by default
- do not downscale unless the user explicitly asks for a fast approximation
- for folders over 10 images, split into 10-image batches and merge the JSON reports
- save Markdown and JSON reports in the derived wrapper's `references/` folder or the active `.omx/runs/` analysis folder
- write a visual-grammar synthesis from the measurements before editing `style-pack.md`

The pixel-plane pass measures value planes, bloom percentage, dark-anchor percentage, palette pools, edge density, edge luma, and 3x3 composition grid pressure. These become evidence for the observation matrix.

Do not pass raw metric names, JSON fields, or numeric tables into image prompts. Convert the measurements into natural drawing language.

## 3. REFERENCE_STYLE_OBSERVATION_MATRIX

Use a matrix, not loose commentary. Each row should include:

```text
reference id | observed trait | base step | evidence strength | production meaning
```

Base step mapping:

- Step 1: intent, mood, viewer effect
- Step 2: composition, silhouette, focal placement, pressure frame
- Step 3: value, lighting, mass grouping
- Step 4: face, eyes, expression restraint/exaggeration
- Step 5: line, shape, edge hierarchy
- Step 6: color, accents, palette release
- Step 7: texture, density, surface breakup
- Step 8: final failure checks, anti-generic checks

## 4. STYLE_GRAMMAR_EXTRACTION

Convert repeated observations into reusable rules. Prefer:

- proportion and hierarchy rules
- where detail density is concentrated or suppressed
- how light masses are grouped
- how edges sharpen or dissolve
- how faces/eyes are prioritized
- how accent color is rationed
- how background pressure frames the focal subject

Avoid:

- captioning each image
- copying one reference pose/composition
- relying on artist/game names as the only instruction
- dumping analysis prose into final prompts

## 5. COPY_RISK_FILTER / anti-overfit transform

In this project, this filter is mainly a **quality and originality guard**, not an assumption that the references are original artist works.

Transform:

- exact reference composition -> reusable composition pressure rule
- exact outfit/object -> material/shape tendency unless the user asks for that object
- exact symbols/logos -> abstract motif family
- accidental AI artifacts -> explicit do-not
- one-off detail -> low-confidence note, not a production rule

## 6. STYLE_APPLICATION_BOUNDARY

Declare what the style wrapper may and may not change.

Style may affect:

- lighting mood
- line/shape treatment
- color palette and accent behavior
- texture density
- face/eye rendering grammar
- background pressure and finishing language

Style must not override:

- user scene requirements
- source-image identity constraints
- object-research facts
- camera class
- perspective calculations
- scale-critical measurements
- Blender/blockout evidence
- approved visual guide composite, especially scale markers
- final handoff input stack

## 7. AESTHETIC_RENDER_BRIEF

This is the production-facing style output. It should be compact natural image language.

Good:

```text
sharp variable ink edges, dark pressure-framed city masses, restrained expression, luminous green eyes, warm skin planes, concentrated cyan and red accents, dense texture only around the focal collision
```

Bad:

```text
REFERENCE_STYLE_OBSERVATION_MATRIX passed, Step 5 line grammar high confidence, anti-generic rule active
```

## Completion check

Before generating or refining a wrapper, confirm:

- pixel-plane measurement exists or the missing measurement is explicitly marked provisional
- any folder over 10 images was measured in auditable batches
- observations are separated from inference
- repeated measured and visual traits became style grammar
- one-off traits did not become hard rules
- style boundary says structure locks win
- final style wording is prompt-ready visual language
