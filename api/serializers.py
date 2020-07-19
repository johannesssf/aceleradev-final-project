from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer

from .models import Record


class UserModelSerializer(ModelSerializer):
    """User serializer.
    """
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'password',
        ]

    def create(self, validated_data):
        # Django password hashing.
        user = User.objects.create_user(**validated_data)
        return user


class RecordModelSerializer(ModelSerializer):
    """Record serializer.
    """
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
