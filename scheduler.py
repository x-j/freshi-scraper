
import schedule
import time
import os
import argparse
import logging

# TODO: logger

class Scheduler:

    def __init__(self, command, every):
        self.command = command
        print(time.strftime('%Y-%m-%d %T [scheduler]', time.localtime()), 'Scheduler initialised.\nCommand: '+command+" | every: "+str(every)+" mins.")
        schedule.every(every).minutes.do(lambda: os.system(command))

    def run(self):
        print(time.strftime('%Y-%m-%d %T [scheduler]', time.localtime()), "Initial run...")
        os.system(self.command)
        while True:
            print(time.strftime('%Y-%m-%d %T [scheduler]', time.localtime()),"Running...")
            schedule.run_pending()
            timeout = 60
            
            time.sleep(timeout)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Scheduler')
    parser.add_argument('command', type=str, help='OS command to be scheduled')
    parser.add_argument('--every', type=int, help='How often to run the scheduled command (in minutes)', dest='every', default=60)

    args = vars(parser.parse_args())
    Scheduler(command = args['command'], every=args['every']).run()
