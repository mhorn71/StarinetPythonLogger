StarinetPythonLogger
====================

Beaglebone Black Python Starinet data logger for the UKRAA Starbase Observatory 


Install Instructions
====================

You need to install the following two additional python packages.

    The Adafruit BBIO Library 
    -------------------------
    https://learn.adafruit.com/setting-up-io-python-library-on-beaglebone-black/overview

    crcmod
    ------
    https://pypi.python.org/pypi/crcmod/1.7



1.) place all files in there own folder

2.) edit the StarinetBeagleLogger.conf file and set the full path of where you want the pid file to live. 

3.) Start as root.

4.) Download Starbase from ukraa.com/builds/beta and set the IP address of your 
    beaglebone in the file BeagleStarinetLogger-instrument.xml  