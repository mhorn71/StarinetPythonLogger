__author__ = 'mark'
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


import crcmod
import logging
import sys


## Set crc16 parameters to polynomial 8408, initial value 0xffff, reversed True, Final XOR value 0x00
crc16 = crcmod.mkCrcFun(0x018408, 0xFFFF, True, 0x0000)

## initialise logger
logger = logging.getLogger('utilities.staribuscCrc')


def checkcrc(buffer0):

    logger.debug("Check crc was called.")

    buffer0 = buffer0.encode('utf-8')

    rxcrc = buffer0[-4:]  # assign the received crc to rxcrc

    logger.debug("%s %s", "Received data crc - ", rxcrc)

    newrxcrc = str(hex(crc16(buffer0[:-4])).replace('x', '')[1:].zfill(4)).upper()  # new crc

    newrxcrc = newrxcrc.encode('utf-8')

    logger.debug("%s %s", "Calculated new crc based on received data -", newrxcrc)

    #### Check old and new crc's match if they don't return string with 0200 crc error
    if newrxcrc != rxcrc:
        logger.debug("%s %s %s %s", "Received crc - ", rxcrc, "does not match our generated crc - ", newrxcrc)
        return '0200'
    else:
        logger.debug("CRC' match")
        return '0'


def newcrc(buffer0):

    logger.debug("New crc was called.")

    buffer0 = buffer0.encode('UTF-8')

    datacrc = str(hex(crc16(buffer0)).replace('x', '')[1:].zfill(4)).upper()
    value = datacrc
    logger.debug("%s %s", "Calculated new message crc -", datacrc)

    return value


if __name__ == "__main__":
    print(newcrc(str(sys.argv[1:])))
