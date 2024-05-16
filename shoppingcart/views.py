from django.shortcuts import render, redirect
from django.contrib import messages
from .utils import ShoppingCart
from .models import Cart, CartItem ,Order, OrderItem
from products.models import Product
from users.models import CustomUser
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import PaymentForm
from .utils import OrderPDFGenerator
from django.shortcuts import render


@login_required
def cart(request):
    customer_id = request.user.id
    customer = CustomUser.objects.get(pk=customer_id)
    cart, create = Cart.objects.get_or_create(customer=customer)
    cart_items = CartItem.objects.filter(cart=cart.pk)
    cart_item = ShoppingCart(request)
    total_cart = cart_item.get_total(cart.pk)
    return render(request, 'cart.html', {'cart': cart, 'cart_items': cart_items,'customer': customer, 'total': total_cart})


@login_required
def add_to_cart(request, product_id):
    cart_item = ShoppingCart(request)
    cart = cart_item.get_cart(request)
    if Product.objects.filter(id=product_id).exists():
        quantity = int(request.POST.get('quantity', 1))
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
    total_quantity = ShoppingCart.get_total_quantity(cart.items.all())

    if request.method == "POST":
        address = request.POST.get("address")
        payment_method = request.POST.get("payment_method")
        
        if payment_method == "Card":
            card_number = request.POST.get("card_number")
            card_expiration_date = request.POST.get("card_expiration_date")
            card_holder = request.POST.get("card_holder")
            card_bank = request.POST.get("card_bank")
            card_cvv = request.POST.get("card_cvv")


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


        cart.items.all().delete()
        
        messages.success(request, "Your order has been created!")
        return redirect("cart:order_confirmation")

    return render(request, "order.html", {
        "cart": cart,
        "cart_items": cart_items,
        "customer": customer,
        "total_price": total_cart,
        "total_quantity": total_quantity
    })


@login_required
def order_confirmation(request):
    cart = Cart.objects.get(customer=request.user)
    cart.items.all().delete()

    return render(request, "order_confirmation.html")

# shoppingcart/views.py
from django.http import HttpResponse
from .utils import OrderPDFGenerator

def order_pdf_view(request):
    # Gather order details
    order_details = {
        'product': 'Maple Taffy',
        'quantity': 1,
        'price': 20000,
        'total': 20000,
        'customer_name': 'carlitos',
        'delivery_address': 'Cll 100A Crr99B #312',
        'box_size': 'Small box: maximum 10 products',
        'total_price': 20000,
    }

    # Create the response object
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="order.pdf"'

    # Create context
    context = {
        'response': response,
        'order_details': order_details,
        'filename': 'Order Details',
    }

    # Generate the PDF
    pdf_generator = OrderPDFGenerator()
    pdf_generator.generate(context)

    return response


