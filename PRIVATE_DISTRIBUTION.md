# Private Distribution Guide

## Goal

Share the current base `illustrate-skill` mechanism, `reference-copy-skill` with pixel-plane reference analysis, and `object-research-skill` with selected collaborators.

Derived style wrappers and raw reference image folders are intentionally excluded.

## Recommended GitHub Setup

1. Create or use a private repository, for example `GPT_illustrate_skill`.
2. Push this local repository to that private remote.
3. Add collaborators with the minimum permission they need, usually read-only.
4. Do not enable public forks or public Pages for this repo.
5. If a collaborator leaves the access group, remove their collaborator access and rotate any deploy keys/tokens.

## Commands If GitHub CLI Is Installed

```powershell
# from this repo root
gh auth login
gh repo create GPT_illustrate_skill --private --source . --remote origin --push

# invite a GitHub user with read-only pull permission
gh api -X PUT repos/<OWNER>/GPT_illustrate_skill/collaborators/<FRIEND_GITHUB_USERNAME> -f permission=pull
```

`gh` is not bundled with this repo. Install it separately if you want these commands.

## Manual GitHub Setup Without GitHub CLI

```powershell
git remote add origin https://github.com/<OWNER>/GPT_illustrate_skill.git
git branch -M main
git push -u origin main
```

Then use GitHub UI:

`Repository -> Settings -> Collaborators and teams -> Add people`

## About Private Links

For private repositories, a plain URL is not enough. The viewer must be authenticated and granted access. This is better than a public unlisted link because random people cannot clone it just by guessing or receiving the URL.

## License Boundary

This package is all-rights-reserved private material. Collaborators may use it personally only if you grant access. They should not redistribute, mirror, publish, or train/share it externally without your explicit permission.
