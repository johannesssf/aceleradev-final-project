from django.urls import path, re_path

from rest_framework.authtoken.views import obtain_auth_token

from .views import UserApiView

urlpatterns = [
    re_path(r'^users/((?P<id>\d+)/)?$', UserApiView.as_view(), name='users'),
    path('auth/token/', obtain_auth_token)
]
