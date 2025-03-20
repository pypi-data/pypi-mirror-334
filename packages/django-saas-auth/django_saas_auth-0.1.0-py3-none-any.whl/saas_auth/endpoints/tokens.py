from rest_framework.mixins import ListModelMixin, CreateModelMixin, DestroyModelMixin
from saas_base.drf.views import AuthenticatedEndpoint
from ..models import UserToken
from ..serializers import UserTokenSerializer

__all__ = [
    'UserTokenListEndpoint',
    'UserTokenItemEndpoint',
]


class UserTokenListEndpoint(ListModelMixin, CreateModelMixin, AuthenticatedEndpoint):
    serializer_class = UserTokenSerializer
    pagination_class = None
    queryset = UserToken.objects.all()

    def filter_queryset(self, queryset):
        return queryset.filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class UserTokenItemEndpoint(DestroyModelMixin, AuthenticatedEndpoint):
    serializer_class = UserTokenSerializer
    queryset = UserToken.objects.all()

    def filter_queryset(self, queryset):
        return queryset.filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
