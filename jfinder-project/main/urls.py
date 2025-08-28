from django.urls import path
from .views import *

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('profile', ProfileView.as_view(), name='profile'),
    path('documents/<int:index>', DocumentView.as_view(), name="get_document"),
    path('education/create', EducationCreateView.as_view(), name = 'education_create'),
    path('education/update/<int:pk>', EducationUpdateView.as_view(), name = 'education_update'),
    path('education/delete/<int:pk>', EducationDeleteView.as_view(), name = 'education_delete'),
    path('experience/create', ExperienceCreateView.as_view(), name = 'experience_create'),
    path('experience/update/<int:pk>', ExperienceUpdateView.as_view(), name = 'experience_update'),
    path('experience/delete/<int:pk>', ExperienceDeleteView.as_view(), name = 'experience_delete'),
]
