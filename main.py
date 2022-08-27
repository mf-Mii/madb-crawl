import pyautogecko as pyautogecko
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from module import easymc
from module import altspizza
from proxies import Proxies


def loadModules():
    easymc.startCrawl()
    altspizza.startCrawl()


proxies = Proxies()


def get_proxies():
    return proxies


global browse_driver
browser_driver = None


def get_browser():
    global browser_driver
    if browser_driver is None:
        pyautogecko.install()
        options = Options()
        options.set_preference('network.trr.mode', 2)
        options.set_preference('network.trr.uri', 'https://mozilla.cloudflare-dns.com/dns-query')
        browser_driver = webdriver.Firefox(options=options)
    return browser_driver


if __name__ == '__main__':
    loadModules()

# PyCharm のヘルプは https://www.jetbrains.com/help/pycharm/ を参照してください