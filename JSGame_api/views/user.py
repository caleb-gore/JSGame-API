""" View module for handling request about games """
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from django.contrib.auth.models import User


class UserView(ViewSet):
    """ JSON serializer for users """

    def list(self, request):
        """Handle GET request to get all users

        Returns:
            Response -- JSON serialized list of profiles
        """
        current_user = request.auth.user
        if current_user.is_staff == True:
            users = User.objects.all()

            serializer = UserSerializer(users, many=True)
            return Response(serializer.data)
        else:
            return Response(None, status=status.HTTP_401_UNAUTHORIZED)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'is_staff', 'is_active')
