from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.shortcuts import get_object_or_404
from user_auth.mixed_views import MixedPermissionModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from django.contrib.sessions.backends.db import SessionStore
from order.models.orders import Order
from order.serializers.orders import *

class CheckoutViewset(MixedPermissionModelViewSet):
    queryset = Order.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes_by_action = {
        'create': [AllowAny],
    }

    def create(self, request, *args, **kwargs):
        order = self.get_object()

        if order.status == 'em aberto':
            order.status = 'fila'
            order.save()
            return Response({'message': 'Order status updated to "fila".'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Esse pedido não pode ser finalizado.'}, status=status.HTTP_400_BAD_REQUEST)
    
