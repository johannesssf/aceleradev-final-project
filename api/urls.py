from django.urls import path, re_path

from rest_framework.authtoken.views import obtain_auth_token

from .views import UserApiView, RecordListCreate, RecordRetrieveUpdateDestroy


urlpatterns = [
    path('auth/token/', obtain_auth_token),
    re_path(
        r'^users/((?P<id>\d+)/)?$',
        UserApiView.as_view(),
        name='users'
    ),
    path(
        'records/',
        RecordListCreate.as_view(),
        name='records-list-create'
    ),
    path(
        'records/<int:pk>/',
        RecordRetrieveUpdateDestroy.as_view(),
        name='records-retrieve-update-destroy'
    ),
]
