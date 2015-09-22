import os
import configparser
import logging


##initialise logger
logger = logging.getLogger('actions.capture')

config = configparser.RawConfigParser()
config.read("StarinetBeagleLogger.conf")


def control():

    logger.debug("getDataBlockCount called")

    value = None

    try:
        lastblock = int(max(os.listdir(config.get("paths", "datafolder")),
                            key=lambda p: os.path.getctime(os.path.join(
                            config.get("paths", "datafolder"), p))), 16) + 1

        value = hex(lastblock).split('x')[1].upper().zfill(4)
    except Exception as e:
        status = 0
        value = '0000'
    except OSError as e:
        status = 0
        value = '0000'
        logger.critical("%s %s", "Unable to open datafolder", e)
    else:
        status = 0

    return status, value
