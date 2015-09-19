import utilities.samplerstatus as samplerstatus
import logging
import logger.readadc as readadc
import getTemperature 

##initialise logger
logger = logging.getLogger('actions.getRealtimeData')


def control():

    logger.debug("getRealtimeData called")

    try:
        samplerresponse = readadc.read()
        logger.info("getRealTimeData sampleresponse = " + str(samplerresponse))
        temp = getTemperature.control()
    except IOError as e:
        status = 4
        value = e
        logger.critical("%s %s", "Unable to get temperature", e)
    else:
        status = 0
        value = temp[1] + '\x1E' + samplerresponse[0] + '\x1E' + samplerresponse[1] + '\x1E' + samplerresponse[2] + \
            '\x1E' + samplerresponse[3]
        logger.debug("%s %s", "getRealtimeData returned value ", value)

    status = status + samplerstatus.status()

    return status, value
