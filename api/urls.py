from django.urls import path

from rest_framework.authtoken.views import obtain_auth_token

from .views import (
    RecordListCreate,
    RecordRetrieveUpdateDestroy,
    UserListCreateView,
    UserRetrieveDestroyView,
)


urlpatterns = [
    path('auth/token/', obtain_auth_token),
    path(
        'users/',
        UserListCreateView.as_view(),
        name='users-list-create'
    ),
    path(
        'users/<int:pk>/',
        UserRetrieveDestroyView.as_view(),
        name='users-retrieve-destroy'
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
