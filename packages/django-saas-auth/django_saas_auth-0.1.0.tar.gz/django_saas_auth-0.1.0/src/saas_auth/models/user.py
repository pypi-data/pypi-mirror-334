from django.db import models
from django.conf import settings


class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='profile',
        editable=False,
    )
    picture = models.URLField(blank=True, null=True)
    region = models.CharField(blank=True, null=True, max_length=4)
    locale = models.CharField(blank=True, null=True, max_length=10)

    class Meta:
        db_table = 'saas_auth_user_profile'
