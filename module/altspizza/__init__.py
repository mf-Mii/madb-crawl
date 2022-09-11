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


def do_crawl():
    global currentAccount
    headers = {
        'Authorization': 'Bearer {}'.format(currentAccount.access_token)
    }
    response = requests.get(f"{Config.get_api_base()}/alt/nfa", headers=headers)
    logger.info(response.text)
    if response.status_code == 401:
        logger.warn('Auth Failed')
        currentAccount = get_account()
        return
    currentAccount.update_account_info()
    if response.status_code == 400 and response.json()['message'] == 'You have reached your plan limit':
        logger.info('Failed to generate alt because reached plan limit. Changing account...')
        currentAccount = get_account()
        return
    response = response.json()
    if response['success']:
        try:
            #mail = json['data']['token']
            logger.info(f"Generated! | {response['data']['username']}")
            alt = MinecraftAccount.login(response['data']['email'], response['data']['password'])
            if isinstance(alt, MinecraftAccount):
                logger.info(f"Success to login alt | {response['data']['username']} | "
                            f"{response['data']['email']}:{response['data']['password']}")
                madb_res = madb_api.add_with_token('Alts.pizza', alt.ac_token, alt.rf_token)
                if madb_res['status'] == 'success':
                    logger.success(f"New Account Added!!")
                else:
                    logger.warn(madb_res['message'])
            else:
                logger.warn(f"Failed to login | {response['data']['username']} | {alt}")
        except KeyError:
            print()
    else:
        currentAccount = get_account()


async def loop_crawl():
    global currentAccount
    while True:
        if currentAccount == None:
            currentAccount = get_account()
        if currentAccount == None:
            logger.warn('There are no account to crawl')
        elif currentAccount.getProgress() == 100:
            currentAccount = None
            continue
        else:
            do_crawl()
        time.sleep(60)


def get_account():
    accounts = Config.get_accounts()
    for account in accounts:
        if account['progress'] == 100:
            continue
        a = AltsPizzaAccount.login(account['mail'], account['pass'])
        a.update_account_info()
        a.start_auto_refresh_token()
        return a
    a = AltsPizzaAccount.login(accounts[0]['mail'], accounts[0]['pass'])
    rs = a.get_reset_time()
    if rs != Config.get_current_reset():
        a.update_account_info()
        for account in accounts:
            if account['progress'] == 100:
                continue
            a = AltsPizzaAccount.login(account['mail'], account['pass'])
            a.update_account_info()
            a.start_auto_refresh_token()
            return a
    return None


def start_crawl():
    Config()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(loop_crawl())
