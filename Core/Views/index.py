from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django_ratelimit.decorators import ratelimit
import API.visual_crossing_api_service
from API.visual_crossing_api_service import WeatherData


class Index(View):
    template_name = "Core/index.html"

    @method_decorator(ratelimit(key='ip', rate='5/s', block=True, method='GET'))
    def get(self, request) -> HttpResponse:
        location: str = request.GET.get('location', 'London')
        selected_date: str = request.GET.get('selected_date', None)

        if selected_date is None:
            weather_data: WeatherData = API.visual_crossing_api_service.get_weather_data(location, datetime.now())
        else:
            date: datetime = datetime.strptime(selected_date, '%Y-%m-%d')
            weather_data: WeatherData = API.visual_crossing_api_service.get_weather_data(location, date)

        return render(request, self.template_name, {'weather_data': weather_data})