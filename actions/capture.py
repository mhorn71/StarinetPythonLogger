import os.path
import subprocess
import utilities.publisherstatus as publisherstatus
import configparser
import signal
import logging
import sys


##initialise logger
logger = logging.getLogger('actions.capture')

config = configparser.RawConfigParser()
#config.read("StarinetBeagleLogger.conf")


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
            status = 8002
        elif sampler.status() == 0:
            logger.debug("%s %s", "samplerstatus reports sampler not active", str(sampler.status()))

            sampler.start()
            status = 0
            
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
            # else:
            #     f = open(config.get("paths", "datafolder") + '0000', 'wb')
            #     f.close()
            #     try:
            #         pro = subprocess.Popen(["/usr/bin/python", "logger/sampler.py"])
            #     except IOError as e:
            #         logger.critical("%s %s", "premature termination", e)
            #         logger.critical("Unable to start capture")
            #         status = 4
            #     else:
            #         try:
            #             pidfile = open(config.get('paths', 'pidfile'), 'w')
            #             pidfile.write(str(pro.pid))
            #             pidfile.close()
            #         except IOError as e:
            #             logger.critical("%s %s", "premature termination", e)
            #             logger.critical("Unable to create pid file")
            #             status = 4
            #         else:
            #             logger.debug("Started logger/sampler ....")
            #             status = 0
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
            # logger.debug("%s %s", "samplerstatus reports sampler active", str(sampler.status()))
            #
            # if publisherstatus.status() == 0:
            #     logger.debug("%s %s", "publisher running terminating first", str(publisherstatus.status()))
            #     try:
            #         pidfile = open(config.get('publisher', 'pidfile'), 'r')
            #         pid = int(pidfile.read())
            #         pidfile.close()
            #         logger.debug("%s %s %s", "publisher.combined pidfile and pid - ", str(pidfile), str(pid))
            #     except IOError as e:
            #         logger.critical("%s %s", "Unable to assign pid to pro.pid capturePublisher.py", e)
            #     else:
            #         try:
            #             os.kill(pid, signal.SIGTERM)
            #         except OSError as e:
            #             logger.debug("%s %s", "Unable to kill process publisher.combined", e)
            #         else:
            #             try:
            #                 os.remove(str(config.get('publisher', 'pidfile')))
            #             except OSError as e:
            #                 logger.critical("%s %s", "Unable to remove pid file fatal error", e)
            #             else:
            #                 pass
            #
            # try:
            #     pidfile = open(config.get('paths', 'pidfile'), 'r')
            #     pid = int(pidfile.read())
            #     pidfile.close()
            #     logger.debug("%s %s %s", "logger/sampler pidfile and pid - ", str(pidfile), str(pid))
            # except IOError as e:
            #     logger.critical("%s %s", "Unable to assign pid to pro.pid capture.py", e)
            #     status = 4
            # else:
            #     try:
            #         os.kill(pid, signal.SIGTERM)
            #     except OSError as e:
            #         logger.debug("%s %s", "Unable to kill process logger/sampler", e)
            #         status = 4
            #     else:
            #         try:
            #             os.remove(str(config.get('paths', 'pidfile')))
            #         except OSError as e:
            #             logger.critical("%s %s", "Unable to remove pid file fatal error", e)
            #             status = 4
            #         else:
            #             status = 0

    else:
        logger.critical("invalid parameter")
        status = 8

    return status, value

if __name__ == "__main__":
    print(control(str(sys.argv[1:])))

