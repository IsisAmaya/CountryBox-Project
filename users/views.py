from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views import View
from django.contrib import messages
from .forms import UserSingupForm



def HomeView(request):
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


def logout_view(request):
    #logout(request)
    return render(request, 'customerTemplates/logoutUser.html')


