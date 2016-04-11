StarinetPython3Logger
=====================

Beaglebone Black Python3 Starinet six channel data logger. 

    Specifications:
    ---------------
    Sample rates 1 - 255 Seconds
    Data blocks 0x0000 - 0x4000 (16384)

Install Instructions from Source
================================

You need to install the following additional python packages.

    The Adafruit BBIO Library 
    -------------------------
    https://learn.adafruit.com/setting-up-io-python-library-on-beaglebone-black/overview

    crcmod
    ------
    https://pypi.python.org/pypi/crcmod/1.7

    You can install the above using apt-get and pip as the root user or using sudo with the following
    commands:

    apt-get install python-pip
    pip install crcmod
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
    root@beaglebone:/home/StarinetPythonLogger2# nohup python3 StarinetPython3Logger.py &

Binary Setup
============

To use the binary available under releases you'll need to do the following. 

Copy the binary to /opt and start main as root :

    sudo ./StarinetPython3Logger

Alternatively you can use the very basic init script located in goodies called starinetlogger

Copy the file to /etc/init.d then update the HOMEBASE variable with where you've installed the software too.

Make the script executable :

    chmod 755 starinetlogger

Then from the cmdline you can do /etc/init.d/starinetlogger start / stop

If you want it to start on powering up the device :

    update-rc.d starinetlogger defaults
    
Below is a full example of the software being installed in the BBB :

    Example Setup    
    -------------
    Note anywhere you see ——  at the start of a line its a comment.  You can just cut and past the lines I use minus debian@beaglebone:~$

    —— First off login to the BBB from the command line on your mac you must have the BBB connected to your local area network.
    
    Marks-MacBook-Pro:~ mark$ ssh debian@192.168.1.13
    Debian GNU/Linux 7
    
    BeagleBoard.org BeagleBone Debian Image 2014-04-23
    
    Support/FAQ: http://elinux.org/Beagleboard:BeagleBoneBlack_Debian
    debian@192.168.1.13's password: 
    Last login: Fri Apr  8 12:19:41 2016 from 192.168.1.30
    
    —— Next using wget download the precompiled binary from github.
    
    debian@beaglebone:~$ wget https://github.com/mhorn71/StarinetPythonLogger/releases/download/v5.0.6-Production/StarinetPythonLogger_Ver_5_0_6_linux-armv7l.tar.gz
    
    --2016-04-08 12:23:33--  https://github.com/mhorn71/StarinetPythonLogger/releases/download/v5.0.6-Production/StarinetPythonLogger_Ver_5_0_6_linux-armv7l.tar.gz
    Resolving github.com (github.com)... 192.30.252.129
    Connecting to github.com (github.com)|192.30.252.129|:443... connected.
    
    —— TRUNCATED OUTPUT ———
    
    HTTP request sent, awaiting response... 200 OK
    Length: 2250966 (2.1M) [application/octet-stream]
    Saving to: `StarinetPythonLogger_Ver_5_0_6_linux-armv7l.tar.gz'

    100%[=============================================================================================================================>] 2,250,966   1.64M/s   in 1.3s    
    
    2016-04-08 12:23:42 (1.64 MB/s) - `StarinetPythonLogger_Ver_5_0_6_linux-armv7l.tar.gz' saved [2250966/2250966]
    
    ——  Next uncompress and open the tar file and move it to /opt and then change directory to the goodies subfolder.
    
    debian@beaglebone:~$ gzip -d StarinetPythonLogger_Ver_5_0_6_linux-armv7l.tar.gz 
    
    debian@beaglebone:~$ tar -xf StarinetPythonLogger_Ver_5_0_6_linux-armv7l.tar 
    
    debian@beaglebone:~$ sudo mv StarinetPythonLogger_Ver_5_0_6_linux-armv7l /opt/
    
    debian@beaglebone:~$ cd /opt/StarinetPythonLogger_Ver_5_0_6_linux-armv7l/goodies/
    
    —— You need to edit the HOMEBASE line in starinetlogger and correct the path name from
    
    —— HOMEBASE=/opt/StarinetPythonLogger_Ver_5_0_4_linux-armv7l
    
    —— to the name of the release version you're using.
    
    —— HOMEBASE=/opt/StarinetPythonLogger_Ver_5_0_6_linux-armv7l
    
    —— I use vi here but use whatever editor you’re used to.
    
    debian@beaglebone:/opt/StarinetPythonLogger_Ver_5_0_6_linux-armv7l/goodies$ sudo vi starinetlogger 

    —— Now copy the file to /etc/init.d and make it executable and enable the software to start on boot up.
    
    debian@beaglebone:/opt/StarinetPythonLogger_Ver_5_0_6_linux-armv7l/goodies$ sudo cp starinetlogger /etc/init.d/
    
    debian@beaglebone:/opt/StarinetPythonLogger_Ver_5_0_6_linux-armv7l/goodies$ sudo chmod +x /etc/init.d/starinetlogger
    
    debian@beaglebone:/opt/StarinetPythonLogger_Ver_5_0_6_linux-armv7l/goodies$ sudo update-rc.d starinetlogger defaults
    perl: warning: Setting locale failed.
    perl: warning: Please check that your locale settings:
        LANGUAGE = (unset),
        LC_ALL = (unset),
        LANG = "en_GB.UTF-8"
        are supported and installed on your system.
    perl: warning: Falling back to the standard locale ("C").
    update-rc.d: using dependency based boot sequencing
    insserv: warning: script 'starinetlogger' missing LSB tags and overrides
    
    —— You can ignore the warnings. ;-)  Now you can manually start the service. 
    
    debian@beaglebone:/opt/StarinetPythonLogger_Ver_5_0_6_linux-armv7l/goodies$ sudo service starinetlogger start
    Starting Starinet Logger
    
    —— You can now exit and setup StarbaseMini :-)  
    
Usage
=====
    
To use the logger you'll need to either use  StarbaseMini located at http://github.com/mhorn71/StarbaseMini.