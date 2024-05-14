from django import forms

class PaymentForm(forms.Form):
    payment_method = forms.ChoiceField(
        label="Método de pago",
        choices=(('Cash', 'Pago en efectivo'), ('Card', 'Pago con tarjeta')),
        widget=forms.RadioSelect,
        initial='Cash',
    )
    card_number = forms.CharField(label="Número de la tarjeta", max_length=16, required=False)
    card_expiration_date = forms.CharField(label="Fecha de expiración (MM/AA)", max_length=5, required=False)
    card_holder = forms.CharField(label="Titular de la tarjeta", max_length=100, required=False)
    card_bank = forms.CharField(label="Banco", max_length=100, required=False)
    card_cvv = forms.CharField(label="CVV", max_length=3, required=False)

    def clean(self):
        cleaned_data = super().clean()
        payment_method = cleaned_data.get("payment_method")
        if payment_method == 'Card':
            if not all([cleaned_data.get("card_number"), cleaned_data.get("card_expiration_date"),
                        cleaned_data.get("card_holder"), cleaned_data.get("card_bank"), cleaned_data.get("card_cvv")]):
                raise forms.ValidationError("Todos los campos de la tarjeta de crédito son obligatorios para pagos con tarjeta.")
        return cleaned_data
