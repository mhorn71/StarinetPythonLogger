# StarinetPython3Logger a data logger for the Beaglebone Black.
# Copyright (C) 2015  Mark Horn
#
# This file is part of StarinetPython3Logger.
#
# StarinetPython3Logger is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 2 of the License, or (at your option) any
# later version.
#
# StarinetPython3Logger is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with StarinetPython3Logger.  If not, see <http://www.gnu.org/licenses/>.


import configparser
import logging
import Adafruit_BBIO.ADC as ADC
import re

try:
    ADC.setup()
except Exception as e:
    print('Adc failed - did you start as root?' + str(e))
    pass

try:
    ADC.read("P9_40")
except Exception as e:
    print('failed to read adc - did you start as root?' + str(e))
    pass


##initialise logger
logger = logging.getLogger('actions.getTemperature')

config = configparser.RawConfigParser()
config.read("StarinetBeagleLogger.conf")


def control():

    logger.debug("getTemperature called")

    try:
        x1 = ADC.read("AIN6")
        x0 = ADC.read("AIN6")
        logger.debug("%s %s", "AIN6 Raw reading ", x0)
        b0 = x0 * 1800
        logger.debug("%s %s", "Raw reading converted to mV ", b0)
        pretemp = (b0 - 500) / 10
        logger.debug("%s %s", "mv converted to C ((b0 - 500) / 10) ", pretemp)

        # We always want to return the following format +/-00.0
        if re.match("^\d$", str(pretemp)):  # matched 0 - 9
            temp = '+' + str(pretemp).zfill(2) + '.' + '0'
        elif re.match("^\d\.\d*$", str(pretemp)):
            a = str(pretemp).split('.')
            b = a[0].zfill(2)
            temp = '+' + b + '.' + a[1][:1]
        elif re.match("^\d{2}$", str(pretemp)):
            temp = '+' + str(pretemp) + '.0'
        elif re.match("^\d{2}\.\d*$", str(pretemp)):
            temp = '+' + str(pretemp)[:4]
        elif re.match("^-\d$", str(pretemp)):
            a = str(pretemp).replace('-', '')
            temp = '-' + str(a).zfill(2) + '.0'
        elif re.match("^-\d{1,2}\.\d*$", str(pretemp)):
            # matched -1.8888
            a = str(pretemp).replace('-', '')
            b = str(a).split('.')
            c = b[0].zfill(2)
            temp = '-' + c + '.' + b[1][:1]
        elif re.match("-\d{2}\.\d*$", str(pretemp)):
            temp = str(pretemp)[:5]
        else:
            temp = '+00.0'

        value = temp

        logger.debug("%s %s", "getTemperature returned value ", value)
    except IOError as e:
        logger.critical("%s %s", "premature termination", e)
        status = 4
        value = e
        logger.critical("%s %s", "getTemperature premature termination", e)
    else:
        status = 0

    status = status

    return status, value

