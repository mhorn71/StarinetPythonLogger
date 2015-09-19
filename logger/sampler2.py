__author__ = 'mark'

import datetime
import time
import threading


class logger(object):
    def __init__(self, data_array):
        self.rate = 1
        self.channel_count = 4
        self.status_ = False
        self.next_call = time.time()
        self.data = data_array

        thread = threading.Thread(target=self.run)
        thread.daemon = True
        thread.start()

    def run(self):
        while 1:
            if self.status_:
                self.next_call += self.rate
                print('Sampler Started: ' + str(datetime.datetime.now()))
                pause = self.next_call - time.time()
                time.sleep(pause)
            elif self.status_ is False:
                time.sleep(1)

    def start(self):
        self.next_call = time.time()
        self.status_ = True

    def stop(self):
        self.status_ = False

    def status(self):

        if self.status_:
            value = 8000
        else:
            value = 0 # should be 0 set to 8000 for testing.

        return value