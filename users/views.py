from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.views import View
from django.contrib import messages
from .forms import UserSingupForm


def home_view(request):
    return render(request, 'templates/home.html')


def signup_view(request):
    if request.method == 'POST':
        form = UserSingupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            messages.success(request, f'Usuario {username} creado con éxito.')
            return redirect('home')
            
        else:
            messages.error(request, 'Por favor, corrija los errores abajo.')
    else:
        form = UserSingupForm()

    context = {'form': form}
    return render(request, 'customerTemplates/singupUser.html', context)


def login_view(request):
    if request.method == 'GET':
        return render(request, 'customerTemplates/loginUser.html',{'form':AuthenticationForm})
    else:
        user = authenticate(request, username=request.POST['username'],password=request.POST['password'])
    if user is None:
        return render(request,'customerTemplates/loginUser.html',{'form': AuthenticationForm(),'error': 'username and password do not match'})
    else:
        login(request, user)
    return redirect('home')


@login_required
def logout_view(request):
    logout(request)
    return redirect('home')
    
    #logout(request)
    #return render(request, 'customerTemplates/logoutUser.html')


