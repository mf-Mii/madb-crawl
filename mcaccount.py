import requests

import main
import logger
from proxies import Proxies

logger = logger.Logger('MinecraftAccount')
class MinecraftAccount:
    def __init__(self, uuid: str, name: str, access_token: str = None, client_token: str = None):
        self.uuid = uuid
        self.name = name
        self.ac_token = access_token
        self.cl_token = client_token

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
        #while True:
        #    proxy = main.get_proxies().getMCProxy()
        #    if proxy is None:
        #        proxy_data = None
        #        break
        #    elif not main.get_proxies().checkProxy(proxy):
        #        main.get_proxies().disable_mc_proxy(proxy)
        #    else:
        #        proxy_data = {
        #            'http': proxy,
        #            'https': proxy
        #        }
        #        break
        logger.info('Starting Login Request')
        resp = requests.post('https://authserver.mojang.com/authenticate', headers=headers, json=req_data, proxies=proxy_data)
        if resp.status_code == 200:
            resp = resp.json()
            uuid = resp['selectedProfile']['id']
            name = resp['selectedProfile']['name']
            access_token = resp['accessToken']
            client_token = resp['clientToken']
            logger.success(f"Login Success: {name}")
            return MinecraftAccount(uuid, name, access_token, client_token)
        else:
            return resp.json()['error'] + ':' + resp.json()['errorMessage']