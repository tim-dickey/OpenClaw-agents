<#
.SYNOPSIS
    Exports a curated public snapshot from the private golden-source repository.

.DESCRIPTION
    Copies only the public-scope paths (defined in the include list below) into
    a target directory, resets git history, and prepares a clean initial commit
    ready to push to the separate public GitHub repository.

    Run this from the root of the private golden-source repository on a clean,
    up-to-date checkout of main.

.PARAMETER TargetDir
    Path to the output directory for the public snapshot.
    Defaults to a sibling folder named openclaw-agents-public.

.PARAMETER PublicRepoUrl
    Optional HTTPS URL of the public GitHub repository.
    If provided, the script configures the remote and offers to push.

.EXAMPLE
    pwsh scripts/export-public-snapshot.ps1
    pwsh scripts/export-public-snapshot.ps1 -TargetDir C:\repos\openclaw-public -PublicRepoUrl https://github.com/tim-dickey/OpenClaw-agents.git
#>

[CmdletBinding(SupportsShouldProcess)]
param(
    [string]$TargetDir = (&{
        $repoRoot = Split-Path $PSScriptRoot -Parent
        $repoParent = Split-Path $repoRoot -Parent
        Join-Path $repoParent "openclaw-agents-public"
    }),
    [string]$PublicRepoUrl = ""
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

# ---------------------------------------------------------------------------
# Pre-flight: must run from a clean, up-to-date main checkout
# ---------------------------------------------------------------------------
$uncommitted = git status --porcelain
if ($uncommitted) {
    Write-Error "Working tree is dirty. Commit or stash all changes before exporting.`n$uncommitted"
    exit 1
}

$currentBranch = git symbolic-ref --short HEAD
if ($currentBranch -ne "main") {
    Write-Error "Must be on main branch before exporting. Currently on: $currentBranch"
    exit 1
}

Write-Host "Pre-flight passed: clean checkout of main." -ForegroundColor Green

# ---------------------------------------------------------------------------
# Public scope: paths copied verbatim into the snapshot
# ---------------------------------------------------------------------------
$includePaths = @(
    "README.md",
    "CONTRIBUTING.md",
    "CODE_OF_CONDUCT.md",
    "LICENSE",
    "ROADMAP.md",
    ".gitignore",
    ".markdownlint.json",
    ".markdownlintignore",
    "package.json",
    "package-lock.json",
    "OpenClaw agent project.png",
    "Agent team.png",
    "Agent actions.png",
    "agents",
    "sub-agents",
    "docs",
    "evals",
    "tests",
    "scripts",
    ".github"
)

# ---------------------------------------------------------------------------
# Paths explicitly excluded even if present under an included parent
# ---------------------------------------------------------------------------
$excludePatterns = @(
    # Infrastructure artefacts
    ".github/scripts/__pycache__",
    ".github/workflows/sync-to-public.yml",
    "docs/public-repo-publish-prep-steps-1-3.md",
    "docs/confidence-layer-rollout-status.md",
    "GOLDEN-SOURCE*.md",
    ".syncignore",

    # IP-sensitive agents and sub-agents: JARVIS name carries Marvel/Disney associations
    "agents/professional/jarvis",
    "sub-agents/communication/jarvis-ops-inbox",
    "sub-agents/developer/jarvis-dev-coder",
    "sub-agents/developer/jarvis-dev-pm",
    "sub-agents/developer/jarvis-dev-reviewer",
    "sub-agents/productivity/jarvis-ops-briefing",
    "sub-agents/productivity/jarvis-ops-calendar",
    "evals/agents/jarvis",
    "evals/sub-agents/jarvis-dev-coder",
    "evals/sub-agents/jarvis-dev-pm",
    "evals/sub-agents/jarvis-dev-reviewer",
    "evals/sub-agents/jarvis-ops-briefing",
    "evals/sub-agents/jarvis-ops-calendar",
    "evals/sub-agents/jarvis-ops-inbox",
    "tests/cases/agents/jarvis",
    "tests/cases/sub-agents/jarvis-ops-briefing"
)

# ---------------------------------------------------------------------------
# Prepare target directory
# ---------------------------------------------------------------------------
if (Test-Path $TargetDir) {
    Write-Host "Removing existing target directory: $TargetDir"
    if ($PSCmdlet.ShouldProcess($TargetDir, "Remove directory")) {
        Remove-Item -Recurse -Force $TargetDir
    }
}
New-Item -ItemType Directory -Path $TargetDir | Out-Null
Write-Host "Created target directory: $TargetDir"

# ---------------------------------------------------------------------------
# Copy public-scope paths
# ---------------------------------------------------------------------------
$sourceRoot = (Get-Location).Path

foreach ($item in $includePaths) {
    $src = Join-Path $sourceRoot $item
    $dst = Join-Path $TargetDir $item

    if (-not (Test-Path $src)) {
        Write-Warning "Skipping missing path: $item"
        continue
    }

    $dstParent = Split-Path $dst -Parent
    if (-not (Test-Path $dstParent)) {
        New-Item -ItemType Directory -Path $dstParent -Force | Out-Null
    }

    Copy-Item -Recurse -Force $src $dst
    Write-Host "  Copied: $item"
}

# ---------------------------------------------------------------------------
# Apply exclusions over the copied tree
# ---------------------------------------------------------------------------
foreach ($pattern in $excludePatterns) {
    $target = Join-Path $TargetDir $pattern
    if (Test-Path $target) {
        Remove-Item -Recurse -Force $target
        Write-Host "  Excluded: $pattern" -ForegroundColor Yellow
    }
}

# Remove any __pycache__ directories that leaked through
Get-ChildItem -Path $TargetDir -Filter "__pycache__" -Recurse -Directory |
    ForEach-Object { Remove-Item -Recurse -Force $_.FullName; Write-Host "  Removed cache: $($_.FullName)" -ForegroundColor Yellow }

# ---------------------------------------------------------------------------
# Verify CI is not expecting private secrets
# ---------------------------------------------------------------------------
$workflowDir = Join-Path $TargetDir ".github/workflows"
if (Test-Path $workflowDir) {
    $secretRefs = Select-String -Path (Join-Path $workflowDir "*.yml") -Pattern "secrets." -SimpleMatch
    if ($secretRefs) {
        Write-Warning "Workflow files reference secrets. Review before pushing to the public repo:"
        $secretRefs | ForEach-Object { Write-Warning "  $($_.Filename):$($_.LineNumber)  $($_.Line.Trim())" }
    }
}

# ---------------------------------------------------------------------------
# Initialise fresh git history in the snapshot
# ---------------------------------------------------------------------------
Push-Location $TargetDir
try {
    git init -b main | Out-Null

    # Ensure a local git identity exists so commit does not fail in fresh environments
    $gitUserName  = git config user.name 2>$null
    $gitUserEmail = git config user.email 2>$null
    if (-not $gitUserName) {
        git config user.name "Snapshot Export"
        Write-Host "Configured local git user.name for snapshot commit." -ForegroundColor Yellow
    }
    if (-not $gitUserEmail) {
        git config user.email "snapshot-export@noreply.local"
        Write-Host "Configured local git user.email for snapshot commit." -ForegroundColor Yellow
    }
    git add .
    git commit -m "Initial public release" | Out-Null
    Write-Host ""
    Write-Host "Snapshot committed with fresh history." -ForegroundColor Green
    git log --oneline -3

    if ($PublicRepoUrl) {
        git remote add origin $PublicRepoUrl
        Write-Host ""
        Write-Host "Remote configured: $PublicRepoUrl"
        Write-Host "Push when ready:"
        Write-Host "  cd `"$TargetDir`""
        Write-Host "  git push -u origin main"
        Write-Host "  git tag v1.0.0 -a -m 'Initial public release'"
        Write-Host "  git push origin v1.0.0"
    }
} finally {
    Pop-Location
}

# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------
$fileCount = (Get-ChildItem -Path $TargetDir -Recurse -File).Count
Write-Host ""
Write-Host "Export complete." -ForegroundColor Green
Write-Host "  Source:     $sourceRoot (main)"
Write-Host "  Target:     $TargetDir"
Write-Host "  Files:      $fileCount"
Write-Host ""
Write-Host "Next steps:"
Write-Host "  1. Review $TargetDir manually before pushing."
Write-Host "  2. Confirm no sensitive content remains."
Write-Host "  3. Push to the public repository and create the first release tag."
