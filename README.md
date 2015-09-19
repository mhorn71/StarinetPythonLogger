StarinetPython3Logger
====================

Currently in development.

Beaglebone Black Python3 Starinet six channel data logger for the UKRAA Starbase Observatory


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

    You can install the above using apt-get and pip as the root user or using sudo with the following
    commands:

    apt-get install python-pip
    pip install crcmod
    pip install python-matplotlib
    pip install psutil
    pip install Adafruit_BBIO



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

    3.) Start as root.

    4.) Use with StarbaseMini available at the same github account this software.