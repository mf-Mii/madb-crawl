import requests

import main
from proxies import Proxies


class MinecraftAccount:
    def __init__(self, uuid: str, name: str, access_token: str = None, refresh_token: str = None):
        self.uuid = uuid
        self.name = name
        self.ac_token = access_token
        self.rf_token = refresh_token

    @staticmethod
    def login(mail: str, pw: str):
        headers = {
            'Content-Type': 'application/json'
        }
        req_data = {
            'agent': {
                'name': 'Minecraft',
                'version': 1
            },
            'username': mail,
            'password': pw,
            'requestUser': True
        }
        proxy_data = {}
        while True:
            proxy = main.get_proxies().getMCProxy()
            if proxy is None:
                proxy_data = None
                break
            elif not main.get_proxies().checkProxy(proxy):
                main.get_proxies().disable_mc_proxy(proxy)
            else:
                proxy_data = {
                    'http': proxy,
                    'https': proxy
                }
                break

        resp = requests.post('https://authserver.mojang.com/authenticate', headers=headers, data=req_data, proxies=proxy_data)
        if resp.status_code == 200:
            resp = resp.json()
            uuid = resp['selectedProfile']['id']
            name = resp['selectedProfile']['name']
            ac_token = resp['accessToken']
            rf_token = resp['refreshToken']
            return MinecraftAccount(uuid, name, ac_token, rf_token)
        else:
            return resp.json()['error'] + ':' + resp.json()['errorMessage']