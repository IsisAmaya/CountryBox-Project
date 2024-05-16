from django.urls import path
from django.urls import path
from . import views
from .views import order_pdf_view

app_name = 'cart'

urlpatterns = [
    path('', views.cart, name='cart'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('order/', views.order, name='order'),
    path('confirmation/', views.order_confirmation, name='order_confirmation'),
    path('order/pdf/', order_pdf_view, name='order_pdf'),
    
]