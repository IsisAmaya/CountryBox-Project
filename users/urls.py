from django.urls import path
from . import views
from .views import recipes_view, category_detail_view, meal_detail_view


urlpatterns = [
    path('', views.home_view, name='home'),
    path('user/singup/', views.signup_view, name='singup'),
    path('user/login/', views.login_view, name='login'),
    path('logout/', views.logout_view , name='logout'),
    path('list/', views.UserList, name="list_users"),
    path('recipes/', views.recipes_view, name='recipes'),
    path('recipes/<str:category_name>/', category_detail_view, name='category_detail'),
    path('meal/<int:meal_id>/', meal_detail_view, name='meal_detail'),


]
