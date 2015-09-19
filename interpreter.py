import re
import struct
import logging
import utilities.staribuscrc as staribuscrc
import configparser
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
import actions.capturePublisher as capturePublisher
import actions.setPublisher as setPublisher
import actions.getPublisher as getPublisher
import actions.setPublisherLabels as setPublisherLabels
import actions.getPublisherLabels as getPublisherLabels
import actions.setPublisherArtist as setPublisherArtist
import actions.getPublisherArtist as getPublisherArtist
import actions.getConfigurationBlockCount as getConfigurationBlockCount
import utilities.samplerstatus as samplerstatus

## initialise logger
logger = logging.getLogger('interpreter')

##initialise config parser
config = configparser.RawConfigParser()
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

    if re.match("^[0-9a-zA-Z]{14}$", buffer0):   # Matched Command with no parameters

        logger.debug("Matched command with no parameters")
        logger.debug("%s %s", "Current current response_command - ", response_command)
        logger.debug("%s %s", "Current current response_status - ", response_status)
        logger.debug("%s %s", "Current current response_value - ", response_value)
        logger.debug("%s %s", "Current current response_crc - ", response_crc)

        try:
            data = buffer0
            logger.debug("%s %s", "Stripped control chars from packet ", repr(data))
        except Exception as e:
            logger.debug("%s %s", "Unable to strip ctl chars from packet ", e)
        else:
            try:
                address, command, crc = struct.unpack('<2s8s4s', data.encode('utf-8'))
                command = command.decode('utf-8')
                address = address.decode('utf-8')
                logger.debug("%s %s %s %s", "Unpacked Staribus command", address, command, crc)
            except struct.error as e:
                logger.debug("%s %s", "Can not unpack command ", e)
            else:
                if int(staribuscrc.checkcrc(buffer0)) == 200:
                    logger.debug("Packet failed crc check")
                    x = 200, None
                else:
                    if int(address) != int(config.get("instaddr", "iaddr")):  # Check Instrument Address Is Correct
                        logger.debug("Instrument address does not match our address")
                        x = 80, None
                    else:
                        ########## Core Module #################
                        if re.match('00010000', command):  # ping
                            logger.debug("Matched command ping")
                            x = ping.ping()
                        elif re.match('000A0000', command):  # getVersion
                            logger.debug("Matched command getVersion")
                            x = getVersion.control()
                        elif re.match('000D0000', command):  # getMACAddress
                            logger.debug("Matched command getMACAddress")
                            x = getMACAddress.control()
                        elif re.match('000E0000', command):  # getStatus
                            logger.debug("Matched command getStatus")
                            x = getStatus.control(response_command, response_status, response_crc)
                        ############ Utilities Module ############
                        elif re.match('01010000', command):  # getTemperature
                            logger.debug("Matched command getTemperature")
                            x = getTemperature.control()
                        elif re.match('010D0000', command):  # getClockDate
                            logger.debug("Matched command getClockDate")
                            x = getClockDate.control()
                        elif re.match('01070000', command):  # getHostname
                            logger.debug("Matched command getHostname")
                            x = getHostname.control()
                        elif re.match('010E0000', command):  # getClockTime
                            logger.debug("Matched command getClockTime")
                            x = getClockTime.control()
                        ############# Data Capture Module ############
                        elif re.match('03000000', command):  # getSpace
                            logger.debug("Matched command getSpace")
                            x = getSpace.control()
                        elif re.match('03040000', command):  # getRate return capture interval
                            logger.debug("Matched command getRate")
                            x = getRate.control()
                        elif re.match('03020000', command):  # getDataBlockCount
                            logger.debug("Matched command getDataBlockCount")
                            x = getDataBlockCount.control()
                        ############# Publisher Module ###############
                        elif re.match('05040000', command):  # getPublisherLabels
                            logger.debug("Matched command getPublisherLabels")
                            x = getPublisherLabels.control()
                        elif re.match('05030000', command):  # getPublisher
                            logger.debug("Matched command getPublisher")
                            x = getPublisher.control()
                        elif re.match('05060000', command): # getPublisherArtist
                            x = getPublisherArtist.control()
                        ############ Logger Plugin ############
                        elif re.match('04000000', command):  # getRealTimeData
                            logger.debug("Matched command getRealTimeData")
                            x = getRealtimeData.control()
                        else:
                            logger.debug("Matched command - NO MATCH")
                            x = 20, None 

    elif re.match("^[0-9a-zA-Z]{10}\x1F*(([0-9a-zA-Z]*)(\x1F)*)*", buffer0):  # Matched Cmd with parameters

        logger.debug("Matched command with parameters")
        logger.debug("%s %s", "Current current response_command - ", response_command)
        logger.debug("%s %s", "Current current response_status - ", response_status)
        logger.debug("%s %s", "Current current response_value - ", response_value)
        logger.debug("%s %s", "Current current response_crc - ", response_crc)

        try:
            data = buffer0.split('\x1F')  # Strip off ctrl characters and split on <us>
            logger.debug("%s %s", "Stripped control chars from packet", repr(data))
        except Exception as e:
            logger.debug("%s %s", "Unable to strip ctl chars from packet ", e)
        else:
            try:
                address, command = struct.unpack('<2s8s', data[0].encode('utf-8'))  # Unpack command
                command = command.decode('utf-8')
                address = address.decode('utf-8')
                logger.debug("%s %s %s", "Unpacked Staribus command", address, command)
            except struct.error as e:
                logger.debug("%s %s", "Can not unpack command ", e)
            else:
                if int(staribuscrc.checkcrc(buffer0)) == 200:  # check crc
                    logger.debug("Packet failed crc check")
                    x = 200, None
                else:
                    if int(address) != int(config.get("instaddr", "iaddr")):  # Check Staribus Inst Address Is Correct
                        logger.debug("Packet instrument address does not match our address")
                        x = 80, None
                    else:
                        ############ Core Module ############
                        if re.match('00050000', command):  # getConfigurationBlockCount
                            logger.debug("Matched command getConfigurationBlockCount")
                            x = getConfigurationBlockCount.control(data[1])
                        elif re.match('00060000', command):  # getConfigurationBlock
                            logger.debug("Matched command getConfigurationBlock")
                            x = getConfigurationBlock.control(data[1], data[2], data[3])
                        elif re.match('00070000', command):  # setConfigurationBlock
                            logger.debug("Matched command setConfigurationBlock")
                            x = setConfigurationBlock.control(data[1], data[2], data[3])
                        ############ Publisher Module ############
                        elif re.match('05050000', command):  # setPublisherLabels
                            logger.debug("Matched command setPublisherLabels")
                            x = setPublisherLabels.control(data[1], data[2], data[3], data[4])
                        elif re.match('05070000', command):  # setPublisherArtist
                            logger.debug("Matched command setPublisherArtist")
                            x = setPublisherArtist.control(data[1], data[2], data[3], data[4], data[5], data[6], data[7])
                        elif re.match('05010000', command):  # publisher
                            logger.debug("Matched command publisher")
                            x = capturePublisher.control(data[1])
                        elif re.match('05020000', command):  # setPublisher
                            logger.debug("Matched command setPublisher")
                            x = setPublisher.control(data[1], data[2], data[3], data[4], data[5], data[6])
                        ############ Analogue Module #############
                        elif re.match('02000000', command):  # getA2D
                            logger.debug("Matched command getA2D")
                            x = getA2D.control(data[1])
                        ############### DataCapture Module ############
                        elif re.match('03030000', command):  # getDataBlock
                            logger.debug("Matched command getDataBlock")
                            x = getDataBlock.control(data[1])
                        elif re.match('03050000', command):  # setRate set capture interval
                            logger.debug("Matched command setRate")
                            x = setRate.control(data[1])
                        elif re.match('03060000', command):  # capture
                            logger.debug("Matched command capture")
                            x = capture.control(data[1])
                        else:
                            logger.debug("Matched command - NO MATCH")
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




