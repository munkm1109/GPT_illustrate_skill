# Pixel-Plane Reference Analysis

Summary: Pixel-plane analysis is the official first-pass measurement method for reference-derived illustration style analysis in this workspace.

Use it before writing or refining any derived style wrapper from reference images or folders. It turns reference pixels into reusable evidence for value, bloom, palette, edge density, dark-anchor placement, and coarse composition pressure. It does not replace vision judgment; it gives the visual grammar extraction a measured floor.

## Required measurement path

1. Inspect the reference folder and count supported images.
2. Measure at source resolution by default. Do not lower resolution unless the user explicitly asks for a fast approximation.
3. For folders larger than 10 images, split analysis into deterministic batches of 10 images:
   - batch 0: `--offset 0 --limit 10`
   - batch 1: `--offset 10 --limit 10`
   - continue until all images are measured
4. Merge batch JSON reports into one full-folder report.
5. Write both Markdown and JSON reports into the derived wrapper's `references/` folder or the active `.omx/runs/` analysis folder.
6. Translate the report into a human visual-grammar synthesis before editing `style-pack.md`.

## Scripts

Folder or batch measurement:

```powershell
python reference-copy-skill\scripts\measure_reference_folder_pixels.py <reference-folder> --out-md <out>.md --out-json <out>.json
```

Batch example:

```powershell
python reference-copy-skill\scripts\measure_reference_folder_pixels.py <reference-folder> --offset 0 --limit 10 --out-md <slug>-pixel-plane-batch-00-09.md --out-json <slug>-pixel-plane-batch-00-09.json
```

Merge batches:

```powershell
python reference-copy-skill\scripts\merge_reference_folder_pixel_batches.py <batch-json>... --out-md <slug>-pixel-plane-full-analysis.md --out-json <slug>-pixel-plane-full-analysis.json
```

## Measurement lanes

Record these lanes as evidence, then map them to the base illustration steps:

- Value planes: luma percentiles, clipped bloom, highlight plane, light-mid plane, mid-shadow plane, dark-anchor percentage.
- Palette pools: k-means palette clusters and quantized color frequency.
- Edge behavior: edge density, edge strength, edge luma.
- 3x3 grid signature: where brightness, dark anchors, saturation, and edge density concentrate.
- Exemplars: highest bloom, highest dark anchors, highest edge density, highest saturation, highest warm/cool pressure.

## Translation rule

Pixel measurements become drawing grammar, not raw prompt numbers.

Use the metrics to infer:

- where the style places high-value light planes
- how much bloom can exist before structure is lost
- whether dark marks are compact anchors or broad shadow masses
- where the composition places focal pressure and edge density
- how restrained or saturated the palette release is
- whether linework is local-color, black, soft, hard, sparse, or dense

Do not write metric field names or numeric tables into final image-generation prompts. Convert them into natural visual language such as `large near-white backlight planes`, `compact chromatic eyelid anchors`, `low edge density outside the focal face`, or `dense dark marks only around hair and costume seams`.

## Evidence discipline

- Treat repeated measured traits across multiple references as strong evidence.
- Treat one-off measured extremes as exemplars, not global rules, unless the user explicitly chooses that lane.
- If the pixel-plane report conflicts with obvious visual inspection, record both and explain the conflict.
- Never infer identity, character design, exact pose, or exact costume copying from pixel-plane metrics alone.
- Never turn a measured ratio into a universal hard lock without a separate segmentation or manual vision pass.

## Style-pack integration

Every new or refined derived style pack should include:

- `Evidence Basis`: links to the pixel-plane Markdown/JSON report and the visual-grammar synthesis.
- `Diagnostic Pixel Bands`: concise measured ranges used for drift checks, not final prompt wording.
- `Official Mapping`: how measurements map to composition, value, face/eye, line/shape, color, texture, and anti-drift rules.
- `Aesthetic Render Brief`: prompt-ready natural language compiled from the measured and visual evidence.
- `Style Application Boundary`: structure, camera, perspective, object research, scale, hands, source identity, and visual-guide locks outrank style.

## Failure triggers

Redo or refine analysis if:

- only image captions were written and no pixel-plane report exists
- analysis downscaled images without user approval
- a folder over 10 images was analyzed as one opaque pass when batching would improve auditability
- style rules were copied from one exemplar instead of repeated measured traits
- raw metric names leaked into image prompts
- final style-pack rules contradict structural locks from `illustrate-skill`
