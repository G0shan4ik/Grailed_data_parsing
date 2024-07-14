dct = {
    "id": '',
    "designer": '',
    "name": '',
    "size": '',
    "color": '',
    "condition": '',
    "sold_price": '',
    "authenticated": False,
    "seller": '',
    "seller_url": '',
    "description": '',
    "listed_at": '',  # !!!
    "favorites": '',
    "url": '',
    "gender": '-',
    "category": '-',
    "subcategory": '-',
    "sold_at": '',  # !!!
    "photo_url": '',
}

# @browser(
#     reuse_driver=True,
#     parallel=4,
#     block_images=True,
#     close_on_crash=True,
# )
# def grailed_parser(driver: Driver, card_link):
#     from pprint import pprint
#     driver.get_via(card_link, 'https://www.grailed.com')
#     driver.sleep(2)
#
#     soup = BeautifulSoup(driver.page_html, 'lxml')
#
#     bar = [item.text for item in soup.select_one('ol.Breadcrumbs_list__7KMdk').select('li.Breadcrumbs_item__AdcIZ')][:-1]
#     text_dct = category_to_dct(bar)
#     pprint(text_dct)
#
#     data_3_5 = soup.select('p.Body_body__dIg1V.Text.Details_detail__J0Uny.Details_nonMobile__AObqX')
#
#     text_dct['id'] = int(card_link.replace('https://www.grailed.com/listings/', '').split('-')[0])
#     text_dct['name'] = soup.select_one('h1.Body_body__dIg1V.Text.Details_title__PpX5v').text
#     text_dct['size'] = data_3_5[0].text.replace('Size ', '')
#     text_dct['color'] = data_3_5[1].text.replace('Color ', '')
#     text_dct['condition'] = data_3_5[2].text.replace('Condition ', '')
#     text_dct['sold_price'] = int(soup.select_one('span.Money_root__8lDCT.SoldPrice_soldPrice__3yy1H').text.replace('$', ''))
#     text_dct['authenticated'] = True if soup.select_one('p.Headline_headline___qUL5.Text.Card_header__E4I5s').text == 'Authenticated' else False
#     text_dct['seller'] = soup.select_one('span.Text.Subhead_subhead__70fsG.UsernameWithBadges_usernameText__ookiK').text
#     text_dct['seller_url'] = f'https://www.grailed.com/{text_dct["seller"]}'
#     text_dct['description'] = soup.select_one('div.SimpleFormat.Description_body__cJryj').text.replace('\n', '').replace('\t', '')
#     text_dct['favorites'] = int(soup.select_one('span.Text.SmallTitle_smallTitle__oio_S.Likes_count__lMavB').text)
#     text_dct['url'] = f'https://www.grailed.com/listings/{text_dct["id"]}'
#     text_dct['photo_url'] = soup.select_one('img.Photo_picture__g7Lsj.Image_fill__QTtNL.Image_clip__bU5A3.Image_center__CG78h').get('src')
#
#     pprint(text_dct)
#     print()
#     print(text_dct)
#     push_to_supadase(data=text_dct)