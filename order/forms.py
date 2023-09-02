from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('slot', 'payment_option')

        widgets = {
            'payment_option': forms.Select(attrs={"class": "form-control", "placeholder": "Select payment option"}),
        }
