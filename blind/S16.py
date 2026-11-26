import json
import requests


def get_json(url):
    response = requests.get(url)
    json_data = json.loads(response.text)
    return json_data
