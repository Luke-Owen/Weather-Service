import unittest
from datetime import datetime
from unittest.mock import patch
from django.test import override_settings, TestCase
from requests.exceptions import HTTPError

from API.visual_crossing_api_service import get_weather_data, WeatherData

@override_settings(VISUAL_CROSSING_API_KEY='dummy_api_key')
@override_settings(CACHES = {
    "default": {
        "BACKEND": 'django.core.cache.backends.dummy.DummyCache',
    }
})
class VisualCrossingAPIServiceTests(TestCase):

    @patch('requests.get')
    def test_get_weather_data_returns_200_assert_instance(self, mock_get):
        # arrange
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'resolvedAddress': 'London, United Kingdom',
            'days': [
                {
                    'description': 'partly cloudy',
                    'temp': 17,
                    'datetime': '2024-09-21'
                }
            ]
        }

        # act
        weather_data = get_weather_data('London', datetime.now())

        # assert
        mock_get.assert_called_once()
        mock_response.json.assert_called_once()
        mock_response.raise_for_status.assert_not_called()
        self.assertIsInstance(weather_data, WeatherData)
        self.assertIs(weather_data.selected_date, '2024-09-21')
        self.assertIs(weather_data.address, 'London, United Kingdom')
        self.assertIs(weather_data.temperature, 17)
        self.assertIs(weather_data.description, 'partly cloudy')
        self.assertIs(weather_data.error_message, None)

    @patch('requests.get')
    def test_get_weather_data_returns_400_assert_returns_error_message(self, mock_get):
        # arrange
        mock_response = mock_get.return_value
        mock_response.status_code = 400
        mock_response.text = 'Bad Request'

        # act
        weather_data = get_weather_data('xxx Random place xxx', datetime.now())

        # assert
        mock_get.assert_called_once()
        mock_response.json.assert_not_called()
        mock_response.raise_for_status.assert_not_called()
        self.assertIsInstance(weather_data, WeatherData)
        self.assertIs(weather_data.selected_date, "")
        self.assertIs(weather_data.address, "")
        self.assertIs(weather_data.temperature, 0)
        self.assertIs(weather_data.description, "")
        self.assertIs(weather_data.error_message, "Bad Request")

    @patch('requests.get')
    def test_get_weather_data_returns_http_error_code_assert_error_raised(self, mock_get):
        # arrange
        mock_response = mock_get.return_value
        mock_response.status_code = 404
        mock_response.raise_for_status.side_effect = HTTPError("An error occurred")

        # act
        with self.assertRaises(HTTPError):
            get_weather_data('London', datetime.now())

        # assert
        mock_get.assert_called_once()
        mock_get.json.assert_not_called()
        mock_response.raise_for_status.assert_called_once()

if __name__ == '__main__':
    unittest.main()
