from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import UserSingupForm
from shoppingcart.models import Cart
from products.models import Product
import random as rd


def home_view(request):
    ids = list(Product.objects.values_list('id', flat=True))
    print(f"Ids: {ids}")
    
    if len(ids) >= 3:
        random_ids = rd.sample(ids, 3)
        instancias = Product.objects.filter(id__in=random_ids)
    else:
        instancias = Product.objects.none()  
    
    random = Product.objects.order_by('?')[:4]
    context = {
        'obj_1' : instancias[0],
        'obj_2' : instancias[1],
        'obj_3' : instancias[2],
    }
    return render(request, 'templates/home.html', context)


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
    if request.method == 'POST':
        user = authenticate(request, username=request.POST['username'],password=request.POST['password'])
        if user is None:
            return render(request, 'userTemplates/loginUser.html', {'form': AuthenticationForm(), 'error': 'Username and password do not match', 'is_login_page': True})
        else:
            login(request, user)
            return redirect('home')
    else:
        # Aquí también pasamos 'is_login_page': True para que se muestre la página de login adecuadamente
        return render(request, 'userTemplates/loginUser.html', {'form': AuthenticationForm(), 'is_login_page': True})


@login_required
def logout_view(request):
    logout(request)
    return redirect('home')
