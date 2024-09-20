from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

import API.visual_crossing_api_service


class Index(View):
    template_name = "Core/index.html"

    def get(self, request) -> HttpResponse:
        weather_data = API.visual_crossing_api_service.get_weather_data("London", datetime.now())
        return render(request, self.template_name, {'weather_data': weather_data})