#!/usr/bin/env python3
"""
openapi_inspect.py - OpenAPI YAML CLI Explorer

Features:
- Lists all paths and methods
- Shows details (parameters, status codes, responses) for path+method
- Outputs individual components/schemas entries

Usage:
  python openapi_inspect.py <api.yaml> paths
  python openapi_inspect.py <api.yaml> path <path> <method>
  python openapi_inspect.py <api.yaml> schema <SchemaName>

Requires: PyYAML (pip install pyyaml)

OpenAPI 3.x only!
"""
import argparse
import sys
import yaml
from pprint import pprint

def load_openapi(path):
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def cmd_paths(spec):
    paths = spec.get('paths', {})
    for path, methods in paths.items():
        for method in methods:
            print(f"{method.upper()} {path}")

def cmd_path_detail(spec, path, method):
    methods = spec.get('paths', {}).get(path)
    if not methods:
        print(f"Path not found: {path}")
        sys.exit(1)
    method_obj = methods.get(method.lower())
    if not method_obj:
        print(f"Method {method} not found for path {path}")
        sys.exit(1)
    print(f"--- {method.upper()} {path} ---")
    # Parameters
    params = method_obj.get('parameters', [])
    if params:
        print("Parameters:")
        for p in params:
            name = p.get('name')
            loc = p.get('in')
            req = p.get('required', False)
            ptype = p.get('schema', {}).get('type')
            desc = p.get('description', '')
            print(f"  - {name} ({loc}, {'required' if req else 'optional'}, type={ptype}): {desc}")
    else:
        print("No parameters.")
    # Status Codes & Responses
    responses = method_obj.get('responses', {})
    if responses:
        print("Responses:")
        for code, resp in responses.items():
            desc = resp.get('description', '')
            content = resp.get('content')
            if content:
                mediatypes = ', '.join(content.keys())
                print(f"  - {code}: {desc} [content: {mediatypes}]")
            else:
                print(f"  - {code}: {desc}")
    else:
        print("No responses defined.")

def cmd_schema(spec, name):
    schemas = spec.get('components', {}).get('schemas', {})
    schema = schemas.get(name)
    if not schema:
        print(f"Schema not found: {name}")
        sys.exit(1)
    pprint(schema)

def main():
    parser = argparse.ArgumentParser(description='OpenAPI YAML Explorer')
    parser.add_argument('file', help='OpenAPI YAML file')
    subparsers = parser.add_subparsers(dest='cmd', required=True)
    
    sp_paths = subparsers.add_parser('paths', help='List all paths and methods')

    sp_path = subparsers.add_parser('path', help='Show details for path+method')
    sp_path.add_argument('path', help='API path (e.g. /users)')
    sp_path.add_argument('method', help='HTTP method (e.g. get, post)')

    sp_schema = subparsers.add_parser('schema', help='Show schema from components/schemas')
    sp_schema.add_argument('name', help='Schema name')

    args = parser.parse_args()
    spec = load_openapi(args.file)

    if args.cmd == 'paths':
        cmd_paths(spec)
    elif args.cmd == 'path':
        cmd_path_detail(spec, args.path, args.method)
    elif args.cmd == 'schema':
        cmd_schema(spec, args.name)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
