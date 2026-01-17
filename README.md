# openapi_inspect.py

[![CI](https://github.com/Nicklas2751/openapi_inspect_script/actions/workflows/test.yml/badge.svg)](https://github.com/Nicklas2751/openapi_inspect_script/actions/workflows/test.yml)
[![Release](https://github.com/Nicklas2751/openapi_inspect_script/actions/workflows/release.yml/badge.svg)](https://github.com/Nicklas2751/openapi_inspect_script/actions/workflows/release.yml)
[![Docker Pulls](https://img.shields.io/badge/docker-pulls-blue?logo=docker)](https://ghcr.io/nicklas2751/openapi_inspect_script)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)

A minimal CLI tool for exploring large OpenAPI YAML specifications.

## Purpose

**openapi_inspect.py** is designed to quickly extract and display relevant information from very large OpenAPI 3.x YAML files (10,000+ lines) via the command line. It enables you to interactively inspect available API paths, parameters, responses, and schema definitions—without the need for a web UI, a heavy OpenAPI library, or parsing the entire spec by hand.

## Features
- **List all available API paths and methods** in the spec (e.g. `GET /users/`, `POST /auth/token`)
- **Show all details for a given path and HTTP method**:
  - Parameters (names, types, required, location, description)
  - Response status codes and their descriptions
  - Response content types (e.g. `application/json`)
- **Show details for a specific component schema** (from `components/schemas`)
- Designed to efficiently handle OpenAPI YAMLs with tens of thousands of lines
- Minimal dependencies: Just [PyYAML](https://pyyaml.org/)

## Usage

```
# List all API paths and available HTTP methods
python openapi_inspect.py <openapi.yaml> paths

# Show full details for a specific path and HTTP method
python openapi_inspect.py <openapi.yaml> path /your/api/path get

# Print a component/schema definition by name
python openapi_inspect.py <openapi.yaml> schema ComponentName
```

### Example

```
python openapi_inspect.py openapi.yaml paths
GET /users/
POST /users/
GET /users/{id}
...

python openapi_inspect.py openapi.yaml path /users/{id} get
--- GET /users/{id} ---
Parameter:
  - id (path, required, type=string): User ID
Responses:
  - 200: Successful response [content: application/json]
  - 404: Not found

python openapi_inspect.py openapi.yaml schema User
{'type': 'object', 'properties': {'id': {'type': 'string'}, ... }}
```

## Requirements
- Python 3.8+
- PyYAML (`pip install pyyaml`)

*For best results and isolation, run in a virtual environment.*

```
python3 -m venv .venv
source .venv/bin/activate
pip install pyyaml
```

## Test

To run the tests, install the dependencies and run pytest from the project root:

```sh
pip install -r requirements.txt
pytest
```

Alternatively, mit pyproject.toml:

```sh
pip install .[test]
pytest
```

All test files are located in the `tests/` directory.

## Limitations
- Tested with OpenAPI 3.x YAML specs only
- Does not automatically resolve `$ref` references
- Only inspects `components/schemas` (not parameters, responses, etc. elsewhere)

## License
MIT License. See LICENSE file for details.

## Author
Nicklas Wiegandt (c) 2026

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
