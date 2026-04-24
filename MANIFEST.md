# Distribution Manifest

Built: 2026-04-25 Asia/Seoul

## Included

- Base workflow: `illustrate-skill/`
- Dependency: `object-research-skill/`
- Wrapped style: `derived-style-skills/Redjuice_Style_illustrate-skill/`
- Validator/pipeline assets: `templates/`, `scripts/`
- Local object cards: `illustration-library/`
- Docs: `docs/`

## Explicitly excluded

- `Reference-Redjuice/` raw JPG files
- `Reference-Huke/`, `Reference-Honkai/`
- Huke/Honkai derived wrappers
- `.omx/` private run state and generated specs
- `output/`, previous `dist/` bundles, caches

## Current base mechanism notes

- Render-bound SPEC runs require staged artifacts.
- Theory-read proof is required.
- Strict object-research validation is supported.
- Blender blockout hard-route is part of the latest base workflow for render-bound image generation.
- Redjuice wrapper is a thin style bias layer; it must not replace the base process.
