from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import views as auth_views
from .views import logout_view

urlpatterns = [
    path('', views.HomeView, name='home'),
    path('singup/', views.signup_view, name='singup'),
    path('login/', LoginView.as_view(template_name='customerTemplates/loginUser.html'), name='login'),
    #path('logout/', LogoutView.as_view(template_name='customerTemplates/logoutUser.html'), name='logout'),
    #path('logout/', views.logout_view, name='logout'),
    path('logout/', logout_view , name='logout'),

]
