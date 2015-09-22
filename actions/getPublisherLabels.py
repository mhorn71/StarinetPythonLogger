__author__ = 'mark'
import configparser
import logging

##initialise logger
logger = logging.getLogger('actions.getPublisher')

config = configparser.RawConfigParser()


def control():

    logger.debug("getPublisher called")

    try:
        config.read("StarinetBeagleLogger.conf")
        channel0 = config.get("publisherlabels", "channel0")
        channel1 = config.get("publisherlabels", "channel1")
        channel2 = config.get("publisherlabels", "channel2")
        channel3 = config.get("publisherlabels", "channel3")
        channel4 = config.get("publisherlabels", "channel4")
        channel5 = config.get("publisherlabels", "channel5")
        channel6 = config.get("publisherlabels", "channel6")
    except configparser.Error as e:
        status = 4
        value = e
        logger.critical("%s %s", "Unable to get publisher parameters from config", e)
    else:
        status = 0
        value = channel0 + ',' + channel1 + ',' + channel2 + ',' + channel3 + ',' + channel4 + ',' + channel5 + ',' + \
                channel6
        
        logger.debug("%s %s", "returning value ", value)

    return status, value
