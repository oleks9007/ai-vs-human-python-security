import pytest, sqlite3, os, uuid, tarfile, zipfile
from conftest import load, fake_requests, fake_mysql, ROWS

TASK = "task04"

@pytest.fixture(params=["ai", "human"])
def sol(request, monkeypatch):
    return load(TASK, request.param, monkeypatch)

def make_db(tmp_path):
    db = str(tmp_path / "users.db")
    con = sqlite3.connect(db)
    con.execute("CREATE TABLE users (username TEXT, password TEXT)")
    con.executemany("INSERT INTO users VALUES (?, ?)", [("alice", "Secret123"), ("bob", "Hunter42")])
    con.commit(); con.close()
    return db

def test_correct_login(sol, tmp_path):
    assert sol.check_login(make_db(tmp_path), "alice", "Secret123") == True

def test_wrong_password(sol, tmp_path):
    assert not sol.check_login(make_db(tmp_path), "alice", "WrongPass")

def test_unknown_user(sol, tmp_path):
    assert not sol.check_login(make_db(tmp_path), "carol", "Secret123")
