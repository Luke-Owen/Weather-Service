"""module handle core url patterns"""
from typing import List
from django.urls import path
from .views import index

urlpatterns: List = [
    path("", index.Index.as_view(), name="index")
]
