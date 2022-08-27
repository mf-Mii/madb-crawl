import asyncio
import time

import requests

class Proxies:
    mcProxies = {}
    def getProxies(self):
        f = open('data/proxies.txt', 'r')
        proxies = f.readlines()
        f.close()
        return proxies

    def getMCProxy(self):
        for p in self.getProxies():
            if p in self.mcProxies:
                used_cnt = self.mcProxies[p]['used']
                if used_cnt < 5 and not self.mcProxies[p]['disabled']:
                    self.mcProxies[p]['used'] += 1
                    self.removeMCProxy(p)
                    return p
                else:
                    continue
            else:
                self.mcProxies[p]['used'] = 1
                self.removeMCProxy(p)
                return p
        return None

    def disable_mc_proxy(self, proxy: str):
        self.mcProxies[proxy]['disabled'] = True

    def removeMCProxy(self, proxy: str):
        asyncio.new_event_loop().run_in_executor(None, self.do_remove_mc_proxy, proxy)

    def do_remove_mc_proxy(self, proxy: str):
        time.sleep(300)
        self.mcProxies[proxy] -= 1
        if self.mcProxies[proxy] < 0:
            self.mcProxies[proxy] = 0

    def checkProxy(self, proxy: str):
        proxy_data = {
            'http': proxy,
            'https': proxy
        }
        try:
            requests.get('https://example.com/', proxies=proxy_data)
            return True
        except requests.exceptions.ProxyError as err:
            return False
