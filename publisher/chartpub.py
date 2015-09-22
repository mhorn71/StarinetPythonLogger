__author__ = 'mark'

import matplotlib

matplotlib.use('Agg')  ## do this before import matplotlib.pyplot so tkinter doesn't cause an error.

import matplotlib.pyplot as plt
import os
import time
import configparser
import re
import datetime
import threading
import ftplib
import gc
from matplotlib.ticker import MaxNLocator

config = configparser.RawConfigParser()
config.read("StarinetBeagleLogger.conf")


class ChartPublisher(object):
    def __init__(self, data_array):
        self.data_array = data_array

        self.label0 = config.get("publisherlabels", "channel0")
        self.label1 = config.get("publisherlabels", "channel1")
        self.label2 = config.get("publisherlabels", "channel2")
        self.label3 = config.get("publisherlabels", "channel3")
        self.label4 = config.get("publisherlabels", "channel4")
        self.label5 = config.get("publisherlabels", "channel5")
        self.label6 = config.get("publisherlabels", "channel6")

        self.art0 = config.get("publisherartist", "channelArt0")
        self.art1 = config.get("publisherartist", "channelArt1")
        self.art2 = config.get("publisherartist", "channelArt2")
        self.art3 = config.get("publisherartist", "channelArt3")
        self.art4 = config.get("publisherartist", "channelArt4")
        self.art5 = config.get("publisherartist", "channelArt5")
        self.art6 = config.get("publisherartist", "channelArt6")

        self.ann = None
        self.bnn = None
        self.cnn = None
        self.dnn = None
        self.enn = None
        self.fnn = None
        self.gnn = None

        self.autoscale = config.get("publisherartist", "autoscale")

        self.rate = int(config.get("publisher", "interval").lstrip("0"))

        self.chan0 = []  # Temperature Channel
        self.chan1 = []
        self.chan2 = []
        self.chan3 = []
        self.chan4 = []
        self.chan5 = []
        self.chan6 = []
        self.datetime = []

        self.row = 0

        self.status_ = False
        self.next_call = time.time()

        thread = threading.Thread(target=self.run)
        thread.daemon = True
        thread.start()

    def run(self):
        while 1:
            if self.status_:
                self.next_call += (self.rate * 60)
                print('Next Call : ', self.next_call)
                print('Rate : ', self.rate)
                pause = self.next_call - time.time()
                print('Pause : ', pause)
                time.sleep(pause)
            else:
                time.sleep(1)

    def start(self):
        self.rate = int(config.get("publisher", "interval").lstrip("0"))
        self.label0 = config.get("publisherlabels", "channel0")
        self.label1 = config.get("publisherlabels", "channel1")
        self.label2 = config.get("publisherlabels", "channel2")
        self.label3 = config.get("publisherlabels", "channel3")
        self.label4 = config.get("publisherlabels", "channel4")
        self.label5 = config.get("publisherlabels", "channel5")
        self.label6 = config.get("publisherlabels", "channel6")

        self.art0 = config.get("publisherartist", "channelArt0")
        self.art1 = config.get("publisherartist", "channelArt1")
        self.art2 = config.get("publisherartist", "channelArt2")
        self.art3 = config.get("publisherartist", "channelArt3")
        self.art4 = config.get("publisherartist", "channelArt4")
        self.art5 = config.get("publisherartist", "channelArt5")
        self.art6 = config.get("publisherartist", "channelArt6")

        self.autoscale = config.get("publisherartist", "autoscale")

        self.next_call = time.time()
        self.status_ = True

    def stop(self):
        self.status_ = False

    def status(self):

        if self.status_:
            value = True
        else:
            value = False

        return value

    def chart_setup(self):
        row = 0

        if self.art0 == 'true':
            row += 1
            self.ann = row

        if self.art1 == 'true':
            row += 1
            self.bnn = row

        if self.art2 == 'true':
            row += 1
            self.cnn = row

        if self.art3 == 'true':
            row += 1
            self.dnn = row

        if self.art4 == 'true':
            row += 1
            self.enn = row

        if self.art5 == 'true':
            row += 1
            self.fnn = row

        if self.art6 == 'true':
            row += 1
            self.gnn = row

    # combined chart
    def combined(self):

        try:
            # initialise plt
            fig, ax1 = plt.subplots(figsize=(10,5))

            # plot channels
            if self.art1 == 'true':
                ax1.plot(self.datetime, self.chan1, 'b-', label=self.label1)

            if self.art2 == 'true':
                ax1.plot(self.datetime, self.chan2, 'g-', label=self.label2)

            if self.art3 == 'true':
                ax1.plot(self.datetime, self.chan3, 'c-', label=self.label3)

            if self.art4 == 'true':
                ax1.plot(self.datetime, self.chan4, 'y-', label=self.label4)

            if self.art5 == 'true':
                ax1.plot(self.datetime, self.chan5, 'm-', label=self.label5)

            if self.art6 == 'true':
                ax1.plot(self.datetime, self.chan6, 'k-', label=self.label6)

            ax1.set_xlabel('Time (UTC)')
            ax1.set_ylabel('mV')
            ax1.yaxis.set_major_locator(MaxNLocator(integer=True))

            if self.autoscale == 'false':
                ax1.set_ylim(0, 1800)
            else:
                ax1.margins(0, 1)

            if self.art0 == 'true':
                ax2 = ax1.twinx()
                ax2.plot(self.datetime, self.chan0, 'r-', label=self.label0)
                ax2.set_ylabel('Celsius')
                ax2.yaxis.set_major_locator(MaxNLocator(integer=True))
                ax2.margins(0, 1)

            # show legend
            ax1.legend(loc='best')

            if self.art0 == 'true':
                ax2.legend(loc='best')

            # auto format date axis
            fig.autofmt_xdate()

            # set grid
            ax1.grid()

            # set tight layout
            plt.tight_layout()

            #plt.show()
            plt.savefig("chart.png")

            # clear last figure clf() see if it helps with memory usage.
            fig.clf()

            # close all figures to see if it helps with memory?
            plt.close('all')

        except Exception as e:
            print("We had a matplotlib error - " + str(e))
        else:
            self.myftp()

    def myftp(self):
        try:
            session = ftplib.FTP(config.get('publisher', 'server'), config.get('publisher', 'username'),
                                 config.get('publisher', 'password'))
            session.cwd(config.get('publisher', 'remotefolder')) # Change directory
            file = open('chart.png','rb')                  # file to send
            session.storbinary('STOR chart.png', file)     # send the file
            file.close()                                    # close file and FTP
            session.quit()
        except ftplib.all_errors as e:
            print("We had an FTP Error - " + str(e))
