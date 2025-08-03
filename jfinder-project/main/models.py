from django.db import models
import uuid

# Create your models here.

from jobs.models import COUNTRIES_CHOICES

PERSONAL_LINK_CHOICES = {
    'IN': "Instagram",
    'FB': "Facebook",
    'TT': "TickTock",
    'X': "X",
    'PW': "Personal Website",
}

DEGREE_CHOICES = {
    'BS': "Bachelor",
    'MA': "Masters",
    'PhD': "Doctor of Philosophy",
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
    skills = models.ManyToManyField('jobs.Skill', related_name="skills")
    accepting_offers = models.BooleanField(default=True)
    contact_info_phone = models.TextField(max_length=20, blank=True)
    address = models.TextField(max_length = 100, blank=True, default="Not specified")
    country_of_residence = models.TextField(choices = COUNTRIES_CHOICES, blank = True, default="Not Specified")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'id'], name='unique_user_profile'
            )
        ]

    def __str__(self):
        return str(self.id)


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

    def __str__(self):
        return str(self.id)


class Document(models.Model):
    name = models.TextField(max_length=50, null=False,
                            blank=False, default="New File")
    uploader = models.ForeignKey(
        'main.UserProfile', on_delete=models.CASCADE)
    file = models.FileField(upload_to=upload_document_path)

    def __str__(self):
        return self.name


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

    def __str__(self):
        return "{}'s Settings profile".format(self.id)


class PersonalLink(models.Model):

    profile = models.ForeignKey('main.UserProfile', on_delete=models.CASCADE)

    link = models.CharField(max_length=255, default="")
    media_type = models.TextField(choices=PERSONAL_LINK_CHOICES)


class Education(models.Model):

    profile = models.ForeignKey('main.UserProfile', on_delete=models.CASCADE)

    institution = models.CharField(max_length=100, null=False)
    specialization = models.CharField(max_length=100, null=False)
    startYear = models.DateField(null=False, blank=False)
    endYear = models.DateField(null=False, blank=False)
    ongoing = models.BooleanField(null=False, blank=True)
    degree = models.TextField(choices=DEGREE_CHOICES, default = 'BS')
    gpa = models.IntegerField(blank=True)
    diploma = models.ForeignKey('main.Document', on_delete=models.CASCADE, blank = True, null=True)
    comment = models.TextField(max_length=1000, blank=True)

    def __str__(self):
        return str(self.id)

    
class Experience(models.Model):

    profile = models.ForeignKey('main.UserProfile', on_delete=models.CASCADE)

    company = models.CharField(max_length=100, null=False)
    position = models.CharField(max_length=100, null=False)
    startYear = models.DateField()
    endYear = models.DateField()
    ongoing = models.BooleanField()
    description = models.TextField(max_length= 1000, null=False)
    duties = models.TextField(max_length=300, null=False)

    def __str__(self):
        return str(self.id)

