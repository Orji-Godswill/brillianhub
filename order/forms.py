from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('slot', 'referrer', 'payment_option')

        widgets = {
            'slot': forms.NumberInput(attrs={"class": "form-control", "placeholder": "Enter number of slots. e.g. 1, 2 or 3"}),

            'payment_option': forms.Select(attrs={"class": "form-control", "placeholder": "Select payment option"}),
        }
