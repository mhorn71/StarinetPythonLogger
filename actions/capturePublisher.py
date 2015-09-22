import configparser
import logging
import sys


##initialise logger
logger = logging.getLogger('actions.capturePublisher')

config = configparser.RawConfigParser()
#config.read("StarinetBeagleLogger.conf")


def control(buffer0, publisher, sampler):

    status = None
    value = None

    config.read("StarinetBeagleLogger.conf")

    logger.debug("%s %s", "capturePublisher buffer0 ", buffer0)

    nx = publisher.status()

    buffer0 = buffer0.lower()

    if buffer0 == 'true':

        logger.debug("Entered true routine")

        if publisher.status():
            logger.debug("%s %s", "publisherstatus reports combined active", str(publisher.status()))
            status = 2
            value = 'capturePublisher_ACTIVE'
        elif publisher.status() is False:
            logger.debug("%s %s", "publisherstatus reports combined not active", str(publisher.status()))

            if sampler.status() == 8000:
                publisher.start()
                value = 'capturePublisher_ACTIVE'
                status = 0
            else:
                logger.debug("capture not active command capturePublisher aborted")
                status = 2
                value = 'capture not active'
        else:
            logger.debug("premature termination")
            status = 4
            value = 'unable to ascertain publisher status'

    elif buffer0 == 'false':

        logger.debug("Entered false routine")

        if publisher.status() is False:
            logger.debug("%s %s", "publisherstatus reports combined not active", str(publisher.status()))
            status = 0
        elif publisher.status():
            publisher.stop()
            status = 0
    else:
        logger.critical("invalid parameter")
        status = 8

    return status, value

if __name__ == "__main__":
    print(control(str(sys.argv[1:])))
