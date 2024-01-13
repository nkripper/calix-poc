import requests
import time


class Calix:
    def __init__(self, client_id, client_secret, username, password):
        self.access_token = None
        self.token_type = None
        self.expires_in = None
        self.refresh_token = None
        self.client_secret = client_secret

        self.base_url = 'https://api.calix.ai/v1'
        self.headers = {'X-Calix-ClientID': client_id}

        self.token(username, password)

    def token(self, username: str, password: str):
        # https://developers.calix.com/api/token-api-password-grant
        url = self.base_url + '/authentication/token'

        data = {
            'grant_type': 'password',
            'username': username,
            'password':  password,
            'client_secret': self.client_secret
        }

        response = requests.post(url, data=data, headers=self.headers)

        if response.status_code == 200:
            self.access_token = response.json().get('access_token')
            self.token_type = response.json().get('token_type')
            self.expires_in = int(response.json().get('expires_in')) + int(time.time())
            self.refresh_token = response.json().get('refresh_token')
            self.headers['X-Calix-AccessToken'] = self.access_token

            return response.json()
        else:
            print("Token error:")
            print(response.text)
            exit(1)

    def token_refresh(self):

        # Does the token need a refresh?
        if int(time.time()) < self.expires_in:
            return False

        url = self.base_url + '/authentication/refresh-token'

        data = {
            'grant_type': 'refresh_token',
            'refresh_token': self.refresh_token,
            'client_secret': self.client_secret
        }

        response = requests.post(url, data=data, headers=self.headers)

        if response.status_code == 200:
            self.access_token = response.json().get('access_token')
            self.token_type = response.json().get('token_type')
            self.expires_in = int(response.json().get('expires_in')) + int(time.time())
            self.refresh_token = response.json().get('refresh_token')
            self.headers['X-Calix-AccessToken'] = self.access_token

            return response.json()
        else:
            print("Refresh Token error:")
            print(response.text)
            exit(1)

    def subscribers(self, **kwargs):
        # https://developers.calix.com/api/subscriber-service#/Subscriber/get_subscribers
        url = self.base_url + '/billing/subscribers'

        self.token_refresh()

        if kwargs.get('_id'):
            url += '/' + kwargs.get('_id')
        else:
            url += '?'

            for key, value in kwargs.items():
                url += f'&{key}={value}'

        response = requests.get(url, headers=self.headers)

        if response.status_code == 200:
            return response.json()
        else:
            print('Status Code:' + str(response.status_code))
            print('Response: ' + response.text)
            print('Headers: ')
            print(self.headers)
            print('URL: ' + url)
            return False

    def devices(self, subscriber_id):
        # https://developers.calix.com/api/subscriber-service#/Subscriber%20-%20Devices/get_subscribers__subscriberId__devices
        self.token_refresh()
        url = self.base_url + f'/billing/subscribers/{subscriber_id}/devices'

        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        else:
            print('Status Code:' + str(response.status_code))
            print('Response: ' + response.text)
            print('Headers: ')
            print(self.headers)
            print('URL: ' + url)
            return False

