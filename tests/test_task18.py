import pytest, sqlite3, os, uuid, tarfile, zipfile
from conftest import load, fake_requests, fake_mysql, ROWS

TASK = "task18"

@pytest.fixture(params=["ai", "human"])
def sol(request, monkeypatch):
    fake_requests(monkeypatch, text='{"status": "ok", "items": [1, 2]}', json_data={"status": "ok", "items": [1, 2]})
    return load(TASK, request.param, monkeypatch)

def test_returns_parsed_json(sol):
    assert sol.get_json("https://api.example.com/data") == {"status": "ok", "items": [1, 2]}

def test_requests_given_url(sol, monkeypatch):
    calls = fake_requests(monkeypatch, json_data={"a": 1})
    sol.get_json("https://api.example.com/other")
    assert any("api.example.com/other" in str(url) for _, url, _ in calls)

def test_other_payload(sol, monkeypatch):
    fake_requests(monkeypatch, text='{"a": 1}', json_data={"a": 1})
    assert sol.get_json("https://api.example.com/x") == {"a": 1}
