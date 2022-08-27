import io

import requests
from pypasser import reCaptchaV2
from pypasser import reCaptchaV3
from pypasser.structs import Proxy
from selenium.webdriver.common.by import By
from PIL import Image

import main


def getProxy():
    proxy = {}
    return proxy


def resolve_v2(url):
    browser = main.get_browser()
    browser.get(url)
    browser.implicitly_wait(10)
    browser.find_element(By.CSS_SELECTOR, 'button.css-1hy2vtq:nth-child(3)')
    recaptcha_frame = browser.find_element(By.XPATH, '//iframe[@title="recaptcha challenge expires in two minutes"]')
    browser.switch_to_frame(recaptcha_frame)
    if 'Select all images with ' in browser.find_element(By.CLASS_NAME, 'rc-imageselect-desc-no-canonical'):
        solve_v2_sel_all(browser)


def solve_v2_sel_all(recaptcha_frame):
    target_type = recaptcha_frame.find_element(By.XPATH, '/html/body/div/div/div[2]/div[1]/div[1]/div[2]/strong')
    target_tr = recaptcha_frame.find_elements(By.XPATH, '/html/body/div/div/div[2]/div[2]/div/table/tbody/tr')
    targets = []
    vertical = 0
    # 要素を二次元配列に格納
    img = None
    for _tr in target_tr:
        target_tr_tds = target_tr[vertical].find_elements(By.CLASS_NAME, 'rc-imageselect-tile')
        width = 0
        for _td in target_tr_tds:
            targets[vertical][width] = _td
            if img is None:
                img = requests.get(_td.find_element(By.TAG_NAME, 'img').get_attribute('src')).content
        vertical += 1
    target_imgs = []

    # 画像を二次元配列に格納
    h_len = len(targets)
    w_len = len(targets[0])
    image = Image.open(io.BytesIO(img))
    tile_size = image.width / w_len
    for vertical in targets:
        for width in targets[vertical]:
            tile_img = image.crop((tile_size * width, tile_size * vertical, tile_size * (width + 1), tile_size * (vertical + 1)))
            targets[vertical][width] = tile_img
            tile_img.save('data/{}.{}.jpg'.format(vertical, width))



def resolveV3(url):
    proxy = getProxy()
    useProxy = proxy != {}
    if useProxy:
        return reCaptchaV3(url, getProxy())
    else:
        return reCaptchaV3(url)
