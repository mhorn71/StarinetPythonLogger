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
            logger.debug("Publisherstatus reports combined active")
            status = 2
            value = 'PUBLISHER_ACTIVE'
        elif publisher.status() is False:
            logger.debug("Publisherstatus reports combined not active")

            if sampler.status() == 8000:
                if parameter_state:
                    publisher.start()
                    value = 'PUBLISHER_ACTIVE'
                    status = 0
                else:
                    value = 'No remote server parameters set.'
                    status = 2
            else:
                logger.debug("Capture not active command capturePublisher aborted")
                status = 2
                value = 'Capture not active'
        else:
            logger.debug("Premature termination")
            status = 4
            value = 'Unable to ascertain publisher status'

    elif buffer0 == 'false':

        logger.debug("Entered false routine")

        if publisher.status() is False:
            logger.debug("%s %s", "Publisherstatus reports combined not active", str(publisher.status()))
            status = 0
            value = ' '
        elif publisher.status():
            publisher.stop()
            status = 0
            value = ' '
    else:
        logger.critical("Invalid parameter")
        status = 8
        value = ' '

    return status, value

if __name__ == "__main__":
    print(control(str(sys.argv[1:])))
