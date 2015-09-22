import configparser
import logging


##initialise logger
logger = logging.getLogger('actions.ping')

config = configparser.RawConfigParser()
config.read("StarinetBeagleLogger.conf")


def ping():

    value = None

    logger.debug("ping called")

    status = 0

    logger.debug("%s %s", "ping status ", status)

    return status, value


