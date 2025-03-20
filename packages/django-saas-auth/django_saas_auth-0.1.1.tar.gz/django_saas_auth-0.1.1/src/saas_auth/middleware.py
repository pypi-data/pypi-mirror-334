import time
from django.contrib.auth import SESSION_KEY as USER_SESSION_KEY
from django.utils import timezone

from .models import Session
from .settings import auth_settings

__all__ = ['SessionRecordMiddleware']

LAST_RECORD_KEY = '_last_record_time'


class SessionRecordMiddleware:
    RECORD_INTERVAL = 300  # 5 minutes

    def __init__(self, get_response=None):
        self.get_response = get_response

    def should_record(self, request):
        user_id = request.session.get(USER_SESSION_KEY)
        if not user_id:
            return False

        last_record = request.session.get(LAST_RECORD_KEY)
        if not last_record:
            return True
        return time.time() - last_record > self.RECORD_INTERVAL

    def record_session(self, request):
        user_id = request.session.get(USER_SESSION_KEY)
        session_key = request.session.session_key
        expiry_date = request.session.get_expiry_date()
        user_agent = request.headers.get('User-Agent', '')
        location = auth_settings.LOCATION_RESOLVER.resolve(request)
        Session.objects.update_or_create(
            user_id=user_id,
            session_key=session_key,
            defaults={
                'expiry_date': expiry_date,
                'user_agent': user_agent,
                'location': location,
                'last_used': timezone.now(),
            },
        )

    def __call__(self, request):
        if not self.should_record(request):
            return self.get_response(request)

        self.record_session(request)
        request.session[LAST_RECORD_KEY] = int(time.time())
        return self.get_response(request)
