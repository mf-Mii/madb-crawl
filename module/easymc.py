import asyncio
import time

import requests
from requests_doh import DNSOverHTTPSAdapter

import madb_api
from logger import Logger

logger = Logger('EasyMC.io')


def doCrawl(reCaptchaToken = None):
    logger.info('Generating EasyMC.io ALT')
    reCaptchaParam = '' if reCaptchaToken == None else '&captcha=' + reCaptchaToken
    doh_adapter = DNSOverHTTPSAdapter(provider='cloudflare')
    session = requests.Session()
    session.mount('https://', doh_adapter)
    session.mount('http://', doh_adapter)
    response = session.get(f"https://api.easymc.io/v1/token?new=true{reCaptchaParam}")
    if response.status_code == 200:
        print(response.text)
        json = response.json()
        try:
            mail = json['token']
            logger.info('Token| ' + mail)
            data = {
                'src': 'EasyMC.io',
                'mail': mail
            }
            add_rsp = madb_api.add(data)
            if add_rsp['status'] == 'success':
                logger.success(add_rsp['message'])
            else:
                logger.warn(add_rsp['message'])
        except KeyError:
            print()
    elif response.status_code == 400:
        logger.warn('Captcha required. Trying solving...')
        #token = recaptcha.resolve_v2('https://easymc.io/get?new')
        # logger.info(token)
        logger.error('reCaptcha solver was not completed')
        #doCrawl(token)
    else:
        logger.error('{} | {}'.format(response.status_code, response.json()['error']))

async def loopCrawl():
    while True:
        doCrawl()
        time.sleep(60)

def startCrawl():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(loopCrawl())