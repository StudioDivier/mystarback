import requests as re
import json

from MyStar import config

client_id = config.OAUTHDATA.SOCIAL_AUTH_MAIL_OAUTH2_KEY
client_secret = config.OAUTHDATA.SOCIAL_AUTH_MAIL_OAUTH2_SECRET


def send_request():
    req_param = {
        'response_type': 'code',
        'client_id': client_id,
    }
    send_re = 'https://connect.mail.ru/oauth/authorize'
    response = re.get(url=send_re, params=req_param)

    link = f'https://connect.mail.ru/oauth/authorize?response_type=code&client_id={client_id}'

    return link


def token(r):
    get_token = 'https://oauth.yandex.ru/token'
    token_param = {
        'grant_type': 'authorization_code',
        'code': r,
        'client_id': client_id,
        'client_secret': client_secret
    }
    data = json.dumps(token_param)
    response = re.post(url=get_token, data=token_param)
    s = json.loads(response.text.replace('\\', ''))

    return s


def ya_auth(r):
    auth = 'https://login.yandex.ru/info'
    auth_param = {
        'format': 'json',
        'oauth_token': r
    }

    response = re.get(url=auth, params=auth_param)
    s = json.loads(response.text)

    return s









