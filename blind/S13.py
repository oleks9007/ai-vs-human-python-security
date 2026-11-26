from pathlib import Path


def delete_file(folder, filename):
    dir_path = Path(folder)
    file_path = dir_path / filename

    file_path.unlink() # remove file