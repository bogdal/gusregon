import requests
import json


GUS_API_URL = 'https://wyszukiwarkaregon.stat.gov.pl/wsBIR/UslugaBIRzewnPubl.svc/ajaxEndpoint/'

LOGIN_ENDPOINT = 'Zaloguj'
CAPTCHA_ENDPOINT = 'PobierzCaptcha'
CHECK_CAPTCHA_ENDPOINT = 'SprawdzCaptcha'
SEARCH_ENDPOINT = 'daneSzukaj'
COMPANY_DETAILS_ENDPOINT = 'DanePobierzPelnyRaport'


class GUS(object):

    sid = None

    report_type = {
        'F': 'DaneRaportFizycznaPubl',
        'P': 'DaneRaportPrawnaPubl'}

    prefix_data = {
        'F': 'fiz_',
        'P': 'praw_'}

    def __init__(self, sid=None):
        self.sid = sid

    def login(self):
        data = {'pKluczUzytkownika': 'aaaaaabbbbbcccccdddd'}
        self.sid = self._post(LOGIN_ENDPOINT, data=json.dumps(data))
        return self.sid

    def get_captcha(self):
        return self._post(CAPTCHA_ENDPOINT)

    def check_captcha(self, captcha):
        data = {'pCaptcha': captcha}
        return self._post(
            CHECK_CAPTCHA_ENDPOINT, data=json.dumps(data))

    def search(self, nip=None, regon=None, krs=None,
               detailed=True, no_prefix=True):
        if not any([nip, regon, krs]):
            raise AttributeError(
                'At least one parameter (nip, regon, krs) is required.')
        if nip:
            search_params = {'Nip': nip}
        elif regon:
            search_params = {'Regon': regon}
        else:
            search_params = {'Krs': krs}
        data = {'pParametryWyszukiwania': search_params}
        basic_info = self._post(
            SEARCH_ENDPOINT, data=json.dumps(data))

        if not detailed or not basic_info:
            return basic_info

        basic_info = json.loads(basic_info)[0]

        data = {
            'pNazwaRaportu': self.report_type.get(basic_info['Typ']),
            'pRegon': basic_info['Regon'],
            'pSilosID': 1,
        }
        details = json.loads(self._post(
            COMPANY_DETAILS_ENDPOINT, data=json.dumps(data)))[0]
        if no_prefix:
            return self._remove_prefix(details)
        return details

    def _post(self, url, **kwargs):
        headers = {'Content-Type': 'application/json'}
        if self.sid:
            headers.update({'sid': self.sid})
        url = '%s%s' % (GUS_API_URL, url)
        response = requests.post(url, headers=headers, **kwargs)
        return json.loads(response.content)['d']

    def _remove_prefix(self, data):
        data_without_prefix = {}
        for key, value in data.iteritems():
            if key.startswith(tuple(self.prefix_data.values())):
                key = key[key.find('_') + 1:]
            data_without_prefix[key] = value
        return data_without_prefix
