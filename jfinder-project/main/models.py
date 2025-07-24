from django.db import models
import uuid

# Create your models here.

PERSONAL_LINK_CHOICES = {
    'IN': "Instagram",
    'FB': "Facebook",
    'TT': "TickTock",
    'X': "X",
    'PW': "Personal Website",
}


def upload_profile_path(instance, filename):
    ext = filename.split('.')[-1]
    return 'profile_img/{0}/{1}'.format(uuid.uuid4(), ext)


def upload_document_path(instance, filename):
    ext = filename.split('.')[-1]
    return 'profile_img/{0}/{1}'.format(str(uuid.uuid4()) + filename.split('.')[-2], ext)


class UserProfile(models.Model):

    user = models.OneToOneField(
        'authentication.User', on_delete=models.CASCADE)

    biography = models.TextField(max_length=1000, null=True, blank=True)
    profile_img = models.ImageField(
        upload_to=upload_profile_path, blank=True, null=True)
    skills = models.ManyToManyField('jobs.Skill', )
    accepting_offers = models.BooleanField(default=True)
    contact_info_phone = models.TextField(max_length=20, blank=True)


class CompanyProfile(models.Model):

    user = models.OneToOneField(
        'authentication.User', on_delete=models.CASCADE)

    moto = models.TextField(max_length=100, blank=True, default="")
    employee_num = models.PositiveIntegerField()
    headquarters_address = models.TextField(
        max_length=100, blank=True, null=False)
    profile_img = models.ImageField(
        upload_to=upload_profile_path, blank=True, null=True)
    about_us = models.TextField(max_length=1000)


class Document(models.Model):
    name = models.TextField(max_length=50, null=False,
                            blank=False, default="New File")
    uploader = models.ForeignKey(
        'authentication.User', on_delete=models.CASCADE)
    file = models.FileField(upload_to=upload_document_path)


class Settings(models.Model):

    user = models.OneToOneField(
        'authentication.User', on_delete=models.CASCADE)

    dark_theme = models.BooleanField(default=False)
    newsletter_subscribed = models.BooleanField(default=False)
    offer_change_notification = models.BooleanField(default=True)
    contact_info_show = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'settings'
        verbose_name_plural = 'settings_set'


class PersonalLink(models.Model):

    user = models.ForeignKey('authentication.User', on_delete=models.CASCADE)

    link = models.CharField(max_length=255, default="")
    media_type = models.TextField(choices=PERSONAL_LINK_CHOICES)


class Education(models.Model):

    user = models.ForeignKey('authentication.User', on_delete=models.CASCADE)

    institution = models.CharField(max_length=100, null=False)
    specialization = models.CharField(max_length=100, null=False)
    startYear = models.DateField()
