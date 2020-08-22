from django import forms

from .models import Credentials


class CForm(forms.ModelForm):
    class Meta:
        model = Credentials
        fields = '__all__'
