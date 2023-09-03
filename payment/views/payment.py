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
from payment.use_cases.payment import CheckoutOrderUseCase

class CheckoutViewset(MixedPermissionModelViewSet):
    queryset = Order.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes_by_action = {
        'create': [AllowAny],
    }

    @action(detail=True, methods=['post'], url_path='checkout', permission_classes=[AllowAny])
    def order_checkout(self, request, pk=None):
        order = self.get_object()
        use_case = CheckoutOrderUseCase()

        try:
            use_case.execute(order)
            return Response({'message': 'Order status updated to "recebido".'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
