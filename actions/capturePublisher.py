import os.path
import subprocess
import utilities.publisherstatus as publisherstatus
import ConfigParser
import signal
import logging
import sys


##initialise logger
logger = logging.getLogger('actions.capturePublisher')

config = ConfigParser.RawConfigParser()
#config.read("StarinetBeagleLogger.conf")


def control(buffer0):

    status = None
    value = None

    config.read("StarinetBeagleLogger.conf")

    logger.debug("%s %s", "capturePublisher buffer0 ", buffer0)

    if buffer0 == 'true':

        logger.debug("Entered true routine")
        if publisherstatus.status() == 0:
            logger.debug("%s %s", "publisherstatus reports sampler active", str(publisherstatus.status()))
            status = 8002
        elif publisherstatus.status() == 1:
            logger.debug("%s %s", "publisherstatus reports sampler not active", str(publisherstatus.status()))
            
            try:
                pro = subprocess.Popen(["/usr/bin/python", "publisher/combined.py"])
            except IOError as e:
                logger.critical("%s %s", "premature termination", e)
                logger.critical("Unable to start capture")
                status = 4
            else:
                try:
                    pidfile = open(config.get('paths', 'pidfile'), 'w')
                    pidfile.write(str(pro.pid))
                    pidfile.close()
                except IOError as e:   
                    logger.critical("%s %s", "premature termination", e)
                    logger.critical("Unable to create pid file")
                    status = 4
                else:
                    logger.debug("Started publisher.combined ....")
                    status = 0
        else:
            logger.debug("premature termination")
            status = 4

    elif buffer0 == 'false':

        logger.debug("Entered false routine")

        if publisherstatus.status() == 1:
            logger.debug("%s %s", "publisherstatus reports sampler not active", str(publisherstatus.status()))
            status = 0
        elif publisherstatus.status() == 0:
            logger.debug("%s %s", "publisherstatus reports sampler active", str(publisherstatus.status()))
            try:
                pidfile = open(config.get('paths', 'pidfile'), 'r')
                pid = int(pidfile.read())
                pidfile.close()
                logger.debug("%s %s %s", "publisher.combined pidfile and pid - ", str(pidfile), str(pid))
            except IOError as e:
                logger.critical("%s %s", "Unable to assign pid to pro.pid capturePublisher.py", e)
                status = 4
            else:
                try:
                    os.kill(pid, signal.SIGTERM)
                except OSError as e:
                    logger.debug("%s %s", "Unable to kill process publisher.combined", e)
                    status = 4
                else:
                    try:
                        os.remove(str(config.get('paths', 'pidfile')))
                    except OSError as e:
                        logger.critical("%s %s", "Unable to remove pid file fatal error", e)
                        status = 4
                    else:
                        status = 0

    else:
        logger.critical("invalid parameter")
        status = 8

    return status, value

if __name__ == "__main__":
    print control(str(sys.argv[1:]))
