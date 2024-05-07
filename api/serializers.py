from products.models import Product
from rest_framework import serializers
from django.urls import reverse


class ProductSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = ('name', 'description' ,'price', 'url')
        
    def get_url(self, obj):
        request = self.context.get('request')
        if request is not None:
            return request.build_absolute_uri(reverse('details', args=[obj.pk]))
        return None