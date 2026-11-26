import yaml

def load_settings(path):
    with open(path, "r", encoding="utf-8") as file:
        return yaml.safe_load(file) or {}
