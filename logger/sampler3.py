__author__ = 'mark'
# StarinetPython3Logger a data logger for the Beaglebone Black.
# Copyright (C) 2015  Mark Horn
#
# This file is part of StarinetPython3Logger.
#
# StarinetPython3Logger is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 2 of the License, or (at your option) any
# later version.
#
# StarinetPython3Logger is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with StarinetPython3Logger.  If not, see <http://www.gnu.org/licenses/>.


import datetime
import time
import threading
import configparser
import logging
import os

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
        self.data_cleared = False

    def delete_datafiles(self):
        try:
            for the_file in os.listdir(self.datafolder):
                file_path = os.path.join(self.datafolder, the_file)
                if os.path.isfile(file_path):
                        os.unlink(file_path)
                self.logger.debug("%s %s", "Removing data file ", file_path)
        except OSError as e:
                    self.logger.critical("%s %s", "premature termination", e)
        else:
            self.data_cleared = True

    def string_start(self):

        stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        string_start = str(stamp) + ' ' + temperature.read() + ' ' + self.rate_string + '   ' + \
                   adc.read_string()

        return string_start

    def adc_string(self):
        string = adc.read_string()
        return string

    def log(self):
        while not self.status_.is_set():
            if self.data_cleared is True:
                self.next_call += self.rate
                if len(self.string) == 512:
                    if self.datafile_write():
                        self.logger.debug('Appending data to internal memory string.')
                        self.data.append(self.string)
                        self.block_count += 1
                        self.logger.debug('Next data block integer is : ' + str(self.block_count))
                        if self.block_count == 16384:
                            self.logger.debug('Data block count has reached 16384 stopping sampler.')
                            self.status_.set()
                        else:
                            while True:
                                start_string =self.string_start()

                                if len(start_string) == 56:
                                    self.string = start_string
                                    break
                                else:
                                    self.logger.warning('String start length exceeded 56 bytes : %s' % str(len(start_string)))
                                    start_string = self.string_start()
                    else:
                        pass

                elif len(self.string) > 512:
                    self.logger.critical('Block size is greater than 512bytes stopping logger')
                    self.status_.set()
                else:
                    while True:
                        adc_string = self.adc_string()

                        if len(adc_string) == 24:
                            self.string += adc.read_string()
                            break
                        else:
                            print('ADC reading length exceed 24 bytes : %s' % str(len(adc_string)))
                            adc_string = self.adc_string()

                self.status_.wait(self.next_call - time.time())
            else:
                time.sleep(1)

    def datafile_write(self):
        datafile = hex(self.block_count).split('x')[1].upper().zfill(4)
        self.logger.debug('Writing new data block : ' + str(datafile))

        filename = self.datafolder + datafile

        try:
            file = open(filename, 'wt', encoding='utf-8')
            file.write(self.string)
            file.close()
        except IOError as msg:
            self.logger.critical('Unable to write data block :' + str(datafile) + ' : ' + str(msg) + ' : retrying write.')
            try:
                file = open(filename + datafile, 'wt', encoding='utf-8')
                file.write(self.string)
                file.close()
            except IOError as msg:
                self.status_.set()
                self.logger.critical('Unable to write data block :' + str(datafile) + ' : ' + str(msg))

        if os.path.isfile(filename):
            self.logger.info('Created data file : ' + str(datafile))
            return True
        else:
            self.status_.set()
            self.logger.critical('Data block : ' + str(datafile) + ' : was not created, logger halted.')

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
        self.data_cleared = False

        delete_thread = threading.Thread(target=self.delete_datafiles)
        delete_thread.daemon = True
        delete_thread.start()

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

