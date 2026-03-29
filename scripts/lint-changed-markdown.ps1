$ErrorActionPreference = "Stop"

$baseRef = if ($env:GITHUB_BASE_REF) {
  "origin/$($env:GITHUB_BASE_REF)...HEAD"
} else {
  git rev-parse --verify HEAD~1 >$null 2>&1
  if ($LASTEXITCODE -eq 0) {
    "HEAD~1...HEAD"
  } else {
    "HEAD"
  }
}
$changed = @(git diff --name-only $baseRef -- "*.md") | Where-Object { $_ -and ($_ -notlike "REFERENCE/*") }

if (-not $changed -or $changed.Count -eq 0) {
  Write-Host "No changed markdown files to lint."
  exit 0
}

Write-Host "Linting changed markdown files:"
$changed | ForEach-Object { Write-Host " - $_" }

npx --yes markdownlint-cli2 @changed
