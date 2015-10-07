import configparser
import logging
import os

##initialise logger
logger = logging.getLogger('actions.getSpace')

config = configparser.RawConfigParser()
config.read("StarinetBeagleLogger.conf")


def control():

    logger.debug("getSpace called")

    try:
        blockcount = int(max(os.listdir(config.get("paths", "datafolder")),
                             key=lambda p: os.path.getctime(os.path.join(
                                 config.get("paths", "datafolder"), p))), 16) + 1
        value = str(int(100 - int(100 * float(blockcount) / 16384))).zfill(3)
    except configparser.Error as e:
        status = 4
        value = e
        logger.critical("%s %s", "Unable to open datafolder", e)
    except OSError as e:
        status = 4
        value = e
        logger.critical("%s %s", "Unable to open datafolder", e)
    except ValueError:
        value = '000'
        status = 0
    else:
        status = 0
        logger.debug("%s %s", "getSpace returned value ", value)

    return status, value
