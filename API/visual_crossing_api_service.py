import string
from datetime import datetime
from typing import Dict
import requests
from django.conf import settings
from django.core.cache import cache

from API import constants

class WeatherData:
    def __init__(self, address: str, description: str, temperature: int, selected_date: str, error_message: str=None):
        self.address = address
        self.description = description
        self.temperature = temperature
        self.selected_date = selected_date
        self.error_message = error_message

def get_weather_data(location: str, start_date: datetime, end_date: datetime=None) -> WeatherData:
    api_key: string = settings.VISUAL_CROSSING_API_KEY
    base_url: string = constants.weather_api_base_url

    formatted_start_date: str = start_date.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'

    if end_date:
        formatted_end_date: str = end_date.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
        url: str = f"{base_url}{location}/{formatted_start_date}/{formatted_end_date}"
    else:
        url: str = f"{base_url}{location}/{formatted_start_date}"

    cache_key: str = f"{location}_{start_date.strftime('%Y-%m-%d')}"
    cached_value: WeatherData = cache.get(cache_key)

    if cached_value:
        return cached_value

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
        temperature: int = days['temp']
        date: str = days['datetime']

        weather_data: WeatherData = WeatherData(resolved_address, description, temperature, date)
        cache.set(cache_key, weather_data, timeout= 60 * 10) # cache for 10 minutes
        return weather_data
    elif response.status_code == 400:
        return WeatherData("", "", 0, "", response.text)
    else:
        response.raise_for_status()
