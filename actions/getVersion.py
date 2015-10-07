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
logger = logging.getLogger('actions.getVersion')

config = configparser.RawConfigParser()


def control():

    logger.debug("getVersion called")

    try:
        config.read("StarinetBeagleLogger.conf")
        value = config.get("version", "version")
    except configparser.Error as e:
        status = 4
        value = e
        logger.critical("%s %s", "Unable to get version from config", e)
    else:
        status = 0
        logger.debug("%s %s", "getVersion returned ", value)

    return status, value
