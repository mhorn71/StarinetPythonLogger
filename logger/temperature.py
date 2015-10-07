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


import Adafruit_BBIO.ADC as ADC
import re

try:
    ADC.setup()
except Exception as e:
    print('Adc failed - did you start as root?' + str(e))
    pass

try:
    ADC.read("AIN6")
except Exception as e:
    print('failed to read adc - did you start as root?' + str(e))
    pass


def read():

    try:
        x0 = ADC.read("AIN6")
        x0 = ADC.read("AIN6")
        b0 = x0 * 1800
        pretemp = (b0 - 500) / 10

        if re.match("^\d$", str(pretemp)):  # matched 0 - 9
            temp = '+' + str(pretemp).zfill(3)
        elif re.match("^\d\.\d*$", str(pretemp)):
            a = str(pretemp).split('.')
            b = a[0].zfill(3)
            temp = '+' + str(b)
        elif re.match("^\d{2}$", str(pretemp)):
            temp = '+' + str(pretemp).zfill(3)
        elif re.match("^\d{2}\.\d*$", str(pretemp)):
            a = str(pretemp).split('.')
            b = a[0].zfill(3)
            temp = '+' + str(b)
        elif re.match("^-\d{1,2}$", str(pretemp)):
            a = str(pretemp).replace('-', '')
            temp = '-' + str(a).zfill(3)
        elif re.match("^-\d\.\d*$", str(pretemp)):
            # matched -1.8888
            a = str(pretemp).replace('-', '')
            b = str(a).split('.')
            c = b[0].zfill(3)
            temp = '-' + c
        elif re.match("-\d{2}\.\d*$", str(pretemp)):
            a = str(pretemp).replace('-', '')
            b = str(a).split('.')
            c = b[0].zfill(3)
            temp = '-' + c
        else:
            temp = '+000'

        value = temp

    except IOError:

        value = '+000'

    return value
