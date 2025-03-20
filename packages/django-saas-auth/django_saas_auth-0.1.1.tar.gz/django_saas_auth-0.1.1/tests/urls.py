from django.urls import path, include

urlpatterns = [
    path('api/user/', include('saas_auth.api_urls.user')),
    path('api/user/sessions/', include('saas_auth.api_urls.session')),
    path('api/user/tokens/', include('saas_auth.api_urls.token')),
]
