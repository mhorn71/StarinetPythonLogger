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
    parameter_state = True

    config.read("StarinetBeagleLogger.conf")
    try:
        interval = config.get("publisher", "interval")
        server = config.get("publisher", "server")
        username = config.get("publisher", "username")
        password = config.get("publisher", "password")
        remotefolder = config.get("publisher", "remotefolder")
    except (configparser.NoSectionError, configparser.NoOptionError):
        parameter_state = False
    else:
        if len(interval) == 0:
            parameter_state = False

        if len(server) == 0:
            parameter_state = False

        if len(username) == 0:
            parameter_state = False

        if len(password) == 0:
            parameter_state = False

        if len(remotefolder) == 0:
            parameter_state = False

    logger.debug("%s %s", "capturePublisher buffer0 ", buffer0)

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
                if parameter_state:
                    publisher.start()
                    value = 'capturePublisher_ACTIVE'
                    status = 0
                else:
                    value = 'No remote server parameters set.'
                    status = 2
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
