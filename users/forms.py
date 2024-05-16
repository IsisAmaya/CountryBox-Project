from django import forms
from django.contrib.auth.forms import UserCreationForm
from users.models import CustomUser #Nuestro modelo
from django.utils.translation import gettext_lazy as _


class UserSingupForm(UserCreationForm):
    email = forms.EmailField(
        label=_('Email')
    )
    
    phone_number = forms.IntegerField(
        min_value=0,
        label=_('Phone number')
    )
    
    address = forms.CharField(
        label=_('Address')
    )
    
    password1 = forms.CharField(
        label=_('Password'),
        strip=False,
        widget=forms.PasswordInput,
        help_text='',
    )
    password2 = forms.CharField(
        label=_('Password confirmation'),
        widget=forms.PasswordInput,
        strip=False,
        help_text=_('Enter the same password as before, for verification.'),
    )

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ['username','email', 'phone_number','address' ,'password1', 'password2']
        help_texts={k:"" for k in fields}



class UserStaffForm(forms.ModelForm):
    is_staff = forms.BooleanField(required=False, label=_("Is staff"))

    class Meta:
        model = CustomUser
        fields = ['is_staff']