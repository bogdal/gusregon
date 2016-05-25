from django import forms


class MyForm(forms.Form):
    nip = forms.CharField()
