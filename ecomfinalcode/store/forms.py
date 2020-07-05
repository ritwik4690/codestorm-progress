from django import forms
from .models import Person

class PersonForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
 
    class Meta:
        model= Person
        fields= ["firstname", "lastname", "email","password"]
