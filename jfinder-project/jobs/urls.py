from django.urls import path
from .views import *

urlpatterns = [
    path('search/', SearchView.as_view(), name = "search"),
    path('job-details/<str:index>', JobDetailsView.as_view(), name="job_details"),
]
