from django.test import TestCase
from django.urls import reverse
from .models import Product


class ProductTestCase(TestCase):
    def setUp(self):
        self.product1 = Product.objects.create(name="Product 1", description="Description 1", country="JP", size="S", price=10)
        self.product2 = Product.objects.create(name="Product 2", description="Description 2", country="BR", size="M", price=20)

    def test_product_list_view(self):
        url = reverse('list')

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

        self.assertIn('products', response.context)

        self.assertIn(self.product1, response.context['products'])
        self.assertIn(self.product2, response.context['products'])
