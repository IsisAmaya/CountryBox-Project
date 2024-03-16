from django import forms

class DeliveryAddressForm(forms.Form):
    address_line_1 = forms.CharField(max_length=100)
    address_line_2 = forms.CharField(max_length=100, required=False)
    city = forms.CharField(max_length=50)
    state = forms.CharField(max_length=50)
    zip_code = forms.CharField(max_length=10)