# Generated by Django 4.1 on 2024-03-17 06:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("shoppingcart", "0002_cart_quantity_delete_cartitem"),
        ("products", "0003_rename_image_products_product_image_product"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="shopping_cart",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="products",
                to="shoppingcart.cart",
            ),
        ),
    ]
