# Installation

## Option A — use as a workspace repo

This is the simplest route.

1. Clone the private repo.
2. Open Codex with the clone as the working directory.
3. Keep these folders together:
   - `illustrate-skill/`
   - `object-research-skill/`
   - `derived-style-skills/Redjuice_Style_illustrate-skill/`
   - `templates/`
   - `scripts/`
   - `illustration-library/`

## Option B — copy skills to `$CODEX_HOME/skills`

Run:

```powershell
.\scripts\install-codex-skills.ps1
```

Default destination:

```text
%USERPROFILE%\.codex\skills
```

The Redjuice wrapper supports both layouts:

- workspace layout: `derived-style-skills/Redjuice_Style_illustrate-skill` next to `../../illustrate-skill`
- installed Codex layout: `Redjuice_Style_illustrate-skill` next to `../illustrate-skill`

## Required runtime notes

- Python is required for validation scripts.
- Blender is required by the latest render-bound base workflow when a SPEC is intended to reach image generation.
- Keep `templates/`, `scripts/`, and `illustration-library/` in the active workspace for full validator/pipeline behavior.
