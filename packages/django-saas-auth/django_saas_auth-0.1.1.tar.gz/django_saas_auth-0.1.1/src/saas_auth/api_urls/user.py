from django.urls import path
from ..endpoints.user import UserEndpoint, UserProfileEndpoint


urlpatterns = [
    path('', UserEndpoint.as_view()),
    path('profile/', UserProfileEndpoint.as_view()),
]
