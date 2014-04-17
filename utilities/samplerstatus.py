import os
import psutil
import ConfigParser
import logging

logger = logging.getLogger('utilities.samplerstatus')

##initialise config parser
config = ConfigParser.RawConfigParser()
config.read("StarinetBeagleLogger.conf")


def status():

    pidfile = config.get('paths', 'pidfile')

    value = None

    try:
        f = open(pidfile, 'r')
        p = int(f.readline())
        proc = psutil.Process(p)
        f.close()
    except IOError:
        logger.debug("No pidfile present")
        value = 0
    except psutil.NoSuchProcess:
        logger.debug("psuti.Process returned no pidfile")
        value = 0
    except ValueError as e:
        logger.debug("psuti.Process returned no value from pidfile")
        os.remove(config.get('paths', 'pidfile'))
    else:
        logger.debug("%s %s", "proc.cmdline reports ", proc.cmdline())
        if proc.cmdline()[1] == 'logger/sampler.py':
            if proc.status == psutil.STATUS_ZOMBIE:
                try:
                    os.remove(config.get('paths', 'pidfile'))
                except IOError as e:
                    logger.debug("%s %s", "Unable to remove pid file fatal error", e)
                    value = 2
            else:
                value = 8000
        else:
            try:
                os.remove(config.get('paths', 'pidfile'))
            except IOError as e:
                logger.debug("%s %s", "Unable to remove pid file fatal error", e)
                value = 2
            else:
                value = 0

        logger.debug("%s %s", "Status = ", str(value))

    return value

if __name__ == "__main__":
    print str(status())

