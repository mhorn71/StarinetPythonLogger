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


import os
import configparser
import logging

##initialise logger
logger = logging.getLogger('actions.capture')

config = configparser.RawConfigParser()
config.read("StarinetBeagleLogger.conf")


def control():

    logger.debug("getDataBlockCount called")

    value = None

    try:
        lastblock = int(max(os.listdir(config.get("paths", "datafolder")),
                            key=lambda p: os.path.getctime(os.path.join(
                            config.get("paths", "datafolder"), p))), 16) + 1

        value = hex(lastblock).split('x')[1].upper().zfill(4)
    except Exception as e:
        status = 0
        value = '0000'
    except OSError as e:
        status = 0
        value = '0000'
        logger.critical("%s %s", "Unable to open datafolder", e)
    else:
        status = 0

    return status, value
