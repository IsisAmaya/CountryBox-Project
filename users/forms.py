from django import forms
from django.contrib.auth.forms import UserCreationForm
#from django.contrib.auth.models import User
from users.models import CustomUser #Nuestro modelo


class UserSingupForm(UserCreationForm):
    email = forms.EmailField(
        label='Email'
    )
    
    phone_number = forms.IntegerField(
        min_value=0
    )
    
    password1 = forms.CharField(
        label='Password',
        strip=False,
        widget=forms.PasswordInput,
        help_text='',
    )
    password2 = forms.CharField(
        label='Password confirmation',
        widget=forms.PasswordInput,
        strip=False,
        help_text='Enter the same password as before, for verification.',
    )

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ['username','email', 'phone_number','address' ,'password1', 'password2','is_staff']
        help_texts={k:"" for k in fields}
   

