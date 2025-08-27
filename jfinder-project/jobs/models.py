from django.db import models
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.fields import ArrayField
from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
import uuid

# Create your models here.

class CountriesChoices(models.TextChoices):
    POLAND = 'PL', _('Poland')
    UKRAINE = 'UA', _('Ukraine')
    RUSSIA = 'RU', _('Russia')
    BULGARIA = 'BG', _('Bulgaria')
    USA = 'US', _('United States')


class ReportDecisionChoices(models.TextChoices):
    PENDING = 'PR', _('Pending Review')
    DETECTED = 'VD', _('Violation Detected')
    NOT_DETECTED = 'VND', _('Violation Not Detected')
    WARNING = 'VMW', _('Violation - Minor, Warning')


class WorkModeChoices(models.TextChoices):
    HYBRID = 'HB', _('Hybrid')
    OFFICE = 'OF', _('From Office')
    HOME = 'HO', _('From Home')


class SalaryModeChoices(models.TextChoices):
    HOURLY = 'H', _('Hourly')
    MONTHLY = 'M', _('Monthly')


class ApplicationStatusChoices(models.TextChoices):
    PENDING = 'P', _('Pending')
    ABANDONED = 'A', _('Abandoned')
    SUCCESS = 'S', _('Success')
    REJECTED = 'R', _('Rejected')


def upload_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = 'tag_icons/{0}.{1}'.format(uuid.uuid4(), ext)
    return filename


class Benefit(models.Model):

    title = models.CharField(max_length=200, blank=False, null=False, unique=True)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = _("benefit")
        verbose_name_plural = _("benefits")

    def save(self, *args, **kwargs):
        new_slug = slugify(self.title, allow_unicode=True)
        if not self.slug or self.slug != new_slug:
            if Benefit.objects.filter(slug=new_slug):
                self.slug = new_slug + str(uuid.uuid4())
            else:
                self.slug = new_slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    
@receiver(post_save, sender = Benefit)
def sync_offer_benefits_slug_on_change(sender, instance, **kwargs):
    offers = instance.offers.all()
    for offer in offers:
        offer.update_benefits_slug()


class Tag(models.Model):

    title = models.CharField(max_length=50, blank=False,
                            null=False, unique=True)
    icon = models.ImageField(upload_to=upload_file_path, blank=True, null=True)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = _("tag")
        verbose_name_plural = _("tags")

    def save(self, *args, **kwargs):
        new_slug = slugify(self.title, allow_unicode=True)
        if not self.slug or self.slug != new_slug:
            if Tag.objects.filter(slug=new_slug):
                self.slug = new_slug + str(uuid.uuid4())
            else:
                self.slug = new_slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    
@receiver(post_save, sender = Tag)
def sync_offer_tags_slug_on_change(sender, instance, **kwargs):
    offers = instance.offers.all()
    for offer in offers:
        offer.update_tags_slug()


class Skill(models.Model):
    title = models.CharField(max_length=50, null=False, blank=False, unique=True)
    is_custom = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=["title"])
        ]

    def __str__(self):
        return self.title


class Offer(models.Model):

    created_by = models.ForeignKey(
        'authentication.User', on_delete=models.DO_NOTHING, related_name="offer_creator")

    created_date = models.DateField(auto_now_add=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    max_candidates = models.IntegerField(default=1)

    company_name = models.CharField(max_length=100, blank=False, null=False, default = 'Company Sp. z o. o.')

    location_country = models.CharField(max_length=2, choices=CountriesChoices.choices)
    location_city = models.CharField(max_length=100, blank=True)

    title = models.CharField(max_length=100, blank=False)
    description = models.TextField(blank=False)

    requirements = models.TextField(blank=False)
    nice_to_have = models.TextField(blank=True)

    work_mode = models.CharField(max_length=2, choices=WorkModeChoices.choices)

    salary_mode = models.CharField(max_length=1, choices=SalaryModeChoices.choices, blank=False, default=SalaryModeChoices.MONTHLY)

    is_salary_brutto = models.BooleanField(default=True, blank=False)
    min_salary = models.IntegerField(blank=False)
    max_salary = models.IntegerField(blank=False)

    applicants = models.ManyToManyField(
        'authentication.User', through="Application", related_name="offers_applied")
    people_interested = models.ManyToManyField(
        'authentication.User', through="dashboard.Bookmark", related_name="offers_bookmarked")
    
    benefits = models.ManyToManyField('jobs.Benefit', related_name="offers_with_benefit")
    benefits_slug = ArrayField(
        models.CharField(),
        blank=True,
        default=list
    )
    
    tags = models.ManyToManyField('jobs.Tag', related_name="offers_with_tags")
    tags_slug = ArrayField(
        models.CharField(),
        blank=True,
        default=list
    )

    class Meta:
        indexes = [
            GinIndex(fields=['tags_slug']),
            GinIndex(fields=["benefits_slug"]),
            models.Index(fields=["min_salary", "max_salary", "salary_mode"]),
            models.Index(fields=["location_country", "location_city", "work_mode"]),
        ]

    def clean(self):
        if self.start_date > self.end_date:
            raise ValidationError(
                _("Offer's start date can not be after the end date"))
        if self.min_salary > self.max_salary:
            raise ValidationError(
                _("Minimum salary offer can not be more then maximun salary offer"))
        if self.min_salary <= 0 or self.max_salary <= 0:
            raise ValidationError(
                _("Salary can not be negative or equal to 0"))
        if self.work_mode in ["HB", "OF"] and not self.location_city:
            raise ValidationError(
                _("For Hybrid and Office employment the location city can not be unspecified"))
        
    def update_tags_slug(self, save = True):
        self.tags_slug = list(self.tags.values_list("slug",flat=True))
        if save:
            self.save(update_fields=["tags_slug"])

    def update_benefits_slug(self, save = True):
        self.benefits_slug = list(self.benefits.values_list("slug", flat=True))
        if save:
            self.save(update_fields=["benefits_slug"])
        
    def __str__(self):
        return self.title
    

@receiver(m2m_changed, sender=Offer.tags.through)
def sync_tags_slug_on_add_delete(sender, instance, **kwargs):
    instance.update_tags_slug()

@receiver(m2m_changed, sender=Offer.benefits.through)
def sync_benefits_slug_on_add_delete(sender, instance, **kwargs):
    instance.update_benefits_slug()


class Application(models.Model):

    applicant = models.ForeignKey(
        'authentication.User', on_delete=models.DO_NOTHING)
    position = models.ForeignKey('jobs.Offer', on_delete=models.DO_NOTHING)
    date = models.DateTimeField(auto_now_add=True, blank=False)
    status = models.CharField(max_length=1,choices=ApplicationStatusChoices.choices, default=ApplicationStatusChoices.PENDING)
    supplied_cv = models.ForeignKey('main.Document', on_delete=models.SET_NULL, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["applicant", "position"], name='unique_user_application')
        ]

    def __str__(self):
        return f"{self.applicant} -> {self.position} ({self.get_status_display()})"


class Report(models.Model):

    reported_by = models.ForeignKey('authentication.User', blank = False, on_delete=models.CASCADE)
    offer = models.ForeignKey('jobs.Offer', blank = False, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    processed = models.BooleanField(default = False)
    decision = models.CharField(max_length=3, choices=ReportDecisionChoices.choices, default=ReportDecisionChoices.PENDING)

    class Meta:
        verbose_name = _("report")
        verbose_name_plural = _("reports")

    def __str__(self):
        return f"Report({self.offer.title} - {self.date})"

    def get_absolute_url(self):
        return reverse("report_detail", kwargs={"pk": self.pk})
