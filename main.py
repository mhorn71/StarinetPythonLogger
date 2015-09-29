import socket
import sys
import threading
import queue
import interpreter
import logging
import logging.config
import configparser
import time
import Adafruit_BBIO.ADC as ADC

## initialise logger
logging.config.fileConfig('StarinetBeagleLogger.conf', disable_existing_loggers=False)
logger = logging.getLogger('main')

##initialise config parser
config = configparser.RawConfigParser()
config.read("StarinetBeagleLogger.conf")

try:
    ADC.setup()
except IOError as e:
    print('Adc failed - did you start as root?' + str(e))
    pass

try:
    ADC.read("P9_40")
except IOError as e:
    pass

mybuffer = 570
my_queue = queue.Queue()


class ReadFromUDPSocket(threading.Thread):

    def __init__(self, my_queue):
        logger.info("ReadFromUDPSocket __init__ initialised.")
        threading.Thread.__init__(self)
        self.my_queue = my_queue

    def run(self):
        logger.debug("ReadFromUDPSocket run initialised.")
        while True:
            buffer1, addr = socketUDP.recvfrom(mybuffer)
            logger.debug("%s %s", "received data - ", repr(buffer1))

            if buffer1.decode().startswith('\x02') and buffer1.decode().endswith('\x04\r\n'):
                logger.debug("%s %s %s",  'Starinet UDP Packet received from', addr, repr(buffer1))
                buffer1 = buffer1.decode().strip('\x02\x04\r\n')
                self.my_queue.put((buffer1, addr))
                self.my_queue.join()


class Process(threading.Thread):

    def __init__(self, my_queue):

        logger.info("Process __init__ initialised.")

        threading.Thread.__init__(self)
        self.my_queue = my_queue
        self.alive = threading.Event()
        self.alive.set()
        self.interpreter = interpreter.Interpreter()

    def run(self):

        logger.debug("Process run initialised.")

        while True:
            buffer3 = self.my_queue.get()
            x = self.interpreter.processor(buffer3[0])

           # print "Interpreter returned - ", repr(x)

            if x is not None:
                #buffer4 = '\x0200000100000000127A\x04\r\n'  # Temp line just for testing.
                buffer4 = x.encode()
                logger.debug("%s %s", "return data ", repr(buffer4))
                socketUDP.sendto(buffer4, buffer3[1])
                self.my_queue.task_done()
            else:
                print("x has no data")
                self.my_queue.task_done()


if __name__ == '__main__':

    # Create socket (IPv4 protocol, datagram (UDP)) and bind to address
    try:
        socketUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        socketUDP.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        socketUDP.bind((config.get("network", "ip"), int(config.get("network", "port"))))
    except socket.error:
        logger.critical("Fatal Error unable to open network port.")
        sys.exit(1)
    else:
        logger.info("%s %s", "Initiated IPv4 Socket bound to port ", config.get("network", "port"))

    # Instantiate & start threads
    myServer = ReadFromUDPSocket(my_queue)
    myInterpreter = Process(my_queue)
    myServer.setDaemon(True)
    myInterpreter.setDaemon(True)

    myServer.start()
    myInterpreter.start()

    while 1:
        time.sleep(1)

    socketUDP.close()
