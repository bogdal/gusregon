from django import forms
from gusregon.fields import GUSCaptchaField


class MyForm(forms.Form):

    nip = forms.CharField()
    gus = GUSCaptchaField(label='Captcha')

