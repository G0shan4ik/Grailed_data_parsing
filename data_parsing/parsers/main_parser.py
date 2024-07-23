from time import sleep
from uuid import uuid4

from botasaurus.browser import browser, Driver

from .helpers import grailed_parser, authorization_to_grailed
from random import randint, uniform

import lxml
from bs4 import BeautifulSoup


def pars_page_links(driver: Driver):
    soup = BeautifulSoup(driver.page_html, 'lxml')
    for item in soup.select('div.feed-item'):
        try:
            _url = f"https://www.grailed.com{item.select_one('a.listing-item-link').get('href')}"
            # result.append(f"https://www.grailed.com{_url}")

            # # <-- Pars Card -->

            if grailed_parser(_url) is None:
                break
            print(_url)
            # # <-- /Pars Card -->
        except:
            ...


@browser(
    profile='Grailed',
    close_on_crash=True,
    proxy='http://wS1WHB:k4eGHy@87.251.69.56:8000',
    # reuse_driver=True,
    # add_arguments=['--disable-dev-shm-usage', '--no-sandbox'],
    add_arguments=['--disable-extensions', '--disable-application-cache', '--disable-gpu', '--no-sandbox',  '--disable-setuid-sandbox', '--disable-dev-shm-usage']
)
def pars_manager(driver: Driver, data: str):
    # <-- Authorization -->
    authorization_to_grailed(driver, data)
    # <-- /Authorization -->

    # # <-- Scroll Page -->
    # how_many = int(driver.select('div.-header').text.split()[0])
    # while True:
    #     for _ in range(4):
    #         driver.run_js(f'window.scrollTo(0, document.body.scrollHeight)')
    #         driver.sleep(2)
    #
    #     ln = len(driver.select_all('div.feed-item'))
    #     if ln >= how_many:
    #         break
    driver.sleep(1)
    # # <-- /Scroll Page -->

    driver.save_screenshot(f'{uuid4()}')

    # <-- Pars All Page Links -->
    pars_page_links(driver)
    # <-- /Pars All Page Links -->

    return


def schedule(links: list[str]):
    print('\n\n\n\n\n<--- START --->\n\n\n\n\n')
    try:
        while True:
            for _link in links:
                print(f"\n<-- Link: {_link} -- num: {links.index(_link)+1}-->\n")
                # u = f"{_link}#reuse" if len(links) != links.index(_link)+1 else f"{_link}#close"
                pars_manager(_link)
                # sleep(randint(25, 35))
            print('\n\nsleep\n\n')
            break
    except Exception as ex:
        print(f'\n\n\n\n\n<--- ERROR MAIN !!!!!! {ex} --->\n\n\n\n\n')

    print('\n\n\n\n\n<---   __STOP__   --->\n\n\n\n\n')