from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.translation import gettext_lazy as _
from .models import User

class CustomUserCreationForm(UserCreationForm):

    #the base model supposedly should provide password1 and password2 fields
    #and will handle the password checking and setting

    class Meta:
        model = User
        fields = [
            "name",
            "email",
            "is_organization",
        ]


class CustomUserChangeForm(UserChangeForm):

    #the base  odel supposedly should provide the readonlyasswordhash field
    #and I need to override the fileds of the base User with my User model's fields

    class Meta:
        model = User
        fields = [
            "name",
            "email",
            "is_organization",
            "is_staff",
            "is_active",
        ]


class CustomUserAdmin(UserAdmin):
    model = User

    # override the default forms for creation and changing of User model
    # that are displayed in admin pannel (since we have a custom user model)
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm

    # Fields to display in the admin list view
    list_display = ('email', 'is_active')
    list_filter = ['is_active']

    # Ordering and search fields
    ordering = ('email',)
    search_fields = ('email', 'name')

    # Fieldsets for displaying user fields in the admin
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('name',
         'is_organization')}),
        (_('Permissions'), {'fields': ('is_active', 'groups',
         'user_permissions', 'is_staff', 'is_superuser')}),
        (_('Important dates'), {'fields': ('last_logged_in', 'date_joined')}),
    )

    # Fieldsets for adding a new user
    # Take into consideration what needs to be despalid based on the user creation form!
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'password1', 'password2'),
        }),
    )

    # Use Django’s password hashing method
    def save_model(self, request, obj, form, change):
        if form.cleaned_data.get('password') and not change:
            # Hash the password
            obj.set_password(form.cleaned_data['password'])
        super().save_model(request, obj, form, change)

# Register your models here.


admin.site.register(User, CustomUserAdmin)
