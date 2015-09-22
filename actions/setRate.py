import configparser
import logging

##initialise logger
logger = logging.getLogger('actions.setRate')

config = configparser.RawConfigParser()


def control(buffer0):

    logger.debug("setRate called")

    try:
        config.read("StarinetBeagleLogger.conf")
        config.set('capture', 'rate', buffer0)  # update
        with open('StarinetBeagleLogger.conf', 'w') as configfile:
            config.write(configfile)
            configfile.close()
    except IOError as e:
        logger.debug("%s %s", "setRate IOError ", e)
        status = 4
        value = e
    else:
        status = 0
        value = None

    logger.debug("%s %s %s", "setRate", buffer0, status)

    return status, value
