import requests
from django.conf import settings
from API import constants

def get_weather_data(location, start_date, end_date=None):
    api_key = settings.VISUAL_CROSSING_API_KEY
    base_url = constants.weather_api_base_url

    if end_date:
        url = f"{base_url}{location}/{start_date}/{end_date}"
    else:
        url = f"{base_url}{location}/{start_date}"

    params = {
        'unitGroup': 'metric',  # For Celsius and metric units
        'key': api_key,
        'include': 'days'  # To get daily data
    }

    response = requests.get(url, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()
