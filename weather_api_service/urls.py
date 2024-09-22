"""url patterns for app"""
from typing import List
from django.contrib import admin
from django.urls import path, include

urlpatterns: List = [
    path('admin/', admin.site.urls),
    path('core/', include('core.urls')),
]
