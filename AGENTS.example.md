# Project routing example for a workspace using this private package

When the user asks for illustration generation, scene design, image prompt planning, or “그려줘”, use `illustrate-skill` first rather than jumping directly to image generation.

For Redjuice-style requests, use `derived-style-skills/Redjuice_Style_illustrate-skill` as a thin wrapper over the base `illustrate-skill` process.

For render-bound SPEC runs:

1. Create a spec from `templates/illustrate-spec-template.md`.
2. Create a theory-read proof from `templates/theory-read-proof-template.md`.
3. Complete Step 1 through Step 8 in order.
4. Use `object-research-skill` when objects, anatomy, hands, props, architecture, vehicles, signage, machinery, or source-image objects need believable form.
5. Validate with `python scripts/validate_illustrate_spec.py <spec-path> --strict-object-research`.
6. Run `python scripts/run_illustrate_pipeline.py <spec-path> --strict-object-research` before image generation.
