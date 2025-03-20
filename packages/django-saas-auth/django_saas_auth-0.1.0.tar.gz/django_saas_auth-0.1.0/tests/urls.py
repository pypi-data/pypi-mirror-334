from django.urls import path, include

urlpatterns = [
    path('m/', include('saas_auth.api_urls')),
]
