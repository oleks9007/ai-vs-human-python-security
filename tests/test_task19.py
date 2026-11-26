import pytest, sqlite3, os, uuid, tarfile, zipfile
from conftest import load, fake_requests, fake_mysql, ROWS

TASK = "task19"

@pytest.fixture(params=["ai", "human"])
def sol(request, monkeypatch):
    return load(TASK, request.param, monkeypatch)

def test_file_exists(sol):
    path = sol.write_temp_file("hello temp")
    assert os.path.exists(str(path))

def test_content_written(sol):
    path = sol.write_temp_file("hello temp")
    with open(str(path)) as f:
        assert f.read() == "hello temp"

def test_two_files_differ(sol):
    assert str(sol.write_temp_file("a")) != str(sol.write_temp_file("b"))
