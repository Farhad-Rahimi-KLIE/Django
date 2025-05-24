# customers/forms.py
from django import forms
from .models import Customer, Account

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'join_date', 'data_allocation', 'savings']
        widgets = {
            'join_date': forms.DateInput(attrs={'type': 'date'}),
        }

class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['date', 'data_used', 'buy_balance', 'bill_image', 'continuous_number', 'extra_off']
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }