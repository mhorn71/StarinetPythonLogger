import utilities.samplerstatus as samplerstatus
import logging
import analogue.readadc as readadc
import actions.getTemperature as getTemperature

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
            '\x1E' + samplerresponse[3] + '\x1E' + samplerresponse[4] + '\x1E' + samplerresponse[5]
        logger.debug("%s %s", "getRealtimeData returned value ", value)

    status = status + samplerstatus.status()

    return status, value
