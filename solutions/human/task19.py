import os
import tempfile


def write_temp_file(data):
    new_file, filename = tempfile.mkstemp()

    os.write(new_file, data.encode())
    os.close(new_file)
    return filename
