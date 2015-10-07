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
logger = logging.getLogger('actions.setConfigurationBlock')

config = configparser.RawConfigParser()
config.read("StarinetBeagleLogger.conf")


def control(buffer0, buffer1, buffer2):

    logger.debug("setConfigurationBlock called")

    if re.match('0', buffer0):
        try:
            f = open(config.get("paths", "module0folder") + buffer1, 'w')
            f.write(buffer2)
            f.close()
        except IOError as e:
            status = 4
            value = e
            logger.critical("%s %s", "SetConfigurationBlock Module 0 IOError", e)
        else:
            status = 0
            value = None
    elif re.match('1', buffer0):
        try:
            f = open(config.get("paths", "module1folder") + buffer1, 'w')
            f.write(buffer2)
            f.close()
        except IOError as e:
            status = 4
            value = e
            logger.critical("%s %s", "SetConfigurationBlock Module 1 IOError ", e)
        else:
            status = 0
            value = None
    else:
        status = 40
        value = None
        logger.critical("setConfigurationBlock unable to locate module or buffer")

    logger.debug("%s %s", "setConfigurationBlock returned ", status)

    return status, value

