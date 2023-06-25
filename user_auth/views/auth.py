
from django.utils.translation import ugettext_lazy as _
from rest_framework.permissions import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

from burgerstore.settings import *
from django.contrib.auth.models import User
from user_auth.models import BaseUser
from user_auth.serializers.auth import UserSerializer, UserGETSerializer, LoginSerializer
from user_auth.mixed_views import MixedPermissionModelViewSet
from user_auth.helpers import *

from rest_framework_simplejwt.tokens import RefreshToken

@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def signin(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = authenticate(
            email=serializer.validated_data['email'],
            password=serializer.validated_data['password']
        )
        if user:
            refresh = RefreshToken.for_user(user)

            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
    return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)



class UserViewSet(MixedPermissionModelViewSet):
    queryset = BaseUser.objects.using('default').all()
    serializer_class = UserSerializer
    permission_classes_by_action = {
        'create': [AllowAny],
        'retrieve': [IsAuthenticated],
        'list': [IsAuthenticated],
        'update': [IsAuthenticated],
        'partial_update': [IsAuthenticated],
        'delete': [IsAuthenticated],
    }

    def get_serializer_class(self):
        method = self.request.method
        if method == 'GET':
            return UserGETSerializer
        else:
            return self.serializer_class

    def get_queryset(self):
        return super().get_queryset().filter(id=self.request.user.id)

    def create(self, request, *args, **kwarsg):
        serializer = UserSerializer(
            data=request.data, context=self.get_serializer_context()
        )
        serializer.is_valid(raise_exception=True)
        saved = serializer.save()

        response_serializer = UserGETSerializer(saved)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)