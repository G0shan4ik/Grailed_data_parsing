from time import sleep
from json import loads

from botasaurus.request import request, Request
from botasaurus.soupify import soupify
from botasaurus.browser import Driver

from datetime import datetime, timezone

from supabase import create_client, Client

from os import getenv
from dotenv import load_dotenv

from loguru import logger


load_dotenv()

email = getenv('EMAIL')
password = getenv('PASSWORD')
key = getenv('KEY')
url = getenv('URL')
tb_name = getenv('TABLE_NAME')


def category_to_dct(category: list[str], dct):
    text_dct = dct
    if len(category) == 4:
        text_dct['designer'], text_dct['gender'], text_dct['category'], text_dct['subcategory'] = category
    elif len(category) == 3:
        text_dct['designer'], text_dct['gender'], text_dct['category'] = category
    elif len(category) == 2:
        text_dct['designer'], text_dct['gender'] = category
    elif len(category) == 1:
        text_dct['designer'] = category[0]

    return text_dct


def is_auth(sp):
    try:
        return True if sp.select_one('p.Headline_headline___qUL5.Text.Card_header__E4I5s').text == 'Authenticated' else False
    except:
        return False


def to_utc(date: str):
    dt = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%fZ")
    dt = dt.replace(tzinfo=timezone.utc)
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def push_to_supadase(data: dict, _url: str) -> bool:
    try:
        supabase: Client = create_client(url, key)
        supabase.table(tb_name).insert(data).execute()
        return True
    except Exception as ex:
        logger.info(f'LINK EXISTS(:  {_url}')
        return False


@request()
def grailed_parser(request: Request, data):
    try:
        responce = request.get(data)
    except:
        return

    soup = soupify(responce)
    try:
        parsed = soup.find('script', id='__NEXT_DATA__')
        parsed_text = parsed.text
        parsed_json: dict = loads(parsed_text)
        ads = parsed_json['props']['pageProps']['listing']
    except:
        return

    try:
        _size: str = soup.select_one('p.Body_body__dIg1V.Text.Details_detail__J0Uny.Details_nonMobile__AObqX').text
    except:
        _size = '-'
    try:
        _color = ads['traits'][0]['value'].capitalize()
    except:
        _color = '-'
    try:
        _condition = ads['condition'].replace('_', ' ').capitalize().replace('Is ', '').capitalize()
    except:
        _condition = '-'
    try:
        _price = ads['soldPrice']
    except:
        _price = 0
    try:
        _descr = ads['description'].replace('\n', ' ').replace('\t', ' ').replace('  ', ' ')
    except:
        _descr = '-'
    try:
        _photo = ads['photos'][0]['url']
    except:
        _photo = '-'
    try:
        _dct = {
            "id": ads['id'],
            "designer": '-',  # ads['designer']['name']
            "name": ads['title'],
            "size": _size.replace('Size ', '') if 'Size' in _size else '-',  # ads['prettySize']
            "color": _color,
            "condition": _condition,
            "sold_price": _price,
            "authenticated": is_auth(soup),  # ads['seller']['isAuthedSeller']
            "seller": ads['seller']['username'],
            "seller_url": f"https://www.grailed.com/{ads['seller']['username']}",
            "description": _descr,
            "listed_at": to_utc(ads['createdAt']),
            "favorites": int(ads['followerCount']),
            "url": data.split('-')[0],
            "gender": '-',  # soup.select('li.Breadcrumbs_item__AdcIZ')[1].text
            "category": '-',  # f"{ads['designer']['name']} {ads['category'].replace('_', ' ').title()}"
            "subcategory": '-',  # ads['subcategory'].replace('&', '')
            "sold_at": to_utc(ads['soldAt']),
            "photo_url": _photo,
        }
    except:
        print("\n\n<-- Error DICT -->\n\n")
        return

    category = [item.text for item in soup.select_one('ol.Breadcrumbs_list__7KMdk').select('li.Breadcrumbs_item__AdcIZ')[:-1]]

    category_to_dct(category=category, dct=_dct)

    if push_to_supadase(data=_dct, _url=data) is False:
        return

    print(_dct['id'])
    return [True, _dct]


def authorization_to_grailed(driver: Driver, url_: str):
    driver.get_via(url_, 'https://www.grailed.com')

    try:
        driver.sleep(2)
        try:
            driver.click('button#onetrust-accept-btn-handler')
        except:
            ...
        driver.click('a[data-testid="login-btn"]')
    except:
        return
    driver.sleep(2)

    driver.save_screenshot(f'BEFORE_authorisation_{datetime.now().strftime("%Y_%m_%d__%H_%M_%S")}')

    driver.click('button[data-cy="login-with-email"]')
    driver.sleep(1)
    driver.type('input#email', email)
    driver.sleep(1)
    driver.type('input#password', password)
    driver.sleep(1)
    driver.click('button[data-cy="auth-login-submit"')
    driver.sleep(2)

    logger.info(f'Submit {url_}')

    driver.get_via(url_, 'https://www.grailed.com')
    driver.sleep(2)