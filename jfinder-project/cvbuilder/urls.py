from django.urls import path, include
from .views import *

urlpatterns = [
    path("", CVBuilderMenuView.as_view(), name="cvbuilder_menu"),
    path("editor", CVBuilderEditorView.as_view(), name = "cvbuilder_editor"),
    path("template-preview", CVBuilderTemplatePreview.as_view(), name="template_preview"),
]
