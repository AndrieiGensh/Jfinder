from django.urls import path, include
from .views import *

urlpatterns = [
    path("", CVBuilderMenuView.as_view(), name="cvbuilder_menu"),
    path("editor", CVBuilderEditorView.as_view(), name = "cvbuilder_editor"),
    path("template-preview", CVBuilderTemplatePreview.as_view(), name="template_preview"),
    path("editor-create-entity", CVBuilderEditorCreateEntity.as_view(), name="editor_create_entity"),
    path("editor-delete-entity", CVBuilderEditorDeleteEntity.as_view(), name="editor_delete_entity"),
    path("editor-edit-entity", CVBuilderEditorEditEntity.as_view(), name="editor_edit_entity"),
    path("editor-sections-conteiner", CVBuilderEditorSectionsContainer.as_view(), name="editor_sections_container"),
]
