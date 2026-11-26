import tarfile
import os

def archive_file(path):
    archive_path = path + ".tar.gz"

    with tarfile.open(archive_path, "w:gz") as archive:
        archive.add(path, arcname=os.path.basename(path))

    return archive_path