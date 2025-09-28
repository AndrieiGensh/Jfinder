from django.forms import Form, ModelForm, ValidationError
from django.utils.translation import gettext_lazy as _
from django import forms
from django.db.models import TextChoices
from .models import ResumeCreationSessionModel

class LanguageMasteryChoices(TextChoices):

    BEGINNER = 'A1', _("Beginner")
    ELEMENTARY = 'A2', _("Elementary")
    INTERMEDIATE = 'B1', _("Intermediate")
    UPPER_INTERMEDIATE = 'B2', _("Upper Intermediate")
    ADVANCED = 'C1', _("Advanced")
    PROFICIENCY = 'C2', _("Proficiency")


class HeaderForm(Form):

    name = forms.CharField(widget=forms.TextInput, required=True)
    phone = forms.CharField(widget=forms.TextInput, required=False)
    email = forms.EmailField(widget=forms.EmailInput, required=True)
    about = forms.CharField(widget=forms.Textarea, required=False)


class EducationForm(Form):

    university = forms.CharField(widget=forms.TextInput, required = True)
    degree = forms.CharField(widget=forms.TextInput, required = True)
    study = forms.CharField(widget=forms.TextInput, required = True)
    study_description = forms.CharField(widget=forms.Textarea, required = False)
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'},), required = True)
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'},), required = False)
    ongoing = forms.BooleanField(required=False)

    def clean(self):
        super().clean()
        start_date = self.cleaned_data.get("start_date")
        end_date = self.cleaned_data.get("end_date")
        ongoing = self.cleaned_data.get("ongoing")

        if not ongoing:
            if not end_date:
                raise ValidationError(_("End date must be provided"))
            if start_date >= end_date:
                raise ValidationError(_("Start date can not be after or equal to end date"))
            

class ExperienceForm(Form):

    company = forms.CharField(widget=forms.TextInput, required = True)
    company_description = forms.CharField(widget=forms.Textarea, required = True)
    position = forms.CharField(widget=forms.TextInput, required = True)
    position_description = forms.CharField(widget=forms.Textarea, required = False)
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'},), required = True)
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'},), required = False)
    ongoing = forms.BooleanField(required=False)

    def clean(self):
        super().clean()
        start_date = self.cleaned_data.get("start_date")
        end_date = self.cleaned_data.get("end_date")
        ongoing = self.cleaned_data.get("ongoing")

        if not ongoing:
            if not end_date:
                raise ValidationError(_("End date must be provided"))
            if start_date >= end_date:
                raise ValidationError(_("Start date can not be after or equal to end date"))
        self.cleaned_data["start_date"] = str(self.cleaned_data.get("start_date"))
        self.cleaned_data["end_date"] = str(self.cleaned_data.get("end_date"))
            

class SkillForm(Form):

    title = forms.CharField(widget=forms.TextInput, required = True)


class LanguageForm(Form):

    title = forms.CharField(widget=forms.TextInput, required = True)
    mastery = forms.ChoiceField(widget=forms.Select, choices=LanguageMasteryChoices, required=True)


class ProjectForm(Form):

    title = forms.CharField(widget=forms.TextInput, required = True)
    link = forms.CharField(widget=forms.TextInput, required = False)
    description = forms.CharField(widget=forms.Textarea, required = True)

