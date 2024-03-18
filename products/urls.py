from django.urls import path
from . import views
#from shoppingcart.views import add_to_cart

urlpatterns = [
    path('create/', views.ProductCreateView, name='create'),
    path('list/', views.ProductListView, name='list'),
    path('denied/', views.access_denied, name='access_denied'),
    path('details/<int:id>/', views.ProductDetailsView, name='details'),
    path('delete/<int:id>/', views.ProductDelete, name='delete'),
    #path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
]
