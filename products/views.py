from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseForbidden
from .models import Product
from .forms import ProductForm
from users import views
from users.utils import is_staff
from django.db.models import Q

# Create your views here.


@user_passes_test(is_staff, login_url="/product/denied/")
def ProductCreateView(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product_form = form.save()
            return redirect(views.home_view)
        
    else:
        return render(request, 'products/create.html', { 'form': ProductForm})


def ProductListView(request):
    orden = request.GET.get('orden')

    if orden == 'desc':
        products = Product.objects.all().order_by('-price')  # Orden descendente
    elif orden == 'asc':
        products = Product.objects.all().order_by('price')   # Orden ascendente o cualquier otro orden por defecto
    else:
        products = Product.objects.all()
    return render(request, "products/list.html", {"products": products})


def ProductDetailsView(request, id):
    if Product.objects.filter(id=int(id)).exists():
        try:
            product_id = int(id)
            if product_id < 1:
                raise ValueError("El id del producto debe ser mayor a 1")
            product = get_object_or_404(Product, pk=product_id)
        
        except (ValueError, IndexError):
            return redirect('home')
    else:
        return redirect('home')
        
    return render(request, 'products/details.html', { 'product': product })


def ProductDelete(request, id):
    if Product.objects.filter(id=int(id)).exists():
        try:
            product_id = int(id)
            
            if product_id < 1:
                raise ValueError("El id del producto debe ser mayor a 1")
            
            product = get_object_or_404(Product, pk=product_id)
            
            product.delete()
        
        except (ValueError, IndexError):
            return redirect('home')
    else:
        return redirect('home')
        
    return redirect('list')


#------------Other Functions--------------------


def access_denied(request):
    return HttpResponseForbidden("No tienes permiso para acceder a esta página.")

# views.py en la aplicación products
def search(request):
    query = request.GET.get('q', '')
    products = Product.objects.filter(
        Q(name__icontains=query) |
        Q(description__icontains=query) |
        Q(country__icontains=query)
    )
    return render(request, 'products/searchresults.html', {'products': products})
  