# Private Distribution Guide

## Goal

Share only the latest base `illustrate-skill` mechanism and the Reference-Redjuice-derived style wrapper with selected friends.

## Recommended GitHub setup

1. Create a **private** repository, for example `illustrate-skill-redjuice-private`.
2. Push this local repository to that private remote.
3. Add friends as collaborators with the minimum permission they need, usually read-only.
4. Do not enable public forks or public Pages for this repo.
5. If a friend leaves the access group, remove their collaborator access and rotate any deploy keys/tokens.

## Commands if GitHub CLI is installed

```powershell
# from this repo root
gh auth login
gh repo create illustrate-skill-redjuice-private --private --source . --remote origin --push

# invite a GitHub user with read-only pull permission
gh api -X PUT repos/<OWNER>/illustrate-skill-redjuice-private/collaborators/<FRIEND_GITHUB_USERNAME> -f permission=pull
```

`gh` is not bundled with this repo. Install it separately if you want these commands.

## Manual GitHub setup without GitHub CLI

```powershell
git remote add origin https://github.com/<OWNER>/illustrate-skill-redjuice-private.git
git branch -M main
git push -u origin main
```

Then use GitHub UI:

`Repository -> Settings -> Collaborators and teams -> Add people`

## About “only people with my link”

For private repositories, a plain URL is not enough. The viewer must be authenticated and granted access. This is better than a public unlisted link because random people cannot clone it just by guessing or receiving the URL.

## License boundary

This package is all-rights-reserved private material. Friends may use it personally only if you grant access. They should not redistribute, mirror, publish, or train/share it externally without your explicit permission.
