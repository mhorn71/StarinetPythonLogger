__author__ = 'mark'

import matplotlib

matplotlib.use('Agg')  ## do this before import matplotlib.pyplot so tkinter doesn't cause an error.

import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import time
import configparser
import re
import datetime
import threading
import ftplib
from matplotlib.ticker import MaxNLocator

config = configparser.RawConfigParser()
config.read("StarinetBeagleLogger.conf")


class ChartPublisher:
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

        self.server = config.get('publisher', 'server')
        self.server_username = config.get('publisher', 'username')
        self.server_password = config.get('publisher', 'password')
        self.server_folder = config.get('publisher', 'remotefolder')

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

        self.status_ = threading.Event()
        self.status_.set()
        self.next_call = time.time()

        plt.rcParams['legend.framealpha'] = 0.5
        plt.rcParams['legend.fancybox'] = True

        thread = threading.Thread(target=self.run)
        thread.daemon = True
        thread.start()

    def run(self):
        while 1:
            while not self.status_.is_set():
                self.next_call += (self.rate * 60)

                self.data_finder()

                print('Publisher', str(datetime.datetime.now()))

                self.status_.wait(self.next_call - time.time())
            else:
                time.sleep(1)

    def start(self):
        config.read("StarinetBeagleLogger.conf")
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

        self.server = config.get('publisher', 'server')
        self.server_username = config.get('publisher', 'username')
        self.server_password = config.get('publisher', 'password')
        self.server_folder = config.get('publisher', 'remotefolder')

        self.autoscale = config.get("publisherartist", "autoscale")

        self.next_call = time.time()
        self.status_.clear()

    def stop(self):
        self.status_.set()

    def status(self):

        if not self.status_.is_set():
            value = True
        else:
            value = False

        return value

    def data_finder(self):
        if len(self.data_array) == 0:
            pass
        else:
            timenow = datetime.datetime.now()  # get the current Unix time
            time_span_start = timenow - datetime.timedelta(seconds=86400)  # start Unix time of chart

            del self.chan0[:]  # Temperature Channel
            del self.chan1[:]
            del self.chan2[:]
            del self.chan3[:]
            del self.chan4[:]
            del self.chan5[:]
            del self.chan6[:]
            del self.datetime[:]

            for item in self.data_array:
                data = item.split()
                # create datetime object
                date = str(data[0]).split('-')  # split date field up
                time = str(data[1]).split(':')  # split time field up
                block_start_time = datetime.datetime(int(date[0]), int(date[1]), int(date[2]), int(time[0]), int(time[1]),
                                              int(time[2]))

                sample_rate = int(data[3])

                if block_start_time >= time_span_start:
                    dt = block_start_time
                    for datum in re.findall('\d{24}', data[4]):  # for every group of 16 digits
                        dat = re.findall('....', str(datum))   # split each 24 digits into groups of 4
                        self.datetime.append(dt)  # append current datetime object
                        self.chan0.append(data[2])  # append temperature
                        self.chan1.append(int(dat[0]))  # append data
                        self.chan2.append(int(dat[1]))
                        self.chan3.append(int(dat[2]))
                        self.chan4.append(int(dat[3]))
                        self.chan5.append(int(dat[4]))
                        self.chan6.append(int(dat[5]))

                        dt = dt + datetime.timedelta(seconds=sample_rate)

            if len(self.datetime) >= 20:
                if config.get('publisherartist', 'chart') == 'combined':
                    self.combined()
                # elif config.get('publisherartist', 'chart') == "stacked":
                    # stacked()

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

        count = 0

        try:
            # initialise plt
            fig, ax1 = plt.subplots(figsize=(10, 5))
            plt.xticks(rotation=30)

            # plot channels
            if self.art0 == 'true':
                ax1.plot(self.datetime, self.chan0, 'r-', label=self.label0)
                count += 1

            if self.art1 == 'true':
                ax1.plot(self.datetime, self.chan1, 'b-', label=self.label1)
                count += 1

            if self.art2 == 'true':
                ax1.plot(self.datetime, self.chan2, 'g-', label=self.label2)
                count += 1

            if self.art3 == 'true':
                ax1.plot(self.datetime, self.chan3, 'c-', label=self.label3)
                count += 1

            if self.art4 == 'true':
                ax1.plot(self.datetime, self.chan4, 'y-', label=self.label4)
                count += 1

            if self.art5 == 'true':
                ax1.plot(self.datetime, self.chan5, 'm-', label=self.label5)
                count += 1

            if self.art6 == 'true':
                ax1.plot(self.datetime, self.chan6, 'k-', label=self.label6)
                count += 1

            ax1.set_xlabel('Time (UTC)')
            ax1.set_ylabel('mV')
            ax1.yaxis.set_major_locator(MaxNLocator(integer=True))

            if self.autoscale == 'false':
                ax1.set_ylim(0, 1800)
            else:
                ax1.margins(0, 1)

            font_size = FontProperties()
            font_size.set_size('small')

            # show legend
            if count == 7:
                lgd = ax1.legend(prop=font_size, loc=9, bbox_to_anchor=(0.455, -0.21), ncol=count)
            else:
                lgd = ax1.legend(prop=font_size, loc=9, bbox_to_anchor=(0.5, -0.21), ncol=count)

            hfmt = matplotlib.dates.DateFormatter('%H:%M:%S')
            ax1.xaxis.set_major_formatter(hfmt)


            # set grid
            ax1.grid()

            plt.savefig("chart.png", bbox_extra_artists=(lgd,), bbox_inches='tight')

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
            session = ftplib.FTP(self.server, self.server_username, self.server_password)
            session.set_debuglevel(1)

            if self.server_folder is not None:
                print(self.server_folder)
                print(session.pwd())
                if session.pwd() is not self.server_folder:
                    session.cwd(self.server_folder)  # Change directory
            else:
                print('server_folder is None')

            file = open('chart.png', 'rb')                  # file to send
            session.storbinary('STOR chart.png', file)     # send the file
            file.close()                                    # close file and FTP
            session.quit()

        except (ftplib.all_errors, AttributeError) as e:
            print("We had an FTP Error - " + str(e))
