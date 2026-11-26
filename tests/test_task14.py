import pytest, sqlite3, os, uuid, tarfile, zipfile
from conftest import load, fake_requests, fake_mysql, ROWS

TASK = "task14"

@pytest.fixture(params=["ai", "human"])
def sol(request, monkeypatch):
    return load(TASK, request.param, monkeypatch)

def test_simple_dict(sol):
    assert sol.parse_dict("{'name': 'Alice', 'age': 30}") == {"name": "Alice", "age": 30}

def test_nested_dict(sol):
    assert sol.parse_dict("{'a': {'b': [1, 2]}}") == {"a": {"b": [1, 2]}}

def test_empty_dict(sol):
    assert sol.parse_dict("{}") == {}
