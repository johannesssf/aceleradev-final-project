from django.contrib.auth.models import User
from django_filters import rest_framework as rest_filters

from rest_framework import generics, filters
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .models import Record
from .serializers import UserModelSerializer, RecordModelSerializer


class UserListCreateView(generics.ListCreateAPIView):
    """Handles get user list and post to create user.

    Authentication and token are mandatory.
    """
    queryset = User.objects.all()
    serializer_class = UserModelSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


class UserRetrieveDestroyView(generics.RetrieveDestroyAPIView):
    """Handles get and delete user.

    Authentication and token are mandatory.
    """
    queryset = User.objects.all()
    serializer_class = UserModelSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


class RecordListCreate(generics.ListCreateAPIView):
    """Handles get record list and post to create record.

    Authentication and token are mandatory.
    Filters and search are enabled.
    """
    queryset = Record.objects.all()
    serializer_class = RecordModelSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [rest_filters.DjangoFilterBackend, filters.SearchFilter]
    filter_fields = ['environment', 'level', 'message', 'origin']
    search_fields = ['message']


class RecordRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    """Handles get record, put/patch to full/partial update and delete
    record.

    Authentication and token are mandatory.
    """
    queryset = Record.objects.all()
    serializer_class = RecordModelSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
