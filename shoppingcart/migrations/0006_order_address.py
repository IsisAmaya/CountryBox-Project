# Generated by Django 5.0.2 on 2024-05-14 01:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shoppingcart', '0005_remove_order_delivery_address_order_cart_orderitem_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='address',
            field=models.CharField(default='Dirección predeterminada', max_length=255),
        ),
    ]
