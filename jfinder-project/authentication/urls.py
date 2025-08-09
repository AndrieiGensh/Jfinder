from django.urls import path, include

from .views import *

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("register/", RegisterView.as_view(), name="register"),
    path("pw-reset-modal/", PasswordResetModal.as_view(), name="pw_reset_modal"),
    path("delete-account-modal/", AccountDeleteModalView.as_view(), name="delete_account_modal"),
    path('change-email/', ChangeEmailView.as_view(), name="change_email"),
    path('change-email/<str:uuidb64>/<str:token>', ChangeEmailView.as_view(), name="change_email_activation"),
    path('change-password/', ChangePasswordView.as_view(), name="change__password"),
]
