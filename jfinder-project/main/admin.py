from django.contrib import admin
from .models import Settings, UserProfile, CompanyProfile, PersonalLink, Document, Education, Experience

# Register your models here.

admin.site.register(
    [Settings, UserProfile, CompanyProfile, PersonalLink, Document, Education, Experience])
