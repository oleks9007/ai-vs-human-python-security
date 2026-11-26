import json
import os
import tempfile

tempdir = tempfile.mkdtemp()
path = os.path.join(tempdir)


def save_cache(key, data):
    with open(path + '/' + key + '.json', 'a') as cred:
        json.dump(data, cred)


def load_cache(key):
    if not os.path.exists(path + '/' + key + '.json'):
        return None
    with open(path + '/' + key + '.json') as cred:
        return json.load(cred)
