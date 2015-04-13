django-gusregon
===============

`GUS (Główny Urząd Statystyczny) REGON <https://wyszukiwarkaregon.stat.gov.pl/appBIR/index.aspx>`_ Internet Database client which allows to get detailed information about company based on NIP, Regon or KRS number.


Quickstart
----------

1. Install the package via ``pip``:

.. code-block:: bash

    pip install django-gusregon


2. Add ``gusregon`` to ``INSTALLED_APPS``:

.. code-block:: python

    INSTALLED_APPS = (
      ...
      'gusregon',
      ...
    )



Usage
-----

.. code-block:: python

    from django import forms
    from gusregon.fields import GUSCaptchaField

    class MyForm(forms.Form):
        nip = forms.CharField()
        gus = GUSCaptchaField(label='Captcha')

    ...

    form = MyForm(data=request.POST or None)
    if form.is_valid():
        gus = form.cleaned_data.get('gus')
        company_details = gus.search(form.cleaned_data.get('nip'))

For more information, see `GUS <https://github.com/bogdal/django-gusregon/gusregon/gus.py>`_ api class.
