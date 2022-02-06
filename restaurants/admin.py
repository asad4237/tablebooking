from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserAdminCreationForm, UserAdminChangeForm

User = get_user_model()

class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ['staffnumber']
    list_filter = ['staffnumber']
    fieldsets = (
        (None, {'fields': ('staffnumber', 'password')}),
        ('Personal info', {'fields': ()}),
        ('Permissions', {'fields': ('is_staff',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('staffnumber', 'password', 'password_2')}
        ),
    )
    search_fields = ['staffnumber']
    ordering = ['staffnumber']
    filter_horizontal = ()



admin.site.register(User, UserAdmin)

