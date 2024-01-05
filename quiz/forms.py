from django import forms
from .models import Question, Choice


class QuizForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text']

    choices = forms.ModelChoiceField(
        queryset=None,
        widget=forms.RadioSelect,
        empty_label=None,
    )

    def __init__(self, *args, **kwargs):
        super(QuizForm, self).__init__(*args, **kwargs)

        if self.instance:
            self.fields['choices'].queryset = self.instance.choice_set.all()


class ChoiceSelectionForm(forms.Form):
    def __init__(self, *args, **kwargs):
        question_id = kwargs.pop('question_id', None)
        super(ChoiceSelectionForm, self).__init__(*args, **kwargs)

        if question_id:
            choices = Choice.objects.filter(question__id=question_id)
            self.fields['choices'] = forms.ModelChoiceField(
                queryset=choices, widget=forms.RadioSelect)
