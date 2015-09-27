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

        self.title = config.get("publisherlabels", "title")
        self.label0 = config.get("publisherlabels", "channel0")
        self.label1 = config.get("publisherlabels", "channel1")
        self.label2 = config.get("publisherlabels", "channel2")
        self.label3 = config.get("publisherlabels", "channel3")
        self.label4 = config.get("publisherlabels", "channel4")
        self.label5 = config.get("publisherlabels", "channel5")

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

        self.row = 0

        self.autoscale = config.get("publisherartist", "autoscale")

        self.hfmt = matplotlib.dates.DateFormatter('%H:%M:%S')

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

        plt.rcParams['xtick.labelsize'] = 'small'
        plt.rcParams['ytick.labelsize'] = 'small'

        plt.rcParams['axes.titlesize'] = 'medium'

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
        self.title = config.get("publisherlabels", "title")

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
                elif config.get('publisherartist', 'chart') == "stacked":
                    self.chart_setup()
                    self.stacked()

    def chart_setup(self):
        self.row = 0

        if self.art0 == 'true':
            self.row += 1
            self.ann = self.row

        if self.art1 == 'true':
            self.row += 1
            self.bnn = self.row

        if self.art2 == 'true':
            self.row += 1
            self.cnn = self.row

        if self.art3 == 'true':
            self.row += 1
            self.dnn = self.row

        if self.art4 == 'true':
            self.row += 1
            self.enn = self.row

        if self.art5 == 'true':
            self.row += 1
            self.fnn = self.row

        if self.art6 == 'true':
            self.row += 1
            self.gnn = self.row

    # combined chart
    def combined(self):

        count = 0

        try:
            # initialise plt
            fig, ax1 = plt.subplots(figsize=(14, 4))

            # plot channels
            if self.art0 == 'true':
                ax1.plot(self.datetime, self.chan0, 'r-', label='Celsius')
                count += 1

            if self.art1 == 'true':
                ax1.plot(self.datetime, self.chan1, 'b-', label=self.label0)
                count += 1

            if self.art2 == 'true':
                ax1.plot(self.datetime, self.chan2, 'g-', label=self.label1)
                count += 1

            if self.art3 == 'true':
                ax1.plot(self.datetime, self.chan3, 'c-', label=self.label2)
                count += 1

            if self.art4 == 'true':
                ax1.plot(self.datetime, self.chan4, 'y-', label=self.label3)
                count += 1

            if self.art5 == 'true':
                ax1.plot(self.datetime, self.chan5, 'm-', label=self.label4)
                count += 1

            if self.art6 == 'true':
                ax1.plot(self.datetime, self.chan6, 'k-', label=self.label5)
                count += 1

            ax1.set_title(self.title)
            ax1.set_xlabel('Time (UT)')
            ax1.set_ylabel('mV')
            ax1.yaxis.set_major_locator(MaxNLocator(integer=True))

            if self.autoscale == 'false':
                ax1.set_ylim(0, 1800)
            else:
                ax1.margins(0, 1)

            font_size = FontProperties()
            font_size.set_size('small')

            # show legend

            lgd = ax1.legend(prop=font_size, loc=9, bbox_to_anchor=(0.5, -0.17), ncol=count)

            for legend_handle in lgd.legendHandles:
                legend_handle.set_linewidth(8.0)

            ax1.xaxis.set_major_formatter(self.hfmt)

            # set grid
            ax1.grid()

            plt.savefig("chart.png", bbox_extra_artists=(lgd,), bbox_inches='tight')

            # # clear last figure clf() see if it helps with memory usage.
            # fig.clf()
            #
            # # close all figures to see if it helps with memory?
            # plt.close('all')

        except Exception as e:
            print("We had a matplotlib error - " + str(e))
        else:
            self.myftp()

    def stacked(self):
        try:
            if self.row == 1:
                plt.figure(figsize=(14, 2.2))
            elif self.row == 2:
                plt.figure(figsize=(14, 4.4))
            elif self.row == 3:
                plt.figure(figsize=(14, 6.6))
            elif self.row == 4:
                plt.figure(figsize=(14, 8.8))
            elif self.row == 5:
                plt.figure(figsize=(14, 11))
            elif self.row == 6:
                plt.figure(figsize=(14, 13.2))
            elif self.row == 7:
                plt.figure(figsize=(14, 15.4))

            plt.suptitle(self.title)

            # Channels
            if self.art0 == 'true':
                ax0 = plt.subplot(self.row, 1, self.ann)
                ax0.plot_date(self.datetime, self.chan0, 'r-')
                ax0.set_title('Instrument Temperature')
                ax0.set_xlabel('Time (UT)')
                ax0.set_ylabel('Celsius')
                ax0.xaxis.set_major_formatter(self.hfmt)
                ax0.yaxis.set_major_locator(MaxNLocator(integer=True))
                ax0.grid()
                ax0.margins(0, 1)

            if self.art1 == 'true':
                ax1 = plt.subplot(self.row, 1, self.bnn)
                ax1.plot_date(self.datetime, self.chan1, 'b-')
                ax1.set_title(self.label0)
                ax1.set_xlabel('Time (UT)')
                ax1.set_ylabel('mV')
                ax1.xaxis.set_major_formatter(self.hfmt)
                ax1.grid()

                if self.autoscale == 'false':
                    ax1.set_ylim(0,1800)
                    ax1.set_yticks((0, 360, 720, 1080, 1440, 1800))
                else:
                    ax1.margins(0, 1)

            if self.art2 == 'true':
                ax2 = plt.subplot(self.row, 1, self.cnn)
                ax2.plot_date(self.datetime, self.chan2, 'g-')
                ax2.set_title(self.label1)
                ax2.set_xlabel('Time (UT)')
                ax2.set_ylabel('mV')
                ax2.xaxis.set_major_formatter(self.hfmt)
                ax2.grid()

                if self.autoscale == 'false':
                    ax2.set_ylim(0, 1800)
                    ax2.set_yticks((0, 360, 720, 1080, 1440, 1800))
                else:
                    ax2.margins(0, 1)

            if self.art3 == 'true':
                ax3 = plt.subplot(self.row, 1, self.dnn)
                ax3.plot_date(self.datetime, self.chan3, 'c-')
                ax3.set_title(self.label2)
                ax3.set_xlabel('Time (UT)')
                ax3.set_ylabel('mV')
                ax3.xaxis.set_major_formatter(self.hfmt)
                ax3.grid()

                if self.autoscale == 'false':
                    ax3.set_ylim(0, 1800)
                    ax3.set_yticks((0, 360, 720, 1080, 1440, 1800))
                else:
                    ax3.margins(0, 1)

            if self.art4 == 'true':
                ax4 = plt.subplot(self.row, 1, self.enn)
                ax4.plot_date(self.datetime, self.chan4, 'y-')
                ax4.set_title(self.label3)
                ax4.set_xlabel('Time (UT)')
                ax4.set_ylabel('mV')
                ax4.xaxis.set_major_formatter(self.hfmt)
                ax4.grid()

                if self.autoscale == 'false':
                    ax4.set_ylim(0, 1800)
                    ax4.set_yticks((0, 360, 720, 1080, 1440, 1800))
                else:
                    ax4.margins(0, 1)

            if self.art5 == 'true':
                ax5 = plt.subplot(self.row, 1, self.fnn)
                ax5.plot_date(self.datetime, self.chan5, 'm-')
                ax5.set_title(self.label4)
                ax5.set_xlabel('Time (UT)')
                ax5.set_ylabel('mV')
                ax5.xaxis.set_major_formatter(self.hfmt)
                ax5.grid()

                if self.autoscale == 'false':
                    ax5.set_ylim(0, 1800)
                    ax5.set_yticks((0, 360, 720, 1080, 1440, 1800))
                else:
                    ax5.margins(0, 1)

            if self.art6 == 'true':
                ax6 = plt.subplot(self.row, 1, self.gnn)
                ax6.plot_date(self.datetime, self.chan6, 'k-')
                ax6.set_title(self.label5)
                ax6.set_xlabel('Time (UT)')
                ax6.set_ylabel('mV')
                ax6.xaxis.set_major_formatter(self.hfmt)
                ax6.grid()

                if self.autoscale == 'false':
                    ax6.set_ylim(0, 1800)
                    ax6.set_yticks((0, 360, 720, 1080, 1440, 1800))
                else:
                    ax6.margins(0, 1)

            plt.tight_layout(rect=[0, 0.03, 1, 0.97])

            plt.savefig("chart.png", bbox_inches='tight')

        except Exception as e:
            print("stacked Exception - " + str(e))
        else:
            self.myftp()

    def myftp(self):
        try:
            session = ftplib.FTP(self.server, self.server_username, self.server_password)
            # session.set_debuglevel(1)

            if self.server_folder is not None:
                if session.pwd() is not self.server_folder:
                    session.cwd(self.server_folder)  # Change directory

            file = open('chart.png', 'rb')                  # file to send
            session.storbinary('STOR chart.png', file)     # send the file
            file.close()                                    # close file and FTP
            session.quit()

        except (ftplib.all_errors, AttributeError) as e:
            print("We had an FTP Error - " + str(e))
