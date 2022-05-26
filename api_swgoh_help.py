import requests
from json import loads, dumps
import time


class api_swgoh_help:
    def __init__(self, instance_settings):
        """
        :param instance_settings: Currently expects settings class object (defined below) or python dictionary
        username and password are required parameters within the settings
        """
        # Set defaults
        self.charStatsApi = 'https://crinolo-swgoh.glitch.me/testCalc/api'
        self.statsLocalPort = "8081"
        self.client_id = '123'
        self.client_secret = 'abc'
        self.token = {}
        self.urlBase = 'https://api.swgoh.help'
        self.signin = '/auth/signin'
        self.endpoints = {'guilds': '/swgoh/guilds',
                          'guild': '/swgoh/guilds',  # alias to support typos in client code
                          'players': '/swgoh/players',
                          'player': '/swgoh/players',  # alias to support typos in client code
                          'roster': '/swgoh/roster',
                          'data': '/swgoh/data',
                          'units': '/swgoh/units',
                          'zetas': '/swgoh/zetas',
                          'squads': '/swgoh/squads',
                          'events': '/swgoh/events',
                          'battles': '/swgoh/battles'}
        self.verbose = False
        self.debug = False
        if isinstance(instance_settings, dict):
            if 'username' in instance_settings:
                self.username = instance_settings['username']
            if 'password' in instance_settings:
                self.password = instance_settings['password']
            if 'client_id' in instance_settings:
                self.client_id = instance_settings['client_id']
            if 'client_secret' in instance_settings:
                self.client_secret = instance_settings['client_secret']
            if 'charStatsApi' in instance_settings:
                self.charStatsApi = instance_settings['charStatsApi']
            if 'statsLocalPort' in instance_settings:
                self.statsLocalPort = instance_settings['statsLocalPort']
            if 'statsUrlBase' in instance_settings:
                self.statsUrlBase = instance_settings['statsUrlBase']
            if 'verbose' in instance_settings:
                self.verbose = instance_settings['verbose']  # currently not implemented
            if 'debug' in instance_settings:
                self.debug = instance_settings['debug']  # currently not implemented
            if 'statsLocalPort' in instance_settings:
                self.statsLocalPort = instance_settings['statsLocalPort']
            if 'statsUrlBase' in instance_settings:
                self.statsUrlBase = instance_settings['statsUrlBase']
            else:
                self.statsUrlBase = "http://127.0.0.1:{}/api".format(self.statsLocalPort)
            if 'charStatsApi' in instance_settings:
                self.charStatsApi = instance_settings['charStatsApi']
        else:
            self.username = instance_settings.username
            self.password = instance_settings.password
            self.client_id = instance_settings.client_id
            self.client_secret = instance_settings.client_secret
            self.charStatsApi = instance_settings.charStatsApi
            self.statsLocalPort = instance_settings.statsLocalPort
            self.statsUrlBase = instance_settings.statsUrlBase
            self.verbose = instance_settings.verbose  # currently not implemented
            self.debug = instance_settings.debug  # currently not implemented
            self.user = "username=" + instance_settings.username
            self.user += "&password=" + instance_settings.password
            self.user += "&grant_type=password"
            self.user += "&client_id=" + instance_settings.client_id
            self.user += "&client_secret=" + instance_settings.client_secret
            if instance_settings.statsLocalPort:
                self.statsLocalPort = instance_settings.statsLocalPort
            if instance_settings.statsUrlBase:
                self.statsUrlBase = instance_settings.statsUrlBase
            else:
                self.statsUrlBase = "http://127.0.0.1:{}/api".format(self.statsLocalPort)
            if instance_settings.charStatsApi:
                self.charStatsApi = instance_settings.charStatsApi
        # Construct API login URL
        self.user = "username=" + self.username
        self.user += "&password=" + self.password
        self.user += "&grant_type=password"
        self.user += "&client_id=" + self.client_id
        self.user += "&client_secret=" + self.client_secret

    class LoginFailure(Exception):
        pass

    def _get_access_token(self):
        """
        Obtain an Authorization Bearer token from API
        :return:
        """
        # the existing token expire time is greater than the current time, return
        if 'expires' in self.token.keys():
            token_expire_time = self.token['expires']
            if token_expire_time > time.time():
                return self.token
        # Otherwise, get a new token
        signin_url = self.urlBase + self.signin
        payload = self.user
        head = {"Content-type": "application/x-www-form-urlencoded"}
        r = requests.request('POST', signin_url, headers=head, data=payload, timeout=10)
        if r.status_code != 200:
            raise self.LoginFailure("Authentication with API failed. [{}]".format(r.content.decode('utf-8')))
        response = loads(r.content.decode('utf-8'))
        self.token = {'Authorization': "Bearer " + response['access_token'],
                      'expires': time.time() + response['expires_in'] - 30}
        return self.token

    def getVersion(self):
        data_url = self.urlBase + '/version'
        try:
            r = requests.get(data_url)
            if r.status_code != 200:
                data = {"status_code": r.status_code,
                        "message": "Unable to fetch version"}
            else:
                data = loads(r.content.decode('utf-8'))
        except Exception as e:
            data = {"message": 'Cannot fetch version', "exception": str(e)}
        return data

    def fetchAPI(self, url, payload):
        self._get_access_token()
        head = {'Content-Type': 'application/json', 'Authorization': self.token['Authorization']}
        data_url = self.urlBase + url
        try:
            r = requests.request('POST', data_url, headers=head, data=dumps(payload))
            if r.status_code != 200:
                # error = 'Cannot fetch data - error code'
                error = r.content.decode('utf-8')
                data = {"status_code": r.status_code,
                        "message": error}
            else:
                data = loads(r.content.decode('utf-8'))
        except Exception as e:
            data = {"message": 'Cannot fetch data', "exception": str(e)}
        return data

    def fetchZetas(self):
        try:
            return self.fetchAPI(self.endpoints['zetas'], {})
        except Exception as e:
            return str(e)

    def fetchSquads(self):
        try:
            return self.fetchAPI(self.endpoints['squads'], {})
        except Exception as e:
            return str(e)

    def fetchBattles(self, payload=None):
        if payload is None:
            p = {'allycodes': payload, 'language': "eng_us", 'enums': True}
            payload = p
        try:
            return self.fetchAPI(self.endpoints['battles'], payload)
        except Exception as e:
            return str(e)

    def fetchEvents(self, payload=None):
        if payload is None:
            p = {'allycodes': payload, 'language': "eng_us", 'enums': True}
            payload = p
        try:
            return self.fetchAPI(self.endpoints['events'], payload)
        except Exception as e:
            return str(e)

    def fetchData(self, payload):
        if not isinstance(payload, dict):
            return {'message': "Payload ERROR: dict expected."}
        if 'collection' not in payload.keys():
            return {'message': "Payload ERROR: No collection element in provided dictionary."}
        try:
            return self.fetchAPI(self.endpoints['data'], payload)
        except Exception as e:
            return str(e)

    def fetchPlayers(self, payload):
        if isinstance(payload, list):
            p = {'allycodes': payload, 'language': "eng_us", 'enums': True}
            payload = p
        elif isinstance(payload, int):
            p = {'allycodes': [payload], 'language': "eng_us", 'enums': True}
            payload = p
        elif not isinstance(payload, dict):
            return {'message': "Payload ERROR: integer, list of integers, or dict expected.", 'status_code': "000"}
        try:
            return self.fetchAPI(self.endpoints['players'], payload)
        except Exception as e:
            return str(e)

    def fetchGuilds(self, payload):
        if isinstance(payload, list):
            p = {'allycodes': payload, 'language': "eng_us", 'enums': True}
            payload = p
        elif isinstance(payload, int):
            p = {'allycodes': [payload], 'language': "eng_us", 'enums': True}
            payload = p
        elif not isinstance(payload, dict):
            return {'message': "Payload ERROR: integer, list of integers, or dict expected.", 'status_code': "000"}
        try:
            return self.fetchAPI(self.endpoints['guilds'], payload)
        except Exception as e:
            return str(e)

    def fetchUnits(self, payload):
        if isinstance(payload, list):
            p = {'allycodes': payload, 'enums': True}
            payload = p
        elif isinstance(payload, int):
            p = {'allycodes': [payload], 'language': "eng_us", 'enums': True}
            payload = p
        elif not isinstance(payload, dict):
            return {'message': "Payload ERROR: integer, list of integers, or dict expected.", 'status_code': "000"}
        try:
            return self.fetchAPI(self.endpoints['units'], payload)
        except Exception as e:
            return str(e)

    def fetchRoster(self, payload):
        if isinstance(payload, list):
            p = {'allycodes': payload, 'enums': True}
            payload = p
        elif isinstance(payload, int):
            p = {'allycodes': [payload], 'enums': True}
            payload = p
        elif not isinstance(payload, dict):
            return {'message': "Payload ERROR: integer, list of integers, or dict expected.", 'status_code': "000"}
        try:
            return self.fetchAPI(self.endpoints['roster'], payload)
        except Exception as e:
            return str(e)


class settings:
    def __init__(self, _username, _password, **kwargs):
        self.username = _username
        self.password = _password
        self.client_id = kwargs.get('client_id', '123')
        self.client_secret = kwargs.get('client_secret', 'abc')
        self.charStatsApi = kwargs.get('charStatsApi', '')
        self.statsLocalPort = kwargs.get('statsLocalPort', "8081")
        self.statsUrlBase = kwargs.get('statsUrlBase', "http://127.0.0.1:{}".format(self.statsLocalPort))
        self.verbose = kwargs.get('verbose', False)  # currently not implemented
        self.debug = kwargs.get('debug', False)  # currently not implemented
        self.dump = kwargs.get('dump', False)  # currently not implemented
