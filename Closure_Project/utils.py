import os
import json
import jwt
import requests
from django.contrib.auth import authenticate

from Closure_Project.settings import API_IDENTIFIER, AUTH0_DOMAIN


def dump_json(o: object, filename: str) -> None:
    with open(filename, 'w', encoding='utf8') as f:
        json.dump(o, f, ensure_ascii=False)


def load_json(filename: str):
    with open(filename, 'r', encoding='utf8') as f:
        return json.load(f)


def setup_django_pycharm():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Closure_Project.settings")
    import django
    django.setup()


def jwt_get_username_from_payload_handler(payload):
    username = payload.get('sub').replace('|', '.')
    authenticate(remote_user=username)
    return username


def jwt_decode_token(token):
    header = jwt.get_unverified_header(token)
    jwks = requests.get('https://{}/.well-known/jwks.json'.format(AUTH0_DOMAIN)).json()
    public_key = None
    for jwk in jwks['keys']:
        if jwk['kid'] == header['kid']:
            public_key = jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(jwk))

    if public_key is None:
        raise Exception('Public key not found.')

    issuer = 'https://{}/'.format(AUTH0_DOMAIN)
    return jwt.decode(token, public_key, audience=API_IDENTIFIER, issuer=issuer, algorithms=['RS256'])
