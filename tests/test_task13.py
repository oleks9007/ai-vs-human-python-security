import pytest, sqlite3, os, uuid, tarfile, zipfile
from conftest import load, fake_requests, fake_mysql, ROWS

TASK = "task13"

@pytest.fixture(params=["ai", "human"])
def sol(request, monkeypatch):
    return load(TASK, request.param, monkeypatch)

def test_precedence(sol):
    assert sol.calculate("2 + 3 * 4") == 14

def test_parentheses_division(sol):
    assert sol.calculate("(10 - 4) / 2") == 3

def test_subtraction(sol):
    assert sol.calculate("100 - 1") == 99
