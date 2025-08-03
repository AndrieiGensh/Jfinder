from django.db import models
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
import uuid

# Create your models here.

COUNTRIES_CHOICES = {
    'PL': 'Poland',
    'UA': 'Ukraine',
    'RU': 'Russia',
    'BG': 'Bulgaria',
    'US': 'United States',
}

REPORT_DECISION_CHOICES = {
    'PR': 'Pending Review',
    'VD': 'Violation Detected',
    'VND': 'Violation Not Detected',
    'VMW': 'Violation - Minor, Warning',
}


def upload_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = 'tag_icons/{0}.{1}'.format(uuid.uuid4(), ext)
    return filename


class Benefit(models.Model):

    title = models.TextField(max_length=200, blank=False, null=False)

    class Meta:
        verbose_name = "benefit"
        verbose_name_plural = "benefits"

    def __str__(self):
        return self.title


class Tag(models.Model):

    name = models.TextField(max_length=50, blank=False,
                            null=False, unique=True)
    icon = models.ImageField(upload_to=upload_file_path, blank=True, null=True)

    class Meta:
        verbose_name = "tag"
        verbose_name_plural = "tags"

    def __str__(self):
        return self.name


class Skill(models.Model):
    title = models.CharField(max_length=50, null=False, blank=False)
    is_custom = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Offer(models.Model):

    created_by = models.ForeignKey(
        'authentication.User', on_delete=models.DO_NOTHING, related_name="offer_creator")

    created_date = models.DateField(auto_now_add=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    max_candidates = models.IntegerField(default=1)
    company_name = models.TextField(max_length=100, blank=False, null=False, default = 'Company Sp. z o. o.')
    title = models.TextField(max_length=100, blank=False)
    location_country = models.TextField(choices=COUNTRIES_CHOICES)
    location_city = models.TextField(max_length=100, blank=True)
    description = models.TextField(max_length=1000, blank=False)
    requirements = models.TextField(max_length=1000, blank=False)
    nice_to_have = models.TextField(max_length=1000, blank=True)
    work_mode = models.TextField(choices={
        'HB': 'Hybrid',
        'OF': 'From Office',
        'HO': 'From Home',
    })

    salary_mode = models.TextField(choices={
        'H': 'Hourly',
        'M': 'Monthly',
    }, blank=False, default='M')
    brutto_flag = models.BooleanField(default=True, blank=False)
    min_salary_offer = models.IntegerField(blank=False)
    max_salary_offer = models.IntegerField(blank=False)

    benefits = models.ManyToManyField('jobs.Benefit')
    applicants = models.ManyToManyField(
        'authentication.User', through="Application", related_name="offer_applicants")
    people_interested = models.ManyToManyField(
        'authentication.User', through="dashboard.Bookmark", related_name="offer_bookmarked_by")
    tags = models.ManyToManyField('jobs.Tag')

    def clean(self):
        if self.start_date > self.end_date:
            raise ValidationError(
                _("Offer's start date can not be before the end date"))
        if self.min_salary_offer > self.max_salary_offer:
            raise ValidationError(
                _("Minimum salary offer can not be more then maximun salary offer"))
        if (self.work_mode != 'HO' or self.work_mode != 'From Home') and self.location_city is None:
            raise ValidationError(
                _("For Hybrid and Office employment the location cith can not be unspecified"))
        
    def __str__(self):
        return self.title


class Application(models.Model):

    applicant = models.ForeignKey(
        'authentication.User', on_delete=models.DO_NOTHING)
    position = models.ForeignKey('jobs.Offer', on_delete=models.DO_NOTHING)
    date = models.DateTimeField(blank=False)
    status = models.TextField(choices={
        'P': 'Pending',
        'A': 'Abandoned',
        'S': 'Success',
        'R': 'Rejected',
    }, default='P')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["applicant", "position"], name='unique_user_application')
        ]


class Report(models.Model):

    reported_by = models.ForeignKey('authentication.User', blank = False, on_delete=models.CASCADE)
    offer = models.ForeignKey('jobs.Offer', blank = False, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    processed = models.BooleanField(default = False)
    decision = models.TextField(choices=REPORT_DECISION_CHOICES, default="PR")

    class Meta:
        verbose_name = _("report")
        verbose_name_plural = _("reports")

    def __str__(self):
        return 'Report-for-{}-dated-at-{}'.format(self.offer, self.date)

    def get_absolute_url(self):
        return reverse("Report_detail", kwargs={"pk": self.pk})
