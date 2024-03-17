from django.urls import path
from shoppingcart.views import cart, order
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('cart/', views.cart, name='cart'),
    path('order/', views.order, name='order'),
]