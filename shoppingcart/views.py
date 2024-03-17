from django.shortcuts import render, redirect
from django.contrib import messages
from .cart import ShoppingCart
from .forms import DeliveryAddressForm
from .models import Cart, CartItem, Order
from products.models import Product
from users.models import CustomUser
from users.utils import is_staff
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test

@login_required
def cart(request):
    cart, created = Cart.objects.get_or_create(customer=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    customer_id = request.session.get('customer_id')
    if customer_id:
        customer = CustomUser.objects.get(id=customer_id)
    else:
        customer = None
    return render(request, 'cart.html', {'cart': cart, 'cart_items': cart_items, 'customer': customer})

@login_required
def add_to_cart(request, product_id):
    cart = ShoppingCart(request)
    if Product.objects.filter(id=product_id).exists():
        quantity = int(request.POST.get('quantity', 1))
        product = Product.objects.get(id=product_id)
        cart.add_product(product_id, quantity)
        return redirect('cart:cart')
    else:
        return HttpResponse("El producto no existe en la base de datos.")

@login_required
def remove_from_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart = ShoppingCart(request.session)
    cart.remove_product(product)
    messages.success(request, f'Producto "{product.name}" eliminado del carrito')
    return redirect('cart:cart')

@login_required
def order(request):
    cart, created = Cart.objects.get_or_create(customer=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    total_price = sum(item.get_total_price() for item in cart_items)

    if request.method == 'POST':
        delivery_address_form = DeliveryAddressForm(request.POST)
        if delivery_address_form.is_valid():
            delivery_address = delivery_address_form.save(commit=False)
            delivery_address.customer = request.user
            delivery_address.save()

            # calculate the final price including delivery fee
            delivery_fee = 5.00  # assume a fixed delivery fee
            final_price = total_price + delivery_fee

            # create an order object with the cart, delivery address, and final price
            order = Order.objects.create(
                cart=cart,
                customer=request.user,
                delivery_address=delivery_address,
                total_price=final_price
            )

            # clear the cart after creating an order
            cart.clear()

            # display a message 'order was realized'
            messages.success(request, 'Order was realized!')

    return render(request, 'order.html', {
        'cart': cart,
        'cart_items': cart_items,
        'delivery_address': delivery_address,
        'total_price': total_price
    })