from django import forms
from .models import Product
from django.utils.translation import gettext_lazy as _


class ProductForm(forms.ModelForm):
    
    COUNTRYS_CHOICES = [
        ('JP', _("Japan")),
        ('BR', _("Brazil")),
        ('CA', _("Canada")),
        ('RU', _("Russia")),
    ]
    
    SIZE_CHOICES = [
        ('L', _("Large")),
        ('M', _("Medium")),
        ('S', _("Small")),    
    ]
    
    name = forms.CharField(label=_("Name"),max_length=255)
    description = forms.CharField(label=_("Description"),max_length=255, widget=forms.Textarea())
    country = forms.ChoiceField(choices = COUNTRYS_CHOICES, label=_("Country"))
    size = forms.ChoiceField(choices = SIZE_CHOICES, label=_("Size"))
    image_product = forms.ImageField(required=False, label=_("Image of product"))
    price = forms.IntegerField(min_value=0, label=_("Price"))
    
    class Meta:
        model = Product
        fields = [
            'name',
            'description',
            'country',
            'size',
            'image_product',
            'price',
        ]
