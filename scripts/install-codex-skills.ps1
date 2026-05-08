param(
    [string]$CodexSkillsDir = $(if ($env:CODEX_HOME) { Join-Path $env:CODEX_HOME 'skills' } else { Join-Path $env:USERPROFILE '.codex\skills' })
)

$ErrorActionPreference = 'Stop'
$RepoRoot = Resolve-Path (Join-Path $PSScriptRoot '..')
$DestRoot = $CodexSkillsDir
New-Item -ItemType Directory -Force -Path $DestRoot | Out-Null

$Skills = @(
    @{ Source = 'illustrate-skill'; Dest = 'illustrate-skill' },
    @{ Source = 'reference-copy-skill'; Dest = 'reference-copy-skill' },
    @{ Source = 'object-research-skill'; Dest = 'object-research-skill' }
)

foreach ($skill in $Skills) {
    $src = Join-Path $RepoRoot $skill.Source
    $dst = Join-Path $DestRoot $skill.Dest
    if (-not (Test-Path $src)) { throw "Missing source skill: $src" }
    if (Test-Path $dst) { Remove-Item -LiteralPath $dst -Recurse -Force }
    Copy-Item -LiteralPath $src -Destination $dst -Recurse -Force
    Write-Host "Installed $($skill.Dest) -> $dst"
}

Write-Host "Done. No derived style wrappers were installed. Keep this repo's templates/, scripts/, and illustration-library/ in workspaces that need validation/pipeline gates."
