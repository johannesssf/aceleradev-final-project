from django.urls import re_path

from .views import UserApiView


urlpatterns = [
    re_path(r'^users/((?P<id>\d+)/)?$', UserApiView.as_view(), name='users'),
]
