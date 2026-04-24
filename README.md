# Private Illustrate Skill + Redjuice Wrapper

Private friend-share repository for the latest local `illustrate-skill` mechanism plus the Reference-Redjuice-derived wrapper.

## Included scope

- `illustrate-skill/` — latest base theory-first illustration workflow.
- `object-research-skill/` — required companion for Step 2.5 / Step 2.6 object research gates.
- `derived-style-skills/Redjuice_Style_illustrate-skill/` — Redjuice-reference-derived thin style wrapper over the base workflow.
- `templates/` — SPEC, theory-read proof, object-research artifact, and invocation-log templates.
- `scripts/` — validators, pipeline gate, theory-read logger, and object-research invocation logger.
- `illustration-library/` — local object cards and scene recipes used by object research.
- `docs/` — usage guide and developer overview.

## Excluded on purpose

- Raw `Reference-Redjuice/` JPG files.
- Other derived wrappers such as Honkai or Huke.
- `.omx/` run history, generated outputs, zips, caches, and personal work artifacts.

## Privacy / access model

This repository is meant to be pushed to a **private Git remote**. Do not make it public.

Important limitation: Git cannot technically stop an authorized recipient from copying files after they clone. Private Git hosting only controls who can access the remote. Use account-based collaborator invites, not a public “secret URL”, if you want only chosen people to clone it.

See `PRIVATE_DISTRIBUTION.md` before pushing.

## Quick use inside the cloned workspace

1. Clone the private repo.
2. Open Codex in the cloned folder.
3. For normal workflow, use `illustrate-skill` first for image-bound requests.
4. For the Redjuice wrapper, route to `derived-style-skills/Redjuice_Style_illustrate-skill` and keep the base `illustrate-skill` process intact.
5. Validate render-bound specs before image generation:

```powershell
python scripts/validate_illustrate_spec.py .omx/runs/<slug>-spec.md --strict-object-research
python scripts/run_illustrate_pipeline.py .omx/runs/<slug>-spec.md --strict-object-research --emit-image-prompt .omx/runs/<slug>-pipeline-prompt.txt
```

## Optional install into Codex skills

From the repo root:

```powershell
.\scripts\install-codex-skills.ps1
```

This copies the three skill folders into `$env:USERPROFILE\.codex\skills` by default. Keep this repo as the working folder, or copy `templates/`, `scripts/`, and `illustration-library/` into any workspace where you want the full validator/pipeline mechanism to run.
