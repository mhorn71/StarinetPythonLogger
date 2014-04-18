import re
import struct
import logging
import utilities.staribuscrc as staribuscrc
import ConfigParser
import actions.capture as capture
import actions.ping as ping
import actions.getDataBlockCount as getDataBlockCount
import actions.getDataBlock as getDataBlock
import actions.getRate as getRate
import actions.getSpace as getSpace
import actions.getStatus as getStatus
import actions.getRealtimeData as getRealtimeData
import actions.getTemperature as getTemperature
import actions.getA2D as getA2D
import actions.getClockTime as getClockTime
import actions.getClockDate as getClockDate
import actions.getHostname as getHostname
import actions.getVersion as getVersion
import actions.getMACAddress as getMACAddress
import actions.setRate as setRate
import actions.setConfigurationBlock as setConfigurationBlock
import actions.getConfigurationBlock as getConfigurationBlock
import actions.getConfigurationBlockCount as getConfigurationBlockCount
import utilities.samplerstatus as samplerstatus

## initialise logger
logger = logging.getLogger('interpreter')

##initialise config parser
config = ConfigParser.RawConfigParser()
config.read("StarinetBeagleLogger.conf")

x = None
response_status = None
response_command = None
response_crc = None
#response_value = None


def processor(buffer0):

    global response_status
    global response_command
    global response_crc
    response_value = None

    logger.debug("Interpreter was called.")

    if re.match("^\x02*[0-9a-zA-Z]{14}\x04*", buffer0):   # Matched Command with no parameters

        logger.debug("Matched command with no parameters")
        logger.debug("%s %s", "Current current response_command - ", response_command)
        logger.debug("%s %s", "Current current response_status - ", response_status)
        logger.debug("%s %s", "Current current response_value - ", response_value)
        logger.debug("%s %s", "Current current response_crc - ", response_crc)

        try:
            data = buffer0.strip('\x02\x1F\x04\r\n')
            logger.debug("%s %s", "Stripped control chars from packet ", repr(data))
        except Exception as e:
            logger.debug("%s %s", "Unable to strip ctl chars from packet ", e)
        else:
            try:
                address, command, crc = struct.unpack('<2s8s4s', data)
                logger.debug("%s %s %s %s", "Unpacked Staribus command", address, command, crc)
            except struct.error as e:
                logger.debug("%s %s", "Can not unpack command ", e)
            else:
                if int(staribuscrc.checkcrc(buffer0)) == 0200:
                    logger.debug("Packet failed crc check")
                    x = 200, None
                else:
                    if int(address) != int(config.get("instaddr", "iaddr")):  # Check Instrument Address Is Correct
                        logger.debug("Instrument address does not match our address")
                        x = 80, None
                    else:
                        ########## Core Module #################
                        if re.match('00010000', command):  # ping
                            x = ping.ping()
                        elif re.match('000A0000', command):  # getVersion
                            x = getVersion.control()
                        elif re.match('000D0000', command):  # getMACAddress
                            x = getMACAddress.control()
                        elif re.match('000E0000', command):  # getStatus
                            x = getStatus.control(response_command, response_status, response_crc)
                        ############ Utilities Module ############
                        elif re.match('01010000', command):  # getTemperature
                            x = getTemperature.control()
                        elif re.match('010D0000', command):  # getClockDate
                            x = getClockDate.control()
                        elif re.match('01070000', command):  # getHostname
                            x = getHostname.control()
                        elif re.match('010E0000', command):  # getClockTime
                            x = getClockTime.control()
                        ############# Data Capture Module ############
                        elif re.match('03000000', command):  # getSpace
                            x = getSpace.control()
                        elif re.match('03040000', command):  # getRate return capture interval
                            x = getRate.control()
                        elif re.match('03020000', command):  # getDataBlockCount
                            x = getDataBlockCount.control()
                        ############ Logger Plugin ############
                        elif re.match('04000000', command):  # getRealTimeData
                            x = getRealtimeData.control()
                        else:
                            x = 20, None 

    elif re.match("^\x02*[0-9a-zA-Z]{10}\x1F*(([0-9a-zA-Z]*)(\x1F)*)*\x04*", buffer0):  # Matched Cmd with parameters

        logger.debug("Matched command with parameters")

        try:
            data = buffer0.strip('\x02\x1F\x03\x04\r\n').split('\x1F')  # Strip off ctrl characters and split on <us>
            logger.debug("%s %s", "Stripped control chars from packet", repr(data))
        except Exception as e:
            logger.debug("%s %s", "Unable to strip ctl chars from packet ", e)
        else:
            try:
                address, command = struct.unpack('<2s8s', data[0])  # Unpack command
                logger.debug("%s %s %s", "Unpacked Staribus command", address, command)
            except struct.error as e:
                logger.debug("%s %s", "Can not unpack command ", e)
            else:
                if int(staribuscrc.checkcrc(buffer0)) == 0200:  # check crc
                    logger.debug("Packet failed crc check")
                    x = 200, None
                else:
                    if int(address) != int(config.get("instaddr", "iaddr")):  # Check Staribus Inst Address Is Correct
                        logger.debug("Packet instrument address does not match our address")
                        x = 80, None
                    else:
                        ############ Core Module ############
                        if re.match('00050000', command):  # getConfigurationBlockCount
                            x = getConfigurationBlockCount.control(data[1])
                        elif re.match('00060000', command):  # getConfigurationBlock
                            x = getConfigurationBlock.control(data[1], data[2], data[3])
                        elif re.match('00070000', command):  # setConfigurationBlock
                            x = setConfigurationBlock.control(data[1], data[2], data[3])
                        ############ Analogue Module #############
                        elif re.match('02000000', command):  # getA2D
                            x = getA2D.control(data[1])
                        ############### DataCapture Module ############
                        elif re.match('03030000', command):  # getDataBlock
                            x = getDataBlock.control(data[1])
                        elif re.match('03050000', command):  # setRate set capture interval
                            x = setRate.control(data[1])
                        elif re.match('03060000', command):  # capture
                            x = capture.control(data[1])
                        else:
                            x = 20, None 

    if (x[0] is not None) and (x[1] is not None):
        response_status = str(x[0]).zfill(4)
        response_value = str(x[1])
        response_command = str(address) + str(command)
        joinvalue = response_command + str(response_status) + '\x1F' + str(response_value) + '\x1F'
        response_crc = str(staribuscrc.newcrc(joinvalue))
        value = '\x02' + joinvalue + response_crc + '\x04\r\n'
        logger.debug("%s %s", "Created Return Message -", repr(value))
    elif (x[0] is not None) and (x[1] is None):
        response_status = str(x[0]).zfill(4)
        response_command = str(address) + str(command)
        response_value = None
        joinvalue = response_command + str(response_status)
        response_crc = str(staribuscrc.newcrc(joinvalue))
        value = '\x02' + joinvalue + response_crc + '\x04\r\n'
        logger.debug("%s %s", "Created Return Message -", repr(value))
    else:
        status = 4 + samplerstatus.status()
        response_status = str(status).zfill(4)
        response_command = str(address) + str(command)
        response_value = None
        joinvalue = response_command + str(response_status)
        response_crc = str(staribuscrc.newcrc(joinvalue))
        value = '\x02' + joinvalue + response_crc + '\x04\r\n'
        logger.debug("%s %s", "Created Return Message -", repr(value))

    return value




