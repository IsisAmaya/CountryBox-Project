from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import user_passes_test
from django.views import View
from django.contrib import messages
from .forms import UserSingupForm
from  shoppingcart.models import Cart
from .utils import is_staff


def home_view(request):
    return render(request, 'templates/home.html')

def signup_view(request):
    if request.method == 'POST':
        form = UserSingupForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data['username']
            Cart.objects.create(customer=user)
            messages.success(request, f'Usuario {username} creado con éxito.')
            return redirect('home')
            
        else:
            messages.error(request, 'Por favor, corrija los errores abajo.')
    else:
        form = UserSingupForm()

    context = {'form': form}
    return render(request, 'userTemplates/singupUser.html', context)


def login_view(request):
    if request.method == 'GET':
        return render(request, 'userTemplates/loginUser.html',{'form':AuthenticationForm})
    else:
        user = authenticate(request, username=request.POST['username'],password=request.POST['password'])
    if user is None:
        return render(request,'userTemplates/loginUser.html',{'form': AuthenticationForm(),'error': 'username and password do not match'})
    else:
        login(request, user)
    return redirect('home')


@login_required
def logout_view(request):
    logout(request)
    return redirect('home')
    
    #logout(request)
    #return render(request, 'customerTemplates/logoutUser.html')


