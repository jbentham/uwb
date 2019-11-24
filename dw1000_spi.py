# Networked SPI interface for DW1000 UWB modules
# Copyright (c) Jeremy P Bentham 2019. See iosoft.blog for details
#
# To enable SPI1, add dtoverlay=spi1-3cs to /boot/config.txt
# Connector pin numbers:
#       SPI0        SPI1
# GND   25          34
# CS    24 (CE0)    36 (CE2)
# MOSI  19          38
# MISO  21          35
# CLK   23          40
# RESET 22 (BCM25)  37 (BCM26)
# IRQ   18          32

import sys, socket, time, select, dw1000_regs as regs
from dw1000_regs import Reg, msdelay

RESET_VAL       = 0xff
ANS_VAL         = 0xaa
SOCK_TIMEOUT    = 0.05
MAX_DATALEN     = 2048
IRQ_VAL         = 0xfe
SEQLEN          = 2
RETRIES         = 3

resetime        = time.time()

# Class for an SPI interface
class Spi(object):
    def __init__(self, spif, ident='1'):
        self.spif, self.ident = spif, ident
        self.txseq = 0
        self.verbose = self.interrupt = False
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        if self.sock:
            self.sock.connect(spif[1:])
            print("Connected to %s:%u" % spif[1:])
        else:
            print("Can't open socket")
    
    # Do an SPI transfer over the network, return response
    def xfer(self, txdata):
        resp = []
        txdata = [self.txseq, len(txdata)] + txdata
        self.txseq = (self.txseq % 255) + 1
        self.send(txdata)
        retries = RETRIES
        rxdata = []
        while not rxdata:
            rxdata = self.receive()
            if len(rxdata) > SEQLEN:
                if rxdata[0] != txdata[0]:
                    rxdata = []
            elif retries>0:
                self.send(txdata)
                retries -= 1
            else:
                break
        if len(rxdata)>SEQLEN and rxdata[SEQLEN]==ANS_VAL:
            resp = bytearray(rxdata[SEQLEN:])
        return resp

    # Send outgoing data
    def send(self, txdata):
        if self.verbose:
            rw = "Wr:" if txdata[SEQLEN] & 0x80 else "Rd:"
            print("%1.3f %s%s %s" % (logtime(), rw,
                  self.ident, regs.data_str(txdata, SEQLEN)))
        self.sock.send(bytearray(txdata))

    # Receive incoming data with timeout
    def recv(self, maxlen=MAX_DATALEN, timeout=SOCK_TIMEOUT):
        data = []
        rd, wr, ex = select.select([self.sock], [], [], timeout)
        for s in rd:
            try:
                data, self.addr = self.sock.recvfrom(maxlen)
            except:
                data = []
        return data

    # Receive network response, single byte is an interrupt
    # Save interrupt in a flag, but don't return unless arg is set
    def receive(self, irq_return=False):
        loop = True
        resp = []
        while loop:
            resp = bytearray(self.recv())
            if self.verbose:
                print("%1.3f    %s %s" % (logtime(), 
                      self.ident, hexvals(resp)))
            if len(resp)==1+SEQLEN and resp[SEQLEN]==IRQ_VAL:
                self.interrupt = True
                if irq_return:
                    loop = False
            else:
                loop = False
        return resp

    # Return timeout value in msec
    def get_timeout(self):
        return int(SOCK_TIMEOUT * 1000)

    # Assert or negate hardware reset pin
    def reset(self, on):
        self.xfer([RESET_VAL] if on else [0])

    # Close socket
    def close(self):
        if self.sock:
            self.sock.close()

# Return modulo-10 time for log
def logtime(reset=False):
    global resetime
    return (time.time() - resetime) % 10.0

# Return string with hex values of bytes    
def hexvals(data):
    return " ".join(["%02X" % b for b in bytearray(data)])

if __name__ == "__main__":
    SPIF = "UDP", "10.1.1.226", 1401
    print("Connecting to %s port %s:%u" % SPIF)
    spi = Spi(SPIF)
    resp = bytearray(spi.xfer(5*[0]))
    print(" ".join(["%02X" % b for b in resp]))
    spi.close()

# EOF

