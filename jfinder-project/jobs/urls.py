from django.urls import path
from .views import *

urlpatterns = [
    path('search/', SearchView.as_view(), name = "search"),
    path('job-details/<str:offer_id>', JobDetailsView.as_view(), name="job_details"),
    path('job-report/<str:offer_id>', ReportOfferModal.as_view(), name="job_report"),
    path('job-bookmark/<int:offer_id>', BookamrkOfferView.as_view(), name="job_bookmark"),
]
