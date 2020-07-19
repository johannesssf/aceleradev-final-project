from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer

from .models import Record


class UserModelSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'password',
        ]


class RecordModelSerializer(ModelSerializer):
    class Meta:
        model = Record
        fields = [
            'id',
            'environment',
            'level',
            'message',
            'origin',
            'date',
            'is_archived',
            'events',
            'user_id',
        ]
