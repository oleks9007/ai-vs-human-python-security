import os

def delete_file(folder, filename):
    path = os.path.join(folder, filename)
    if os.path.isfile(path):
        os.remove(path)
        return True
    return False