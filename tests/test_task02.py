import importlib.util, pathlib, pytest

ROOT = pathlib.Path(__file__).resolve().parent.parent

def load(group):
    path = ROOT / "solutions" / group / "task02.py"
    spec = importlib.util.spec_from_file_location(f"{group}_task02", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

@pytest.fixture(params=["ai", "human"])
def sol(request):
    return load(request.param)

def test_login_correct(sol):
    users = {}
    sol.register_user(users, "alice", "Secret123")
    assert sol.login(users, "alice", "Secret123") is True

def test_login_wrong_password(sol):
    users = {}
    sol.register_user(users, "alice", "Secret123")
    assert sol.login(users, "alice", "WrongPass") is False

def test_unknown_user(sol):
    users = {}
    assert sol.login(users, "bob", "Secret123") is False