StarinetPython3Logger
=====================

Beaglebone Black Python3 Starinet six channel data logger. 

Install Instructions from Source
================================

You need to install the following additional python packages.

    The Adafruit BBIO Library 
    -------------------------
    https://learn.adafruit.com/setting-up-io-python-library-on-beaglebone-black/overview

    crcmod
    ------
    https://pypi.python.org/pypi/crcmod/1.7

    psutils
    -------
    https://code.google.com/p/psutil/

    matplotlib - Version 1.4.3 or greater.
    ----------
    https://github.com/matplotlib/matplotlib

    You can install the above using apt-get and pip as the root user or using sudo with the following
    commands:

    apt-get install python-pip
    pip install crcmod
    pip install python-matplotlib
    pip install psutil
    pip install Adafruit_BBIO



Not required but you will need to attach a TMP36 to ADC Channel AIN6 to get a sensible temperature reading.

    TMP36 Temperature Sensor
    ------------------------
    https://learn.adafruit.com/measuring-temperature-with-a-beaglebone-black/wiring

Software install and startup

    1.) place all files in there own folder and then start as shown below assuming you've uncompressed in /home

    user@beaglebone:~$ sudo su -                   
    [sudo] password for user: 
    root@beaglebone:~# cd /home/StarinetPythonLogger2/
    root@beaglebone:/home/StarinetPythonLogger2# nohup python3 main.py &

Binary Setup
============

To use the binary available under releases you'll need to do the following. 

Copy the binary to /opt and start main as root :

    sudo ./main 

Alternatively you can use the very basic init script located in goodies called starinetlogger

Copy the file to /etc/init.d then update the HOMEBASE variable with where you've installed the software too.

Make the script executable :

    chmod 755 starinetlogger

Then from the cmdline you can do /etc/init.d/starinetlogger start / stop

If you want it to run on restarts :

    update-rc.d starinetlogger defaults
    
Usage
=====
    
To use the logger you'll need to either use the latest Starbase-Beta available from http://www.ukraa.com/builds/beta/
by adding the file located in Starbase-Instrument-Files follow the README or by using StarbaseMini located at
http://github.com/mhorn71/StarbaseMini.

Using StarinetPythonLogger2 with StarbaseMini.  Please note StarbaseMini has a number of limitations compared to Starbase
so a minor amount of manual configuration is required if using the chart publisher.  

To set up the FTP chart publisher do the following if using StarbaseMini, note Starbase-Beta can set all parameters 
though the UI:

    1. Make a backup of StarinetBeagleLogger.conf before editing. 
    
    2. Edit the StarinetBeagleLogger.conf and update the following sections please note leave a space after the = sign
       and enclose string in quotes do not include comments as they will be lost.
    
    
    [publisher]
    server = your.server.com  # Either the domainname or IP address of your server
    username = user@your.server.com  # The username need to log into server
    password = yourpassword  # The password as required
    remotefolder = /  # The remote folder.
    interval = 0005  #  The interval in minutes between uploads must be padded with zeros as shown
    
    [publisherlabels]
    title = Staribus MultiChannel Data  #  The chart time title can be left blank if not needed, e.g. title = 
    channel0 = channel0  # The channel label these must be present. 
    channel1 = channel1
    channel2 = channel2
    channel3 = channel3
    channel4 = channel4
    channel5 = channel5
    
    [publisherartist]
    chart = combined  # either 'combined' all plots overlaying one another or 'stacked' each plot on its own one above the other.
    channelArt0 = true  # 'true' or 'false' to show channel in figure channel 0 is temperature.
    channelArt1 = true
    channelArt2 = true
    channelArt3 = true
    channelArt4 = true
    channelArt5 = true
    channelArt6 = true
    autoscale = false #  Autoscale Y axis or leave with preset 0 - 1800