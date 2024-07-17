from data_parsing.parsers.main_parser import schedule

from time import sleep


with open('pars_list', 'r', encoding='utf8') as f:
    all_links: list[str] = list(map(lambda item: item.replace('\n', ''), f.readlines()))

def start_dev():
    while True:
        schedule(links=all_links)

        sleep(3000)


if __name__ == '__main__':
    start_dev()