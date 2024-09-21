import unittest
from datetime import datetime
from unittest.mock import patch
from django.test import override_settings, TestCase

from API.visual_crossing_api_service import get_weather_data, WeatherData

@override_settings(VISUAL_CROSSING_API_KEY='dummy_api_key')
@override_settings(CACHES = {
    "default": {
        "BACKEND": 'django.core.cache.backends.dummy.DummyCache',
    }
})
class VisualCrossingAPIServiceCachingTests(TestCase):
    @patch('requests.get')
    @patch('django.core.cache.backends.dummy.DummyCache')
    def test_get_weather_data_assert_cache_miss(self, mock_cache, mock_get):
        # arrange
        mock_cache_instance = mock_cache.return_value
        mock_cache_instance.get.return_value = None
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = self.mock_json_data

        # act
        get_weather_data('London', datetime.now())

        # assert
        mock_cache_instance.get.assert_called_once()
        mock_cache_instance.set.assert_called_once()

    @patch('requests.get')
    @patch('django.core.cache.backends.dummy.DummyCache')
    def test_get_weather_data_assert_cache_hits(self, mock_cache, mock_get):
        # arrange
        mock_cache_instance = mock_cache.return_value
        mock_cache_instance.get.return_value = {'London_2024-09-21': WeatherData}
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = self.mock_json_data

        # act
        get_weather_data('London', datetime.now())

        # assert
        mock_cache_instance.get.assert_called_once()
        mock_cache_instance.set.assert_not_called()

        mock_cache_instance.get.return_value = None

    mock_json_data = {
            'resolvedAddress': 'London, United Kingdom',
            'days': [
                {
                    'description': 'partly cloudy',
                    'temp': 17,
                    'datetime': '2024-09-21'
                }
            ]
        }


if __name__ == '__main__':
    unittest.main()
