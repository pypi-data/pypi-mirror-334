from django.db import models
from django.conf import settings
from django.utils import timezone
from ..util import gen_token_key


class UserToken(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        db_index=True,
        related_name='+',
    )
    tenant = models.ForeignKey(
        settings.SAAS_TENANT_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        db_index=True,
        related_name='+',
    )
    name = models.CharField(max_length=48)
    key = models.CharField(unique=True, max_length=48, default=gen_token_key, editable=False)
    scope = models.CharField(max_length=255)
    expires_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now, editable=False)

    class Meta:
        db_table = 'saas_auth_user_token'
        ordering = ('-created_at',)

    def __str__(self):
        return f'UserToken<{self.name}>'
