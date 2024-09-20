from typing import List
from .Views import index
from django.urls import path

urlpatterns: List = [
    path("", index.Index.as_view(), name="index")
]