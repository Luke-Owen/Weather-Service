"""module handles requests made from app index view"""
from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django_ratelimit.decorators import ratelimit
import api.visual_crossing_api_service
from api.visual_crossing_api_service import WeatherData


class Index(View):
    """class handles requests made from app index view"""
    template_name = "core/index.html"

    @method_decorator(ratelimit(key='ip', rate='5/s', block=True, method='GET'))
    def get(self, request) -> HttpResponse:
        """get weather data from visual crossing api"""
        location: str = request.GET.get('location', 'London')
        selected_date: str = request.GET.get('selected_date', None)

        if selected_date is None:
            weather_data: WeatherData = api.visual_crossing_api_service.get_weather_data(location, datetime.now())
        else:
            date: datetime = datetime.strptime(selected_date, '%Y-%m-%d')
            weather_data: WeatherData = api.visual_crossing_api_service.get_weather_data(location, date)

        return render(request, self.template_name, {'weather_data': weather_data})
