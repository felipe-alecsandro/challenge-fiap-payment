from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from django.shortcuts import get_object_or_404
from user_auth.mixed_views import MixedPermissionModelViewSet
from rest_framework.response import Response
from rest_framework import status
from user_auth.models import BaseUser
from order.models.products import Product
from order.models.orders import OrderItems, Order
from order.serializers.products import *

class ProductiewSet(MixedPermissionModelViewSet):

    queryset = Product.objects.using('default').all()
    serializer_class = ProductSerializer
    permission_classes = (AllowAny,)
    
    
    def get_queryset(self):
        request = self.request
        qs = super().get_queryset()
        uf = request.query_params.get('estado', None)
        
        if uf:
            qs = qs.filter(uf=uf)

        return qs


class OrderViewSet(MixedPermissionModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (AllowAny,)

    serializer_action_classes = {
        'create': OrderSerializer,
        'create_item': OrderItemsSerializer,
        'list': OrderInlineItemsSerializer,
        'retrieve': OrderInlineItemsSerializer,
        'update': OrderSerializer,
    }

    def create(self, serializer):
        serializer = OrderSerializer(data=self.request.data)
        if serializer.is_valid():
            instance = serializer.save()
            cart_item_serializer = OrderItemsSerializer(data=self.request.data)
            if cart_item_serializer.is_valid():
                cart_item_serializer.save(cart=instance)
            cart_serializer = OrderInlineItemsSerializer(instance)  # Serialize the Cart object
            return Response(cart_serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)
        

    def list(self, request, *args, **kwargs):
        user = self.request.user
        user_profile = BaseUser.objects.get(id=user)
        queryset = super().get_queryset().filter(user=user)
        serializer = OrderInlineItemsSerializer(queryset, many=True)
        return Response(serializer.data)
    

    def retrieve(self, request, pk=None, *args, **kwargs):
        order = get_object_or_404(Order, pk=pk)
        serializer = self.get_serializer(order)
        return Response(serializer.data)

    def partial_update(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


    def get_serializer_class(self):
        """
        Returns the serializer class to be used for the retrieve action.
        """
        if self.action == 'retrieve':
            return OrderInlineItemsSerializer  # Specify the serializer class for retrieve action
        return super().get_serializer_class()
    

class OrderItemsViewSet(MixedPermissionModelViewSet):
    queryset = OrderItems.objects.all()
    serializer_class = OrderItemsSerializer
    permission_classes = (AllowAny,)

    serializer_action_classes = {
        'create': OrderItemsSerializer,
        'create_item': OrderItemsSerializer,
        'list': OrderInlineItemsSerializer,
        'retrieve': OrderItemsSerializer,
        'update': OrderItemsSerializer,

    }

    def create(self, serializer):
        serializer = OrderItemsWriteSerializer(data=self.request.data)
        if serializer.is_valid():
            instance = serializer.save()
            result = OrderItemsSerializer(instance)  # Serialize the Cart object
            return Response(result.data, status=201)
        else:
            return Response(serializer.errors, status=400)
        

    def delete(self, request, pk=None):
        order_item = self.get_object()  # Get the order item object
        order_item.delete()  # Delete the order item
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def retrieve(self, request, pk=None, *args, **kwargs):
        order = get_object_or_404(Order, pk=pk)
        serializer = self.get_serializer(order)
        return Response(serializer.data)

    def partial_update(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)