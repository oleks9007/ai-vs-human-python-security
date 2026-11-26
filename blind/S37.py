from pathlib import Path


def read_file(folder, filename):
    data_folder = Path(folder)
    file_to_open = data_folder / filename

    f = open(file_to_open)
    return f.read()