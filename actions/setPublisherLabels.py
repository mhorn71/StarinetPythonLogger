__author__ = 'mark'
import utilities.publisherstatus as publisherstatus
import utilities.samplerstatus as samplerstatus
import ConfigParser
import logging

##initialise logger
logger = logging.getLogger('actions.setPublisherLabels')

config = ConfigParser.RawConfigParser()
config.read("StarinetBeagleLogger.conf")


def control(buffer0, buffer1, buffer2, buffer3):

    logger.debug("setPublisherLabels called")
    logger.debug("%s %s %s %s", buffer0, buffer1, buffer2, buffer3)

    if publisherstatus.status() == 0:
        status = 2  # ABORT
        value = 'capturePublisher_ACTIVE'
    else:
        try:
            config.set('publisherlabels', 'channel0', buffer0)  # update
            config.set('publisherlabels', 'channel1', buffer1)  # update
            config.set('publisherlabels', 'channel2', buffer2)  # update
            config.set('publisherlabels', 'channel3', buffer3)  # update
            with open('StarinetBeagleLogger.conf', 'wb') as configfile:
                config.write(configfile)
        except IOError as e:
            logger.debug("%s %s", "setPublisherLabels IOError ", e)
            status = 4  # PREMATURE_TERMINATION
            value = e
        else:
            status = 0  # SUCCESS
            value = None
    logger.debug("%s %s", "setPublisherLabels returned ", status)

    status = status + samplerstatus.status()

    return status, value
