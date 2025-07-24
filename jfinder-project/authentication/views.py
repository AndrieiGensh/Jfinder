from django.shortcuts import render, redirect, resolve_url
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model, authenticate, login
from django.views.generic.base import View
from django.conf import settings

from .tasks import send_greeting_email

from .forms import CustomAuthenticationForm, CustomRegistrationForm

# Create your views here.


class LoginView(View):

    template_name = "authentication/login.html"
    authentication_form = CustomAuthenticationForm

    def post(self, request):
        form = self.authentication_form(request.POST)
        print(form.data)
        if form.is_valid():
            print('login form valid')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(
                username=email, password=password)
            print("auth ", user.password, user)
            if user is not None:
                login(request, user)
                return redirect('/dashboard')

    def get(self, request):
        send_greeting_email(settings.RECIPIENT_ADDRESS)
        return render(request, "authentication/login.html", context={'form': self.authentication_form()})


class PasswordResetModal(View):

    def get(self, request):
        return render(request, 'authentication/forgot_password_modal.html', context={})


class RegisterView(View):

    template_name = 'authentication/register.html'
    registration_form = CustomRegistrationForm

    def get(self, request):
        return render(request, self.template_name, context={'form': self.registration_form()})

    def post(self, request):
        form = self.registration_form(request.POST)
        print(form.data)
        if form.is_valid():
            print("form is valid")
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password_1")
            name = form.cleaned_data.get("name")
            is_organization = form.cleaned_data.get("is_organization")
            user = form.save()
            print(user)
            if user is not None:
                print(user.password)
                result = login(request, user)
                send_greeting_email(settings.RECIPIENT_ADDRESS)
                return redirect('/dashboard')
        print('form is not valid', form.errors)
        # return render(request, self.template_name, context={'form':self.registration_form()})
