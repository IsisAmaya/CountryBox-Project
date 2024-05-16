from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import UserSingupForm, UserStaffForm
from shoppingcart.models import Cart
from products.models import Product
from .models import CustomUser
import random as rd
from .services import list_all_categories, get_meals_by_category, get_meal_details




def home_view(request):
    ids = list(Product.objects.values_list('id', flat=True))
    
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

def UserList(request):
    if request.method == 'POST':
        form = UserStaffForm(request.POST)
        if form.is_valid():
            user_id = request.POST.get('user_id')
            is_staff = request.POST.get('is_staff') == 'on'  # 'on' si el checkbox está marcado
            CustomUser.objects.filter(pk=user_id).update(is_staff=is_staff)
            return redirect('list_users')  # Redirige a una URL de éxito
    else:
        users = CustomUser.objects.all()
        form = UserStaffForm()
    return render(request, 'userTemplates/listUser.html', {'form': form, 'users':users})

@login_required
def logout_view(request):
    logout(request)
    return redirect('home')

def recipes_view(request):
    categories = list_all_categories()
    return render(request, 'templates/recipes.html', {'categories': categories})

def category_detail_view(request, category_name):
    meals = get_meals_by_category(category_name)
    return render(request, 'templates/category_detail.html', {'meals': meals, 'category_name': category_name})

def meal_detail_view(request, meal_id):
    meal = get_meal_details(meal_id)
    meal_data = meal['meals'][0]
    
    ingredients = []
    for i in range(1, 21):  # TheMealDB API provides up to 20 ingredients
        ingredient = meal_data.get(f'strIngredient{i}')
        measure = meal_data.get(f'strMeasure{i}')
        if ingredient:
            ingredients.append({'ingredient': ingredient, 'measure': measure})
    
    return render(request, 'templates/meal_detail.html', {'meal': meal_data, 'ingredients': ingredients})