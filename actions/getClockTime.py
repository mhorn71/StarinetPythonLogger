import utilities.samplerstatus as samplerstatus
import configparser
import logging
import datetime

##initialise logger
logger = logging.getLogger('actions.getClockTime')

config = configparser.RawConfigParser()
config.read("StarinetBeagleLogger.conf")


def control():
    
    logger.debug("getClockTime called")

    try:
        value = datetime.datetime.now().strftime("%H:%M:%S")
    except Exception as e:
        logger.critical("%s %s", "premature termination", e)
        value = e
        status = 4
    else:
        status = 0
        
    logger.debug("%s %s", "getClockTime returned ", value)

    status = status + samplerstatus.status()

    return status, value
