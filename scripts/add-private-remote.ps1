param(
    [Parameter(Mandatory=$true)]
    [string]$RemoteUrl,
    [string]$RemoteName = 'origin'
)

$ErrorActionPreference = 'Stop'
$RepoRoot = Resolve-Path (Join-Path $PSScriptRoot '..')
Push-Location $RepoRoot
try {
    $inside = git rev-parse --is-inside-work-tree
    if ($inside -ne 'true') { throw 'Not inside a git repository.' }

    $existing = git remote get-url $RemoteName 2>$null
    if ($LASTEXITCODE -eq 0 -and $existing) {
        git remote set-url $RemoteName $RemoteUrl
        Write-Host "Updated remote $RemoteName -> $RemoteUrl"
    } else {
        git remote add $RemoteName $RemoteUrl
        Write-Host "Added remote $RemoteName -> $RemoteUrl"
    }

    git branch -M main
    Write-Host "Ready. Push with: git push -u $RemoteName main --tags"
    Write-Host "Make sure the remote repository is PRIVATE before pushing."
}
finally {
    Pop-Location
}
