# core/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Wager, Transaction

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class BetForm(forms.ModelForm):
    class Meta:
        model = Wager
        fields = ['outcome', 'stake']
        widgets = {
            'outcome': forms.Select(attrs={'class': 'form-control'}),
            'stake': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
        }

    def clean_stake(self):
        stake = self.cleaned_data['stake']
        if stake <= 0:
            raise forms.ValidationError("Stake must be greater than zero.")
        return stake


class DepositForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['amount']
        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
        }

    def clean_amount(self):
        amount = self.cleaned_data['amount']
        if amount <= 0:
            raise forms.ValidationError("Deposit amount must be greater than zero.")
        return amount


class WithdrawForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['amount']
        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
        }

    def clean_amount(self):
        amount = self.cleaned_data['amount']
        if amount <= 0:
            raise forms.ValidationError("Withdrawal amount must be greater than zero.")
        # User balance check will happen in the view
        return amount