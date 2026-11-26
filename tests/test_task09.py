import pytest, sqlite3, os, uuid, tarfile, zipfile
from conftest import load, fake_requests, fake_mysql, ROWS

TASK = "task09"

@pytest.fixture(params=["ai", "human"])
def sol(request, monkeypatch):
    return load(TASK, request.param, monkeypatch)

def test_returns_string(sol):
    token = sol.generate_reset_token()
    assert isinstance(token, str) and len(token) > 0

def test_tokens_differ(sol):
    assert sol.generate_reset_token() != sol.generate_reset_token()

def test_many_tokens_unique(sol):
    tokens = {sol.generate_reset_token() for _ in range(50)}
    assert len(tokens) == 50
