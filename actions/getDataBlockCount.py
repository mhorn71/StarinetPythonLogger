import os
import utilities.samplerstatus as samplerstatus
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
    except Exception:
        status = 800
    except OSError as e:
        status = 4
        value = e
        logger.critical("%s %s", "Unable to open datafolder", e)
    else:
        status = 0

    status = status + samplerstatus.status()

    return status, value
