StarinetPythonLogger
====================

Beaglebone Black Python Starinet four channel data logger for the UKRAA Starbase Observatory


Install Instructions
====================

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

    matplotlib
    ----------
    https://github.com/matplotlib/matplotlib


You will need to attach the below hardware to ADC Channel AIN6

    TMP36 Temperature Sensor
    ------------------------
    https://learn.adafruit.com/measuring-temperature-with-a-beaglebone-black/wiring

Software install

    1.) place all files in there own folder

    2.) create the following folders in the folder you extract the code too.
        run
        memory/data
        memory/module
        memory/module/0
        memory/module/1

    3.) edit the StarinetBeagleLogger.conf file and set the full path of where you want the pid file to live.

    4.) Start as root.

    5.) Download Starbase from ukraa.com/builds/beta and set the IP address of your
        beaglebone in the file StarinetPythonLogger-instrument.xml