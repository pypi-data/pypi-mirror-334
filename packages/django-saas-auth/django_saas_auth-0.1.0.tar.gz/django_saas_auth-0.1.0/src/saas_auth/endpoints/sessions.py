from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, DestroyModelMixin
from saas_base.drf.views import AuthenticatedEndpoint
from ..models import Session
from ..serializers import SessionSerializer

__all__ = [
    'SessionRecordListEndpoint',
    'SessionRecordItemEndpoint',
]


class SessionRecordListEndpoint(ListModelMixin, AuthenticatedEndpoint):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer

    def filter_queryset(self, queryset):
        return queryset.filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class SessionRecordItemEndpoint(RetrieveModelMixin, DestroyModelMixin, AuthenticatedEndpoint):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer

    def filter_queryset(self, queryset):
        return queryset.filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def perform_destroy(self, instance):
        self.request.session.delete(instance.session_key)
        instance.delete()
