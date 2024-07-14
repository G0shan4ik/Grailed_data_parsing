from json import loads
from time import sleep

from botasaurus.browser import browser, Driver
from botasaurus.request import request, Request
from botasaurus.soupify import soupify

from supabase import create_client, Client

from data_parsing.database import CardData
# from helpers import dct

from random import randint, uniform

from os import getenv
from dotenv import load_dotenv

import lxml
from bs4 import BeautifulSoup

from datetime import datetime, timezone

load_dotenv()

email = getenv('EMAIL')
password = getenv('PASSWORD')
key = getenv('KEY')
url = getenv('URL')
tb_name = getenv('TABLE_NAME')


def to_utc(date: str):
    dt = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%fZ")
    dt = dt.replace(tzinfo=timezone.utc)
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def chek_db_match(listing_URL: str):
    _select = CardData.select().where(CardData.Listing_URL == listing_URL)
    if _select.exists():
        print(True)  # не парсим
        return True
    print(False)  # парсим
    return False


def push_to_supadase(data: dict):
    url = 'https://cjnjheetblycwuttmnch.supabase.co'
    key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNqbmpoZWV0Ymx5Y3d1dHRtbmNoIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTcyMDcwMjgzMSwiZXhwIjoyMDM2Mjc4ODMxfQ.mk8DZwWSAWevP3QGET9KKShMkCkn_RcoDdpYuV3Fyls'
    tb_name = 'GRAILED'
    try:
        supabase: Client = create_client(url, key)
        supabase.table(tb_name).insert(data).execute()
    except Exception as ex:
        print(f"\n\n\nError SUREDASE: {ex}\n\n")


def pars_page_links(driver: Driver) -> list[str]:
    result:  list[str] = []
    soup = BeautifulSoup(driver.page_html, 'lxml')
    cnt = 0
    for item in soup.select('div.feed-item'):
        try:
            _url = item.select_one('a.listing-item-link').get('href')
            result.append(f"https://www.grailed.com{_url}")
        except:
            ...
        # try:
        #     _url = item.select_one('a.listing-item-link').get('href')
        #     if not chek_db_match(_url):
        #         result.append(f'https://www.grailed.com{_url}')
        #     elif cnt == 3:
        #         return []
        #     else:
        #         cnt += 1
        # except:
        #     continue
    with open('links3.txt', 'a', encoding='utf-8') as f:
        for i in result:
            f.write(f'{i}\n')
    # print(*result, sep='\n')
    return result


def authorization_to_grailed(driver: Driver, url_: str):
    driver.get_via(url_, 'https://www.grailed.com')
    try:
        driver.sleep(2)
        driver.click('a[data-testid="login-btn"]')
    except:
        return
    driver.click('button[data-cy="login-with-email"]')
    driver.sleep(1)
    driver.type('input#email', email)
    driver.sleep(1)
    driver.type('input#password', password)
    driver.sleep(1)
    driver.click('button[data-cy="auth-login-submit"')
    driver.sleep(2)
    driver.get_via(url_, 'https://www.grailed.com')
    driver.sleep(2)


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

@request(
    cache=True,
)
def grailed_parser(request: Request, data):
    from pprint import pprint
    responce = request.get(data)

    soup = soupify(responce)

    parsed = soup.find('script', id='__NEXT_DATA__')
    parsed_text = parsed.text
    parsed_json: dict = loads(parsed_text)
    ads = parsed_json['props']['pageProps']['listing']

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

    category = [item.text for item in soup.select_one('ol.Breadcrumbs_list__7KMdk').select('li.Breadcrumbs_item__AdcIZ')[:-1]]

    category_to_dct(category=category, dct=_dct)
    # pprint(_dct)
    _select = CardData.select().where(CardData.id == ads['id'])
    if _select.exists():
        return

    CardData.create(**_dct)
    print(_dct['id'])
    push_to_supadase(data=_dct)


@browser(
    reuse_driver=True,
    block_images=True,
    profile='Grailed',
    close_on_crash=True,
)
def pars_manager(driver: Driver, data: str):
    # <-- Authorization -->
    authorization_to_grailed(driver, data)
    # <-- /Authorization -->

    # # <-- Scroll Page -->
    how_many = int(driver.select('div.-header').text.split()[0])
    while True:
        for _ in range(4):
            driver.run_js(f'window.scrollTo(0, document.body.scrollHeight)')
            driver.sleep(2)

        ln = len(driver.select_all('div.feed-item')) - 3
        if ln >= how_many:
            break
    driver.sleep(1)
    # # <-- /Scroll Page -->

    # <-- Pars All Page Links -->
    all_listing_urls: list[str] = pars_page_links(driver)
    # <-- /Pars All Page Links -->

    # s.split('/')[2].split('-')[0]

    # # <-- Pars Card -->
    # for i in range(0, len(all_listing_urls), 4):
    #     grailed_parser(all_listing_urls[i:i + 4])
    # # <-- /Pars Card -->


def schedule(links: list[str]):
    print('\n\n\n\n\n<--- START --->\n\n\n\n\n')

    cnt = 0

    while True:
        # for _link in links:
        #     cnt += 1
        #     print(f"\n<-- Link: {_link} -->\n")
        #     pars_manager(_link)
        #     if cnt % 6 == 0:
        #         sleep(uniform(240, 300))
        #
        # print('\n\nsleep\n\n')
        # sleep(uniform(240, 300))

        with open('links2.txt', 'r', encoding='utf-8') as f:
            _mass = [item.replace('\n', '') for item in f.readlines()]

        for lnk in _mass:
            grailed_parser(lnk)
        print('\n\n\n\n\n\n')


if __name__ == '__main__':
    m = [
        # "https://www.grailed.com/sold/sNemahZAdg",
        # "https://www.grailed.com/sold/izGTk7yGJQ",
        # "https://www.grailed.com/sold/OMKwb97AcQ",
        # "https://www.grailed.com/sold/2M2w0tAH0w",
        "https://www.grailed.com/sold/ltOQAGhAqQ",
        "https://www.grailed.com/sold/ZAbmsXyMGQ",
        "https://www.grailed.com/sold/FZPsQt7UfQ",
        "https://www.grailed.com/sold/jQqwgp-KWA",
    ]
    s = [
        "https://www.grailed.com/sold/2XWaha7YJA",
        "https://www.grailed.com/sold/Y2swMVhYTA",
        "https://www.grailed.com/sold/EEqPt1cRcg",
        "https://www.grailed.com/sold/Km4dRpe0ZQ",
        "https://www.grailed.com/sold/yNLPGQZ-xQ",
        "https://www.grailed.com/sold/TWbrrFiFzg",
        "https://www.grailed.com/sold/oJuIW1Hk2g",
    ]
    for item in m:
        pars_manager(item)
    # with open('cards_links.txt', 'r', encoding='utf-8') as f:
    #     mass = [item.replace('\n', '') for item in f.readlines()]
    #
    # for link in mass:
    #     grailed_parser(link)
