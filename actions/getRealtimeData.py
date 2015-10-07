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


import logging
import analogue.readadc as readadc
import actions.getTemperature as getTemperature

##initialise logger
logger = logging.getLogger('actions.getRealtimeData')


def control():

    logger.debug("getRealtimeData called")

    try:
        samplerresponse = readadc.read()
        logger.info("getRealTimeData sampleresponse = " + str(samplerresponse))
        temp = getTemperature.control()
    except IOError as e:
        status = 4
        value = e
        logger.critical("%s %s", "Unable to get temperature", e)
    else:
        status = 0
        value = temp[1] + '\x1E' + samplerresponse[0] + '\x1E' + samplerresponse[1] + '\x1E' + samplerresponse[2] + \
            '\x1E' + samplerresponse[3] + '\x1E' + samplerresponse[4] + '\x1E' + samplerresponse[5]
        logger.debug("%s %s", "getRealtimeData returned value ", value)

    return status, value
