from django import forms
from main.models import Document, Education, Experience, DEGREE_CHOICES
from django.forms import ValidationError
from django.utils.translation import gettext_lazy as _

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ["file"]

    def clean_file(self):

        file = self.cleaned_data.get('file')

        if not file.name.lower().endswith(".pdf"):
            raise ValidationError("File must be .pdf")
        if file.size > 5 * 1024 * 1024:
            raise ValidationError("Max file size must be 5MB.")
        if file.content_type != "application/pdf":
            raise ValidationError("Uploaded file is not a valid pdf file")
        
        return file

class EducationForm(forms.ModelForm):
    specialization = forms.CharField(
        widget=forms.TextInput, 
        required=True,
    )
    institution = forms.CharField(
        widget=forms.TextInput, 
        required=True,
    )
    start_year = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"}),
        required=True
    )
    end_year = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"}),
        required=False
    )
    ongoing = forms.BooleanField(
        widget=forms.CheckboxInput,
        required=False
    )
    degree = forms.ChoiceField(
        choices=DEGREE_CHOICES,
        widget=forms.Select,
        required=True
    )
    gpa = forms.IntegerField(
        widget=forms.NumberInput,
        required=False
    )

    class Meta:
        model = Education
        fields = [
            "institution",
            "specialization",
            "start_year",
            "end_year",
            "ongoing",
            "degree",
            "gpa",
        ]

    def clean(self):
        cd = self.cleaned_data

        start_year = cd.get("start_year")
        end_year = cd.get("end_year")
        ongoing = cd.get("ongoing")

        if ongoing:
            self.cleaned_data["end_year"] = None
        else:
            if not end_year:
                raise ValidationError(_("End year is required if the education is not ongoing"))
            if end_year and start_year and end_year > start_year:
                raise ValidationError(_("End Year can noy be before Start Year"))
        
        return cd
    

class ExperienceForm(forms.Form):

    company = forms.CharField(widget=forms.TextInput, required = True)
    position = forms.CharField(widget=forms.TextInput, required = True)
    start_year = forms.DateField(widget=forms.DateInput(attrs={"type":"date"}))
    end_year = forms.DateField(widget=forms.DateInput(attrs={"type":"date"}))
    ongoing = forms.BooleanField(widget=forms.CheckboxInput, required=False)
    description = forms.CharField(widget=forms.TextInput, required = True)
    duties = forms.CharField(widget=forms.Textarea, required = True)

    class Meta:
        model = Experience
        fields = [
            "company", "position", "start_year", "end_year", "ongoing", "description", "duties"
        ]

    def clean(self):
        cd = self.cleaned_data

        start_year = cd.get("start_year")
        end_year = cd.get("end_year")
        ongoing = cd.get("ongoing")

        if ongoing:
            self.end_year["end_year"] = None
        else:
            if not end_year:
                raise ValidationError(_("End year is required if this position is not ypur current occupation"))
            if end_year and start_year and end_year > start_year:
                raise ValidationError(_("End Year can noy be before Start Year"))
        
        return cd
        


