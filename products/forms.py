from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    COUNTRYS_CHOICES = [
        ("Japon","Japon"),
        ("Brasil","Brasil"),
        ("Canada","Canada"),
        ("Rusia","Rusia"),
    ]
    
    SIZE_CHOICES = [
        ("Grande","Grande"),
        ("Mediano", "Mediano"),
        ("Pequeño","Pequeño"),    
    ]
    
    name = forms.CharField(label="Nombre",max_length=255)
    description = forms.CharField(label="Descripcion",max_length=255, widget=forms.Textarea())
    country = forms.ChoiceField(choices = COUNTRYS_CHOICES)
    size = forms.ChoiceField(choices = SIZE_CHOICES)
    image_product = forms.ImageField(required=False, label="Imagen del producto")
    price = forms.IntegerField(min_value=0)
    
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

# In your Django form definition (forms.py)



class YourProductForm(forms.Form):  # or forms.ModelForm if you have a model
    # your fields definitions here
    # ...

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({'class': 'form-check-input'})
            else:
                field.widget.attrs.update({'class': 'form-control'})
