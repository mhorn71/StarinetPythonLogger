import configparser
import logging
import re

##initialise logger
logger = logging.getLogger('actions.setConfigurationBlock')

config = configparser.RawConfigParser()
config.read("StarinetBeagleLogger.conf")


def control(buffer0, buffer1, buffer2):

    logger.debug("setConfigurationBlock called")

    if re.match('0', buffer0):
        try:
            f = open(config.get("paths", "module0folder") + buffer1, 'w')
            f.write(buffer2)
            f.close()
        except IOError as e:
            status = 4
            value = e
            logger.critical("%s %s", "SetConfigurationBlock Module 0 IOError", e)
        else:
            status = 0
            value = None
    elif re.match('1', buffer0):
        try:
            f = open(config.get("paths", "module1folder") + buffer1, 'w')
            f.write(buffer2)
            f.close()
        except IOError as e:
            status = 4
            value = e
            logger.critical("%s %s", "SetConfigurationBlock Module 1 IOError ", e)
        else:
            status = 0
            value = None
    else:
        status = 40
        value = None
        logger.critical("setConfigurationBlock unable to locate module or buffer")

    logger.debug("%s %s", "setConfigurationBlock returned ", status)

    return status, value

