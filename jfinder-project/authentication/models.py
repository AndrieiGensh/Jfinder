from django.db import models
from django import forms
from django.utils import timezone
from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser
from django.contrib.auth.base_user import BaseUserManager

# Create your models here.


class UserManager(BaseUserManager):

    def _create_user(self, email: str, password: str, **extrafields):
        if not email:
            raise ValueError("You have not provided the email address.")

        email = self.normalize_email(email)
        user = self.model(email=email, **extrafields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, email, password, **extrafields):
        extrafields.setdefault("is_staff", False)
        extrafields.setdefault('is_superuser', False)

        return self._create_user(email=email, password=password, **extrafields)

    def create_superuser(self, email=None, password=None, **extrafields):
        extrafields.setdefault("is_staff", True)
        extrafields.setdefault('is_superuser', True)

        return self._create_user(email=email, password=password, **extrafields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(blank=True, default="", unique=True)
    name = models.CharField(max_length=255, default="", blank=True)

    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_organization = models.BooleanField(default=False)

    date_joined = models.DateTimeField(default=timezone.now)
    last_logged_in = models.DateTimeField(blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta():
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.name or self.email.split("@")[0]


# class UserForm(UserCreationForm):
#     class Meta(UserCreationForm.Meta):
#         model = User
#         fileds = UserCreationForm.Meta.fields + ("is_organization")
