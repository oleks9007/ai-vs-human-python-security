import requests


def download_page(url):
    headers = {'Accept-Encoding': 'identity'}
    r = requests.get(url, headers=headers)
    return r.text
