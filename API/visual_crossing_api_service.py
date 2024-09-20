import string
from datetime import datetime
from typing import Dict

import requests
from django.conf import settings
from API import constants

class WeatherData:
    def __init__(self, address: str, description: str):
        self.address = address
        self.description = description

def get_weather_data(location: str, start_date: datetime, end_date: datetime=None):
    api_key: string = settings.VISUAL_CROSSING_API_KEY
    base_url: string = constants.weather_api_base_url

    formatted_start_date: str = start_date.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'

    if end_date:
        formatted_end_date: str = end_date.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
        url: str = f"{base_url}{location}/{formatted_start_date}/{formatted_end_date}"
    else:
        url: str = f"{base_url}{location}/{formatted_start_date}"

    params: Dict[str, str] = {
        'unitGroup': 'metric',  # For Celsius and metric units
        'key': api_key,
        'include': 'days'  # To get daily data
    }

    response = requests.get(url, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        json_response: Dict = response.json()
        resolved_address: str = json_response['resolvedAddress']
        days: Dict = json_response['days'][0]
        description: str = days['description']
        return WeatherData(resolved_address, description)
    else:
        response.raise_for_status()
