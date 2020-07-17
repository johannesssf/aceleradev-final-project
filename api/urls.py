from django.urls import path, re_path

from rest_framework.authtoken.views import obtain_auth_token

from .views import UserApiView, RecordApiView

urlpatterns = [
    path('auth/token/', obtain_auth_token),
    re_path(
        r'^users/((?P<id>\d+)/)?$',
        UserApiView.as_view(),
        name='users'
    ),
    re_path(
        r'^records/((?P<id>\d+)/)?$',
        RecordApiView.as_view(),
        name='records'
    ),
]
