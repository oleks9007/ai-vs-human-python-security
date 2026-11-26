import importlib.util, pathlib, os, sys, types, builtins

ROOT = pathlib.Path(__file__).resolve().parent.parent


class _LenientEnv(dict):
    """os.environ replacement: missing variables return a dummy value instead of KeyError."""
    def __missing__(self, key):
        return "test-value"


def load(task, group, monkeypatch):
    """Load solutions/<group>/<task>.py with safe defaults for example code at module level."""
    monkeypatch.setattr(os, "environ", _LenientEnv(os.environ))
    monkeypatch.setattr(builtins, "input", lambda *a, **k: "test")
    path = ROOT / "solutions" / group / f"{task}.py"
    if not path.exists():
        import pytest
        pytest.skip(f"{group}/{task}.py not created yet")
    spec = importlib.util.spec_from_file_location(f"{group}_{task}", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class FakeResponse:
    def __init__(self, text="", json_data=None):
        if not text and json_data is not None:
            import json
            text = json.dumps(json_data)
        self.text = text
        self._json = json_data
        self.content = text.encode()
        self.status_code = 200
        self.ok = True
        self.headers = {"Content-Type": "text/html"}
        self.encoding = "utf-8"
        self.url = "https://example.com"
    def json(self, **kwargs):
        return self._json
    def raise_for_status(self):
        return None
    def iter_content(self, chunk_size=1, **kwargs):
        yield self.content
    def close(self):
        pass
    def __enter__(self):
        return self
    def __exit__(self, *a):
        return False


def fake_requests(monkeypatch, text="", json_data=None):
    """Make every requests call (get, post, Session...) return a FakeResponse without network access."""
    import requests
    calls = []
    def fake_request(self, method, url, *args, **kwargs):
        calls.append((method, url, kwargs))
        return FakeResponse(text, json_data)
    monkeypatch.setattr(requests.sessions.Session, "request", fake_request)
    return calls


ROWS = [(1, "alice", "alice@example.com"), (2, "bob", "bob@example.com")]


class FakeCursor:
    description = [("id",), ("username",), ("email",)]
    rowcount = len(ROWS)
    def execute(self, *a, **k):
        return len(ROWS)
    def fetchall(self):
        return list(ROWS)
    def fetchone(self):
        return ROWS[0]
    def fetchmany(self, size=1):
        return list(ROWS)[:size]
    def __iter__(self):
        return iter(ROWS)
    def close(self):
        pass
    def __enter__(self):
        return self
    def __exit__(self, *a):
        return False


class FakeConnection:
    def cursor(self, *a, **k):
        return FakeCursor()
    def commit(self):
        pass
    def close(self):
        pass
    def is_connected(self):
        return True
    def __enter__(self):
        return self
    def __exit__(self, *a):
        return False


def fake_mysql(monkeypatch):
    """Replace pymysql, MySQLdb and mysql.connector with fakes that return two user rows."""
    connect = lambda *a, **k: FakeConnection()
    cursors = types.SimpleNamespace(DictCursor=object, Cursor=object)
    err = type("Error", (Exception,), {})
    pymysql = types.ModuleType("pymysql")
    pymysql.connect = pymysql.Connect = connect
    pymysql.cursors = cursors
    pymysql.Error = pymysql.MySQLError = err
    mysqldb = types.ModuleType("MySQLdb")
    mysqldb.connect = mysqldb.Connect = connect
    mysqldb.Error = err
    mysqldb.cursors = cursors
    mysql = types.ModuleType("mysql")
    connector = types.ModuleType("mysql.connector")
    connector.connect = connect
    connector.Error = err
    connector.errorcode = types.SimpleNamespace()
    mysql.connector = connector
    for name, mod in [("pymysql", pymysql), ("pymysql.cursors", cursors), ("MySQLdb", mysqldb),
                      ("MySQLdb.cursors", cursors), ("mysql", mysql), ("mysql.connector", connector)]:
        monkeypatch.setitem(sys.modules, name, mod)
