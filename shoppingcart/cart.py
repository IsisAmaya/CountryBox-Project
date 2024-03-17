from django.contrib.sessions.models import Session
from users.models import CustomUser
from django.http import HttpRequest

class ShoppingCart:
    def __init__(self, request):
        self.request = request
        self.session = request.session
        self.cart = self.get_cart()

    def get_cart(self):
        cart = self.session.get('cart', [])
        return cart

    def add_product(self, product_id, quantity):
        cart = self.get_cart()
        if not cart:
            cart = []
        if product_id not in cart:
            cart.append({'id': product_id, 'quantity': quantity})
        else:
            for item in cart:
                if item['id'] == product_id:
                    item['quantity'] += quantity
                    break
        self.session['cart'] = cart

    def remove_product(self, product):
        cart = self.get_cart()
        if product in cart:
            del cart[product]
            self.session['cart'] = cart

    def get_cart_quantity(self):
        cart = self.get_cart()
        return sum(item['quantity'] for item in cart.values())

    def get_cart_total_price(self):
        cart = self.get_cart()
        return sum(item['price'] * item['quantity'] for item in cart.values())

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