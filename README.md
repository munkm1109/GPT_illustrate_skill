# Private Illustrate Skill Distribution

Private repository for the current `illustrate-skill` workflow and its required companion skills/assets.

This package intentionally excludes all derived style wrappers. Reference-derived style learning is still supported through `reference-copy-skill`, but no generated style pack or artist-specific wrapper is bundled here.

## Included Scope

- `illustrate-skill/` - base theory-first illustration workflow.
- `reference-copy-skill/` - reference-folder analysis and style-skill builder, including pixel-plane first-pass analysis.
- `object-research-skill/` - required companion for Step 2.5 / Step 2.6 object, anatomy, and scene-structure gates.
- `templates/` - SPEC, theory-read proof, object-research, post-image verdict, and repair templates.
- `scripts/` - validators, pipeline gate, theory-read logger, object-research logger, and visual-guide helpers.
- `illustration-library/` - local object cards and scene recipes used by object research.
- `docs/` - usage guide and developer overview.

## Excluded On Purpose

- `derived-style-skills/` and all generated style wrappers.
- Raw `Reference-*` image folders.
- `.omx/` run history, generated outputs, zips, caches, and personal work artifacts.
- `Char_pack/`, `spec-builders/`, and one-off local test runs.

## Reference Analysis

`reference-copy-skill` uses pixel-plane analysis as the official first pass for reference-folder analysis. It measures full-resolution references by default, batches folders larger than 10 images, merges batch JSON reports, then translates the measured value, bloom, palette, edge, grid, and density evidence into reusable visual grammar.

## Quick Use Inside A Cloned Workspace

1. Clone the private repo.
2. Open Codex in the cloned folder.
3. Use `illustrate-skill` first for image-bound requests.
4. Use `reference-copy-skill` when creating or refining a reference-derived style skill.
5. Validate render-bound specs before image generation:

```powershell
python scripts/validate_illustrate_spec.py .omx/runs/<slug>-spec.md --strict-object-research
python scripts/run_illustrate_pipeline.py .omx/runs/<slug>-spec.md --strict-object-research --emit-image-prompt .omx/runs/<slug>-pipeline-prompt.txt
```

## Optional Install Into Codex Skills

From the repo root:

```powershell
.\scripts\install-codex-skills.ps1
```

This copies `illustrate-skill`, `reference-copy-skill`, and `object-research-skill` into `$env:USERPROFILE\.codex\skills` by default. Keep this repo as the active workspace, or copy `templates/`, `scripts/`, and `illustration-library/` into any workspace where you want the full validator/pipeline mechanism to run.
