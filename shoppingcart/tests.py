from django.test import TestCase
from users.models import CustomUser
from products.models import Product
from django.contrib.auth.models import User
from .utils import ShoppingCart
from .models import Cart, CartItem, Product

class ShoppingCartTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(username="testuser", email="test@example.com")
        self.product = Product.objects.create(name="Test Product", price=10.0)
        self.cart = Cart.objects.create(customer=self.user)
        self.cart_item = CartItem.objects.create(cart=self.cart, product=self.product, quantity=2)

    def test_get_total_quantity(self):
        cart_items = CartItem.objects.filter(cart=self.cart)
        total_quantity = ShoppingCart.get_total_quantity(cart_items)
        self.assertEqual(total_quantity, 2)