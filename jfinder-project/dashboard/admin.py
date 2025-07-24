from django.contrib import admin
from .models import Message, Bookmark

# Register your models here.

admin.site.register([Message, Bookmark])
