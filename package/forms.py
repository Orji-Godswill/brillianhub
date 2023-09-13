from django import forms
from .models import Package


class CreatePackageForm(forms.ModelForm):
    class Meta:
        model = Package

        fields = ('title', 'cost', 'description', 'area', 'location', 'user')
        widgets = {
            'title': forms.TextInput(attrs={"class": "form-control", "placeholder": "Title"}),
            'cost': forms.NumberInput(attrs={"class": "form-control", "placeholder": "Amount"}),
            'area': forms.NumberInput(attrs={"class": "form-control", "placeholder": "Plan Area"}),
            'location': forms.TextInput(attrs={"class": "form-control", "placeholder": "Location"}),
            'user': forms.HiddenInput(attrs={"class": "form-control"}),
        }
