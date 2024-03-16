from django.shortcuts import render, redirect
from django.contrib import messages
from .cart import ShoppingCart
from .forms import DeliveryAddressForm
from .models import Cart, CartItem, Order
from users.models import CustomUser
from users.utils import is_staff
from django.contrib.auth.decorators import login_required, user_passes_test

@user_passes_test(is_staff, login_url="/product/denied/")
@login_required
def cart(request):
    cart, created = Cart.objects.get_or_create(customer=request.user)
    cart_items = CartItem.all()
    customer = CustomUser.objects.get(id=request.session.get('customer_id'))
    return render(request, 'cart.html', {'cart': cart, 'cart_items': cart_items, 'customer': customer})

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
    cart_items = CartItem.all()
    delivery_address = None  # initialize delivery address variable
    total_price = sum(item.get_total_price() for item in cart_items)  # calculate total price

    if request.method == 'POST':
        # handle form submission for delivery address
        delivery_address_form = DeliveryAddressForm(request.POST)
        if delivery_address_form.is_valid():
            # save the delivery address to the user's profile
            delivery_address = delivery_address_form.save(commit=False)
            delivery_address.customer = request.user
            delivery_address.save()

            # calculate the final price including delivery fee
            delivery_fee = 5.00  # assume a fixed delivery fee for simplicity
            final_price = total_price + delivery_fee

            # create an order object with the cart, delivery address, and final price
            order = Order.objects.create(
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