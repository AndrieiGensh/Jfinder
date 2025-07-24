from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate
from django import forms

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
