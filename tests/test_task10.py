import pytest, sqlite3, os, uuid, tarfile, zipfile
from conftest import load, fake_requests, fake_mysql, ROWS

TASK = "task10"

@pytest.fixture(params=["ai", "human"])
def sol(request, monkeypatch):
    return load(TASK, request.param, monkeypatch)

def test_returns_string(sol):
    key = sol.generate_api_key()
    assert isinstance(key, str) and len(key) > 0

def test_keys_differ(sol):
    assert sol.generate_api_key() != sol.generate_api_key()

def test_many_keys_unique(sol):
    keys = {sol.generate_api_key() for _ in range(50)}
    assert len(keys) == 50
