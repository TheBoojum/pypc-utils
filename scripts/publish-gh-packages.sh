#!/usr/bin/env bash

# Script for Linux/ macOS
# Make executable with chmod +x

set -euo pipefail

# Config (fill these or export env vars)
OWNER="${GH_OWNER:-OWNER}"
REPO="${GH_REPO:-REPO}"
GH_USERNAME="${GH_USERNAME:-${OWNER}}"
GH_PAT="${GH_PAT:-}"

# GitHub Packages registry URL (for reference)
REGISTRY="https://pypi.pkg.github.com/${OWNER}/${REPO}"

# 0) Preflight
if [ -z "$GH_PAT" ]; then
  echo "ERROR: GH_PAT is not set. Export it (e.g., export GH_PAT=...)"
  exit 1
fi

# 1) Build the distribution
poetry build

# 2) Configure Poetry credentials for the GitHub registry
poetry config http-basic.github "$GH_USERNAME" "$GH_PAT"

# 3) Publish to GitHub Packages
poetry publish -r github --build

echo "Published to GitHub Packages: ${REGISTRY}"