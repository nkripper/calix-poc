import requests
import time
from urllib.parse import urlencode


class Calix:
    BASE_URL = 'https://api.calix.ai/v1'

    def __init__(self, client_id, client_secret, username, password):
        self.access_token = None
        self.token_type = None
        self.expires_in = None
        self.refresh_token = None
        self.client_secret = client_secret
        self.headers = {'X-Calix-ClientID': client_id}
        self.token(username, password)

    def set_auth_data(self, response):
        self.access_token = response.get('access_token')
        self.token_type = response.get('token_type')
        self.expires_in = int(response.get('expires_in')) + int(time.time())
        self.refresh_token = response.get('refresh_token')
        self.headers['X-Calix-AccessToken'] = self.access_token

    def send_request(self, url, method='get', data=None):
        request_method = getattr(requests, method)
        response = request_method(url, data=data, headers=self.headers)

        if response.status_code == 200:
            return response.json()
        else:
            print(f'Status Code:' + response.text)
            exit(1)

    def token(self, username: str, password: str):
        # https://developers.calix.com/api/token-api-password-grant
        url = self.BASE_URL + '/authentication/token'

        data = {
            'grant_type': 'password',
            'username': username,
            'password':  password,
            'client_secret': self.client_secret
        }

        response = self.send_request(url, method='post', data=data)
        self.set_auth_data(response)

    def token_refresh(self):
        # Does the token need a refresh?
        if int(time.time()) < self.expires_in:
            return False

        url = self.BASE_URL + '/authentication/refresh-token'

        data = {
            'grant_type': 'refresh_token',
            'refresh_token': self.refresh_token,
            'client_secret': self.client_secret
        }

        response = requests.post(url, data=data, headers=self.headers)

        if response.status_code == 200:
            self.set_auth_data(response.json())
            return response.json()
        else:
            print(f"Refresh Token error: {response.text}")
            exit(1)

    def subscribers(self, **kwargs):
        # https://developers.calix.com/api/subscriber-service#/Subscriber/get_subscribers
        url = self.BASE_URL + '/billing/subscribers'

        self.token_refresh()

        if kwargs.get('_id'):
            url += '/' + kwargs.get('_id')
        else:
            query_string = urlencode(kwargs)
            url += f'?{query_string}'

            # for key, value in kwargs.items():
            #    url += f'&{key}={value}'

        response = self.send_request(url)

        return response

    def devices(self, subscriber_id):
        # https://developers.calix.com/api/subscriber-service#/Subscriber%20-%20Devices/get_subscribers__subscriberId__devices
        self.token_refresh()
        url = self.BASE_URL + f'/billing/subscribers/{subscriber_id}/devices'

        response = self.send_request(url)
        return response
