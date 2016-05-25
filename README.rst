django-gusregon
===============

`GUS (Główny Urząd Statystyczny) REGON <https://wyszukiwarkaregon.stat.gov.pl/appBIR/index.aspx>`_ Internet Database client which allows to get detailed information about company based on NIP, Regon or KRS number.


Quickstart
----------

Install the package via ``pip``:

.. code-block:: bash

    pip install django-gusregon


Usage
-----

.. code-block:: python

    from django import forms
    from gusregon.gus import GUS

    class MyForm(forms.Form):
        nip = forms.CharField()

    ...

    form = MyForm(data=request.POST or None)
    if form.is_valid():
        gus = GUS()
        company_details = gus.search(form.cleaned_data.get('nip'))


API

.. code-block:: python

    from gusregon.gus import GUS
    
    gus = GUS()
    gus.search(nip='..')
    gus.search(krs='..')
    gus.search(regon='..')


For more information, see `GUS <https://github.com/bogdal/django-gusregon/blob/master/gusregon/gus.py>`_ api class.
