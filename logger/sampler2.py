__author__ = 'mark'

import datetime
import time
import threading
import configparser

import analogue.readadc as adc
import logger.temperature as temperature


class logger(object):
    def __init__(self, data_array):
        self.config = configparser.RawConfigParser()
        self.config.read("StarinetBeagleLogger.conf")
        self.datafolder = self.config.get("paths", "datafolder")
        self.rate = 1
        self.rate_string = '0001'
        self.channel_count = 4
        self.status_ = False
        self.next_call = time.time()
        self.data = data_array
        self.string = ''
        self.block_count = 0

        thread = threading.Thread(target=self.run)
        thread.daemon = True
        thread.start()

    def run(self):
        while 1:
            if self.status_:
                self.next_call += self.rate
                if len(self.string) == 512:
                    self.datafile_write()
                    self.data.append(self.string)
                    self.block_count += 1
                    if self.block_count == 4096:
                        self.status_ = False
                    else:
                        stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        self.string = str(stamp) + ' ' + temperature.read() + ' ' + self.rate_string + '   ' + adc.read_string()
                else:
                    self.string += adc.read_string()

                pause = self.next_call - time.time()
                time.sleep(pause)
            elif self.status_ is False:
                time.sleep(1)

    def datafile_write(self):
        datafile = hex(self.block_count).split('x')[1].upper().zfill(4)
        file = open(self.datafolder + datafile, 'wt', encoding='utf-8')
        file.write(self.string)
        file.close()

    def start(self):
        self.rate_string = self.config.get('capture', 'rate')
        self.rate = int(self.rate_string)
        self.block_count = 0
        self.next_call = time.time()
        stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.string = str(stamp) + ' ' + temperature.read() + ' ' + self.rate_string + '   ' + adc.read_string()
        self.status_ = True

    def stop(self):
        self.status_ = False
        if len(self.string) > 0:
            self.data.append(self.string)
            self.datafile_write()

    def status(self):

        if self.status_:
            value = 8000
        else:
            value = 0

        return value