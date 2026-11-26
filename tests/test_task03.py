import pytest, sqlite3, os, uuid, tarfile, zipfile
from conftest import load, fake_requests, fake_mysql, ROWS

TASK = "task03"

@pytest.fixture(params=["ai", "human"])
def sol(request, monkeypatch):
    return load(TASK, request.param, monkeypatch)

def make_db(tmp_path):
    db = str(tmp_path / "users.db")
    con = sqlite3.connect(db)
    con.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, email TEXT)")
    con.executemany("INSERT INTO users (username, email) VALUES (?, ?)",
                    [("alice", "alice@example.com"), ("bob", "bob@example.com")])
    con.commit(); con.close()
    return db

def values(row):
    if hasattr(row, "keys"):
        return [row[k] for k in row.keys()]
    return list(row)

def test_finds_alice(sol, tmp_path):
    row = sol.get_user(make_db(tmp_path), "alice")
    assert row is not None and "alice" in values(row)

def test_finds_bob_not_alice(sol, tmp_path):
    row = sol.get_user(make_db(tmp_path), "bob")
    assert row is not None and "bob" in values(row) and "alice" not in values(row)

def test_unknown_user_returns_none(sol, tmp_path):
    assert sol.get_user(make_db(tmp_path), "carol") is None
