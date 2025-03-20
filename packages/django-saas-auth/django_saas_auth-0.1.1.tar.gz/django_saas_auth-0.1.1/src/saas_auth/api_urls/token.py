from django.urls import path
from ..endpoints.tokens import UserTokenListEndpoint, UserTokenItemEndpoint


urlpatterns = [
    path('', UserTokenListEndpoint.as_view()),
    path('<pk>/', UserTokenItemEndpoint.as_view()),
]
