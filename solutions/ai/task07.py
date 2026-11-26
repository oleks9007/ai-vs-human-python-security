from pathlib import Path

def read_file(folder, filename):
    file_path = Path(folder) / filename
    return file_path.read_text(encoding="utf-8")