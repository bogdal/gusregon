gusregon
========

.. image:: https://img.shields.io/circleci/project/bogdal/gusregon/master.svg
    :target: https://circleci.com/gh/bogdal/gusregon/tree/master
    
.. image:: https://img.shields.io/pypi/v/gusregon.svg   
     :target: https://pypi.python.org/pypi/gusregon
  
  
`GUS (Główny Urząd Statystyczny) REGON <https://wyszukiwarkaregon.stat.gov.pl/appBIR/index.aspx>`_ Internet Database client which allows to get detailed information about company based on NIP, Regon or KRS number.

It requires an **API key** to the `BIR1 service <http://bip.stat.gov.pl/dzialalnosc-statystyki-publicznej/rejestr-regon/interfejsyapi/>`_.

*Note:* Currently ``django-gusregon`` package is outdated and should be replaced by ``gusregon``.


Quickstart
----------

Install the package via ``pip``:

.. code-block:: bash

    pip install gusregon

Usage
-----
Returns the business address

.. code-block:: python

    from gusregon import GUS

    gus = GUS(api_key='my_api_key')
    gus.get_address(nip='1112223344')

output

.. code-block::

    {
        'name': 'REGON SYSTEMS SPÓŁKA AKCYJNA',
        'street_address': 'ul. Tęczowa 14',
        'postal_code': '35-322',
        'city': 'Rzeszów'
    }

Returns PKD codes


.. code-block:: python

    gus.get_pkd(nip='1112223344')

output

.. code-block::

    [
        {
            'code': '6201Z',
            'name': 'DZIAŁALNOŚĆ ZWIĄZANA Z OPROGRAMOWANIEM',
            'main': True
        },
        {
            'code': '6312Z':
            'name': 'DZIAŁALNOŚĆ PORTALI INTERNETOWYCH',
            'main': False
        },
        ...
    ]

Returns all data from BIR1 service

.. code-block:: python

    gus.search(nip='1112223344')

output

.. code-block::

    {
        'adsiedzkraj_symbol': 'PL',
        'datazawieszeniadzialalnosci': '',
        'jednosteklokalnych': '0',
        'rodzajrejestruewidencji_symbol': '138',
        'adkorulica_nazwa': '',
        ...
        'adkorpowiat_symbol': '63',
        'datawpisudoregon': '2012-06-01',
        'rodzajrejestruewidencji_nazwa': 'REJESTR PRZEDSIĘBIORCÓW',
        'adsiedznumernieruchomosci': '14',
        'adkorkodpocztowy': '35322',
        'adsiedzkraj_nazwa': 'POLSKA',
        'adsiedzulica_symbol': '10013',
        'adsiedzkodpocztowy': '35322',
    }



Sandbox mode for testing:

.. code-block:: python

    from gusregon import GUS

    gus = GUS(sandbox=True)
    gus.get_address(nip='1112223344')
