from django.contrib.sessions.models import Session
from users.models import CustomUser
from products.models import Product
from .models import Cart, CartItem
from django.http import HttpRequest

class ShoppingCart:
    def __init__(self, request):
        self.request = request
        self.session = request.session

    def get_cart(self, request):
        customer_id = request.user.id
        customer = CustomUser.objects.get(pk=customer_id)
        cart = Cart.objects.get(customer=customer)
        return cart

    def add_product(self, cart_id, product_id, quantity):
        cart = Cart.objects.get(pk=cart_id)
        product = Product.objects.get(pk=product_id)
        query = CartItem.objects.filter(cart=cart, product=product)
        if not query.exists():
            item = CartItem(cart_id=cart_id, product_id = product_id, quantity=quantity)
            item.save()

    def remove_product(self, cart_id, product_id):
        cart = Cart.objects.get(pk=cart_id)
        product = Product.objects.get(pk=product_id)
        query = CartItem.objects.filter(cart=cart, product=product)
        if query.exists():
            item = CartItem.objects.filter(cart=cart, product=product)
            item.delete()
            
    def get_total(self, cart_id):
        total = 0
        cart = Cart.objects.get(pk=cart_id)
        query = CartItem.objects.filter(cart=cart)
        print(query)
            
    def get_cart_quantity(self):
        cart = self.get_cart()
        return sum(item['quantity'] for item in cart.values())
    
    def get_total_quantity(cart_items):
        total_quantity = 0
        for item in cart_items:
            total_quantity += item.quantity
        return total_quantity

    def get_cart_id(self):
        return self.session.session_key

    def get_customer(self):
        customer_id = self.session.get('customer_id')
        if customer_id:
            return CustomUser.objects.get(id=customer_id)
        return None

    def get_customer_name(self):
        customer = self.get_customer()
        if customer:
            return customer.name
        return None

    def get_customer_address(self):
        customer = self.get_customer()
        if customer:
            return customer.address
        return