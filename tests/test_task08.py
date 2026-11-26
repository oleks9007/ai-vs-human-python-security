import pytest, sqlite3, os, uuid, tarfile, zipfile
from conftest import load, fake_requests, fake_mysql, ROWS

TASK = "task08"

@pytest.fixture(params=["ai", "human"])
def sol(request, monkeypatch):
    return load(TASK, request.param, monkeypatch)

def test_deletes_file(sol, tmp_path):
    (tmp_path / "old.txt").write_text("x")
    sol.delete_file(str(tmp_path), "old.txt")
    assert not (tmp_path / "old.txt").exists()

def test_other_files_kept(sol, tmp_path):
    (tmp_path / "old.txt").write_text("x")
    (tmp_path / "keep.txt").write_text("y")
    sol.delete_file(str(tmp_path), "old.txt")
    assert (tmp_path / "keep.txt").exists()

def test_delete_second_file(sol, tmp_path):
    (tmp_path / "a.txt").write_text("x")
    (tmp_path / "b.txt").write_text("y")
    sol.delete_file(str(tmp_path), "b.txt")
    assert (tmp_path / "a.txt").exists() and not (tmp_path / "b.txt").exists()
