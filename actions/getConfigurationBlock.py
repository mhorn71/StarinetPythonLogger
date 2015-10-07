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
import re

##initialise logger
logger = logging.getLogger('actions.getConfigurationBlock')

config = configparser.RawConfigParser()
config.read("StarinetBeagleLogger.conf")


def control(buffer0, buffer1, buffer2):

    logger.debug("%s %s %s %s", "getConfigurationBlock called ", buffer0, buffer1, buffer2)

    value = None
    status = None

    if re.match('0', buffer0):
        logger.debug("Matched module 0")
        try:
            f = open(config.get("paths", "module0folder") + buffer1, 'r')
            logger.debug("%s %s", "opening file ", f)
            value = f.read().strip('\x02\x1F\x03\x04\r\n')
            f.close()
        except IOError as e:
            status = 8
            value = None
            logger.critical("%s %s", "Unable to locate module 0 block ", e)
        else:
            status = 0
    elif re.match('1', buffer0):
        logger.debug("Matched module 1")
        try:
            f = open(config.get("paths", "module1folder") + buffer1, 'r')
            logger.debug("%s %s", "opening file ", f)
            value = f.read().strip('\x02\x1F\x03\x04\r\n')
            f.close()
        except IOError as e:
            status = 8
            value = None
            logger.critical("%s %s", "Unable to locate module 1 block ", e)
        else:
            status = 0
    else:
        logger.critical("invalid module")
        status = 40

    logger.debug("%s %s %s", "getConfigurationBlock returned ", status, value)

    return status, value
