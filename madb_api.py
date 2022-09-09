import os

import requests


def addWithToken(src, accessToken, refreshToken):
    data = {
        'src': src,
        'accessToken': accessToken,
        'refreshToken': refreshToken
    }
    return add(data)

def addWithCombo(src, mail, password):
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
