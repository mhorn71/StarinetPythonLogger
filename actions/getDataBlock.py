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

##initialise logger
logger = logging.getLogger('actions.getDataBlock')

config = configparser.RawConfigParser()
config.read("StarinetBeagleLogger.conf")


def control(buffer0):

    logger.debug("getDataBlock called")

    value = None

    try:
        f = open(config.get("paths", "datafolder") + str(buffer0), 'r')
        datablock = f.read().strip('\x02\x1F\x04\r\n\x00')
        f.close()
        logger.debug("%s %s", "getting data block ", buffer0)
    except IOError as e:
        status = 8
        logger.critical("%s %s", "unable to open data block", e)
    else:
        status = 0
        value = datablock.ljust(512, '0').strip('\r\n\x00')
        logger.debug("%s %s", "returning data block", buffer0)

    return status, value


