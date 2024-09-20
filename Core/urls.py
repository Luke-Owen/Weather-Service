from typing import List
from . import views
from django.urls import path

urlpatterns: List = [
    path("", views.Index.as_view(), name="index")
]