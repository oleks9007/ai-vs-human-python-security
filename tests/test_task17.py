import pytest, sqlite3, os, uuid, tarfile, zipfile
from conftest import load, fake_requests, fake_mysql, ROWS

TASK = "task17"

@pytest.fixture(params=["ai", "human"])
def sol(request, monkeypatch):
    fake_requests(monkeypatch, text="<html><body>Hello page</body></html>")
    return load(TASK, request.param, monkeypatch)

def test_returns_html(sol):
    assert "Hello page" in sol.download_page("https://example.com")

def test_returns_string(sol):
    assert isinstance(sol.download_page("https://example.com"), str)

def test_requests_given_url(sol, monkeypatch):
    calls = fake_requests(monkeypatch, text="<html>x</html>")
    sol.download_page("https://example.org/page")
    assert any("example.org/page" in str(url) for _, url, _ in calls)
