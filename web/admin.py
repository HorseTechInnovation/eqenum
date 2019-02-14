from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.translation import ugettext_lazy as _

from .models import *

from import_export import resources
from import_export.admin import ImportExportActionModelAdmin




class EnumTypeResource(resources.ModelResource):

    class Meta:
        model = EnumType
        import_id_fields = ('ref',)
        fields = ('ref','name')

class EnumResource(resources.ModelResource):

    class Meta:
        model = Enum
        import_id_fields = ('ref',)
        fields = ('ref','name','emumtype_id','ordering')



class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'country','language', )

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format

        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField(label= ("Password"),
        help_text= ('<a href="../password/">Change Password</a>.'))

    class Meta:
        model = CustomUser
        fields = ('email', 'password', 'first_name', 'last_name','country','language', 'is_active' )

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'first_name','last_name')
    list_filter = ('date_joined',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name','country','language',)}),
        # (_('Subscribed'), {'fields': ('subscribed', 'unsubscribed', 'status', 'free_account')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined', 'removed_date')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'date_of_birth', 'password1', 'password2')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

class EnumTypeAdmin(ImportExportActionModelAdmin):
    resource_class = EnumTypeResource
    list_display = ('ref', 'parent', 'name','status','creator', 'created',)
    list_filter = ( 'status','created','parent')


class EnumDisplayInline(admin.TabularInline):
    model = EnumDisplay
    extra = 3

class EnumAdmin(ImportExportActionModelAdmin):
    class Meta:
        model = Enum

    list_display = ( 'ref', 'enumtype', 'ordering','creator', 'created',)
    list_filter = ( 'status','created','enumtype')
    search_fields = ('ref', 'enumtype',)
    inlines = [EnumDisplayInline,]
    resource_class = EnumResource


admin.site.register(CustomUser, UserAdmin)
admin.site.register(EnumType, EnumTypeAdmin)
admin.site.register(Enum, EnumAdmin)
admin.site.register(EnumDisplay)