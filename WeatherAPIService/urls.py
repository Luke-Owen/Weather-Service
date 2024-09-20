from typing import List
from django.contrib import admin
from django.urls import path, include

urlpatterns: List = [
    path('admin/', admin.site.urls),
    path('Core/', include('Core.urls')),
]
