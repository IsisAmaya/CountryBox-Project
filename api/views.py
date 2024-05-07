from django.shortcuts import render
from products.models import Product
from . import serializers
from rest_framework import generics, status
from rest_framework.response import Response

# Create your views here.

class ProductListViewApi(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = serializers.ProductSerializer