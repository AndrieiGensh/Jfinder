from django.urls import path
from .views import *

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('profile', ProfileView.as_view(), name='profile'),
    path('documents/<int:index>', DocumentView.as_view(), name="get_document"),
    path('education/', EducationCreateView.as_view(), name = 'education_create'),
]
