from rest_framework.generics import get_object_or_404
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin
from saas_base.drf.views import AuthenticatedEndpoint
from saas_base.endpoints.user import UserEndpoint as BaseUserEndpoint

from ..models import UserProfile
from ..serializers import UserSerializer, UserProfileSerializer


class UserEndpoint(BaseUserEndpoint):
    serializer_class = UserSerializer


class UserProfileEndpoint(RetrieveModelMixin, UpdateModelMixin, AuthenticatedEndpoint):
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()

    def get_object(self):
        obj = get_object_or_404(self.queryset, user=self.request.user)
        self.check_object_permissions(self.request, obj)
        return obj

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
