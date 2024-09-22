"""Module handles api calls to visual crossing api."""

from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Optional
import requests
from django.conf import settings
from django.core.cache import cache
from api import constants

@dataclass
class WeatherData:
    """class handles params for WeatherData class"""
    address: str
    description: str
    temperature: float
    selected_date: str
    error_message: Optional[str] = None

def get_weather_data(location: str, start_date: datetime, end_date: datetime=None) -> WeatherData:
    """function handles logic for sending GET request to visual crossing api"""
    formatted_start_date: str = start_date.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'

    if end_date:
        formatted_end_date: str = end_date.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
        url: str = f"{constants.weather_api_base_url}{location}/{formatted_start_date}/{formatted_end_date}"
    else:
        url: str = f"{constants.weather_api_base_url}{location}/{formatted_start_date}"

    cache_key: str = f"{location}_{start_date.strftime('%Y-%m-%d')}"
    cached_value: WeatherData = cache.get(cache_key)

    if cached_value:
        return cached_value

    response = requests.get(url, params= {
        'unitGroup': 'metric',  # For Celsius and metric units
        'key': settings.VISUAL_CROSSING_API_KEY,
        'include': 'days'  # To get daily data
    }, timeout=60)

    # Check if the request was successful
    if response.status_code == 200:
        json_response: Dict = response.json()
        days: Dict = json_response['days'][0]
        weather_data: WeatherData = WeatherData(
            address=json_response['resolvedAddress'],
            description=days['description'],
            temperature=days['temp'],
            selected_date=days['datetime'])
        cache.set(cache_key, weather_data, timeout= 60 * 10) # cache for 10 minutes
        return weather_data
    if response.status_code == 400:
        return WeatherData("", "", 0, "", response.text)

    raise response.raise_for_status()
