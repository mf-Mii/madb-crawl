import byerecaptcha
from pypasser import reCaptchaV2
from pypasser import reCaptchaV3
from pypasser.structs import Proxy

import main


def getProxy():
    proxy = {}
    return proxy

def resolveV2(url):
    browser = main.get_browser()
    return byerecaptcha.solveRecaptcha(browser.get_driver(), url, False)

def resolveV3(url):
    proxy = getProxy()
    useProxy = proxy != {}
    if useProxy:
        return reCaptchaV3(url, getProxy())
    else:
        return reCaptchaV3(url)