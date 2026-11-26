import pytest, sqlite3, os, uuid, tarfile, zipfile
from conftest import load, fake_requests, fake_mysql, ROWS

TASK = "task15"

@pytest.fixture(params=["ai", "human"])
def sol(request, monkeypatch):
    fake_mysql(monkeypatch)
    return load(TASK, request.param, monkeypatch)

def test_returns_all_rows(sol):
    assert len(list(sol.get_all_users())) == 2

def test_contains_alice(sol):
    rows = [tuple(r) if not isinstance(r, dict) else tuple(r.values()) for r in sol.get_all_users()]
    assert any("alice" in r for r in rows)

def test_contains_bob(sol):
    rows = [tuple(r) if not isinstance(r, dict) else tuple(r.values()) for r in sol.get_all_users()]
    assert any("bob" in r for r in rows)
