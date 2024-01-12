import os
from dotenv import load_dotenv
import requests
import json


def main():
    load_dotenv()

    client_secret = os.environ.get('CALIX_CLIENT_SECRET')
    client_id = os.environ.get('CALIX_CLIENT_ID')
    username = os.environ.get('CALIX_USERNAME')
    password = os.environ.get('CALIX_PASSWORD')

    calix = Calix(client_id)

    calix.token(client_id, client_secret, username, password)
    response = calix.subscribers(_id='cb6b529e-d9a4-4186-bb57-ba7d91cd67eb')

    print(json.dumps(response, indent=4))

    print(calix.access_token)
    print(calix.headers)


class Calix:
    def __init__(self, client_id):
        self.access_token: str
        self.token_type: str
        self.exipres_in: int
        self.refresh_token: str
        self.base_url = 'https://api.calix.ai/v1'
        self.headers = {'X-Calix-ClientID': client_id}

    def token(self, client_id: str, client_secret: str, username: str, password: str):
        # https://developers.calix.com/api/token-api-password-grant
        url = self.base_url + '/authentication/token'

        data = {
            'grant_type': 'password',
            'username': username,
            'password':  password,
            'client_secret': client_secret
        }

        response = requests.post(url, data=data, headers=self.headers)

        if response.status_code == 200:
            self.access_token = response.json().get('access_token')
            self.token_type = response.json().get('token_type')
            self.exipres_in = response.json().get('exipres_in')
            self.refresh_token = response.json().get('refresh_token')
            self.headers['X-Calix-AccessToken'] = self.access_token
        else:
            print("Token error:")
            print(response.text)
            exit(1)

        return response.json()

    def subscribers(self, **kwargs):
        # https://developers.calix.com/api/subscriber-service#/Subscriber/get_subscribers
        url = self.base_url + '/billing/subscribers'

        print(kwargs)

        if kwargs.get('_id'):
            url += '/' + kwargs.get('_id')
        else:
            url += '?'

            for key, value in kwargs.items():
                url += f'&{key}={value}'

        print(url)
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


if __name__ == '__main__':
    main()

