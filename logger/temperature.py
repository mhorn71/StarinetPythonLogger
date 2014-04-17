import Adafruit_BBIO.ADC as ADC
import re

try:
    ADC.setup()
except Exception as e:
    print 'Adc failed - did you start as root?', e
    pass

try:
    ADC.read("AIN6")
except Exception as e:
    print 'failed to read adc - did you start as root?', e
    pass


def read():

    try:
        x0 = ADC.read("AIN6")
        x0 = ADC.read("AIN6")
        b0 = x0 * 1800
        pretemp = (b0 - 500) / 10

        if re.match("^\d{1}$", str(pretemp)):  #matched 0 - 9
            temp = '+' + str(pretemp.zfill(3))
        elif re.match("^\d{1}\.\d*$", str(pretemp)):
            a = str(pretemp).split('.')
            b = a[0].zfill(3)
            temp = '+' + str(b)
        elif re.match("^\d{2}$", str(pretemp)):
            temp = '+' + str(pretemp.zfill(3))
        elif re.match("^\d{2}\.\d*$", str(pretemp)):
            a = str(pretemp).split('.')
            b = a[0].zfill(3)
            temp = '+' + str(b)
        elif re.match("^-\d{1,2}$", str(pretemp)):
            a = str(pretemp).replace('-','')
            temp = '-' + str(a.zfill(3))
        elif re.match("^-\d\.\d*$", str(pretemp)):
            # matched -1.8888
            a = str(pretemp).replace('-','')
            b = str(a).split('.')
            c = str(b[0]).zfill(3)
            temp = '-' + c
        elif re.match("-\d{2}\.\d*$",str(pretemp)):
            a = str(pretemp).replace('-','')
            b = str(a).split('.')
            c = str(b[0]).zfill(3)
            temp = '-' + c
        else:
            temp = '+000'

        value = temp

    except IOError as e:

         value = '+000'

    return value
