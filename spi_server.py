# Simple SPI server for RPi and Decawave DW1000
# Copyright (c) Jeremy P Bentham 2019. See iosoft.blog for details

# To enable SPI1, add dtoverlay=spi1-3cs to /boot/config.txt
# Connector pin numbers:
#       SPI0        SPI1
# GND   25          34
# CS    24 (CE0)    36 (CE2)
# MOSI  19          38
# MISO  21          35
# CLK   23          40
# IRQ   18          32
# RESET 22 (BCM25)  37 (BCM26)
# NRST  16 (BCM23)  31 (BCM6)

import sys, socket, time, select, spidev, RPi.GPIO as GPIO

VERSION = "0.13"

SPIF1       = 0,0   # First SPI interface
RST_PIN1    = 22
NRST_PIN1   = 16
IRQ_PIN1    = 18
SPIF2       = 1,2   # Second SPI interface
RST_PIN2    = 37
NRST_PIN2   = 31
IRQ_PIN2    = 32
SPI_SPEED   = 2000000

RESET_VAL   = 0xff  # Values for first network byte
ANS_VAL     = 0xaa
IRQ_VAL     = 0xfe

NET_MODE    = "UDP" # UDP or TCP mode
PORTNUM     = 1401  # Default port (for first SPI interface)
portnum     = PORTNUM
MAXDATA     = 2048

SOCK_TIMEOUT= 0.005 # Socket read timeout (sec)

verbose     = False # Global flags
interrupt   = False
connection  = None
SEQLEN      = 2

# Simple UDP server
class Server(object):
    def __init__(self):
        self.rxdata, self.txdata = [], []
        self.sock = self.addr = None

    # Open socket
    def open(self, portnum):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(('', portnum))
        return self.sock

    # Receive incoming data with timeout
    def recv(self, maxlen=MAXDATA, timeout=SOCK_TIMEOUT):
        rxdata = []
        socks = [self.sock]
        rd, wr, ex = select.select(socks, [], [], timeout)
        for s in rd:
            rxdata, self.addr = s.recvfrom(maxlen)
        return rxdata

    # Receive incoming request, return iterator for data blocks
    # If sequence number is unchanged, resend last transmission
    def receive(self):
        self.rxdata = bytearray(self.recv(MAXDATA))
        if len(self.rxdata) > SEQLEN:
            if verbose:
                tim = time.time() - toff
                print("%1.3f Rx: %s" % (tim%10.0, hexvals(self.rxdata)))
            if len(self.txdata)>SEQLEN and self.rxdata[0]==self.txdata[0]:
                self.xmit(self.txdata, '*')
            else:
                self.txdata = [self.rxdata[0]]
                rxd = self.rxdata[SEQLEN-1:]
                while len(rxd)>1 and len(rxd)>rxd[0]:
                    n = rxd[0] + 1
                    yield(rxd[1:n])
                    rxd = rxd[n:]

    # Add response data to list
    def send(self, data):
        self.txdata += [len(data)] + data

    # Transmit responses
    def xmit(self, txdata, suffix=''):
        if self.addr and len(txdata)>SEQLEN:
            txd = bytearray(txdata)
            if verbose:
                tim = time.time() - toff
                print("%1.3f Tx: %s %s" % (tim%10.0, hexvals(txd), suffix))
            self.sock.sendto(txd, self.addr)

    # Transmit an IRQ
    def xmit_irq(self):
        self.xmit((0, 1, IRQ_VAL))

    # Close socket
    def close(self):
        if self.sock:
            self.sock.close()
        self.sock = None

# Handle pin-change event: set interrupt flag
def irq_handler(chan):
    global interrupt
    interrupt = True
    
# Return string with hex values of bytes    
def hexvals(data):
    return " ".join(["%02X" % b for b in bytearray(data)])

if __name__ == "__main__":
    # Handle command-line args
    print("SPI_SERVER v" + VERSION)
    for arg in sys.argv[1:]:
        if arg.lower() == "-v":
            verbose = True
        elif arg[0].isdigit():
            portnum = int(arg)
        else:
            print("Unrecognised argument '%s'" % arg)

    # Set up SPI interface; use 2nd if 2nd port number
    spif = SPIF1 if portnum==PORTNUM else SPIF2
    rst_pin = RST_PIN1 if portnum==PORTNUM else RST_PIN2
    nrst_pin = NRST_PIN1 if portnum==PORTNUM else NRST_PIN2
    irq_pin = IRQ_PIN1 if portnum==PORTNUM else IRQ_PIN2
    spi = spidev.SpiDev()
    spi.open(*spif)
    spi.max_speed_hz = SPI_SPEED
    spi.mode = 0

    # Set up board I/O
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    GPIO.setup(rst_pin, GPIO.OUT)
    GPIO.setup(nrst_pin, GPIO.IN)
    GPIO.setup(irq_pin, GPIO.IN)
    GPIO.add_event_detect(irq_pin, GPIO.RISING, callback=irq_handler)

    # Set up server
    sock = Server()
    sock.open(portnum)
    print("Listening on UDP port %u" % portnum)

    resp = bytearray(spi.xfer(5*[0]))
    print("Device ID: %s" % hexvals(resp))

    # Main loop
    toff = time.time()
    while True:
        resp = []
        # If interrupt has been received, send single-byte message
        if interrupt:
            if verbose:
                tim = time.time() - toff
                print("%1.3f IRQ pin %u" % ((tim % 10.0), irq_pin))
            sock.xmit_irq()
            interrupt = False
        # Check for incoming commands
        for data in sock.receive():
            # Single-byte command is a reset
            if len(data) == 1:
                if data[0] == RESET_VAL:
                    GPIO.output(rst_pin, 1)
                    GPIO.setup(nrst_pin, GPIO.OUT)
                    GPIO.output(nrst_pin, 0)
                    print("Reset pin %u" % rst_pin)
                    toff = time.time()
                    interrupt = False
                else:
                    GPIO.output(rst_pin, 0)
                    GPIO.setup(nrst_pin, GPIO.IN)
                resp = [data[0]]
            # Multi-byte command: send to SPI
            elif len(data) > 1:
                resp = spi.xfer(data)
                # Change 1st byte of read response to be 'AA'
                if data[0] & 0x80 == 0:
                    resp[0] = ANS_VAL
            if resp:
                sock.send(resp)
        if len(resp):
            sock.xmit(sock.txdata)
    GPIO.cleanup()
    sock.close()

# EOF
