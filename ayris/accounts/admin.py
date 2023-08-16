from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import (
CustomUser,
Profile,
Email,
Talent,
SocialNetworkLink,
NetworkName,
Character,
SearchParam,
GuestBook
)


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('email', 'is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)


class EmailAdmin(admin.ModelAdmin):
    list_display = ('email', 'profile', )


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'name', 'title', 'age', )

    # TODO SET city depends on the choiced country

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Talent)
admin.site.register(Character)
admin.site.register(SocialNetworkLink)
admin.site.register(NetworkName)
admin.site.register(GuestBook)

admin.site.register(Email, EmailAdmin)
