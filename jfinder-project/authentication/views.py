from django.http import HttpResponse
from django.shortcuts import render, redirect, resolve_url
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model, authenticate, login
from django.views.generic.base import View
from django.conf import settings
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.sites.shortcuts import get_current_site

from .tasks import send_greeting_email, process_email_change_request, process_forgotten_password_reset_request

from .forms import CustomAuthenticationForm, CustomRegistrationForm, PasswordChangeForm, EmailChangeForm, ForgottenPasswordEmailForm, ForgottenPasswordResetForm

from .utils import check_uuid_and_token

from .models import User


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
        return render(request, "authentication/login.html", context={'form': self.authentication_form()})


class PasswordResetModal(View):

    template = 'authentication/forgot_password_modal.html'
    email_form = ForgottenPasswordEmailForm

    def get(self, request):
        form = self.email_form()
        context = {
            'form': form,
        }
        return render(request, self.template, context=context)
    
    def post(self, request):

        form = self.email_form(request.POST)

        if form.is_valid():
            print("valid")
            request_secure = request.is_secure()
            domain = get_current_site(request).domain
            process_forgotten_password_reset_request.delay(request_secure, domain, form.cleaned_data['email'])  
        print("invalid")      
        return HttpResponse('An email with instruction has been sent to your mailbox')



class RegisterView(View):

    template_name = 'authentication/register.html'
    registration_form = CustomRegistrationForm

    def get(self, request):
        return render(request, self.template_name, context={'form': self.registration_form()})

    def post(self, request):
        form = self.registration_form(request.POST)
        print(form.data)
        if form.is_valid():
            user = form.save()
            print(user)
            if user is not None:
                #create user's profile automatically
                from main.models import UserProfile
                user_profile = UserProfile(user=user)
                user_profile.save()
                result = login(request, user)
                send_greeting_email(settings.RECIPIENT_ADDRESS)
                return redirect('/dashboard')
        print('form is not valid', form.errors)
        # return render(request, self.template_name, context={'form':self.registration_form()})


class ChangeEmailView(View):

    email_change_form = EmailChangeForm

    def get(self, request, uuidb64: str, token: str):
        check_status, user = check_uuid_and_token(request, uuidb64, token)
        if check_status:
            # if yes - then set the new email to the user
            from authentication.models import UserEmailChangeRequestModel
            qs = UserEmailChangeRequestModel.objects.filter(user = user, validation_token = token).first()

            print(qs)

            if qs is not None:
                new_email = qs.new_email
                user.email = new_email
                user.is_email_confirmed = True
                user.save()

                return redirect('/dashboard')
            else:
                # it means that either the user has not created a request, or that the request has not been created (which is unlikely)
                # or that user has submitted sevvera emails for the validation and only the most recent request has been saved in db
                return HttpResponse("There is no record of request for this email's confirmation")
        else:
            return HttpResponse("The link you are using is invalid")


    def post(self, request):
        form = self.email_change_form(user=request.user, data = request.POST or None)
        if form.is_valid():
            user_id = request.user.pk
            request_secure = request.is_secure()
            domain = get_current_site(request).domain
            # form already checked if the password is valid for the user
            process_email_change_request.delay(request_secure, domain, user_id, form.cleaned_data.get('new_email'))

            return HttpResponse("An email with the activation link has been sent to your mailbox")
            

class ChangePasswordView(View):

    password_reset_template = None

    def get(self, request):
        pass

    def post(self, request):
        current_password = request.POST["current-password"]
        new_password = request.POST["new-password"]
        new_password_repeat = request.POST["new-password-confirm"]
        # DO THIS WITH DJANGO FORMS!!!
        pass


class ResetForgottenPasswordView(View):

    reset_forgotten_password_form = ForgottenPasswordResetForm

    template = 'authentication/components/reset_forgotten_password.html'
    invalid_link_template = 'authentication/components/reset_forgotten_password_invalid_link.html'
    error_template = 'authentication/components/reset_forgotten_password_error.html'
    success_template = 'authentication/components/reset_forgotten_password_success.html'

    def get(self, request, uuidb64: str, token: str):
        form = self.reset_forgotten_password_form()
        check_status, user = check_uuid_and_token(request, uuidb64, token)
        print(form)
        if check_status:
            return render(request, self.template, context = {
                'form': form,
            })
        else:
            return render(request, self.invalid_link_template, context={})
        
    def post(self, request, uuidb64: str, token: str):

        from .models import UserForgottenPasswordResetRequestModel
        # check the token and uuid
        check_status, user = check_uuid_and_token(request, uuidb64, token)
        # if the token and uuid are valid
        if check_status:
            # check if the request for this token and user exists in db
            # only the most recent one is pesisted in db
            qs = UserForgottenPasswordResetRequestModel.objects.filter(user = user, validation_token = token).first()
            # if it does not exist - return error template
            if qs is None:
                context = {
                    'error': "This link is outdated. Check your email for the most recent email with instructions or submit a new request."
                }
                return render(request, self.error_template, context=context)
            
            # if it exists - go on
            # check the form
            form = self.reset_forgotten_password_form(request.POST)
            # if the form is valid - reset the password, send a success template with attached hyperscript
            # that will redirect the user to login in 5 seconds after beinf loaded
            if form.is_valid():
                user.set_password(form.cleaned_data.get('new_password'))
                user.save()
                return render(request, self.success_template, context={})
            # if form is invalid - render an error template
            else:
                context = {
                    'error': "The submitted form for password reset is invalid"
                }
                return render(request, self.error_template, context=context)
        # if the token and uuid check failed - return an error template
        context = {
            'error': 'The link is either outdated, invalid or has been temperred with'
        }
        return render(request, self.error_template, context=context)
            


class AccountDeleteModalView(View):

    template_name = 'authentication/components/delete_account_modal.html'
    template_ok_response = 'authentication/components/delete_account_modal_response_ok.html'
    template_error_response = 'authentication/components/delete_account_modal_response_error.html'

    def get(self, request):
        return render(request, self.template_name, context = {})
    
    def post(self, request):
        password = request.POST['delete-account-password']
        context = {}
        print(password)
        if password == "test_ok":
            context['message'] = "Deletion confirmed. See ypu later!"
            return render(request, self.template_ok_response, context=context)
        context['message'] = "Wrong password provided"
        return render(request, self.template_error_response, context=context)
