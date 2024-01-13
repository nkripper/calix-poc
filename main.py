import os
from dotenv import load_dotenv
import json
from calix import Calix


def main():
    load_dotenv()

    client_secret = os.environ.get('CALIX_CLIENT_SECRET')
    client_id = os.environ.get('CALIX_CLIENT_ID')
    username = os.environ.get('CALIX_USERNAME')
    password = os.environ.get('CALIX_PASSWORD')

    calix = Calix(client_id, client_secret, username, password)

    response = calix.subscribers(_id='cb6b529e-d9a4-4186-bb57-ba7d91cd67eb')
    response = calix.devices('cb6b529e-d9a4-4186-bb57-ba7d91cd67eb')

    print(json.dumps(response, indent=4))


if __name__ == '__main__':
    main()

