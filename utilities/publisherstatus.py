import os
import psutil
import ConfigParser
import logging

logger = logging.getLogger('utilities.publisherstatus')

##initialise config parser
config = ConfigParser.RawConfigParser()
config.read("StarinetBeagleLogger.conf")

## the following status will return: 0 = Not Running, 1 = Running, 2 = Error

def status():

    pidfile = config.get('publisherstatus', 'pidfile')

    value = None

    try:
        f = open(pidfile, 'r')
        p = int(f.readline())
        proc = psutil.Process(p)
        f.close()
    except IOError:
        logger.debug("No pidfile present")
        value = 1
    except psutil.NoSuchProcess:
        logger.debug("psuti.Process returned no pidfile")
        value = 1
    except ValueError as e:
        logger.debug("psuti.Process returned no value from pidfile")
        os.remove(config.get('paths', 'pidfile'))
        value = 1
    else:
        logger.debug("%s %s", "proc.cmdline reports ", proc.cmdline())
        try:
            b = proc.cmdline()[1]
        except IndexError as e:
            logger.debug("proc.cmdline returned no value from pidfile")
            os.remove(config.get('paths', 'pidfile'))
            value = 1
        else:
            if b == 'publisher/combined.py':
                if proc.status == psutil.STATUS_ZOMBIE:
                    try:
                        os.remove(config.get('publisher', 'pidfile'))
                    except IOError as e:
                        logger.debug("%s %s", "Unable to remove pid file fatal error", e)
                        value = 2
                else:
                    value = 0
            else:
                try:
                    os.remove(config.get('publisher', 'pidfile'))
                except IOError as e:
                    logger.debug("%s %s", "Unable to remove pid file fatal error", e)
                    value = 2
                else:
                    value = 1

        logger.debug("%s %s", "Status = ", str(value))

    return value