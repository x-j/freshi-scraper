
import schedule
import time
import os
import argparse
import logging

# TODO: logger

class Scheduler:

    def __init__(self, command: str, every: int):
        self.logger = logging.getLogger(type(self).__name__)
        self.command = command
        self.logger.info('Scheduler initialised.\t| command: '+command+' | every: '+str(every)+' mins.')
        schedule.every(every).minutes.do(lambda: os.system(command))

    def run(self):
        self.logger.info('Initial run...')
        os.system(self.command)
        while True:
            schedule.run_pending()
            timeout = 59
            time.sleep(timeout)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Scheduler')
    parser.add_argument('command', type=str, help='OS command to be scheduled')
    parser.add_argument('--every', type=int, help='how often to run the scheduled command (in minutes)', dest='every', default=60)

    args = vars(parser.parse_args())
    Scheduler(command = args['command'], every=args['every']).run()
