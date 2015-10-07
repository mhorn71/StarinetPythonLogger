__author__ = 'mark'

import datetime
import time
import threading
import configparser
import logging

import analogue.readadc as adc
import logger.temperature as temperature


class Logger:
    def __init__(self, data_array):
        self.config = configparser.RawConfigParser()
        self.config.read("StarinetBeagleLogger.conf")
        self.datafolder = self.config.get("paths", "datafolder")
        self.rate = 1
        self.rate_string = '0001'
        self.channel_count = 4
        self.status_ = threading.Event()
        self.status_.set()
        self.next_call = time.time()
        self.data = data_array
        self.string = ''
        self.block_count = 0
        self.logger = logging.getLogger('logger.Logger')
        self.logger.info('Logger initialising')

    def log(self):
        while not self.status_.is_set():
            self.next_call += self.rate
            if len(self.string) == 512:
                self.datafile_write()
                self.logger.debug('Appending data to internal memory string.')
                self.data.append(self.string)
                self.block_count += 1
                self.logger.debug('Next data block integer is : ' + str(self.block_count))
                if self.block_count == 16384:
                    self.logger.debug('Data block count has reached 16384 stopping sampler.')
                    self.status_.set()
                else:
                    stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    self.string = str(stamp) + ' ' + temperature.read() + ' ' + self.rate_string + '   ' + \
                                  adc.read_string()
            else:
                self.string += adc.read_string()

            self.status_.wait(self.next_call - time.time())

    def datafile_write(self):
        datafile = hex(self.block_count).split('x')[1].upper().zfill(4)
        self.logger.debug('Writing new data block : ' + str(datafile))
        try:
            file = open(self.datafolder + datafile, 'wt', encoding='utf-8')
            file.write(self.string)
            file.close()
        except IOError as msg:
            self.status_.set()
            self.logger.critical('Unable to write data block :' + str(datafile) + ' : ' + str(msg))

    def start(self):
        self.logger.debug('Clearing internal data array')
        del self.data[:]
        self.logger.debug('Data array length :' + str(len(self.data)))
        self.config.read("StarinetBeagleLogger.conf")
        self.rate_string = self.config.get('capture', 'rate')
        self.rate = int(self.rate_string)
        self.logger.debug('Sampler rate set too : ' + str(self.rate))
        self.block_count = 0
        self.logger.debug('Block count reset to : ' + str(self.block_count))
        self.next_call = time.time()
        stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.string = str(stamp) + ' ' + temperature.read() + ' ' + self.rate_string + '   ' + adc.read_string()
        self.status_.clear()

        global thread
        thread = threading.Thread(target=self.log)
        thread.daemon = True
        thread.start()

        if thread.is_alive():
            self.logger.info('Logger thread started')

    def stop(self):
        self.status_.set()
        thread.join()

        if len(self.string) > 0:
            self.logger.debug('Internal memory string has data flushing to disk.')
            self.data.append(self.string)
            self.datafile_write()

        self.logger.info('Sampler Stopped...')

    def status(self):

        if not self.status_.is_set():
            value = 8000
        else:
            value = 0

        return value

