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

    You can install the above using apt-get and pip as the root user or using sudo with the following
    commands:

    apt-get install python-pip
    pip install crcmod
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

If you want it to start on powering up the device :

    update-rc.d starinetlogger defaults
    
Usage
=====
    
To use the logger you'll need to either use the latest Starbase-Beta available from http://www.ukraa.com/builds/beta/
by adding the file located in Starbase-Instrument-Files follow the README or by using StarbaseMini located at
http://github.com/mhorn71/StarbaseMini.