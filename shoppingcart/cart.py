from django.contrib.sessions.models import Session
from users.models import CustomUser

class ShoppingCart:
    def __init__(self, session):
        self.session = session
        self.cart = self.session.get('cart', [])
        self.customer = self.get_customer()

    def add_product(self, product):
        self.cart.append(product)
        self.session['cart'] = self.cart

    def remove_product(self, product):
        self.cart.remove(product)
        self.session['cart'] = self.cart

    def get_products(self):
        return self.cart

    def get_total_price(self):
        total_price = 0
        for product in self.cart:
            total_price += product['price'] * product['quantity']
        return total_price

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
        return None

    def get_customer_phone(self):
        customer = self.get_customer()
        if customer:
            return customer.phone
        return None

    def get_customer_email(self):
        customer = self.get_customer()
        if customer:
            return customer.email
        return None

    def get_cart_quantity(self):
        return len(self.cart)