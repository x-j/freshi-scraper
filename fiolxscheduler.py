import os
import argparse

from scheduler import Scheduler

class FiolxScheduler(Scheduler):

    def __init__(self, command: str, every=60):
        assert command.startswith('https://www.olx.pl') or command.startswith('www.olx.pl')
        command = f"scrapy crawl fiolxs -a search_url={command}"
        super().__init__(command=command, every=every)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='FiolxScheduler. Runs a fiolxspider every N minutes (60 by default).')
    parser.add_argument('spider_args', type=str, help='fiolxs crawl arguments. -a search_url= is implied, so this needs start with a valid url. You can append additional spider argumetns if you want (e.g. -L INFO).')
    parser.add_argument('--every', type=int, help='how often to run the scheduled spider (in minutes)', dest='every', default=60)

    args = vars(parser.parse_args())
    FiolxScheduler(command = args['spider_args'], every=args['every']).run()
