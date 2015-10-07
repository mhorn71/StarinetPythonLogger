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
import os

##initialise logger
logger = logging.getLogger('actions.getConfigurationBlockCount')

config = configparser.RawConfigParser()
config.read("StarinetBeagleLogger.conf")


def control(buffer0):

    logger.debug("getConfigurationBlockCount called")

    if re.match('0', buffer0):
        logger.debug("%s %s", "Matched module 0 ", buffer0)
        try:
            lastblock = int(max(os.listdir(config.get("paths", "module0folder")),
                                key=lambda p: os.path.getctime(os.path.join(
                                    config.get("paths", "module0folder"), p))), 16) + 1
            logger.debug("%s %s", "last block appears to be ", lastblock)
            value = hex(lastblock).split('x')[1].upper().zfill(4)
            logger.debug("%s %s", "last block value converted to hex ", value)
        except IOError as e:
            status = 8
            value = None
            logger.critical("%s %s", "Unable to locate module 0 ", e)
        except ValueError:
            status = 8
            value = None
        except OSError as e:
            status = 2
            value = e
            logger.critical("%s %s", "Unable to open datafolder", e)
        else:
            status = 0
    elif re.match('1', buffer0):
        logger.debug("%s %s", "Matched module 1 ", buffer0)
        try:
            lastblock = int(max(os.listdir(config.get("paths", "module1folder")),
                                key=lambda p: os.path.getctime(os.path.join(
                                    config.get("paths", "module1folder"), p))), 16) + 1
            logger.debug("%s %s", "last block appears to be ", lastblock)
            value = hex(lastblock).split('x')[1].upper().zfill(4)
            logger.debug("%s %s", "last block value converted to hex ", value)
        except ValueError:
            status = 8
            value = None
        except Exception as e:
            status = 8
            value = None
            logger.critical("%s %s", "Unable to locate module 1 ", e)
        except OSError as e:
            status = 0
            value = '0000'
            logger.critical("%s %s", "Unable to open datafolder", e)
        else:
            status = 0
    else:
        logger.critical("%s %s", "Invalid module - ", buffer0)
        status = 40
        value = None

    logger.debug("%s %s %s", "getConfigurationBlockCount returned ", status, value)

    return status, value

