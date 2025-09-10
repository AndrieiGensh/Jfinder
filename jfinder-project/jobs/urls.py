from django.urls import path
from .views import *

urlpatterns = [
    path('search/', SearchView.as_view(), name = "search"),
    path('job-details/<str:offer_id>', JobDetailsView.as_view(), name="job_details"),
    path('job-details-full', JobDetailsFullView.as_view(), name="job_details_full"),
    path('job-report/<str:offer_id>', ReportOfferModal.as_view(), name="job_report"),
    path('job-bookmark/<int:offer_id>', BookamrkOfferView.as_view(), name="job_bookmark"),
    path("job-apply/<int:id>", ApplicationCreateModal.as_view(), name="job_apply"),
    path('job-apply/internal-file-modal', ApplicationWithInternalFileModal.as_view(), name="application_internal_file_modal"),
    path('job-apply/external-file-modal', ApplicationWithExternalFileModal.as_view(), name="application_external_file_modal"),
]
