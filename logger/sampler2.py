__author__ = 'mark'

import datetime
import time
import threading


class logger(object):
    def __init__(self, parent):
        self.ui = parent.ui
        self.rate = 1
        self.channel_count = 4
        self.status = False
        self.next_call = time.time()

        thread = threading.Thread(target=self.run)
        thread.daemon = True
        thread.start()

    def run(self):
        while 1:
            if self.status:
                self.next_call += self.rate
                print('Sampler Started: ' + str(datetime.datetime.now()))
                pause = self.next_call - time.time()
                time.sleep(pause)
            elif self.status is False:
                time.sleep(1)

    def start(self):
        self.next_call = time.time()
        self.status = True

    def stop(self):
        self.status = False

    def status(self):

        if self.status:
            status = 8000
        else:
            status = 0

        return status