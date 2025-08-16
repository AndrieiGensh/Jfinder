from django.urls import path, include

from .views import *

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("register/", RegisterView.as_view(), name="register"),
    path("forgotten-password-reset-modal/", PasswordResetModal.as_view(), name="pw_reset_modal"),
    path('forgotten-password-reset/', ResetForgottenPasswordView.as_view(), name="forgotten_password_reset"),
    path('forgotten-password-reset/<str:uuidb64>/<str:token>', ResetForgottenPasswordView.as_view(), name="forgotten_password_reset_confirmation"),
    path("delete-account-modal/", AccountDeleteModalView.as_view(), name="delete_account_modal"),
    path('change-email/', ChangeEmailView.as_view(), name="change_email"),
    path('change-email/<str:uuidb64>/<str:token>', ChangeEmailView.as_view(), name="change_email_activation"),
    path('change-password/', ChangePasswordView.as_view(), name="change_password"),
]
