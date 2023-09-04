from django import forms

from . import models

class StartForm(forms.Form):
    username = forms.EmailField()

class AnswerForm(forms.Form):
    hate_level = forms.ChoiceField(choices=models.HateLevel.choices,widget=forms.RadioSelect)
    hate_cathegory = forms.ChoiceField(choices=models.HateCathegory.choices,widget=forms.RadioSelect)
