import pytest, sqlite3, os, uuid, tarfile, zipfile
from conftest import load, fake_requests, fake_mysql, ROWS

TASK = "task06"

@pytest.fixture(params=["ai", "human"])
def sol(request, monkeypatch):
    return load(TASK, request.param, monkeypatch)

def test_archive_is_created(sol, tmp_path):
    f = tmp_path / "report.txt"
    f.write_text("hello")
    result = sol.archive_file(str(f))
    assert result and os.path.exists(str(result))

def test_archive_is_valid(sol, tmp_path):
    f = tmp_path / "data.txt"
    f.write_text("some data")
    result = str(sol.archive_file(str(f)))
    assert tarfile.is_tarfile(result) or zipfile.is_zipfile(result)

def test_original_file_kept(sol, tmp_path):
    f = tmp_path / "keep.txt"
    f.write_text("keep me")
    sol.archive_file(str(f))
    assert f.exists()
