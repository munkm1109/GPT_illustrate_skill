# Installation

## Option A - Use As A Workspace Repo

This is the simplest route.

1. Clone the private repo.
2. Open Codex with the clone as the working directory.
3. Keep these folders together:
   - `illustrate-skill/`
   - `reference-copy-skill/`
   - `object-research-skill/`
   - `templates/`
   - `scripts/`
   - `illustration-library/`

## Option B - Copy Skills To `$CODEX_HOME/skills`

Run:

```powershell
.\scripts\install-codex-skills.ps1
```

Default destination:

```text
%USERPROFILE%\.codex\skills
```

The installer copies only the three skill folders:

- `illustrate-skill`
- `reference-copy-skill`
- `object-research-skill`

No derived style wrapper is installed by this package.

## Required Runtime Notes

- Python is required for validation scripts.
- Blender is optional and only used when an approved render-bound route needs structural blockout/composite evidence.
- Keep `templates/`, `scripts/`, and `illustration-library/` in the active workspace for full validator/pipeline behavior.
