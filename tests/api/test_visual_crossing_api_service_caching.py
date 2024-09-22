"""imports for api service cache tests"""
import unittest
from datetime import datetime
from unittest.mock import patch
from django.test import override_settings, TestCase
from api.visual_crossing_api_service import get_weather_data, WeatherData
from tests.api.helper.data import mock_json_data

@override_settings(VISUAL_CROSSING_API_KEY='dummy_api_key')
@override_settings(CACHES = {
    "default": {
        "BACKEND": 'django.core.cache.backends.dummy.DummyCache',
    }
})
class TestVisualCrossingAPIServiceCachingMissTest(TestCase):
    """test get_weather_data cache miss function"""
    @patch('requests.get')
    @patch('django.core.cache.backends.dummy.DummyCache')
    def test_get_weather_data_assert_cache_miss(self, mock_cache, mock_get):
        """test get_weather_data with cache miss"""
        # arrange
        mock_cache_instance = mock_cache.return_value
        mock_cache_instance.get.return_value = None
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = mock_json_data

        # act
        get_weather_data('London', datetime.now())

        # assert
        mock_cache_instance.get.assert_called_once()
        mock_cache_instance.set.assert_called_once()

class TestVisualCrossingAPIServiceCachingHitTest(TestCase):
    """test get_weather_data cache hit function"""
    @patch('requests.get')
    @patch('django.core.cache.backends.dummy.DummyCache')
    def test_get_weather_data_assert_cache_hits(self, mock_cache, mock_get):
        """test get_weather_data cache hit success"""
        # arrange
        mock_cache_instance = mock_cache.return_value
        mock_cache_instance.get.return_value = {'London_2024-09-21': WeatherData}
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = mock_json_data

        # act
        get_weather_data('London', datetime.now())

        # assert
        mock_cache_instance.get.assert_called_once()
        mock_cache_instance.set.assert_not_called()

        mock_cache_instance.get.return_value = None

if __name__ == '__main__':
    unittest.main()