from django.db import models
from users.models import CustomUser
from products.models import Product


class Cart(models.Model):
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} ({self.quantity})"

    def get_total_price(self):
        return self.product.price * self.quantity

    
    @classmethod
    def all(cls):
        return cls.objects.all()


class Order(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    address = models.CharField(max_length=255, default='Dirección predeterminada')


    def __str__(self):
        return f"Order {self.pk}"
    
    def get_total_quantity(self):
        total_quantity = 0
        for item in self:
            total_quantity += item.quantity
        return total_quantity

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} ({self.quantity})"

    def get_total_price(self):
        return self.price * self.quantity
    
    def get_total_cart_price(self):
        total_price = sum(item.get_total_price() for item in self.cartitem_set.all())
        return total_price


    @classmethod
    def all(cls):
        return cls.objects.all()