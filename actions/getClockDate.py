import logging
import datetime
import configparser

##initialise logger
logger = logging.getLogger('actions.getClockDate')

config = configparser.RawConfigParser()
config.read("StarinetBeagleLogger.conf")


def control():

    logger.debug("getClockDate called")

    try:
        value = datetime.datetime.now().strftime("%Y-%m-%d")
    except Exception as e:
        logger.critical("%s %s", "premature termination", e)
        value = e
        status = 4
    else:
        status = 0

    logger.debug("%s %s", "getClockDate returned ", value)

    return status, value

