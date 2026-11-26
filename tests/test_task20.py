import pytest, sqlite3, os, uuid, tarfile, zipfile
from conftest import load, fake_requests, fake_mysql, ROWS

TASK = "task20"

@pytest.fixture(params=["ai", "human"])
def sol(request, monkeypatch):
    return load(TASK, request.param, monkeypatch)

def test_roundtrip(sol):
    key = "k" + uuid.uuid4().hex[:8]
    sol.save_cache(key, {"x": 1, "y": [1, 2]})
    assert sol.load_cache(key) == {"x": 1, "y": [1, 2]}

def test_missing_key_returns_none(sol):
    assert sol.load_cache("missing" + uuid.uuid4().hex[:8]) is None

def test_overwrite(sol):
    key = "k" + uuid.uuid4().hex[:8]
    sol.save_cache(key, {"v": 1})
    sol.save_cache(key, {"v": 2})
    assert sol.load_cache(key) == {"v": 2}
