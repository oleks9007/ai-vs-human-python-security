import importlib.util, pathlib, pytest

ROOT = pathlib.Path(__file__).resolve().parent.parent

def load(group):
    path = ROOT / "solutions" / group / "task01.py"
    spec = importlib.util.spec_from_file_location(f"{group}_task01", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

@pytest.fixture(params=["ai", "human"])
def sol(request):
    return load(request.param)

def test_correct_password(sol):
    stored = sol.hash_password("Secret123")
    assert sol.verify_password("Secret123", stored) is True

def test_wrong_password(sol):
    stored = sol.hash_password("Secret123")
    assert sol.verify_password("WrongPass", stored) is False

def test_two_users(sol):
    alice = sol.hash_password("alice-pass")
    bob = sol.hash_password("bob-pass")
    assert sol.verify_password("alice-pass", bob) is False