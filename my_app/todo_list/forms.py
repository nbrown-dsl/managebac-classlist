from django import forms
from functions.models import List

class ListForm(forms.ModelForm):
    class Meta:
        model = List
        fields = ["item","completed","priority"] 

