from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UserModelSerializer


class UserApiView(APIView):
    """View to handle the api/users endpoint.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

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
                data = {"message": "User not found."}
                return Response(data, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, id=None):
        """Handles POST HTTP method to create users.
        """
        serializer = UserModelSerializer(data=request.data)
        if serializer.is_valid():
            User.objects.create_user(**serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        """Handles DELETE HTTP method to delete users.
        """
        user = User.objects.filter(id=id).first()
        if user:
            user.delete()
            data = {"message": "User deleted."}
            return Response(data, status=status.HTTP_200_OK)
        else:
            data = {"message": "User not found."}
            return Response(data, status=status.HTTP_404_NOT_FOUND)
