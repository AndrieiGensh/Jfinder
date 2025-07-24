from django.urls import path, include
from .views import *

urlpatterns = [
    path("", CVBuilderView.as_view(), name="cvbuilder"),
]
