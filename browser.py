import os

from selenium.webdriver.firefox.options import Options
from selenium import webdriver

from logger import Logger

logger = Logger('Browser')
class Browser:
    def __init__(self):
        options = Options()
        options.set_preference('network.trr.mode', 2)
        options.set_preference('network.trr.uri', 'https://mozilla.cloudflare-dns.com/dns-query')
        self.driver = webdriver.Firefox(options=options)

    def open(self, url: str):
        if url is not None and url is not '':
            self.driver.get(url)
            logger.info('Opened url in firefox: '+url)
        else:
            logger.warn('Invalid url')

    def get_driver(self):
        return self.driver
