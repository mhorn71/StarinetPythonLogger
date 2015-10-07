import re
import struct
import logging
import configparser


import utilities.staribuscrc as staribuscrc
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
import logger.sampler3 as sampler


class Interpreter(object):
    def __init__(self):

        # initialise logger
        self.logger = logging.getLogger('interpreter')

        # initialise config parser
        self.config = configparser.RawConfigParser()
        self.config.read("StarinetBeagleLogger.conf")

        self.x = None
        self.response_status = None
        self.response_crc = None
        self.response_command = None
        self.response_value = None
        self.data_array = []

        self.sampler = sampler.Logger(self.data_array)


    def processor(self, buffer0):

        self.logger.debug("Interpreter was called.")

        if re.match("^[0-9a-zA-Z]{14}$", buffer0):   # Matched Command with no parameters

            self.logger.debug("Matched command with no parameters")
            self.logger.debug("%s %s", "Current current response_command - ", self.response_command)
            self.logger.debug("%s %s", "Current current response_status - ", self.response_status)
            self.logger.debug("%s %s", "Current current response_value - ", self.response_value)
            self.logger.debug("%s %s", "Current current response_crc - ", self.response_crc)

            try:
                data = buffer0
                self.logger.debug("%s %s", "Stripped control chars from packet ", repr(data))
            except Exception as e:
                self.logger.debug("%s %s", "Unable to strip ctl chars from packet ", e)
            else:
                try:
                    address, command, crc = struct.unpack('<2s8s4s', data.encode('utf-8'))
                    command = command.decode('utf-8')
                    address = address.decode('utf-8')
                    self.logger.debug("%s %s %s %s", "Unpacked Staribus command", address, command, crc)
                except struct.error as e:
                    self.logger.debug("%s %s", "Can not unpack command ", e)
                else:
                    if int(staribuscrc.checkcrc(buffer0)) == 200:
                        self.logger.debug("Packet failed crc check")
                        self.x = 200, None
                    else:
                        if int(address) != int(self.config.get("instaddr", "iaddr")):  # Check Instrument Address Is Correct
                            self.logger.debug("Instrument address does not match our address")
                            self.x = 80, None
                        else:
                            ########## Core Module #################
                            if re.match('00010000', command):  # ping
                                self.logger.debug("Matched command ping")
                                self.x = ping.ping()
                            elif re.match('000A0000', command):  # getVersion
                                self.logger.debug("Matched command getVersion")
                                self.x = getVersion.control()
                            elif re.match('000D0000', command):  # getMACAddress
                                self.logger.debug("Matched command getMACAddress")
                                self.x = getMACAddress.control()
                            elif re.match('000E0000', command):  # getStatus
                                self.logger.debug("Matched command getStatus")
                                self.x = getStatus.control(self.response_command, self.response_status,
                                                           self.response_crc)
                            ############ Utilities Module ############
                            elif re.match('01010000', command):  # getTemperature
                                self.logger.debug("Matched command getTemperature")
                                self.x = getTemperature.control()
                            elif re.match('010D0000', command):  # getClockDate
                                self.logger.debug("Matched command getClockDate")
                                self.x = getClockDate.control()
                            elif re.match('01070000', command):  # getHostname
                                self.logger.debug("Matched command getHostname")
                                self.x = getHostname.control()
                            elif re.match('010E0000', command):  # getClockTime
                                self.logger.debug("Matched command getClockTime")
                                self.x = getClockTime.control()
                            ############# Data Capture Module ############
                            elif re.match('03000000', command):  # getSpace
                                self.logger.debug("Matched command getSpace")
                                self.x = getSpace.control()
                            elif re.match('03040000', command):  # getRate return capture interval
                                self.logger.debug("Matched command getRate")
                                self.x = getRate.control()
                            elif re.match('03020000', command):  # getDataBlockCount
                                self.logger.debug("Matched command getDataBlockCount")
                                self.x = getDataBlockCount.control()
                            ############ Logger Plugin ############
                            elif re.match('04000000', command):  # getRealTimeData
                                self.logger.debug("Matched command getRealTimeData")
                                self.x = getRealtimeData.control()
                            else:
                                self.logger.debug("Matched command - NO MATCH")
                                self.x = 20, None

        elif re.match("^[0-9a-zA-Z]{10}\x1F*(([0-9a-zA-Z]*)(\x1F)*)*", buffer0):  # Matched Cmd with parameters

            self.logger.debug("Matched command with parameters")
            self.logger.debug("%s %s", "Current current response_command - ", self.response_command)
            self.logger.debug("%s %s", "Current current response_status - ", self.response_status)
            self.logger.debug("%s %s", "Current current response_value - ", self.response_value)
            self.logger.debug("%s %s", "Current current response_crc - ", self.response_crc)

            try:
                data = buffer0.split('\x1F')  # Strip off ctrl characters and split on <us>
                self.logger.debug("%s %s", "Stripped control chars from packet", repr(data))
            except Exception as e:
                self.logger.debug("%s %s", "Unable to strip ctl chars from packet ", e)
            else:
                try:
                    address, command = struct.unpack('<2s8s', data[0].encode('utf-8'))  # Unpack command
                    command = command.decode('utf-8')
                    address = address.decode('utf-8')
                    self.logger.debug("%s %s %s", "Unpacked Staribus command", address, command)
                except struct.error as e:
                    self.logger.debug("%s %s", "Can not unpack command ", e)
                else:
                    if int(staribuscrc.checkcrc(buffer0)) == 200:  # check crc
                        self.logger.debug("Packet failed crc check")
                        self.x = 200, None
                    else:
                        if int(address) != int(self.config.get("instaddr", "iaddr")):  # Check Staribus Inst Address Is Correct
                            self.logger.debug("Packet instrument address does not match our address")
                            self.x = 80, None
                        else:
                            ############ Core Module ############
                            if re.match('00050000', command):  # getConfigurationBlockCount
                                self.logger.debug("Matched command getConfigurationBlockCount")
                                self.x = getConfigurationBlockCount.control(data[1])
                            elif re.match('00060000', command):  # getConfigurationBlock
                                self.logger.debug("Matched command getConfigurationBlock")
                                self.x = getConfigurationBlock.control(data[1], data[2], data[3])
                            elif re.match('00070000', command):  # setConfigurationBlock
                                self.logger.debug("Matched command setConfigurationBlock")
                                self.x = setConfigurationBlock.control(data[1], data[2], data[3])
                            ############ Analogue Module #############
                            elif re.match('02000000', command):  # getA2D
                                self.logger.debug("Matched command getA2D")
                                self.x = getA2D.control(data[1])
                            ############### DataCapture Module ############
                            elif re.match('03030000', command):  # getDataBlock
                                self.logger.debug("Matched command getDataBlock")
                                self.x = getDataBlock.control(data[1])
                            elif re.match('03050000', command):  # setRate set capture interval
                                self.logger.debug("Matched command setRate")
                                self.x = setRate.control(data[1])
                            elif re.match('03060000', command):  # capture
                                self.logger.debug("Matched command capture")
                                self.x = capture.control(data[1], self.sampler)
                            else:
                                self.logger.debug("Matched command - NO MATCH")
                                self.x = 20, None

        if (self.x[0] is not None) and (self.x[1] is not None):
            status = self.x[0] + self.sampler.status()
            self.response_status = str(status).zfill(4)
            self.response_value = str(self.x[1])
            self.response_command = str(address) + str(command)
            joinvalue = self.response_command + str(self.response_status) + '\x1F' + str(self.response_value) + '\x1F'
            self.response_crc = str(staribuscrc.newcrc(joinvalue))
            value = '\x02' + joinvalue + self.response_crc + '\x04\r\n'
            self.logger.debug("%s %s", "Created Return Message -", repr(value))
        elif (self.x[0] is not None) and (self.x[1] is None):
            status = self.x[0] + self.sampler.status()
            self.response_status = str(status).zfill(4)
            self.response_command = str(address) + str(command)
            self.response_value = None
            joinvalue = self.response_command + str(self.response_status)
            self.response_crc = str(staribuscrc.newcrc(joinvalue))
            value = '\x02' + joinvalue + self.response_crc + '\x04\r\n'
            self.logger.debug("%s %s", "Created Return Message -", repr(value))
        else:
            status = 4 + self.sampler.status()
            self.response_status = str(status).zfill(4)
            self.response_command = str(address) + str(command)
            self.response_value = None
            joinvalue = self.response_command + str(self.response_status)
            self.response_crc = str(staribuscrc.newcrc(joinvalue))
            value = '\x02' + joinvalue + self.response_crc + '\x04\r\n'
            self.logger.debug("%s %s", "Created Return Message -", repr(value))

        return value




