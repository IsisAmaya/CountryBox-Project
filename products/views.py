from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseForbidden
from .models import Product
from .forms import ProductForm
from users import views
from users.utils import is_staff

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
    products = Product.objects.all()
    return render(request, "products/list.html", {"products": products})



#------------Other Functions--------------------

def access_denied(request):
    return HttpResponseForbidden("No tienes permiso para acceder a esta página.")
    
    