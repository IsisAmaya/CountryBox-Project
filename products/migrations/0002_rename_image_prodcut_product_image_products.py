# Generated by Django 4.1 on 2024-03-16 22:32

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="product",
            old_name="image_prodcut",
            new_name="image_products",
        ),
    ]