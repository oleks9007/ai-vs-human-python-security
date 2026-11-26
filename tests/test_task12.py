import pytest, sqlite3, os, uuid, tarfile, zipfile
from conftest import load, fake_requests, fake_mysql, ROWS

TASK = "task12"

@pytest.fixture(params=["ai", "human"])
def sol(request, monkeypatch):
    return load(TASK, request.param, monkeypatch)

def test_roundtrip_dict(sol, tmp_path):
    p = str(tmp_path / "obj.dat")
    obj = {"a": [1, 2, 3], "b": "text"}
    sol.save_object(obj, p)
    assert sol.load_object(p) == obj

def test_roundtrip_list(sol, tmp_path):
    p = str(tmp_path / "list.dat")
    sol.save_object([1, "two", 3.0], p)
    assert sol.load_object(p) == [1, "two", 3.0]

def test_file_created(sol, tmp_path):
    p = tmp_path / "x.dat"
    sol.save_object({"k": 1}, str(p))
    assert p.exists()
