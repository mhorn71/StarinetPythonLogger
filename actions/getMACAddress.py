import configparser
import logging
import re
import uuid

##initialise logger
logger = logging.getLogger('actions.getMACAddress')

config = configparser.RawConfigParser()
config.read("StarinetBeagleLogger.conf")


def control():

    logger.debug("getMACAddress called")

    try:
        value = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
    except Exception as e:
        status = 4
        value = e
        logger.critical("%s %s", "failure to get uuid.getnode() ", e)
    else:
        status = 0

    logger.debug("%s %s", "getMACAddress returned ", value)

    return status, value
