__author__ = 'mark'
import utilities.publisherstatus as publisherstatus
import utilities.samplerstatus as samplerstatus
import ConfigParser
import logging

##initialise logger
logger = logging.getLogger('actions.setPublisher')

config = ConfigParser.RawConfigParser()
config.read("StarinetBeagleLogger.conf")


def control(buffer0, buffer1, buffer2, buffer3, buffer4, buffer5):

    logger.debug("setPublisher called")

    if publisherstatus.status() == 0:
        status = 2  # ABORT
        value = None
    else:
        try:
            config.set('publisher', 'chart', buffer0)  # update
            config.set('publisher', 'interval', buffer1)  # update
            config.set('publisher', 'server', buffer2)  # update
            config.set('publisher', 'username', buffer3)  # update
            config.set('publisher', 'password', buffer4)  # update
            config.set('publisher', 'remotefolder', buffer5)  # update
            with open('StarinetBeagleLogger.conf', 'wb') as configfile:
                config.write(configfile)
        except IOError as e:
            logger.debug("%s %s", "setPulisher IOError ", e)
            status = 4  # PREMATURE_TERMINATION
            value = e
        else:
            status = 0  # SUCCESS
            value = None
    logger.debug("%s %s", "setPublisher returned ", status)

    status = status + samplerstatus.status()

    return status, value