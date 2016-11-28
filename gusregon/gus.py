from bs4 import BeautifulSoup, Tag
from suds.bindings import binding
from suds.client import Client
from suds.plugin import MessagePlugin
from suds.sax.element import Element

binding.envns = ('SOAP-ENV', 'http://www.w3.org/2003/05/soap-envelope')


class GUS(object):
    wsdl = 'https://wyszukiwarkaregontest.stat.gov.pl/wsBIR/wsdl/UslugaBIRzewnPubl.xsd'
    location = 'https://wyszukiwarkaregon.stat.gov.pl/wsBIR/UslugaBIRzewnPubl.svc'
    headers = {'Content-Type': 'application/soap+xml; charset=utf-8'}
    report_type = {
        'F': 'PublDaneRaportDzialalnoscFizycznejCeidg',
        'P': 'PublDaneRaportPrawna'}

    def __init__(self, api_key=None, sandbox=False):
        if not any([api_key, sandbox]):
            raise AttributeError('Api key is required.')
        self.api_key = api_key
        self.sandbox = sandbox
        self.sid = None
        if sandbox:
            self.api_key = 'abcde12345abcde12345'
            self.location = 'https://wyszukiwarkaregontest.stat.gov.pl/wsBIR/UslugaBIRzewnPubl.svc'
        self.client = Client(
            self.wsdl, location=self.location, headers=self.headers, plugins=[MultipartFilter()])
        self._login()

    def _service(self, action, *args, **kwargs):
        wsans = ('wsa', "http://www.w3.org/2005/08/addressing")
        action_text = 'http://CIS/BIR/PUBL/2014/07/IUslugaBIRzewnPubl/%s' % (action,)
        self.client.set_options(soapheaders=[
            Element('To', ns=wsans).setText(self.location),
            Element('Action', ns=wsans).setText(action_text)])
        if self.sid:
            self.headers.update({'sid': self.sid})
            self.client.set_options(headers=self.headers)
        service = getattr(self.client.service, action)
        return service(*args, **kwargs)

    def _login(self):
        self.sid = self._service('Zaloguj', self.api_key)

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


class MultipartFilter(MessagePlugin):
    def received(self, context):
        ending_tag = b'</s:Envelope>'
        start = context.reply.find(b'<s:Envelope')
        end = context.reply.find(ending_tag) + len(ending_tag)
        context.reply = context.reply[start:end]
