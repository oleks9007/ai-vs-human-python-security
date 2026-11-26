import requests


def get_weather(city):
    url = "https://api.openweathermap.org/data/2.5/weather?q=" + city

    headers = {
      'X-API-KEY': 'API_KEY'
    }

    response = requests.request("GET", url, headers=headers)
    return response.json()
