Installation
============

1. Adding the Library to Your Project

'pypc_utils' is stored as a GitHub release.

The recommended way to install it is via Poetry:

    poetry add git+https://github.com/<your-org-or-username>/pypc_utils.git@<tag-or-branch>

where <tag-or-branch> is something like 'main' or 'v0.1.0'.

2. Configure pyproject.toml

Poetry automatically updates your pyproject.toml when you use poetry add. Here's what it will look like:

For a PyPI Package
 
    [tool.poetry.dependencies]
    python = "^3.11"
    pypc_utils = "^1.0.0"

For a GitHub Release

    [tool.poetry.dependencies]
    python = "^3.11"
    pypc_utils = { git = "https://github.com/example/pypc_utils.git", tag = "v1.0.0" }

Or, if you use a branch:

    [tool.poetry.dependencies]
    python = "^3.11"
    pypc_utils = { git = "https://github.com/example/pypc_utils.git", branch = "main" }
