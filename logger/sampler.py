__author__ = 'mark'
import ConfigParser
import datetime
import time
import os
import threading
import readadc
import temperature
import signal

## initialise config parser
config = ConfigParser.RawConfigParser()
config.read("StarinetBeagleLogger.conf")

## initialise next_call
next_call = time.time()


def mylogger():
    #print "Started mylogger"

    #immediatly set schedule of next sample.
    global next_call
    rate = int(config.get('capture', 'rate').lstrip("0"))
    #next_call = next_call + int(config.get('capture', 'rate').lstrip("0"))
    next_call += rate
    threading.Timer(next_call - time.time(), mylogger).start()

    #get name of last data file and set assign to datafile
    files = os.listdir(config.get("paths", "datafolder"))
    name_n_timestamp = dict([(x, os.stat(config.get("paths", "datafolder")+x).st_mtime) for x in files])
    datafile = max(name_n_timestamp, key=lambda k: name_n_timestamp.get(k))

    #set number of last file
    lastfilenumber = len(files)

    #open datafile
    f = open(config.get("paths", "datafolder") + datafile, 'rb')

    #set the first sample time stamp
    stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    junk = f.readline()

    if f.tell() == 0:
        print "Data File appears to be 0 bytes", f.tell()
        f.close()
        f = open(config.get("paths", "datafolder") + datafile, 'ab')
        samplerdata = ''.join(readadc.read())
        #print "samplerdata = ", repr(samplerdata)
        data = str(stamp) + ' ' + temperature.read() + ' ' + str(config.get('capture', 'rate')) + '   ' + \
            str(samplerdata)
        f.write(data)
        f.close()
    elif f.tell() == 512:
        print "Data File was greater than 0 and greater than 512", f.tell()
        f.close()
        datafile = hex(lastfilenumber).split('x')[1].upper().zfill(4)  # change filenumber to hex
        print "NEW DATA FILE IS CALLED : ", datafile

        if datafile == 'FFFE':
            try:
                pidfile = open(config.get('paths', 'pidfile'), 'r')
                pid = int(pidfile.read())
                pidfile.close()
            except IOError as e:
                print "Unable to assign pid to pro.pid capture.py"
            else:
                try:
                    os.kill(pid, signal.SIGTERM)
                except OSError as e:
                    print "Unable to kill process logger/sampler"
                else:
                    try:
                        os.remove(str(config.get('paths', 'pidfile')))
                    except OSError as e:
                        print "Unable to remove pid file fatal error"

        f = open(config.get("paths", "datafolder") + datafile, 'wb')
        samplerdata = ''.join(readadc.read())
        #print "samplerdata = ", repr(samplerdata)
        data = str(stamp) + ' ' + temperature.read() + ' ' + str(config.get('capture', 'rate')) + '   ' + \
            str(samplerdata)
        f.write(data)
        f.close()
    else:
        print "Datafile size between 0 - 512 bytes", f.tell()
        f.close()
        f = open(config.get("paths", "datafolder") + datafile, 'ab')
        samplerdata = ''.join(readadc.read())
        print "samplerdata = ", repr(samplerdata)
        data = str(samplerdata)
        f.write(data)
        f.close()

mylogger()

