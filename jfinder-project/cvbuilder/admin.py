from django.contrib import admin
from .models import ResumeSettings, ResumeCreationSessionModel, ResumeTemplate

# Register your models here.

admin.site.register([ResumeTemplate, ResumeSettings, ResumeCreationSessionModel])