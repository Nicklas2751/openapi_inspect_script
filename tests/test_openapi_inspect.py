import io
import sys
import yaml
import pytest
from contextlib import redirect_stdout

# Annahme: Das Skript liegt im selben Ordner wie dieser Test
import openapi_inspect as oi

def test_load_openapi(tmp_path):
    content = 'openapi: "3.0.0"\npaths: {}\ncomponents: {schemas: {}}\n'
    f = tmp_path / "t.yaml"
    f.write_text(content, encoding='utf-8')
    spec = oi.load_openapi(str(f))
    assert spec['openapi'] == '3.0.0'
    assert 'paths' in spec
    assert 'components' in spec

def test_cmd_paths_prints_paths():
    spec = {'paths': {'/a': {'get': {}}, '/b': {'post': {}}}}
    out = io.StringIO()
    with redirect_stdout(out):
        oi.cmd_paths(spec)
    res = out.getvalue()
    assert 'GET /a' in res
    assert 'POST /b' in res

def test_cmd_path_detail_prints_info():
    spec = {
        'paths': {
            '/foo': {
                'get': {
                    'parameters': [
                        {'name':'x','in':'query','required':True,'schema':{'type':'string'},'description':'desc'}
                    ],
                    'responses': {
                        '200': {'description':'ok','content':{'application/json':{}}},
                        '404': {'description':'not found'}
                    }
                }
            }
        }
    }
    out = io.StringIO()
    with redirect_stdout(out):
        oi.cmd_path_detail(spec, '/foo', 'get')
    res = out.getvalue()
    assert 'GET /foo' in res
    assert 'desc' in res
    assert '200' in res and 'application/json' in res
    assert '404' in res

@pytest.mark.parametrize("path,method,expected", [
    ('/missing', 'get', 'Path not found'),
    ('/foo', 'post', 'Method post not found'),
])
def test_cmd_path_detail_error_exit(path, method, expected):
    spec = {'paths': {'/foo': {'get': {'responses': {}}}}}
    out = io.StringIO()
    with pytest.raises(SystemExit):
        with redirect_stdout(out):
            oi.cmd_path_detail(spec, path, method)
    assert expected in out.getvalue()

def test_cmd_schema_print():
    spec = {'components': {'schemas': {'User': {'type': 'object','x': 1}}}}
    out = io.StringIO()
    with redirect_stdout(out):
        oi.cmd_schema(spec, 'User')
    assert 'object' in out.getvalue()

@pytest.mark.parametrize("name", ["Missing"])
def test_cmd_schema_notfound_exit(name):
    spec = {'components': {'schemas': {'User': {}}}}
    out = io.StringIO()
    with pytest.raises(SystemExit):
        with redirect_stdout(out):
            oi.cmd_schema(spec, name)
    assert 'Schema not found' in out.getvalue()
