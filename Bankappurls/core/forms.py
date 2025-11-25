from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class QuickWalletForm(forms.Form):
    ACTIONS = (
        ('DEPOSIT', 'Deposit'),
        ('WITHDRAW', 'Withdraw'),
    )
    action = forms.ChoiceField(choices=ACTIONS)
    amount = forms.DecimalField(min_value=0.01, max_digits=10, decimal_places=2)
