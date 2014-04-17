import Adafruit_BBIO.ADC as ADC

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

    _reading = None

    try:
        x0 = ADC.read_raw("AIN0")
        x0 = ADC.read_raw("AIN0")
        x1 = ADC.read_raw("AIN1")
        x1 = ADC.read_raw("AIN1")
        x2 = ADC.read_raw("AIN2")
        x2 = ADC.read_raw("AIN2")
        x3 = ADC.read_raw("AIN3")
        x3 = ADC.read_raw("AIN3")

        b0 = int(int(x0) * float(0.439))
        b1 = int(int(x1) * float(0.439))
        b2 = int(int(x2) * float(0.439))
        b3 = int(int(x3) * float(0.439))

        r0 = "{0:04d}".format(b0)
        r1 = "{0:04d}".format(b1)
        r2 = "{0:04d}".format(b2)
        r3 = "{0:04d}".format(b3)

    except IOError:
        _reading = '0000', '0000', '0000', '0000'
    except RuntimeError:
        _reading = '0000', '0000', '0000', '0000'
    else:
        _reading = r0, r1, r2, r3

    return _reading

if __name__ == "__main__":
    print read()

