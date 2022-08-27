import asyncio
import json
import time

import requests
import madb_api
import recaptcha
from logger import Logger
from module.altspizza.account import AltsPizzaAccount
from module.altspizza.config import AltsPizzaConfig as Config

currentAccount = None
logger = Logger('Alts.pizza')


def doCrawl(reCaptchaToken=None):
    reCaptchaParam = '' if reCaptchaToken == None else '&captcha=' + reCaptchaToken
    response = requests.get(f"https://api.easymc.io/v1/token?new=true{reCaptchaParam}")
    if response.status_code == 200:
        json = response.json()
        try:
            mail = json['token']
            print('[EasyMC.io] ' + mail)
            data = {
                'src': 'EasyMC.io',
                'mail': mail
            }
            madb_api.add(data)
        except KeyError:
            print()
    elif response.status_code == 400:
        token = recaptcha.resolveV3('')
        doCrawl(token)


async def loopCrawl():
    while True:
        if currentAccount == None:
            currentAccount = getAccount()
        if currentAccount == None:
            logger.warn('There are no account to crawl')
            AltsPizzaAccount.generate('')
        else:
            doCrawl()
        time.sleep(60)


def getAccount():
    accounts = Config.getAccounts()
    for account in accounts:
        if account['progress'] == 100:
            continue
        return AltsPizzaAccount.login(account['mail'], account['pass'])
    return None


def startCrawl():
    Config()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(loopCrawl())
