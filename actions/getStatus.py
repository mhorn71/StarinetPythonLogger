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
logger = logging.getLogger('actions.getStatus')

config = configparser.RawConfigParser()
config.read("StarinetBeagleLogger.conf")


def control(buffer0, buffer1, buffer2):  # buffer0 = reponse_command, buffer1 = response_status, buffer2 = response_crc

    logger.debug("%s %s %s %s", "getStatus called", buffer0, buffer1, buffer2)

    #status_code = {'0000': 'SUCCESS',
    #               '0001': 'TIMEOUT',
    #               '0002': 'ABORT',
    #               '0004': 'PREMATURE_TERMINATION',
    #               '0008': 'INVALID_PARAMETER',
    #               '0010': 'INVALID_MESSAGE',
    #               '0020': 'INVALID_COMMAND',
    #               '0040': 'INVALID_MODULE',
    #               '0080': 'INVALID_INSTRUMENT',
    #               '0200': 'CRC_ERROR',
    #               '0400': 'INVALID_XML',
    #               '8000': 'CAPTURE_ACTIVE'}

    if buffer0 is not None:
        basecommand = buffer0[2:]
        command = basecommand[:4]
        commandvariant = basecommand[4:]
        #print "getStatus buffer 0 stripped of address ", basecommand 
        #print "getStatus basecommand stripped of command variant ", command 
        #print "getStatus basecommand stripped of code base and command ", commandVariant 
        #print "getStatus response status of last command ", buffer1
        #print "getStatus response crc of last command ", buffer2 
        value = command + ' ' + commandvariant + ' ' + buffer1 + ' ' + buffer2
    else:
        value = '0000 0000 0000 0000'

    status = 0
 
    logger.debug("%s %s", "getStatus returned ", value)

    return status, value
