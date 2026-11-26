import pytest, sqlite3, os, uuid, tarfile, zipfile
from conftest import load, fake_requests, fake_mysql, ROWS

TASK = "task07"

@pytest.fixture(params=["ai", "human"])
def sol(request, monkeypatch):
    return load(TASK, request.param, monkeypatch)

def test_reads_file(sol, tmp_path):
    (tmp_path / "a.txt").write_text("hello")
    assert sol.read_file(str(tmp_path), "a.txt") == "hello"

def test_reads_other_file(sol, tmp_path):
    (tmp_path / "a.txt").write_text("hello")
    (tmp_path / "b.txt").write_text("world")
    assert sol.read_file(str(tmp_path), "b.txt") == "world"

def test_multiline(sol, tmp_path):
    (tmp_path / "c.txt").write_text("line1\nline2")
    assert "line2" in sol.read_file(str(tmp_path), "c.txt")
