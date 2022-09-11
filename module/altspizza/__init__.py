import asyncio
import json
import time
import datetime

import requests

import log_alt
import madb_api
import mcaccount
import recaptcha
from logger import Logger
from module.altspizza.account import AltsPizzaAccount
from module.altspizza.config import AltsPizzaConfig as config
from mcaccount import MinecraftAccount

currentAccount = None
logger = Logger('Alts.pizza')
alt_logger = log_alt.AltLogger('AltsPizza')
auto_register = False


def set_auto_register(enable: bool):
    global auto_register
    auto_register = enable


def do_crawl():
    global currentAccount
    headers = {
        'Authorization': 'Bearer {}'.format(currentAccount.access_token)
    }
    response = requests.get(f"{config.get_api_base()}/alt/nfa", headers=headers)
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
            logger.info(f"Generated! | {response['data']['username']}")
            email = response['data']['email']
            pw = response['data']['password']
            alt = MinecraftAccount.login(email, pw)
            if isinstance(alt, MinecraftAccount):
                logger.success(f"Success to login alt | {alt.name}")
                madb_res = madb_api.add_with_token('Alts.pizza', alt.ac_token, alt.cl_token)
                #logger.info(madb_res)
                if madb_res['status'] == 'success':
                    logger.success(f"New Account Added!!")
                else:
                    logger.warn(madb_res['message'])
            else:
                alt_logger.fail(response['data']['username'], response['data']['skin'])
                logger.warn(f"Failed to login | {response['data']['username']} | {alt}")
        except KeyError:
            print('KeyError Happen')
    else:
        currentAccount = get_account()


async def loop_crawl():
    global currentAccount
    while True:
        if currentAccount == None:
            currentAccount = get_account()
        if currentAccount == None:
            logger.warn('There are no account to crawl')
        elif currentAccount.get_progress() == 100:
            currentAccount.logout()
            currentAccount = None
            continue
        else:
            do_crawl()
        time.sleep(60)


def get_account():
    global currentAccount
    global auto_register
    if currentAccount is not None:
        logger.info('Logout...')
        currentAccount.logout()
        currentAccount = None
    accounts = config.get_accounts()
    for account in accounts:
        if account['progress'] == 100:
            continue
        a = AltsPizzaAccount.login(account['mail'], account['pass'])
        a.update_account_info()
        a.start_auto_refresh_token()
        return a
    # すべてのアカウントがリミット
    if auto_register:
        logger.info('All account reached plan limit. Registering New Account...')
        old_a = None
        ref = None
        for ac in accounts:
            if not ac['referrer_used']:
                old_a = AltsPizzaAccount.login(ac['mail'], ac['pass'])
                ref = old_a.referral_code_get()
                if ref is None:
                    ref = old_a.referral_code_new()
        new_a = AltsPizzaAccount.register(ref=ref)
        if old_a.referral_subscribe():
            old_a.update_account_info()
        new_a.update_account_info()
    else:
        logger.info('All account reached plan limit. Checking reset time...')
        if config.get_current_reset() == '':
            a = AltsPizzaAccount.login(accounts[0]['mail'], accounts[0]['pass'])
            rs = a.get_reset_time()
            if rs != config.get_current_reset():
                logger.info('Reset time updated!')
                a.update_account_info()
                for account in accounts:
                    account['progress'] = 0
                return a
            else:
                a.logout()
        elif datetime.datetime.strptime(config.get_current_reset(),
                                        '%Y-%m-%dT%H:%M:%S.999Z') < datetime.datetime.utcnow():
            for account in accounts:
                account['progress'] = 0
            a = AltsPizzaAccount.login(accounts[0]['mail'], accounts[0]['pass'])
            a.update_account_info()
            a.start_auto_refresh_token()
            return a
        return None


def start_crawl():
    config()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(loop_crawl())
