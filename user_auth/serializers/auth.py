from rest_framework import serializers
from user_auth.models import BaseUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseUser
        fields = ['email', 'name', 'password_confirmation']


class UserGETSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseUser
        fields = [
            'id',
            'email',
        ]

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
