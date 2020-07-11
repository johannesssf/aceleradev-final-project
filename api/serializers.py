from rest_framework.serializers import ModelSerializer

from .models import User, Record


class UserModelSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
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
        ]
