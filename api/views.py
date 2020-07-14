from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import User
from .serializers import UserModelSerializer


class UserApiView(APIView):
    """View to handle the api/users endpoint.
    """

    def get(self, request, id=None):
        """Handles GET HTTP method to list users.

        If 'id' is None, returns a list of users otherwise a single user.
        """
        if id is None:
            users = User.objects.all()
            serializer = UserModelSerializer(users, many=True)
            return Response(serializer.data)
        else:
            user = User.objects.filter(id=id).first()
            if user:
                serializer = UserModelSerializer(user)
                return Response(serializer.data)
            else:
                data = {"message": "User not found"}
                return Response(data, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, id=None):
        """Handles POST HTTP method to create users.
        """
        serializer = UserModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        """Handles DELETE HTTP method to delete users.
        """
        user = User.objects.filter(id=id).first()
        if user:
            user.delete()
            data = {"message": "User deleted"}
            return Response(data, status=status.HTTP_200_OK)
        else:
            data = {"message": "User not found"}
            return Response(data, status=status.HTTP_404_NOT_FOUND)
