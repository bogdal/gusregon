from django import forms
from django.forms.fields import CharField, MultiValueField
from django.utils.translation import ugettext_lazy as _

from .gus import GUS
from .widgets import GUSCaptchaInput


class GUSCaptchaField(MultiValueField):

    widget = GUSCaptchaInput

    def __init__(self, *args, **kwargs):
        fields = (
            CharField(show_hidden_initial=True),
            CharField())
        super(GUSCaptchaField, self).__init__(fields, *args, **kwargs)

    def compress(self, data_list):
        if data_list:
            return ','.join(data_list)
        return None

    def clean(self, value):
        super(GUSCaptchaField, self).clean(value)
        sid, captcha_code = value
        if captcha_code:
            gus = GUS(sid)
            if not gus.check_captcha(captcha_code):
                raise forms.ValidationError(_('Invalid CAPTCHA'))
            return gus
        return None
