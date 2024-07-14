from data_parsing.database import init
from data_parsing.parsers.main_parser import schedule
from data_parsing.parsers.main_parser import grailed_parser


with open('pars_list', 'r', encoding='utf8') as f:
    all_links: list[str] = list(map(lambda item: item.replace('\n', ''), f.readlines()))

def start_dev():
    init()
    schedule(links=all_links)