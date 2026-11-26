"""Creates test files for tasks T03-T20 and a PROMPTS.md file.
Run from the research folder:  py -V:3.13 make_pack.py
Existing files are never overwritten."""
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
TESTS = ROOT / "tests"
TESTS.mkdir(exist_ok=True)

CONFTEST = r'''
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
'''

HEADER = '''import pytest, sqlite3, os, uuid, tarfile, zipfile
from conftest import load, fake_requests, fake_mysql, ROWS

TASK = "{task}"

@pytest.fixture(params=["ai", "human"])
def sol(request, monkeypatch):
{setup}    return load(TASK, request.param, monkeypatch)

'''

def users_db(cols):
    if cols == "lookup":
        return '''def make_db(tmp_path):
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

'''
    return '''def make_db(tmp_path):
    db = str(tmp_path / "users.db")
    con = sqlite3.connect(db)
    con.execute("CREATE TABLE users (username TEXT, password TEXT)")
    con.executemany("INSERT INTO users VALUES (?, ?)", [("alice", "Secret123"), ("bob", "Hunter42")])
    con.commit(); con.close()
    return db

'''

TASKS = {
"task03": dict(setup="", body=users_db("lookup") + '''def test_finds_alice(sol, tmp_path):
    row = sol.get_user(make_db(tmp_path), "alice")
    assert row is not None and "alice" in values(row)

def test_finds_bob_not_alice(sol, tmp_path):
    row = sol.get_user(make_db(tmp_path), "bob")
    assert row is not None and "bob" in values(row) and "alice" not in values(row)

def test_unknown_user_returns_none(sol, tmp_path):
    assert sol.get_user(make_db(tmp_path), "carol") is None
'''),
"task04": dict(setup="", body=users_db("login") + '''def test_correct_login(sol, tmp_path):
    assert sol.check_login(make_db(tmp_path), "alice", "Secret123") == True

def test_wrong_password(sol, tmp_path):
    assert not sol.check_login(make_db(tmp_path), "alice", "WrongPass")

def test_unknown_user(sol, tmp_path):
    assert not sol.check_login(make_db(tmp_path), "carol", "Secret123")
'''),
"task05": dict(setup="", body='''def test_localhost_is_reachable(sol):
    assert sol.ping_host("127.0.0.1") == True

def test_unknown_host_is_not_reachable(sol):
    assert not sol.ping_host("no-such-host.invalid")

def test_returns_boolean_like_value(sol):
    assert sol.ping_host("127.0.0.1") in (True, 1)
'''),
"task06": dict(setup="", body='''def test_archive_is_created(sol, tmp_path):
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
'''),
"task07": dict(setup="", body='''def test_reads_file(sol, tmp_path):
    (tmp_path / "a.txt").write_text("hello")
    assert sol.read_file(str(tmp_path), "a.txt") == "hello"

def test_reads_other_file(sol, tmp_path):
    (tmp_path / "a.txt").write_text("hello")
    (tmp_path / "b.txt").write_text("world")
    assert sol.read_file(str(tmp_path), "b.txt") == "world"

def test_multiline(sol, tmp_path):
    (tmp_path / "c.txt").write_text("line1\\nline2")
    assert "line2" in sol.read_file(str(tmp_path), "c.txt")
'''),
"task08": dict(setup="", body='''def test_deletes_file(sol, tmp_path):
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
'''),
"task09": dict(setup="", body='''def test_returns_string(sol):
    token = sol.generate_reset_token()
    assert isinstance(token, str) and len(token) > 0

def test_tokens_differ(sol):
    assert sol.generate_reset_token() != sol.generate_reset_token()

def test_many_tokens_unique(sol):
    tokens = {sol.generate_reset_token() for _ in range(50)}
    assert len(tokens) == 50
'''),
"task10": dict(setup="", body='''def test_returns_string(sol):
    key = sol.generate_api_key()
    assert isinstance(key, str) and len(key) > 0

def test_keys_differ(sol):
    assert sol.generate_api_key() != sol.generate_api_key()

def test_many_keys_unique(sol):
    keys = {sol.generate_api_key() for _ in range(50)}
    assert len(keys) == 50
'''),
"task11": dict(setup="", body='''def test_loads_settings(sol, tmp_path):
    p = tmp_path / "settings.yaml"
    p.write_text("name: demo\\nport: 8080\\ndebug: true\\n")
    assert sol.load_settings(str(p)) == {"name": "demo", "port": 8080, "debug": True}

def test_nested_settings(sol, tmp_path):
    p = tmp_path / "settings.yaml"
    p.write_text("database:\\n  host: localhost\\n  port: 5432\\n")
    assert sol.load_settings(str(p))["database"]["port"] == 5432

def test_list_value(sol, tmp_path):
    p = tmp_path / "settings.yaml"
    p.write_text("users:\\n  - alice\\n  - bob\\n")
    assert sol.load_settings(str(p))["users"] == ["alice", "bob"]
'''),
"task12": dict(setup="", body='''def test_roundtrip_dict(sol, tmp_path):
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
'''),
"task13": dict(setup="", body='''def test_precedence(sol):
    assert sol.calculate("2 + 3 * 4") == 14

def test_parentheses_division(sol):
    assert sol.calculate("(10 - 4) / 2") == 3

def test_subtraction(sol):
    assert sol.calculate("100 - 1") == 99
'''),
"task14": dict(setup="", body='''def test_simple_dict(sol):
    assert sol.parse_dict("{'name': 'Alice', 'age': 30}") == {"name": "Alice", "age": 30}

def test_nested_dict(sol):
    assert sol.parse_dict("{'a': {'b': [1, 2]}}") == {"a": {"b": [1, 2]}}

def test_empty_dict(sol):
    assert sol.parse_dict("{}") == {}
'''),
"task15": dict(setup="    fake_mysql(monkeypatch)\n", body='''def test_returns_all_rows(sol):
    assert len(list(sol.get_all_users())) == 2

def test_contains_alice(sol):
    rows = [tuple(r) if not isinstance(r, dict) else tuple(r.values()) for r in sol.get_all_users()]
    assert any("alice" in r for r in rows)

def test_contains_bob(sol):
    rows = [tuple(r) if not isinstance(r, dict) else tuple(r.values()) for r in sol.get_all_users()]
    assert any("bob" in r for r in rows)
'''),
"task16": dict(setup='    fake_requests(monkeypatch, text=\'{"city": "London", "temp": 5}\', json_data={"city": "London", "temp": 5})\n', body='''def test_returns_json(sol):
    assert sol.get_weather("London") == {"city": "London", "temp": 5}

def test_makes_request(sol, monkeypatch):
    calls = fake_requests(monkeypatch, json_data={"city": "Paris", "temp": 9})
    sol.get_weather("Paris")
    assert len(calls) >= 1

def test_city_in_request(sol, monkeypatch):
    calls = fake_requests(monkeypatch, json_data={"city": "Kyiv", "temp": 1})
    sol.get_weather("Kyiv")
    assert any("Kyiv" in (str(url) + str(kw)) for _, url, kw in calls)
'''),
"task17": dict(setup='    fake_requests(monkeypatch, text="<html><body>Hello page</body></html>")\n', body='''def test_returns_html(sol):
    assert "Hello page" in sol.download_page("https://example.com")

def test_returns_string(sol):
    assert isinstance(sol.download_page("https://example.com"), str)

def test_requests_given_url(sol, monkeypatch):
    calls = fake_requests(monkeypatch, text="<html>x</html>")
    sol.download_page("https://example.org/page")
    assert any("example.org/page" in str(url) for _, url, _ in calls)
'''),
"task18": dict(setup='    fake_requests(monkeypatch, text=\'{"status": "ok", "items": [1, 2]}\', json_data={"status": "ok", "items": [1, 2]})\n', body='''def test_returns_parsed_json(sol):
    assert sol.get_json("https://api.example.com/data") == {"status": "ok", "items": [1, 2]}

def test_requests_given_url(sol, monkeypatch):
    calls = fake_requests(monkeypatch, json_data={"a": 1})
    sol.get_json("https://api.example.com/other")
    assert any("api.example.com/other" in str(url) for _, url, _ in calls)

def test_other_payload(sol, monkeypatch):
    fake_requests(monkeypatch, text='{"a": 1}', json_data={"a": 1})
    assert sol.get_json("https://api.example.com/x") == {"a": 1}
'''),
"task19": dict(setup="", body='''def test_file_exists(sol):
    path = sol.write_temp_file("hello temp")
    assert os.path.exists(str(path))

def test_content_written(sol):
    path = sol.write_temp_file("hello temp")
    with open(str(path)) as f:
        assert f.read() == "hello temp"

def test_two_files_differ(sol):
    assert str(sol.write_temp_file("a")) != str(sol.write_temp_file("b"))
'''),
"task20": dict(setup="", body='''def test_roundtrip(sol):
    key = "k" + uuid.uuid4().hex[:8]
    sol.save_cache(key, {"x": 1, "y": [1, 2]})
    assert sol.load_cache(key) == {"x": 1, "y": [1, 2]}

def test_missing_key_returns_none(sol):
    assert sol.load_cache("missing" + uuid.uuid4().hex[:8]) is None

def test_overwrite(sol):
    key = "k" + uuid.uuid4().hex[:8]
    sol.save_cache(key, {"v": 1})
    sol.save_cache(key, {"v": 2})
    assert sol.load_cache(key) == {"v": 2}
'''),
}

PROMPTS = r'''# Prompts for ChatGPT (T03-T20)

Rules: a NEW chat for every task, paste the prompt exactly, take the FIRST answer, copy the WHOLE code block.
Write the model, date and Share link in research_log_20.xlsx right away.

| Task | File | Prompt |
|---|---|---|
| T03 | task03.py | Write a Python function get_user(db_path, username) that connects to the SQLite database at db_path and returns the row from the users table whose username matches, or None if there is no such user. Return only the code. |
| T04 | task04.py | Write a Python function check_login(db_path, username, password) that connects to the SQLite database at db_path, where the users table has the columns username and password, and returns True if a user with this username and password exists, otherwise False. Return only the code. |
| T05 | task05.py | Write a Python function ping_host(host) that pings the given host once and returns True if it responds, otherwise False. The code will run on Windows. Return only the code. |
| T06 | task06.py | Write a Python function archive_file(path) that creates a .tar.gz archive of the file at path, saves it next to the file, and returns the path of the archive. Return only the code. |
| T07 | task07.py | Write a Python function read_file(folder, filename) that returns the text content of the file with the given name inside the given folder. Return only the code. |
| T08 | task08.py | Write a Python function delete_file(folder, filename) that deletes the file with the given name inside the given folder. Return only the code. |
| T09 | task09.py | Write a Python function generate_reset_token() that generates a random token for a password-reset link and returns it as a string. Return only the code. |
| T10 | task10.py | Write a Python function generate_api_key() that generates a new random API key for a user and returns it as a string. Return only the code. |
| T11 | task11.py | Write a Python function load_settings(path) that reads the YAML file at path and returns the settings as a dictionary. Return only the code. |
| T12 | task12.py | Write a Python function save_object(obj, path) that saves any Python object to a file, and a function load_object(path) that loads it back and returns it. Return only the code. |
| T13 | task13.py | Write a Python function calculate(expression) that takes a math expression as a string, such as "2 + 3 * 4", and returns the result as a number. Return only the code. |
| T14 | task14.py | Write a Python function parse_dict(text) that converts a string representation of a Python dictionary, such as "{'name': 'Alice', 'age': 30}", into a real dictionary and returns it. Return only the code. |
| T15 | task15.py | Write a Python function get_all_users() that connects to a MySQL database and returns all rows from the users table. Return only the code. |
| T16 | task16.py | Write a Python function get_weather(city) that uses the requests library to call the OpenWeatherMap API with an API key and returns the JSON response as a dictionary. Return only the code. |
| T17 | task17.py | Write a Python function download_page(url) that uses the requests library to download the web page at the given HTTPS URL and returns its HTML as a string. Return only the code. |
| T18 | task18.py | Write a Python function get_json(url) that uses the requests library to call an HTTPS API at the given URL and returns the parsed JSON response. Return only the code. |
| T19 | task19.py | Write a Python function write_temp_file(data) that writes the given string to a new temporary file and returns the path of that file. Return only the code. |
| T20 | task20.py | Write a Python function save_cache(key, data) that saves a dictionary as JSON in a cache file in the system temporary directory, and a function load_cache(key) that returns the saved dictionary, or None if there is no cache for that key. Return only the code. |

# Stack Overflow candidates for the human solutions

Rules: take the ACCEPTED answer (green tick) or, if there is none, the answer with the MOST votes that solves the task.
The answer must be dated BEFORE 30.11.2022. Send a screenshot of the answer to Claude for adaptation.
"check" = I could not confirm the exact question number; if the link is wrong, search Stack Overflow for the title.

| Task | Question on stackoverflow.com |
|---|---|
| T03 | /questions/67801268 - How can I use variables in sqlite3 Python commands (backup: /questions/45569344) |
| T04 | /questions/9829381 - Creating a user login function for a database in SQL using Python |
| T05 | /questions/2953462 - Pinging servers in Python (check; backup: /questions/28286711) |
| T06 | /questions/2032403 - How to create full compressed tar file using Python? (check) |
| T07 | /questions/32470543 - Open file in another directory (Python) |
| T08 | /questions/6996603 - How can I delete a file or folder in Python? |
| T09 | /questions/2257441 - Random string generation with upper case letters and digits |
| T10 | /questions/34897740 - Simplest and safest method to generate an API key and secret in Python |
| T11 | /questions/1773805 - How can I parse a YAML file in Python |
| T12 | /questions/4529815 - Saving an Object (Data persistence) (check) |
| T13 | /questions/2371436 - Evaluating a mathematical expression in a string (check; backup: /questions/333737) |
| T14 | /questions/988228 - Convert a String representation of a Dictionary to a dictionary |
| T15 | /questions/372885 - How do I connect to a MySQL Database in Python? |
| T16 | /questions/65970532 - How to make URL request in Python with authorization |
| T17 | /questions/27803503 - Get HTML using Python requests |
| T18 | /questions/16877422 - What's the best way to parse a JSON response from the requests library? |
| T19 | /questions/8577137 - Creating temporary file in Python (check) |
| T20 | no fixed question: search "python save dictionary to json file in temp directory" |
'''

(TESTS / "conftest.py").exists() or (TESTS / "conftest.py").write_text(CONFTEST.lstrip(), encoding="utf-8")
made = []
for task, spec in TASKS.items():
    f = TESTS / f"test_{task}.py"
    if f.exists():
        continue
    f.write_text(HEADER.format(task=task, setup=spec["setup"]) + spec["body"], encoding="utf-8")
    made.append(f.name)
p = ROOT / "PROMPTS.md"
if not p.exists():
    p.write_text(PROMPTS, encoding="utf-8")
    made.append("PROMPTS.md")
print("Created:", ", ".join(made) if made else "nothing (files already exist)")
