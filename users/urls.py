from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('user/singup/', views.signup_view, name='singup'),
    path('user/login/', views.login_view, name='login'),
    path('logout/', views.logout_view , name='logout'),
    
    #path('logout/', LogoutView.as_view(template_name='customerTemplates/logoutUser.html'), name='logout'),
    #path('logout/', views.logout_view, name='logout'),

]
