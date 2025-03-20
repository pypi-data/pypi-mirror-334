from django.urls import path
from ..endpoints.sessions import SessionRecordListEndpoint, SessionRecordItemEndpoint


urlpatterns = [
    path('', SessionRecordListEndpoint.as_view()),
    path('<pk>/', SessionRecordItemEndpoint.as_view()),
]
