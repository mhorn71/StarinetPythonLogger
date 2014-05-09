import Adafruit_BBIO.ADC as ADC
import logging


## initialise logger
logger = logging.getLogger('analogue')

try:
    ADC.setup()
except Exception as e:
    print 'Adc failed - did you start as root?', e
    pass

try:
    ADC.read("P9_40")
except Exception as e:
    print 'failed to read adc - did you start as root?', e
    pass


def read():

    logger.debug("Analogue.readadc called")

    _reading = None

    try:
        x0 = ADC.read("AIN0")
        x0 = ADC.read("AIN0")
        x1 = ADC.read("AIN1")
        x1 = ADC.read("AIN1")
        x2 = ADC.read("AIN2")
        x2 = ADC.read("AIN2")
        x3 = ADC.read("AIN3")
        x3 = ADC.read("AIN3")

 #       print "Reading are 0 = ", x0
 #       print "Reading are 1 = ", x1
 #       print "Reading are 2 = ", x2
 #       print "Reading are 3 = ", x3

        b0 = int(x0 * 1800)
        b1 = int(x1 * 1800)
        b2 = int(x2 * 1800)
        b3 = int(x3 * 1800)

 #       print "Reading are 0 = ", b0
 #       print "Reading are 1 = ", b1
 #       print "Reading are 2 = ", b2
 #       print "Reading are 3 = ", b3

        r0 = "{0:04d}".format(b0)
        r1 = "{0:04d}".format(b1)
        r2 = "{0:04d}".format(b2)
        r3 = "{0:04d}".format(b3)
    except IOError:
        _reading = '0000', '0000', '0000', '0000'
        logger.debug("%s %s", "adc IO Error ", e)
    except RuntimeError:
        _reading = '0000', '0000', '0000', '0000'
        logger.debug("%s %s", "adc RuntimeError ", e)
    else:
        _reading = r0, r1, r2, r3

    return _reading

if __name__ == "__main__":
    print read()

