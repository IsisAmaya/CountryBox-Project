from django.urls import path
from . import views
from api.views import ProductListViewApi

urlpatterns = [
    path('create/', views.ProductCreateView, name='create'),
    path('list/', views.ProductListView, name='list'),
    path('denied/', views.access_denied, name='access_denied'),
    path('details/<int:id>/', views.ProductDetailsView, name='details'),
    path('delete/<int:id>/', views.ProductDelete, name='delete'),
    path('search/', views.search, name='search'),
    path('countrybox-api/', ProductListViewApi.as_view(), name='api'),

]
