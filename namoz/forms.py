from django import forms
from .models import Namoz

class NamozForm(forms.ModelForm):
    class Meta:
        model = Namoz
        fields = ['bomdod', 'peshin', 'asr', 'shom', 'xufton', 'vitr']