from django.db.models import fields
from rest_framework import serializers
from order.models.products import Product
from order.models.orders import OrderItems, Order


class ProductSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Product
        fields = '__all__'       

class OrderItemsSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)   

    class Meta:
        model = OrderItems
        fields = ('id', 'order', 'product', 'quantity', 'changes')  

class OrderItemsWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItems
        fields = '__all__'      

class OrderSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Order
        fields = '__all__'       

class OrderInlineItemsSerializer(serializers.ModelSerializer):
    item = serializers.SerializerMethodField()  # Use SerializerMethodField for custom serialization
    
    class Meta:
        model = Order
        fields = [
            'id',
            'user',
            'cpf',
            'status',
            'created_at',
            'updated_at',
            'item'
        ]

    def get_item(self, obj):
        # Define custom method to serialize related CartItem objects
        order_items = OrderItems.objects.filter(order=obj)  # Fetch related CartItem objects
        serializer = OrderItemsSerializer(order_items, many=True)  # Serialize related CartItem objects
        return serializer.data  # Return serialized data