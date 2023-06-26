from rest_framework import serializers
from django.contrib.auth import authenticate
from user_auth.models import BaseUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseUser
        fields = ['email', 'name', 'password']

    def create(self, validated_data):
        user = BaseUser.objects.create(**validated_data)
        user.set_password(validated_data['password'])

        user.save()
        return user


class UserGETSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseUser
        fields = [
            'id',
            'email',
        ]


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(email=email, password=password)
            if not user:
                raise serializers.ValidationError('Invalid credentials')
            if not user.is_active:
                raise serializers.ValidationError('User account is disabled')
        else:
            raise serializers.ValidationError('Email and password are required')

        attrs['user'] = user
        return attrs

