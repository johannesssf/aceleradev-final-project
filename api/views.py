from rest_framework.views import APIView
from rest_framework.response import Response

from .models import User
from .serializers import UserModelSerializer


class UserApiView(APIView):
    def get(self, request, id=None, format=None):
        if not id:
            users = User.objects.all()
            serializer = UserModelSerializer(users, many=True)
        else:
            user = User.objects.get(pk=id)
            serializer = UserModelSerializer(user)

        return Response(serializer.data)
