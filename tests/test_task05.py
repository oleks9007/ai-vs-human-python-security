import pytest, sqlite3, os, uuid, tarfile, zipfile
from conftest import load, fake_requests, fake_mysql, ROWS

TASK = "task05"

@pytest.fixture(params=["ai", "human"])
def sol(request, monkeypatch):
    return load(TASK, request.param, monkeypatch)

def test_localhost_is_reachable(sol):
    assert sol.ping_host("127.0.0.1") == True

def test_unknown_host_is_not_reachable(sol):
    assert not sol.ping_host("no-such-host.invalid")

def test_returns_boolean_like_value(sol):
    assert sol.ping_host("127.0.0.1") in (True, 1)
