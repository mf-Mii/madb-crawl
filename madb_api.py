import os

import requests


def add_with_token(src, access_token, client_token):
    data = {
        'src': src,
        'accessToken': access_token,
        'clientToken': client_token
    }
    return add(data)


def add_with_combo(src, mail, password):
    print('Disabled')


def add(data):
    headers = {
        'Authorization': os.environ.get('MADB_TOKEN'),
        'X-User': 'mf_Mii',
        'Content-Type': 'application/json'
    }
    resp = requests.post('https://dev-srv.mcaltsdb.cc/add.php', json=data, headers=headers, params={'v': 2})
    # print(resp.text)
    return resp.json()
