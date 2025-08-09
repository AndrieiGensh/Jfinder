from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate
from django import forms

from django.forms import Form, ValidationError

from .models import User


class CustomAuthenticationForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'autofocus': True}))
    password = forms.CharField(
        max_length=63, widget=forms.PasswordInput(attrs={'autofocus': True}))

    def clean(self):
        super(CustomAuthenticationForm, self).clean()
        email = self.cleaned_data.get('email')
        if email:
            self.user_cache = authenticate(
                username=email,
                password=self.cleaned_data.get('password')
            )
            if self.user_cache is None:
                raise forms.ValidationError(
                    'Invalid email or password'
                )
        return self.cleaned_data


class CustomRegistrationForm(forms.ModelForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'autofocus': True}), required=True)
    name = forms.CharField(
        max_length=63, widget=forms.TextInput(), required=True)
    password = forms.CharField(
        max_length=63, widget=forms.PasswordInput(attrs={'autofocus': True}), required=True)
    password_confirm = forms.CharField(
        max_length=63, widget=forms.PasswordInput(attrs={'autofocus': True}), required=True)
    is_organization = forms.BooleanField(
        required=False, initial=False, widget=forms.CheckboxInput())

    class Meta:
        model = User
        fields = (
            "name",
            "email",
            "is_organization",
            "password",
        )

    def clean(self):
        super(CustomRegistrationForm, self).clean()
        email = self.cleaned_data.get('email')
        if self.cleaned_data.get("password") != self.cleaned_data.get("password_confirm"):
            raise forms.ValidationError("Passwords do not match")
        return self.cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        print("user in save ", user)
        user.set_password(self.cleaned_data.get('password'))
        user.save()
        print('user after save and after commit and after pwd set ',
              user, user.password)
        return user


class PasswordChangeForm(Form):

    current_password = forms.CharField(max_length=30, min_length=8, required=True, widget=forms.PasswordInput(attrs= {'autofocus': True}))
    new_password = forms.CharField(max_length=30, min_length=8, required=True, widget=forms.PasswordInput(attrs= {'autofocus': True}))
    new_password_confirm = forms.CharField(max_length=30, min_length=8, required=True, widget=forms.PasswordInput(attrs= {'autofocus': True}))

    def __init__(self, user: User, data = None):
        self.user = user
        super(PasswordChangeForm, self).__init__(data)

    def clean_current_password(self):
        password = self.cleaned_data["current_password"]
        if not self.user.check_password(password):
            raise ValidationError("Invalid password")
    
    def clean(self):
        super().clean()
        if self.cleaned_data.get('new_password') != self.cleaned_data.get("new_password_confirm"):
            raise forms.ValidationError("New Password and Confirmed New Password must be the same")
        return self.cleaned_data
    

class EmailChangeForm(Form):

    password = forms.CharField(max_length=30, min_length=8, required=True, widget=forms.PasswordInput(attrs={'autofocus': True}))
    new_email = forms.EmailField(max_length=30, min_length=8, required=True, widget=forms.EmailInput(attrs={'autofocus': True}))

    def __init__(self, user: User, data = None):
        self.user = user
        super(EmailChangeForm, self).__init__(data)

    def clean_current_password(self):
        password = self.cleaned_data["password"]
        if not self.user.check_password(password):
            raise ValidationError("Invalid Password")
