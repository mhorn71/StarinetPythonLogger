__author__ = 'mark'
import matplotlib

matplotlib.use('Agg')  ## do this before import matplotlib.pyplot so tkinter doesn't cause an error.

import matplotlib.pyplot as plt
import os
import time
import ConfigParser
import re
import datetime
import threading
import ftplib
import gc
# from guppy import hpy   ## install guppy if you want heap mem diags

config = ConfigParser.RawConfigParser()
config.read("StarinetBeagleLogger.conf")

## initialise next_call
next_call = time.time()

ptn = 0


def mypublisher():

    global ptn

    print "\nNew publisher thread started at", datetime.datetime.now(), "thread number ", ptn
    print "Number of active threads ", threading.active_count()

    #  enable for heap mem diags h = hpy()
    #  enable for heap mem diags print h.heap()
  
    ptn += 1

    #immediatly set schedule of next sample.
    global next_call
    interval = int(config.get('publisher', 'interval').lstrip("0"))
    #print "Interval set to - ", interval
    rate = interval * 60
    #print "Rate has been converted to seconds - ", rate
    next_call += rate
    threading.Timer(next_call - time.time(), mypublisher).start()

    #print "yep we got to _type function"

    # set channel arrays
    channel0 = []
    channel1 = []
    channel2 = []
    channel3 = []
    temperature = []
    sampletime = []

    def myftp():
        try:
            session = ftplib.FTP(config.get('publisher', 'server'),config.get('publisher', 'username'),
                                 config.get('publisher', 'password'))
            file = open('chart.png','rb')                  # file to send
            session.storbinary('STOR chart.png', file)     # send the file
            file.close()                                    # close file and FTP
            session.quit()
        except ftplib.all_errors as e:
            print "We had an FTP Error - ", e
        else:
            gc.collect()

    # combined chart
    def combined(sampletime,channel0,channel1,channel2,channel3,temperature):

        try:
            # initialise plt
            fig, ax1 = plt.subplots(figsize=(10,5))

            # plot channels
            ax1.plot(sampletime, channel0, 'b-', label='Channel 0')
            ax1.plot(sampletime, channel1, 'g-', label='Channel 1')
            ax1.plot(sampletime, channel2, 'c-', label='Channel 2')
            ax1.plot(sampletime, channel3, 'y-', label='Channel 3')
            ax1.set_xlabel('UTC')
            ax1.set_ylabel('mV')
            ax1.set_ylim(0, 1800)

            ax2 = ax1.twinx()
            ax2.plot(sampletime, temperature, 'r-', label='Temp')
            ax2.set_ylabel('Celsius')
            ax2.set_ylim(-10, 80)

            # show legend
            ax1.legend(loc = 'upper left')
            ax2.legend(loc = 'upper right')

            # auto format date axis
            fig.autofmt_xdate()

            # set grid
            plt.grid()

            # set tight layout
            plt.tight_layout()

            #plt.show()
            plt.savefig("chart.png")

            # clear last figure clf() see if it helps with memory usage.
            fig.clf()

            # close all figures to see if it helps with memory?
            plt.close('all')

        except Exception as e:
            print "We had a matplotlib error - ", e
        else:
            myftp()

    # stacked chart

    def stacked(sampletime,channel0,channel1,channel2,channel3,temperature):

        try:
            plt.figure(figsize=(7, 9), dpi=70)

            #print "sampltime - ", sampletime

            # Channels
            ax1 = plt.subplot(5, 1, 1)
            ax1.plot_date(sampletime, channel0, 'b-', label='_nolegend_')
            ax1.set_title("Channel 0")
            ax1.set_xlabel("UTC")
            ax1.set_ylabel("mV")
            ax1.locator_params(axis='y',nbins=4)

            ax2 = plt.subplot(5, 1, 2)
            ax2.plot_date(sampletime, channel1, 'g-', label='_nolegend_')
            ax2.set_title("Channel 1")
            ax2.set_xlabel("UTC")
            ax2.set_ylabel("mV")
            ax2.locator_params(axis='y',nbins=4)


            ax3 = plt.subplot(5, 1, 3)
            ax3.plot_date(sampletime, channel2, 'c-', label='_nolegend_')
            ax3.set_title("Channel 2")
            ax3.set_xlabel("UTC")
            ax3.set_ylabel("mV")
            ax3.locator_params(axis='y',nbins=4)

            ax4 = plt.subplot(5, 1, 4)
            ax4.plot_date(sampletime, channel3, 'y-', label='_nolegend_')
            ax4.set_title("Channel 3")
            ax4.set_xlabel("UTC")
            ax4.set_ylabel("mV")
            ax4.locator_params(axis='y',nbins=4)

            ax5 = plt.subplot(5, 1, 5)
            ax5.plot_date(sampletime, temperature, 'r-', label='_nolegend_')
            ax5.set_title("Instrument Temperature")
            ax5.set_xlabel("UTC")
            ax5.set_ylabel("Celsius")
            #plt.legend()

            plt.tight_layout()

            #plt.show()
            plt.savefig("chart.png")

            # experimental plt.clf() see if it helps with memory usage.
            plt.clf()

            # experimental plt.close see if it helps with memory?
            plt.close('all')
        except Exception as e:
            print "stacked Exception - ", e
        else:
            myftp()

    # find all files in memory/data and get creation time

    def get_information(directory):
        #print "Find all files created in last 24 hours in ", directory
        file_list = []
        for i in os.listdir(directory):
            ##print "os.listdir reports ", i
            a = str(os.path.join(directory,i))
            ##print "os.path.join report ", a
            file_list.append([a,os.path.getctime(a)])  #[file,created]
            ##print "file_list data is ", file_list
            file_list.sort()
        return file_list

    for _file in get_information(config.get('paths', 'datafolder')):

        #print "_file is set to ", _file

        timenow = time.time()  # get the current Unix time
        timespan = 86400  # time in seconds (24 Hours) of chart
        dawn = timenow - timespan  # start Unix time of chart

        #print "time now ", timenow
        #print "time span ", timespan
        #print "dawn ", dawn
        #print "file[0] ", _file[0]
        #print "file[1] ", _file[1]

        if float(_file[1]) >= dawn:
            block = open(_file[0]).readline().split(' ')

            #print "block ", block

            # create datetime object
            n = str(block[0]).split('-')  # split date field up
            b = str(block[1]).split(':')  # split time field up
            dt = datetime.datetime(int(n[0]),int(n[1]),int(n[2]),int(b[0]),int(b[1]),int(b[2]))

            #dt = str(block[0]) + ',' + str(block[1])

            #print "dt set to ", dt
            ##print "block[6] ", block[6]

            for datum in re.findall('\d{16}', block[6]):  # for every group of 16 digits
                dat = re.findall('....', str(datum))   # split each 16 digits into groups of 4
                sampletime.append(dt)  # append current datetime object to sampletime
                #print "date set to - ", dt
                channel0.append(int(dat[0]))  # append data to channel arrays
                channel1.append(int(dat[1]))
                channel2.append(int(dat[2]))
                channel3.append(int(dat[3]))
                temperature.append(block[2])  # append temperature to temperature array
                #print "temperature set to - ", block[2]

                dt = dt + datetime.timedelta(seconds=1)  # create next sample datetime object based on get.config rate
                #print "New dt is set to - ", dt


    if config.get('publisher', 'chart') == 'combined':
        print "Combined was selected"
        combined(sampletime,channel0,channel1,channel2,channel3,temperature)
    elif config.get('publisher', 'chart') == "stacked":
        stacked(sampletime,channel0,channel1,channel2,channel3,temperature)


mypublisher()
