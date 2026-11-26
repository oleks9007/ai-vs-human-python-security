import pytest, sqlite3, os, uuid, tarfile, zipfile
from conftest import load, fake_requests, fake_mysql, ROWS

TASK = "task16"

@pytest.fixture(params=["ai", "human"])
def sol(request, monkeypatch):
    fake_requests(monkeypatch, text='{"city": "London", "temp": 5}', json_data={"city": "London", "temp": 5})
    return load(TASK, request.param, monkeypatch)

def test_returns_json(sol):
    assert sol.get_weather("London") == {"city": "London", "temp": 5}

def test_makes_request(sol, monkeypatch):
    calls = fake_requests(monkeypatch, json_data={"city": "Paris", "temp": 9})
    sol.get_weather("Paris")
    assert len(calls) >= 1

def test_city_in_request(sol, monkeypatch):
    calls = fake_requests(monkeypatch, json_data={"city": "Kyiv", "temp": 1})
    sol.get_weather("Kyiv")
    assert any("Kyiv" in (str(url) + str(kw)) for _, url, kw in calls)
