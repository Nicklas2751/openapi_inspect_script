# AGENTS.md

[![CI](https://github.com/Nicklas2751/openapi_inspect_script/actions/workflows/test.yml/badge.svg)](https://github.com/Nicklas2751/openapi_inspect_script/actions/workflows/test.yml)
[![Release](https://github.com/Nicklas2751/openapi_inspect_script/actions/workflows/release.yml/badge.svg)](https://github.com/Nicklas2751/openapi_inspect_script/actions/workflows/release.yml)
[![Docker Pulls](https://img.shields.io/badge/docker-pulls-blue?logo=docker)](https://ghcr.io/nicklas2751/openapi_inspect_script)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)

> **Repository Agentic Guide**  
> This file is for both agentic coding agents and humans contributing to maintain high quality and consistency in this repo. Please read before contributing changes or running automation.

---

## 1. Build, Lint, and Test Commands

### Setup
- Python version: **3.8+** (tested on higher versions, e.g. 3.14)
- Main dependency: **pyyaml**

**Recommended installation:**
```sh
python3 -m venv .venv
source .venv/bin/activate
pip install pyyaml
```

### Linting
- No explicit linter config is checked in.
- Use default `flake8` and `pylint` for basic code hygiene.
- **Ad-hoc commands:**
  - `pip install flake8 pylint`
  - `flake8 openapi_inspect.py`
  - `pylint openapi_inspect.py`

### Formatting
- No formatter configuration (such as Black, isort) is checked in.
- For consistency, run (with defaults):
  - `pip install black isort`
  - `black openapi_inspect.py`
  - `isort openapi_inspect.py`

  > **Note:** Formatting is currently not enforced; do not reformat large sections unless necessary – prefer minimal diffs.

### Testing
- There are currently **_no formal tests_** (no tests/ directory, no pytest/unittest structure).
- Manual testing is performed by running the script against sample OpenAPI YAMLs.
- Sample manual test:
  ```sh
  python openapi_inspect.py openapi.yaml paths
  python openapi_inspect.py openapi.yaml path /users/{id} get
  python openapi_inspect.py openapi.yaml schema User
  ```
- **Adding tests:**
  - If you add formal tests, prefer `pytest` and put tests in a `tests/` directory.
  - Minimal test setup example:
    ```sh
    pip install pytest
    pytest
    ```

---
## 2. Code Style Guidelines

_All code should align with the following conventions for imports, formatting, typing, naming, and more._

### Imports
- Standard library imports (argparse, sys, etc.) come first
- Third-party (PyYAML) imports go below
- No relative imports are currently used or needed
- Avoid wildcard (`*`) imports – import only what you need

### Formatting & Layout
- Use 4 spaces per indentation (PEP8 default)
- Max line length: 90 (for readability)
- Separate top-level functions with 2 blank lines
- Use single blank lines between logical code blocks
- Inline comments are preceded by two spaces; block comments get a single `#` at start of line

### Typing
- This repo follows a minimalist (non-annotated) style.
- If you add new functions, **add type hints where practical** (PEP484/PEP526 style)
- Use type hints on all public APIs if/when adding new files

### Naming Conventions
- functions: `snake_case`
- variables: `snake_case`
- constants: `UPPER_SNAKE_CASE`
- classes: `CamelCase`
- Arguments should be meaningful, avoid single-letter names except for `f`, `x`, `y`, or standard iterator patterns

### Functions
- Prefer small, simple functions
- Each function should have a clear single responsibility
- Top-level docstrings are encouraged (multi-line strings at file/function top)
- CLI entry point is always guarded by `if __name__ == '__main__'` block

### Error Handling
- Use `sys.exit(1)` for terminal error exits in the CLI (see existing patterns)
- Print informative error messages on failure
- Do not swallow exceptions silently; handle or display them
- Use `try`/`except` only where necessary
- Fail loudly and clearly for invalid input or missing files

### Documentation
- Each function should have a docstring if nontrivial
- Keep README up to date with all user-facing CLI changes
- Update this AGENTS.md with any new rules or tool configuration

### Automation & Agents
- Before running code transformers or agents, ensure the venv is active and dependencies are up to date
- Do not reformat or refactor working code without human/code review
- Automatons can assume all code is Python unless new files state otherwise
- Do not introduce new dependencies without updating installation guidance, and document any new tools
- Seek human confirmation before deleting files or making destructive changes

---

## 3. Copilot/Cursor/Agentic Rules
- **No Copilot or Cursor rules are present.** If added, merge/highlight them here and cite the authoritative file/location.

---

## 4. Contribution Pro Tips
- Prefer small, focused PRs.
- Always check for breaking CLI/API changes
- Test against real-world OpenAPI 3.x YAMLs if available
- Be explicit about limitations and avoid feature creep
- Always include _why_ a change was made in PR descriptions and commit messages

---

## 5. Updating This File
Whenever you add test infrastructure, editor configs, agent instructions, etc., **update this file** with new rules, sample commands, and rationale. Treat this as the canonical source for contributors and coding AIs.

---

## Docker

This project can be built and run as a Docker container. The Dockerfile is included in the repository.

### Build & Run

```sh
docker build -t openapi-inspect .
```

To analyze an OpenAPI YAML file, mount it into the container filesystem. Example:

```sh
docker run --rm -v "$PWD/openapi.yaml:/app/openapi.yaml" openapi-inspect /app/openapi.yaml paths
```

The script can be executed in the container with any arguments. The OpenAPI file is provided via volume mount.

### GitHub Packages

The Docker image is published automatically via GitHub Actions to GitHub Packages:

- Repository: https://github.com/Nicklas2751/openapi_inspect_script
- Image: `ghcr.io/nicklas2751/openapi_inspect_script:<tag>` (and `latest`)

Example to pull the image:

```sh
docker pull ghcr.io/nicklas2751/openapi_inspect_script:latest
```

> Note: The image is tagged with both the release tag and `latest`.

---

Last updated: 2026-01-17
