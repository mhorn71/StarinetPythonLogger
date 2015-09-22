__author__ = 'mark'
import utilities.publisherstatus as publisherstatus
import configparser
import logging

##initialise logger
logger = logging.getLogger('actions.setPublisherLabels')

config = configparser.RawConfigParser()


def control(buffer0, buffer1, buffer2, buffer3, buffer4, buffer5, buffer6):

    logger.debug("setPublisherLabels called")
    logger.debug("%s %s %s %s %s %s %s", buffer0, buffer1, buffer2, buffer3, buffer4, buffer5, buffer6)

    try:
        config.read("StarinetBeagleLogger.conf")
        config.set('publisherlabels', 'channel0', buffer0)  # update
        config.set('publisherlabels', 'channel1', buffer1)  # update
        config.set('publisherlabels', 'channel2', buffer2)  # update
        config.set('publisherlabels', 'channel3', buffer3)  # update
        config.set('publisherlabels', 'channel4', buffer4)  # update
        config.set('publisherlabels', 'channel5', buffer5)  # update
        config.set('publisherlabels', 'channel6', buffer6)  # update
        with open('StarinetBeagleLogger.conf', 'w') as configfile:
            config.write(configfile)
            configfile.close()
    except IOError as e:
        logger.debug("%s %s", "setPublisherLabels IOError ", e)
        status = 4  # PREMATURE_TERMINATION
        value = e
    else:
        status = 0  # SUCCESS
        value = None
    logger.debug("%s %s", "setPublisherLabels returned ", status)

    return status, value
