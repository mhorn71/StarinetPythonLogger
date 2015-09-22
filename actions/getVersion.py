import configparser
import logging

##initialise logger
logger = logging.getLogger('actions.getVersion')

config = configparser.RawConfigParser()


def control():

    logger.debug("getVersion called")

    try:
        config.read("StarinetBeagleLogger.conf")
        value = config.get("version", "version")
    except configparser.Error as e:
        status = 4
        value = e
        logger.critical("%s %s", "Unable to get version from config", e)
    else:
        status = 0
        logger.debug("%s %s", "getVersion returned ", value)

    return status, value
