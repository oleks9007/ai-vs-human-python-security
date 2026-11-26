import tempfile

def write_temp_file(data):
    with tempfile.NamedTemporaryFile(mode="w", delete=False, encoding="utf-8") as temp_file:
        temp_file.write(data)
        return temp_file.name
