from django import forms
from .models import Code
from users.models import CustomUser


class CodeForm(forms.ModelForm):
    number = forms.CharField(label='Code', help_text="Enter SMS verification Code",
                             widget=forms.TextInput(attrs={'autofocus': True}))

    class Meta:
        model = Code
        fields = ('number',)
