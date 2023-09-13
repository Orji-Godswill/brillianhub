from django import forms
from .models import Earn, Payout, Referrer
from django.contrib.auth import get_user_model

User = get_user_model()


class PayoutForm(forms.ModelForm):
    class Meta:
        model = Payout
        fields = ('email', 'amount')
        widgets = {
            'amount': forms.NumberInput(attrs={"class": "form-control", "placeholder": "Amount"}),
            'email': forms.EmailInput(attrs={"class": "form-control", "placeholder": "Enter a valid email address"})
        }

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if float(amount) % 10000 != 0:
            raise forms.ValidationError(
                'Amount must be in multpiles of 10,000.00')
        return amount
