import asyncio
import random
import string
import time
from selenium.webdriver.common.by import By

import browser
import main
import recaptcha
import requests

from exception.LoginException import LoginException
from logger import Logger

from module.altspizza.config import AltsPizzaConfig as config

logger = Logger('AltsPizzaAccount')
class AltsPizzaAccount:
    def __init__(self, name: str, email: str, pw: str, plan: str, access_token: str, refresh_token: str):
        self.name = name
        self.email = email
        self.pw = pw
        self.plan = plan
        self.token = {'access': access_token, 'refresh': refresh_token}

    @staticmethod
    def login(email: str, pw: str):
        logger.info('Login Challenge {}:{}'.format(email, pw))
        driver = main.get_browser()
        driver.get('https://dashboard.alts.pizza/login')
        driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div/form/div[1]/div/input').send_keys(email)
        time.sleep(1)
        driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div/form/div[2]/div/input').send_keys(pw)
        time.sleep(1)
        driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div/form/button').click()
        try_cnt = 0
        while True:
            if driver.current_url != 'https://dashboard.alts.pizza/login':
                break
            time.sleep(1)
            try_cnt += 1
            if try_cnt > 10:
                logger.warn('Failed to login')
                break
        if try_cnt > 10:
            return 'Error'
        #
        #recaptcha_token = recaptcha.resolve_v2('https://www.google.com/recaptcha/api2/anchor?ar=1&k=6LfwhowfAAAAAFUbWzxDwfYG5n1wbi-fvud7peyC&co=aHR0cHM6Ly9kYXNoYm9hcmQuYWx0cy5waXp6YTo0NDM.&hl=en&v=3TZgZIog-UsaFDv31vC4L9R_&theme=light&size=invisible&cb=t0f89paj8nxd')
        #req_data = {
        #    'username': email,
        #    'password': pw,
        #    'recaptcha': recaptcha_token
        #}
        #headers = {
        #    'Content-Type': 'application/json'
        #}
        #resp = requests.post(config.getAPIBase() + '/auth/login', data=req_data, headers=headers).json()
        #if resp['success']:
        #    ac_tk = resp['data']['accessToken']
        #    rf_tk = resp['data']['refreshToken']
        #    name = resp['data']['username']
        #    plan = resp['data']['plan']
        #    return AltsPizzaAccount(name, email, pw, plan, ac_tk, rf_tk)
        #else:
        #    messages = ''
        #    for msg_obj in resp['message']:
        #        messages += msg_obj['msg']
        #    raise LoginException(messages)

    @staticmethod
    def register(username: str = ''.join(random.choices(string.ascii_letters + string.digits, k=12)),
                 email: str = ''.join(random.choices(string.ascii_letters + string.digits, k=18))+'@example.come',
                 pw: str = 'P@ssW0rd',
                 ref: str = None):
        recaptcha_token = recaptcha.reCaptchaV3(
            'https://www.google.com/recaptcha/api2/anchor?ar=1&k=6LfwhowfAAAAAFUbWzxDwfYG5n1wbi-fvud7peyC&co=aHR0cHM6Ly9kYXNoYm9hcmQuYWx0cy5waXp6YTo0NDM.&hl=en&v=3TZgZIog-UsaFDv31vC4L9R_&theme=light&size=invisible&cb=t0f89paj8nxd')
        req_data = {
            'username': username,
            'email': email,
            'password': pw,
            'confirmPassword': pw,
            'recaptcha': recaptcha_token,
            'referral_code': ref
        }
        headers = {
            'Content-Type': 'application/json'
        }
        resp = requests.post(config.getAPIBase() + '/auth/register', data=req_data, headers=headers).json()
        if resp['success']:
            return True
        else:
            return False

    refresh_loop = asyncio.new_event_loop()

    def getProgress(self, alt_type: str = 'nfa'):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.token['access']
        }
        resp = requests.get(config.getAPIBase() + '/alt/comsumed/{}'.format(alt_type), headers=headers).json()
        if resp['success']:
            return resp['data']['consumed']
        else:
            return resp['message']

    def generateAlt(self, alt_type: str = 'nfa'):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.token['access']
        }
        resp = requests.get(config.getAPIBase() + '/alt/{}'.format(alt_type), headers=headers).json()
        if resp['success']:
            return resp['data']['email']
        else:
            return resp['message']


    async def do_refresh_token(self):
        req_data = {
            'refreshToken': self.token['refresh']
        }
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.token['access']
        }
        resp = requests.post(config.getAPIBase(), data=req_data, headers=headers).json()
        if resp['success']:
            self.token['access'] = resp['data']['accessToken']
            self.token['refresh'] = resp['data']['refreshToken']
            await asyncio.sleep(300)
        else:
            self.refresh_loop.stop()

    def start_auto_refresh_token(self):
        self.refresh_loop.run_until_complete(self.do_refresh_token())
        try:
            self.refresh_loop.run_forever()
        finally:
            self.refresh_loop.close()
