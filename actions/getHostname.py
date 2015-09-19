import configparser
import logging
import socket

##initialise logger
logger = logging.getLogger('actions.getHostname')

config = configparser.RawConfigParser()
config.read("StarinetBeagleLogger.conf")


def control():

    logger.debug("getHostname called")

    try:
        value = socket.gethostname()
    except Exception as e:
        status = 4
        value = e
        logger.critical("%s %s", "failure to get gethostname() ", e)
    else:
        status = 0
        
    logger.debug("%s %s", "getHostname returned ", value)

    return status, value
