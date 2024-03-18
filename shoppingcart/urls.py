from django.urls import path
from shoppingcart.views import cart, order
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'cart'

urlpatterns = [
    path('', views.cart, name='cart'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('order/', views.order, name='order'),
     path('confirmation/', views.order_confirmation, name='order_confirmation'),
]