from django.forms import Form, ModelForm
from .models import ResumeCreationSessionModel

class CVForm(ModelForm):

    class Meta:
        fileds = [
            "template",
            "image",
            "content_config",
        ]