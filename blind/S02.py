import tarfile
import os.path

def make_tarfile(output_filename, source_dir):
    with tarfile.open(output_filename, "w:gz") as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))


def archive_file(path):
    output_filename = path + ".tar.gz"
    make_tarfile(output_filename, path)
    return output_filename