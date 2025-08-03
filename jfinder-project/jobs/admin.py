from django.contrib import admin
from .models import Offer, Skill, Tag, Benefit, Report

# Register your models here.

admin.site.register([Offer, Skill, Tag, Benefit, Report])
