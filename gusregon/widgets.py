from django.forms.widgets import TextInput, HiddenInput, MultiWidget
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from .gus import GUS


class GUSCaptchaInput(MultiWidget):

    def __init__(self, attrs=None):
        widgets = (
            HiddenInput(attrs),
            TextInput(attrs))
        super(GUSCaptchaInput, self).__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            return value.split(',')
        return [None, None]

    def render(self, name, value, attrs=None):
        gus = GUS()
        gus.login()
        value = [gus.sid, '']
        captcha_img = '<img src="data:image/jpg;base64,%s" alt="captcha" ' \
            'class="gus-captcha" />' % (gus.get_captcha(),)
        html = super(GUSCaptchaInput, self).render(name, value, attrs=attrs)
        return mark_safe(captcha_img + html)
