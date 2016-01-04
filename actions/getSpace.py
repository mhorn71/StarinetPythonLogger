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
import os

##initialise logger
logger = logging.getLogger('actions.getSpace')

config = configparser.RawConfigParser()
config.read("StarinetBeagleLogger.conf")


def control(data_array):

    logger.debug("getSpace called")

    if len(data_array) > 0:
        status = 0
        blockcount = len(data_array) + 1

        value = str(int(100 - int(100 * float(blockcount) / 16384))).zfill(3)
        logger.debug("%s %s", "getSpace returned value ", value)
    else:
        try:
            blockcount = int(max(os.listdir(config.get("paths", "datafolder")),
                                 key=lambda p: os.path.getctime(os.path.join(
                                     config.get("paths", "datafolder"), p))), 16) + 1
            value = str(int(100 - int(100 * float(blockcount) / 16384))).zfill(3)
        except configparser.Error as e:
            status = 4
            value = e
            logger.critical("%s %s", "Unable to open datafolder", e)
        except OSError as e:
            status = 4
            value = e
            logger.critical("%s %s", "Unable to open datafolder", e)
        except ValueError:
            value = '000'
            status = 0
        else:
            status = 0
            logger.debug("%s %s", "getSpace returned value ", value)

    return status, value
