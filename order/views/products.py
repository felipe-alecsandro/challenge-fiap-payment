from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.shortcuts import get_object_or_404
from user_auth.mixed_views import MixedPermissionModelViewSet
from rest_framework.response import Response
from rest_framework import status
from django.contrib.sessions.backends.db import SessionStore
from user_auth.models import BaseUser
from order.models.products import Product
from order.models.orders import OrderItems, Order
from order.serializers.products import *

class ProductViewSet(MixedPermissionModelViewSet):

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
    authentication_classes = [JWTAuthentication]
    permission_classes_by_action = {
        'create': [AllowAny],
        'retrieve': [AllowAny],
        'list': [AllowAny],
        'update': [AllowAny],
        'partial_update': [AllowAny],
        'delete': [IsAuthenticated],
    }

    serializer_action_classes = {
        'create': OrderSerializer,
        'create_item': OrderItemsSerializer,
        'list': OrderInlineItemsSerializer,
        'retrieve': OrderInlineItemsSerializer,
        'update': OrderSerializer,
    }

    def create(self, request, *args, **kwargs):
        user = request.user
        session = request.session if user.is_authenticated else SessionStore()
        session.create()
        session_token = session.session_key
        user = user if user.is_authenticated else None

        serializer = OrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save(session_token=session_token, user=user)

        cart_serializer = OrderInlineItemsSerializer(instance)
        return Response(cart_serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        user = request.user
        queryset = self.queryset.filter(user=user) if user.is_authenticated else self.queryset.filter(session_token=request.query_params.get('session'))
        serializer = OrderInlineItemsSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, *args, **kwargs):
        user = request.user
        order = get_object_or_404(Order, pk=pk, id=user.id) if user.is_authenticated else get_object_or_404(Order, pk=pk, session_token=request.query_params.get('session'))
        serializer = self.get_serializer(order)
        return Response(serializer.data)

    def partial_update(self, request, pk=None):
        user = request.user
        instance = get_object_or_404(Order, pk=pk, user=user.id) if user.is_authenticated else get_object_or_404(Order, pk=pk, session_token=request.query_params.get('session'))
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return OrderInlineItemsSerializer
        return super().get_serializer_class()
    

class OrderItemsViewSet(MixedPermissionModelViewSet):
    queryset = OrderItems.objects.all()
    serializer_class = OrderItemsSerializer
    permission_classes = (AllowAny,)

    serializer_action_classes = {
        'create': OrderItemsWriteSerializer,
        'create_item': OrderItemsSerializer,
        'list': OrderInlineItemsSerializer,
        'retrieve': OrderItemsSerializer,
        'update': OrderItemsSerializer,

    }

    def create(self, serializer):
        order_id = serializer.validated_data['order']
        user = self.request.user

        if user.is_authenticated:
            try:
                order = Order.objects.get(id=order_id, user=user)
            except Order.DoesNotExist:
                return Response({'error': 'Você não tem permissão para editar esse carrinho'}, status=403)
        else:
            session = self.request.query_params.get('session')
            try:
                order = Order.objects.get(id=order_id, session_token=session)
            except Order.DoesNotExist:
                return Response({'error': 'Você não tem permissão para editar esse carrinho'}, status=403)

        instance = serializer.save(order=order)
        return Response(serializer.data, status=201)


    def delete(self, request, pk=None):
        order_item = self.get_object()
        order = order_item.order
        user = request.user

        if user.is_authenticated:
            if order.user != user:
                return Response({'error': 'Você não tem permissão para editar esse carrinho'}, status=403)
        else:
            session = request.query_params.get('session')
            if order.session_token != session:
                return Response({'error': 'Você não tem permissão para editar esse carrinho'}, status=403)

        order_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def retrieve(self, request, pk=None, *args, **kwargs):
        order = get_object_or_404(Order, pk=pk)
        user = request.user

        if user.is_authenticated:
            if order.user != user:
                return Response({'error': 'Você não tem permissão para visualizar esse carrinho'}, status=403)
        else:
            session = request.query_params.get('session')
            if order.session_token != session:
                return Response({'error': 'Você não tem permissão para visualizar esse carrinho'}, status=403)

        serializer = self.get_serializer(order)
        return Response(serializer.data)

    def partial_update(self, request, pk=None):
        instance = self.get_object()
        order = instance.order
        user = request.user

        if user.is_authenticated:
            if order.user != user:
                return Response({'error': 'Você não tem permissão para editar esse carrinho'}, status=403)
        else:
            session = request.query_params.get('session')
            if order.session_token != session:
                return Response({'error': 'Você não tem permissão para editar esse carrinho'}, status=403)

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)