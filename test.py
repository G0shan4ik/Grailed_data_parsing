import asyncio
from datetime import datetime, timezone
from json import loads
from typing import Awaitable

import aiohttp
from bs4 import BeautifulSoup
from supabase import create_client, Client


def to_utc(date: str):
    dt = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%fZ")
    dt = dt.replace(tzinfo=timezone.utc)
    return dt.strftime("%Y-%m-%d %H:%M:%S")

def push_to_supadase(data: dict):
    url = 'https://cjnjheetblycwuttmnch.supabase.co'
    key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNqbmpoZWV0Ymx5Y3d1dHRtbmNoIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTcyMDcwMjgzMSwiZXhwIjoyMDM2Mjc4ODMxfQ.mk8DZwWSAWevP3QGET9KKShMkCkn_RcoDdpYuV3Fyls'
    tb_name = 'GRAILED'
    try:
        supabase: Client = create_client(url, key)
        supabase.table(tb_name).insert(data).execute()
    except Exception as ex:
        print(f"\n\n\nError SUREDASE: {ex}\n\n")


def is_auth(sp):
    try:
        return True if sp.select_one('p.Headline_headline___qUL5.Text.Card_header__E4I5s').text == 'Authenticated' else False
    except:
        return False


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


async def get_result_parser_kuf(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            soup = BeautifulSoup(await response.text(encoding='utf-8'), 'lxml')
    try:
        parsed = soup.find('script', id='__NEXT_DATA__')
        parsed_text = parsed.text
        parsed_json: dict = loads(parsed_text)
        ads = parsed_json['props']['pageProps']['listing']
    except:
        await asyncio.sleep(4)
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                soup = BeautifulSoup(await response.text(encoding='utf-8'), 'lxml')

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
            "url": url.split('-')[0],
            "gender": '-',  # soup.select('li.Breadcrumbs_item__AdcIZ')[1].text
            "category": '-',  # f"{ads['designer']['name']} {ads['category'].replace('_', ' ').title()}"
            "subcategory": '-',  # ads['subcategory'].replace('&', '')
            "sold_at": to_utc(ads['soldAt']),
            "photo_url": _photo,
        }

        category = [item.text for item in
                    soup.select_one('ol.Breadcrumbs_list__7KMdk').select('li.Breadcrumbs_item__AdcIZ')[:-1]]

        category_to_dct(category=category, dct=_dct)
        # pprint(_dct)
        push_to_supadase(data=_dct)
        print(ads['id'])
    except:
        print('<---- EXEPTION ----->')
        ...


def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


async def main():
    with open('cards_links.txt', 'r', encoding='utf-8') as f:
        _mass = [item.replace('\n', '') for item in f.readlines()]

    for link in _mass[248:]:
        await get_result_parser_kuf(link)


# if __name__ == '__main__':
#     asyncio.run(main())

b = ['1', 2, 3]


