from django.core.signals import setting_changed
from saas_base.settings import Settings

DEFAULTS = {
    'LOCATION_RESOLVER': {
        'backend': 'saas_auth.location.cloudflare.CloudflareBackend',
    }
}


class AuthSettings(Settings):
    IMPORT_PROVIDERS = [
        'LOCATION_RESOLVER',
    ]


auth_settings = AuthSettings('SAAS_AUTH', defaults=DEFAULTS)
setting_changed.connect(auth_settings.listen_setting_changed)
