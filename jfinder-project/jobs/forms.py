from django.forms import ModelMultipleChoiceField, Form
from django import forms
from .models import Tag


class TagListForm(Form):
    tags_list = ModelMultipleChoiceField(queryset=Tag.objects.all(), required=False, widget = forms.CheckboxSelectMultiple)
