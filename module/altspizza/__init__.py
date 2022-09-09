import asyncio
import json
import time

import requests
import madb_api
import mcaccount
import recaptcha
from logger import Logger
from module.altspizza.account import AltsPizzaAccount
from module.altspizza.config import AltsPizzaConfig as Config
from mcaccount import MinecraftAccount

currentAccount = None
logger = Logger('Alts.pizza')


def doCrawl():
    response = requests.get(f"{Config.getAPIBase()}/alt/nfa").json()
    if response['success']:
        try:
            mail = json['token']
            logger.info(f"Generated! | {response['data']['username']}")
            alt = MinecraftAccount.login(response['data']['email'], response['data']['password'])
            if isinstance(alt, MinecraftAccount):
                madb_res = madb_api.addWithToken('Alts.pizza', alt.ac_token, alt.rf_token)
                if madb_res['status'] == 'success':
                    logger.success(f"New Account Added!!")
                else:
                    logger.warn(madb_res['message'])
            else:
                logger.warn(f"Failed to login | {response['data']['username']} | {alt}")
        except KeyError:
            print()
    else:
        currentAccount = getAccount()


async def loopCrawl():
    global currentAccount
    while True:
        if currentAccount == None:
            currentAccount = getAccount()
        if currentAccount == None:
            logger.warn('There are no account to crawl')
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
