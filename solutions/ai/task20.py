import json
import hashlib
import tempfile
from pathlib import Path


def _cache_path(key):
    filename = hashlib.sha256(str(key).encode()).hexdigest() + ".json"
    return Path(tempfile.gettempdir()) / filename


def save_cache(key, data):
    path = _cache_path(key)
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False)


def load_cache(key):
    path = _cache_path(key)
    if not path.exists():
        return None

    try:
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        return None
