<#
.SYNOPSIS
Publish pypc_utils to GitHub Packages using Poetry.

.NOTES
- You must set the following environment variables:
  GH_OWNER, GH_REPO, GH_USERNAME (optional, defaults to GH_OWNER), GH_PAT
- Example: $Env:GH_PAT = "<your_token>"
#>

$ErrorActionPreference = "Stop"

$OWNER  = if ($env:GH_OWNER) { $env:GH_OWNER } else { "TheBoojum" }
$REPO   = if ($env:GH_REPO)  { $env:GH_REPO }  else { "pypc_utils" }
$USERNAME = if ($env:GH_USERNAME) { $env:GH_USERNAME } else { $OWNER }
$PAT    = $env:GH_PAT

if (-not $PAT) {
    Write-Error "GH_PAT is not set. Export it as an environment variable."
    exit 1
}

$REGISTRY = "https://pypi.pkg.github.com/$OWNER/$REPO"

# Build
poetry build

# Configure credentials
poetry config http-basic.github $USERNAME $PAT

# Publish
poetry publish -r github

Write-Host "Published to GitHub Packages: $REGISTRY"