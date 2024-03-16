from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.ProductCreateView, name='create'),
    path('list/', views.ProductListView, name='list'),
    path('denied/', views.access_denied, name='access_denied'),
]
