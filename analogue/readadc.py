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
import logging


## initialise logger
logger = logging.getLogger('analogue')

try:
    ADC.setup()
except Exception as e:
    logger.critical('Adc failed - did you start as root?' + str(e))

try:
    ADC.read("P9_40")
except Exception as e:
    logger.critical('failed to read adc - did you start as root?' + str(e))


def read():

    _reading = None

    try:
        x0 = ADC.read("AIN0")
        x0 = ADC.read("AIN0")
        x1 = ADC.read("AIN1")
        x1 = ADC.read("AIN1")
        x2 = ADC.read("AIN2")
        x2 = ADC.read("AIN2")
        x3 = ADC.read("AIN3")
        x3 = ADC.read("AIN3")
        x4 = ADC.read("AIN4")
        x4 = ADC.read("AIN4")
        x5 = ADC.read("AIN5")
        x5 = ADC.read("AIN5")

        b0 = int(x0 * 1800)
        b1 = int(x1 * 1800)
        b2 = int(x2 * 1800)
        b3 = int(x3 * 1800)
        b4 = int(x4 * 1800)
        b5 = int(x5 * 1800)

        r0 = "{0:04d}".format(b0)
        r1 = "{0:04d}".format(b1)
        r2 = "{0:04d}".format(b2)
        r3 = "{0:04d}".format(b3)
        r4 = "{0:04d}".format(b4)
        r5 = "{0:04d}".format(b5)

    except IOError:
        _reading = '0000', '0000', '0000', '0000', '0000', '0000'
        logger.debug("%s %s", "adc IO Error ", e)
    except RuntimeError:
        _reading = '0000', '0000', '0000', '0000', '0000', '0000'
        logger.debug("%s %s", "adc RuntimeError ", e)
    else:
        _reading = r0, r1, r2, r3, r4, r5
        logger.debug('ADC Reading was : ' + str(repr(_reading)))

    return _reading


def read_string():
    data_list = ''.join(read())
    return data_list

if __name__ == "__main__":
    print(read())

