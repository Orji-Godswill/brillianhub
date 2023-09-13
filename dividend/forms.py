from django import forms
from .models import Dividend


class DividendForm(forms.ModelForm):
    class Meta:
        model = Dividend

        fields = ('package', 'amount')

        widgets = {
            'amount': forms.Select(attrs={"class": "form-control", "placeholder": "Enter amount here"}),
        }
