__author__ = 'mark'
import configparser
import logging

##initialise logger
logger = logging.getLogger('actions.getPublisherArtist')

config = configparser.RawConfigParser()


def control():

    logger.debug("getPublisherArtist called")

    try:
        config.read("StarinetBeagleLogger.conf")
        chart = config.get("publisherartist", "chart")
        channel0 = config.get("publisherartist", "channelArt0")
        channel1 = config.get("publisherartist", "channelArt1")
        channel2 = config.get("publisherartist", "channelArt2")
        channel3 = config.get("publisherartist", "channelArt3")
        temperature = config.get("publisherartist", "TemperatureArt")
        autoscale = config.get("publisherartist", "autoscale")
    except configparser.Error as e:
        status = 4
        value = e
        logger.critical("%s %s", "Unable to get publisher artist parameters from config", e)
    else:
        status = 0
        value = chart + ',' + channel0 + ',' + channel1 + ',' + channel2 + ',' + channel3 + ',' + temperature
        logger.debug("%s %s", "returning value ", value)

    return status, value