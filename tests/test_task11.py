import pytest, sqlite3, os, uuid, tarfile, zipfile
from conftest import load, fake_requests, fake_mysql, ROWS

TASK = "task11"

@pytest.fixture(params=["ai", "human"])
def sol(request, monkeypatch):
    return load(TASK, request.param, monkeypatch)

def test_loads_settings(sol, tmp_path):
    p = tmp_path / "settings.yaml"
    p.write_text("name: demo\nport: 8080\ndebug: true\n")
    assert sol.load_settings(str(p)) == {"name": "demo", "port": 8080, "debug": True}

def test_nested_settings(sol, tmp_path):
    p = tmp_path / "settings.yaml"
    p.write_text("database:\n  host: localhost\n  port: 5432\n")
    assert sol.load_settings(str(p))["database"]["port"] == 5432

def test_list_value(sol, tmp_path):
    p = tmp_path / "settings.yaml"
    p.write_text("users:\n  - alice\n  - bob\n")
    assert sol.load_settings(str(p))["users"] == ["alice", "bob"]
