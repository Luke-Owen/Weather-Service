"""module handles tests for visual crossing service."""

import unittest
from datetime import datetime
from unittest.mock import patch
from django.test import override_settings, TestCase
from requests.exceptions import HTTPError
from api.visual_crossing_api_service import get_weather_data, WeatherData
from tests.api.helper.data import mock_json_data

@override_settings(VISUAL_CROSSING_API_KEY='dummy_api_key')
@override_settings(CACHES = {
    "default": {
        "BACKEND": 'django.core.cache.backends.dummy.DummyCache',
    }
})
class TestVisualCrossingAPIService(TestCase):
    """class handles unit tests for visual crossing api service"""
    @patch('requests.get')
    def test_get_weather_data_returns_200_assert_instance(self, mock_get):
        """test get_weather_data returns 200 OK"""
        # arrange
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = mock_json_data

        # act
        weather_data = get_weather_data('London', datetime.now())

        # assert
        mock_get.assert_called_once()
        mock_response.json.assert_called_once()
        mock_response.raise_for_status.assert_not_called()
        self.assertIsInstance(weather_data, WeatherData)
        self.assertEqual(weather_data.selected_date, '2024-09-21')
        self.assertEqual(weather_data.address, 'London, United Kingdom')
        self.assertEqual(weather_data.temperature, 17)
        self.assertEqual(weather_data.description, 'partly cloudy')
        self.assertEqual(weather_data.error_message, None)

    @patch('requests.get')
    def test_get_weather_data_returns_400_assert_returns_error_message(self, mock_get):
        """test get_weather_data returns 400 error with message"""
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
        """test get_weather_data raises HTTPError"""
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
