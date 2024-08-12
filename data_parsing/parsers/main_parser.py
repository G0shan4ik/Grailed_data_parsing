from datetime import datetime

import requests
from botasaurus.browser import browser, Driver

from .helpers import grailed_parser, authorization_to_grailed

import lxml
from bs4 import BeautifulSoup

from loguru import logger


def pars_page_links(driver: Driver):
    soup = BeautifulSoup(driver.page_html, 'lxml')
    data = []
    for item in soup.select('div.feed-item'):
        try:
            _url = f"https://www.grailed.com{item.select_one('a.listing-item-link').get('href')}"

            # <-- Pars Card -->
            fl, dct = grailed_parser(_url)[0], grailed_parser(_url)[1]
            if fl is None:
                break
            logger.info(f'UNIQUE LINK):  {_url}')
            data.append(dct)
            # <-- /Pars Card -->
        except:
            ...
    return data


@browser(
    profile='Grailed',
    close_on_crash=True,
    add_arguments=['--disable-extensions', '--disable-application-cache', '--disable-gpu', '--no-sandbox',  '--disable-setuid-sandbox', '--disable-dev-shm-usage']
)
def pars_manager(driver: Driver, data: str):
    # <-- Authorization -->
    authorization_to_grailed(driver, data)
    logger.info(f'Success authorization {data}')
    # <-- /Authorization -->

    driver.sleep(1)

    driver.save_screenshot(f'AFTER_authorisation_{datetime.now().strftime("%Y_%m_%d__%H_%M_%S")}.png')

    # <-- Pars All Page Links -->
    result = pars_page_links(driver)
    # <-- /Pars All Page Links -->

    url = "http://159.223.33.34:8000/accept_data"
    requests.post(url, data=str(result))

    return


def schedule(links: list[str]):
    print('\n\n\n\n\n<--- START --->\n\n\n\n')
    try:
        while True:
            for _link in links:
                logger.info(f"Run check link: {_link},\nnumber link in list:  {links.index(_link)+1}\n\n")
                pars_manager(_link)
            print('\n\nsleep\n\n')
            break
    except Exception as ex:
        logger.error(f"ERROR MAIN ( func schedule() ): {ex}")

    print('\n\n\n\n\n<---   __STOP__   --->\n\n\n\n\n')