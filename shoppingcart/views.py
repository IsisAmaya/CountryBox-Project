from django.shortcuts import render, redirect
from django.contrib import messages
from .utils import ShoppingCart
from .models import Cart, CartItem ,Order, OrderItem
from products.models import Product
from users.models import CustomUser
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.decorators import login_required

@login_required
def cart(request):
    customer_id = request.user.id
    customer = CustomUser.objects.get(pk=customer_id)
    cart, create = Cart.objects.get_or_create(customer=customer)
    cart_items = CartItem.objects.filter(cart=cart.pk)
    cart_item = ShoppingCart(request)
    total_cart = cart_item.get_total(cart.pk)
    box_size = request.session.get('box_size', None)
    if box_size is not None:
        request.session['box_size'] = box_size
    return render(request, 'cart.html', {'cart': cart, 'cart_items': cart_items,'customer': customer, 'total': total_cart, 'box_size': box_size})

@login_required
def add_to_cart(request, product_id):
    cart_item = ShoppingCart(request)
    cart = cart_item.get_cart(request)
    if Product.objects.filter(id=product_id).exists():
        quantity = int(request.POST.get('quantity', 1))
        print(cart.pk)
        cart_item.add_product(cart.id, product_id, quantity)
        return redirect('cart:cart')
    else:
        return HttpResponse("El producto no existe en la base de datos.")

@login_required
def remove_from_cart(request, product_id):
    product = Product.objects.get(pk=product_id)
    cart_item = ShoppingCart(request)
    cart = cart_item.get_cart(request)
    cart_item.remove_product(cart.pk ,product_id)
    messages.success(request, f'Producto "{product.name}" eliminado del carrito')
    return redirect('cart:cart')


@login_required
def order(request):
    customer_id = request.user.id
    customer = CustomUser.objects.get(pk=customer_id)
    cart, create = Cart.objects.get_or_create(customer=customer)
    cart_items = CartItem.objects.filter(cart=cart.pk)
    total_cart = sum(item.get_total_price() for item in cart_items)

    if request.method == "POST":
        address = request.POST["address"]
        order = Order.objects.create(
            cart=cart,
            customer=customer,
            address=address,
            total_price=total_cart,
        )

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price,
            )

        # Clear the cart after creating an order
        cart.items.clear()

        messages.success(request, "Your order has been created!")
        return redirect("cart:order_confirmation")
    
     # Get cart items after clearing the cart
    cart_items = CartItem.objects.filter(cart=cart.pk)

    return render(request, "order.html", {"cart": cart, "cart_items": cart_items, 'customer': customer, "total_price": total_cart})

@login_required
def order_confirmation(request):
    return render(request, "order_confirmation.html")