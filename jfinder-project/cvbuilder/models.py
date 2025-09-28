from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from django.utils.translation import gettext_lazy as _

from uuid import uuid4

def upload_cv_profile_image_path(instance, filename):
    return f"cv_image/{uuid4()}.{filename.split(".")[-1]}"

# Create your models here.

class ResumeStatusChoices(models.TextChoices):
    SAVED = 'SV', _('Saved progress')
    UNFINISHED = 'UF', _('Unfinished work')

class ResumeCreationSessionModel(models.Model):

    name = models.TextField(max_length=100, blank = True, null = False, default = "New CV building session")

    user = models.ForeignKey('authentication.User', on_delete=models.CASCADE, unique=False)
    document = models.ForeignKey('main.Document', on_delete=models.SET_NULL, null=True, blank=True)

    last_edited = models.DateTimeField(auto_now_add=True, null=False)
    status = models.TextField(choices=ResumeStatusChoices.choices, default = ResumeStatusChoices.UNFINISHED)

    settings = models.ForeignKey('cvbuilder.ResumeSettings', on_delete = models.SET_NULL, blank = True, null = True)
    template = models.ForeignKey('cvbuilder.ResumeTemplate', on_delete=models.SET_NULL, blank=True, null=True)

    image = models.ImageField(upload_to=upload_cv_profile_image_path)

    content_config = models.JSONField(blank = True, null = True)


@receiver(pre_save, sender=ResumeCreationSessionModel)
def resume_pre_save(sender, instance, **kwargs):
    if not instance.settings:
        instance.settings = ResumeSettings.objects.get_or_create(
            config = {
                'font_size': 10,
            }
        )[0]
    if not instance.template:
        instance.template = ResumeTemplate.objects.get_or_create(
            structure = """
                Something here.
            """
        )[0]
    if not instance.content_config:
        instance.content_config = {
            "name": {"show": True, "data": "John Doe"},
            "phone": {"show": True, "data": "123456789"},
            "email": {"show": True, "data": "test@gmail.com"},
            "about": {"show": True, "data": "Soemthext about here"},
            "education": {
                "show": True,
                "data": {
                    "1": {
                        "show": True,
                        "data": {
                            "university": "John Doe",
                            "study": "+123456789",
                            "study_description": "example@gmail.com",
                            "degree": "Bachelor",
                            "start_date": "Some text here",
                            "end_date": "Some text",
                            "ongoing": True,
                        },
                    },
                }
            },
            "experience": {
                "show": True,
                "data": {},
            },
            "soft_skills": {
                "show": True,
                "data": {},
            },
            "hard_skills": {
                "show": True,
                "data": {},
            },
            "projects": {
                "show": True,
                "data": {},
            },
            "languages": {
                "show": True,
                "data": {},
            },
            "custom_sections": {
                "show": True,
                "data": {},
            },
        }
    
class ResumeSettings(models.Model):

    user = models.OneToOneField('authentication.User', on_delete=models.CASCADE, blank = True, null = True)
    config = models.JSONField(blank = False, null = False)


class ResumeTemplate(models.Model):

    name = models.CharField(max_length=50, null = False, blank = False, default = "Template")
    structure = models.TextField(blank = False, null = False) # maybe there is a better way to save a latex template definition




