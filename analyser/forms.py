from django import forms


return_choices = (
    (1, 'Annual'),
    (2, 'Biannual'),
    (4, 'Quarterly'),
    (12, 'Monthly'),
    (52, 'Weekly'),
    (365, 'Daily'),
)

frequency_choices = (
    (1, "I don't have recurring savings plan"),
    (1, "One time in a year"),
    (2, "Two times in a year"),
    (4, "Four times in a year"),
    (12, "Monthly"),
    (52, "Weekly"),
    (365, "Daily"),
)


class SavingsCalculationForm(forms.Form):
    initial_deposit = forms.FloatField(label='Initial deposit', initial=1000)
    installmental_payment = forms.FloatField(
        label="Regular deposits", initial=0.00)
    frequency_installment_payment = forms.ChoiceField(
        label="How often is your regular deposit?", choices=frequency_choices)
    duration = forms.IntegerField(
        label="How long in years do you plan to save?", initial=5)
    interest_rate = forms.FloatField(label="Interest rate %", initial=5)
    rate_of_return = forms.ChoiceField(choices=return_choices)


# Savings Target Calculator Form
return_frequency = (
    (1, 'Annual'),
    (2, 'Biannual'),
    (4, 'Quarterly'),
    (12, 'Monthly'),
    (52, 'Weekly'),
    (365, 'Daily'),
)


class SavingsTargetForm(forms.Form):
    target_amount = forms.FloatField(label='Savings Target', initial=5000)
    initial_deposit = forms.FloatField(label='Initial deposit', initial=1000)
    duration = forms.IntegerField(
        label="How long in years do you plan to save?", initial=5)
    interest_rate = forms.FloatField(label="Interest rate %", initial=5)
    rate_of_return = forms.ChoiceField(choices=return_frequency)


class StockReturnForm(forms.Form):
    symbol = forms.CharField(label='Stock Symbol', max_length=10)
    invested_amount = forms.FloatField(label='Amount invested', initial=1000)
