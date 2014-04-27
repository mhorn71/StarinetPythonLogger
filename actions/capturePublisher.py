__author__ = 'mark'

import utilities.samplerstatus as samplerstatus
import ConfigParser
import logging

##initialise logger
logger = logging.getLogger('actions.capturePublisher')

config = ConfigParser.RawConfigParser()
config.read("StarinetBeagleLogger.conf")

def control(buffero):
    return 0, None
