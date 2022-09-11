import asyncio
import json
import random
import string
import time

import schedule
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
        self.access_token = access_token
        self.refresh_token = refresh_token

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
        logger.info("Trying login")
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
        logger.success('Logged in')
        ref_token = driver.get_cookie('_auth_refresh')['value']
        token = driver.get_cookie('_auth')['value']
        driver.close()
        payload = json.dumps({
            'refreshToken': ref_token
        })
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': 'Bearer {}'.format(token)
        }
        logger.info('Requesting refresh token')
        resp = requests.post(config.get_api_base() + '/auth/refresh', data=payload, headers=headers).json()
        # logger.info(token)
        # logger.info(ref_token)
        # logger.info(resp)
        if resp['success']:
            a_tkn = resp['data']['accessToken']
            r_tkn = resp['data']['refreshToken']
            name = resp['data']['user']['username']
            plan = resp['data']['user']['plan']
            logger.success('Login Success!!')
            return AltsPizzaAccount(name, email, pw, plan, a_tkn, r_tkn)
        else:
            logger.warn('Failed to login')

        #
        # recaptcha_token = recaptcha.resolve_v2('https://www.google.com/recaptcha/api2/anchor?ar=1&k=6LfwhowfAAAAAFUbWzxDwfYG5n1wbi-fvud7peyC&co=aHR0cHM6Ly9kYXNoYm9hcmQuYWx0cy5waXp6YTo0NDM.&hl=en&v=3TZgZIog-UsaFDv31vC4L9R_&theme=light&size=invisible&cb=t0f89paj8nxd')
        # req_data = {
        #    'username': email,
        #    'password': pw,
        #    'recaptcha': recaptcha_token
        # }
        # headers = {
        #    'Content-Type': 'application/json'
        # }
        # resp = requests.post(config.getAPIBase() + '/auth/login', data=req_data, headers=headers).json()
        # if resp['success']:
        #    ac_tk = resp['data']['accessToken']
        #    rf_tk = resp['data']['refreshToken']
        #    name = resp['data']['username']
        #    plan = resp['data']['plan']
        #    return AltsPizzaAccount(name, email, pw, plan, ac_tk, rf_tk)
        # else:
        #    messages = ''
        #    for msg_obj in resp['message']:
        #        messages += msg_obj['msg']
        #    raise LoginException(messages)

    @staticmethod
    def register(username: str = ''.join(random.choices(string.ascii_letters + string.digits, k=12)),
                 email: str = ''.join(random.choices(string.ascii_letters + string.digits, k=18)) + '@example.come',
                 pw: str = 'P@55W0rd',
                 ref: str = None):
        #OLD Method
        #recaptcha_token = recaptcha.reCaptchaV3(
        #    'https://www.google.com/recaptcha/api2/anchor?ar=1&k=6LfwhowfAAAAAFUbWzxDwfYG5n1wbi-fvud7peyC&co=aHR0cHM6Ly9kYXNoYm9hcmQuYWx0cy5waXp6YTo0NDM.&hl=en&v=3TZgZIog-UsaFDv31vC4L9R_&theme=light&size=invisible&cb=t0f89paj8nxd')
        #req_data = {
        #    'username': username,
        #    'email': email,
        #    'password': pw,
        #    'confirmPassword': pw,
        #    'recaptcha': recaptcha_token,
        #    'referral_code': ref
        #}
        #headers = {
        #    'Content-Type': 'application/json'
        #}
        #resp = requests.post(config.get_api_base() + '/auth/register', data=req_data, headers=headers).json()
        #if resp['success']:
        #    return True
        #else:
        #    return False
        driver = main.get_browser()
        url = '/register' if ref is None else '/ref?ref={}'.format(ref)
        driver.get('https://dashboard.alts.pizza' + url)
        cnt = 0
        while cnt <= 3:
            if driver.current_url == 'https://dashboard.alts.pizza/register':
                break
            cnt += 1
            time.sleep(1)
        if driver.current_url != 'https://dashboard.alts.pizza/register':
            return 'Failed to redirect register page'
        driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/form/div[1]/div/input').send_keys(username)
        driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/form/div[2]/div/input').send_keys(email)
        driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/form/div[3]/div/input').send_keys(pw)
        driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/form/div[4]/div/input').send_keys(pw)
        driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/form/div[5]/div/label/input').click()
        driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/form/button').click()
        cnt = 0
        while cnt <= 10:
            if driver.current_url != 'https://dashabord.alts.pizza/register':
                break
            cnt += 1
            time.sleep(1)
        if cnt > 10:
            return 'Failed to register'
        return AltsPizzaAccount.login(email, pw)




    refresh_loop = True

    def get_progress(self, alt_type: str = 'nfa'):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.access_token
        }
        resp = requests.get(config.get_api_base() + '/alt/comsumed/{}'.format(alt_type), headers=headers).json()
        if resp['success']:
            return resp['data']['consumed']
        else:
            return resp['message']

    def generate_alt(self, alt_type: str = 'nfa'):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.access_token
        }
        resp = requests.get(config.get_api_base() + '/alt/{}'.format(alt_type), headers=headers).json()
        if resp['success']:
            return resp['data']['email']
        else:
            return resp['message']

    def is_referrer_used(self):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.access_token
        }
        resp = requests.get(config.get_api_base() + '/referral/check', headers=headers)
        if resp.status_code == 200:
            return resp.json()['status']
        return False

    def update_account_info(self):
        ac_data = {
            'mail': self.email,
            'pass': self.pw,
            'user': self.name,
            'progress': self.get_progress(),
            'referrer_used': self.is_referrer_used()
        }
        data = config.get_data()
        data['reset'] = self.get_reset_time()
        for i in range(len(data['accounts'])):
            _a = data['accounts'][i]
            if _a['mail'] == self.email:
                data['accounts'][i] = ac_data
                break
        config.save_config(data)

    def get_reset_time(self):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.access_token
        }
        resp = requests.get(config.get_api_base() + '/stat/reset', headers=headers)
        if resp.status_code == 200:
            return resp.json()['data']['resetTime']
        return None

    async def do_refresh_token(self):
        req_data = {
            'refreshToken': self.refresh_token
        }
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.access_token
        }
        resp = requests.post(config.get_api_base() + '/auth/refresh', data=req_data, headers=headers).json()
        if resp['success']:
            self.access_token = resp['data']['accessToken']
            self.refresh_token = resp['data']['refreshToken']
        else:
            self.refresh_loop = False

    async def start_auto_refresh_token(self):
        schedule.every(5).minutes.do(self.do_refresh_token())
        while True:
            schedule.run_pending()
            time.sleep(1)
