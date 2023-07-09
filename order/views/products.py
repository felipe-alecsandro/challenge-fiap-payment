from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from user_auth.mixed_views import MixedPermissionModelViewSet
from order.models.products import Product
from order.serializers.products import *

class ProductViewSet(MixedPermissionModelViewSet):

    queryset = Product.objects.using('default').all()
    serializer_class = ProductSerializer
    permission_classes = (AllowAny,)
    
    
    def get_queryset(self):
        request = self.request
        qs = super().get_queryset()
        category = request.query_params.get('category', None)
        
        if category:
            qs = qs.filter(category=category)

        return qs