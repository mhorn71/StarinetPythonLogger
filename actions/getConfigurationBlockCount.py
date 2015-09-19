import utilities.samplerstatus as samplerstatus
import configparser
import logging
import re
import os

##initialise logger
logger = logging.getLogger('actions.getConfigurationBlockCount')

config = configparser.RawConfigParser()
config.read("StarinetBeagleLogger.conf")


def control(buffer0):

    logger.debug("getConfigurationBlockCount called")

    if re.match('0', buffer0):
        logger.debug("%s %s", "Matched module 0 ", buffer0)
        try:
            lastblock = int(max(os.listdir(config.get("paths", "module0folder")),
                                key=lambda p: os.path.getctime(os.path.join(
                                    config.get("paths", "module0folder"), p))), 16) + 1
            logger.debug("%s %s", "last block appears to be ", lastblock)
            value = hex(lastblock).split('x')[1].upper().zfill(4)
            logger.debug("%s %s", "last block value converted to hex ", value)
        except IOError as e:
            status = 8
            value = None
            logger.critical("%s %s", "Unable to locate module 0 ", e)
        except ValueError:
            status = 8
            value = None
        except OSError as e:
            status = 4
            value = e
            logger.critical("%s %s", "Unable to open datafolder", e)
        else:
            status = 0
    elif re.match('1', buffer0):
        logger.debug("%s %s", "Matched module 1 ", buffer0)
        try:
            lastblock = int(max(os.listdir(config.get("paths", "module1folder")),
                                key=lambda p: os.path.getctime(os.path.join(
                                    config.get("paths", "module1folder"), p))), 16) + 1
            logger.debug("%s %s", "last block appears to be ", lastblock)
            value = hex(lastblock).split('x')[1].upper().zfill(4)
            logger.debug("%s %s", "last block value converted to hex ", value)
        except ValueError:
            status = 8
            value = None
        except StandardError as e:
            status = 8
            value = None
            logger.critical("%s %s", "Unable to locate module 1 ", e)
        except OSError as e:
            status = 4
            value = e
            logger.critical("%s %s", "Unable to open datafolder", e)
        else:
            status = 0
    else:
        logger.critical("%s %s", "Invalid module - ", buffer0)
        status = 40
        value = None

    status = status + samplerstatus.status()

    logger.debug("%s %s %s", "getConfigurationBlockCount returned ", status, value)

    return status, value

