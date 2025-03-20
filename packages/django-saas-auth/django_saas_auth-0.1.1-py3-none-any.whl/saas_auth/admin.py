from django.contrib import admin
from .models import (
    Session,
    UserProfile,
    UserToken,
)


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'country', 'user_agent', 'expiry_date', 'last_used')

    def country(self, obj):
        return obj.location.get('country')


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'picture', 'region', 'locale')


@admin.register(UserToken)
class UserTokenAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'name', 'scope', 'expires_at')
