import os.path
import configparser
import logging
import sys

# initialise logger
logger = logging.getLogger('actions.capture')

config = configparser.RawConfigParser()


def control(buffer0, sampler):

    status = None
    value = None

    config.read("StarinetBeagleLogger.conf")

    logger.debug("%s %s", "Capture buffer0 ", buffer0)

    buffer0 = buffer0.lower()

    if buffer0 == 'true':

        logger.debug("Entered true routine")
        if sampler.status() == 8000:
            logger.debug("%s %s", "samplerstatus reports sampler active", str(sampler.status()))
            status = 2
        elif sampler.status() == 0:
            logger.debug("%s %s", "samplerstatus reports sampler not active", str(sampler.status()))
            
            folder = config.get('paths', 'datafolder')

            try:
                for the_file in os.listdir(folder):
                    file_path = os.path.join(folder, the_file)
                    if os.path.isfile(file_path):
                            os.unlink(file_path)
                    logger.debug("%s %s", "Removing data file ", file_path)
            except OSError as e:
                        logger.critical("%s %s", "premature termination", e)
                        status = 4

            sampler.start()

            if sampler.status() == 8000:
                status = 0
            else:
                sampler.status()

            if sampler.status() == 8000:
                status = 0
            else:
                status = 4

        else:
            logger.debug("premature termination")
            status = 4

    elif buffer0 == 'false':

        logger.debug("Entered false routine")

        if sampler.status() == 0:
            logger.debug("%s %s", "samplerstatus reports sampler not active", str(sampler.status()))
            status = 0
        elif sampler.status() == 8000:
            sampler.stop()
            status = 0
    else:
        logger.critical("invalid parameter")
        status = 8

    return status, value

if __name__ == "__main__":
    print(control(str(sys.argv[1:])))

