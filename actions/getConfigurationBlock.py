import utilities.samplerstatus as samplerstatus
import ConfigParser
import logging
import re

##initialise logger
logger = logging.getLogger('actions.getConfigurationBlock')

config = ConfigParser.RawConfigParser()
config.read("StarinetBeagleLogger.conf")


def control(buffer0, buffer1, buffer2):

    logger.debug("%s %s %s %s", "getConfigurationBlock called ", buffer0, buffer1, buffer2)

    value = None
    status = None


    if re.match('0', buffer0):
        logger.debug("Matched module 0")
        try:
            f = open(config.get("paths", "module0folder") + buffer1, 'r')
            logger.debug("%s %s", "opening file ", f)
            value = f.read().strip('\x02\x1F\x03\x04\r\n')
            f.close()
        except IOError as e:
            status = 8
            value = None
            logger.critical("%s %s", "Unable to locate module 0 block ", e)
        else:
            status = 0
    elif re.match('1', buffer0):
        logger.debug("Matched module 1")
        try:
            f = open(config.get("paths", "module1folder") + buffer1, 'r')
            logger.debug("%s %s", "opening file ", f)
            value = f.read().strip('\x02\x1F\x03\x04\r\n')
            f.close()
        except IOError as e:
            status = 8
            value = None
            logger.critical("%s %s", "Unable to locate module 1 block ", e)
        else:
            status = 0
    else:
        logger.critical("invalid module")
        status = 40

    logger.debug("%s %s %s", "getConfigurationBlock returned ", status, value)

    status = status + samplerstatus.status()

    return status, value
