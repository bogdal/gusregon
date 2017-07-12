from bs4 import BeautifulSoup, Tag
from requests import Session
from zeep import Client, Transport

WSDL = 'https://wyszukiwarkaregontest.stat.gov.pl/wsBIR/wsdl/UslugaBIRzewnPubl.xsd'
ENDPOINT = 'https://wyszukiwarkaregon.stat.gov.pl/wsBIR/UslugaBIRzewnPubl.svc'
ENDPOINT_SANDBOX = 'https://wyszukiwarkaregontest.stat.gov.pl/wsBIR/UslugaBIRzewnPubl.svc'


class GUS(object):
    endpoint = ENDPOINT
    headers = {'User-Agent': 'gusregon'}
    report_type = {
        'F': 'PublDaneRaportDzialalnoscFizycznejCeidg',
        'P': 'PublDaneRaportPrawna'
        'LP': 'PublDaneRaportLokalnaPrawnej',
        'LF': 'PublDaneRaportLokalnaFizycznej'}

    def __init__(self, api_key=None, sandbox=False):
        if not any([api_key, sandbox]):
            raise AttributeError('Api key is required.')
        self.api_key = api_key
        self.sandbox = sandbox
        if sandbox:
            self.api_key = api_key or 'abcde12345abcde12345'
            self.endpoint = ENDPOINT_SANDBOX
        session = Session()
        session.headers = self.headers
        client = Client(WSDL, transport=Transport(session=session))
        self.service = client.create_service('{http://tempuri.org/}e3', self.endpoint)
        self.headers.update({'sid': self._service('Zaloguj', self.api_key)})
        client.transport.session.headers = self.headers

    def _service(self, action, *args, **kwargs):
        service = getattr(self.service, action)
        return service(*args, **kwargs)

    def _remove_prefix(self, data):
        data = {item.name: item.get_text()
                for item in BeautifulSoup(data, 'lxml').dane if isinstance(item, Tag)}
        parsed_data = {}
        for name, value in data.items():
            parsed_data[name.split('_', 1)[1]] = value.strip()
        return parsed_data

    def search(self, nip=None, regon=None, krs=None):
        if not any([nip, regon, krs]):
            raise AttributeError(
                'At least one parameter (nip, regon, krs) is required.')
        if nip:
            search_params = {'Nip': nip}
        elif regon:
            search_params = {'Regon': regon}
        else:
            search_params = {'Krs': krs}

        details = self._service('DaneSzukaj', search_params)
        if details is not None:
            data = BeautifulSoup(details, 'lxml')
            report_type = self.report_type.get(data.typ.get_text())
            return self._remove_prefix(self._service(
                'DanePobierzPelnyRaport', data.regon.get_text(), report_type))

    def get_address(self, *args, **kwargs):
        details = self.search(*args, **kwargs)
        if details:
            postal_code = details['adsiedzkodpocztowy']
            address = '%s %s' % (details['adsiedzulica_nazwa'],
                                 details['adsiedznumernieruchomosci'])
            if details['adsiedznumerlokalu']:
                address += '/%s' % details['adsiedznumerlokalu']
            return {
                'name': details['nazwa'],
                'street_address': address,
                'postal_code': '%s-%s' % (postal_code[:2], postal_code[2:]),
                'city': details['adsiedzmiejscowosc_nazwa']}
