# Decawave DWM1000 register definitions
# See DW1000 User Manual, version 2.11
# Copyright (c) Jeremy P Bentham 2019. See iosoft.blog for details

from ctypes import LittleEndianStructure as Structure, Union
from ctypes import c_uint as U32, c_ulonglong as U64
import time

# Default values
DEF_PAN         = 10    # PAN ID
DEF_ADDR        = 1     # Address in PAN
DEF_CHAN        = 2     # Channel 1, 2, 3, 4, 5 or 7
DEF_RATE        = 110   # 110, 850, or 6800 kBPS
DEF_PULSE_FREQ  = 64    # 16 or 64 MHz
DEF_PREAM_LEN   = 1024  # 64, 128, 256, 512, 1024, 1536, 2048 or 4096
SMART_TX_POWER  = False # Enable smart Tx power control
RX_DOUBLE_BUFF  = False # Enable receiver double-buffering
LONG_FRAMES     = False # Enable 1023-byte frames (standard is 127)
RX_AUTO_EN      = False # Auto enable Rx after Tx
AUTO_ACK        = False # Automatically acknowledge transmission
USE_INTERRUPT   = True  # Use IRQ line

# DW1000 register addr, length, sub-register addr, and fields
DEV_ID    = 0x0, 4, None,(("REV",        U32, 4), ("VER",        U32, 4),
                          ("MODEL",      U32, 8), ("RIDTAG",     U32,16))
EUI       = 0x1, 8, None,()
PANADR    = 0x3, 4, None,(("SHORT_ADDR", U32, 16),("PAN_ID", U32, 16))
SYS_CFG   = 0x4, 4, None,(("FFEN",       U32, 1), ("FFBC",       U32, 1), ("FFAB",       U32, 1),
                          ("FFAD",       U32, 1), ("FFAA",       U32, 1), ("FFAM",       U32, 1),
                          ("FFAR",       U32, 1), ("FFA4",       U32, 1), ("FFA5",       U32, 1),
                          ("HIRQ_POL",   U32, 1), ("SPI_EDGE",   U32, 1), ("DIS_FCE",    U32, 1),
                          ("DIS_DRXB",   U32, 1), ("DIS_PHE",    U32, 1), ("DIS_RSDE",   U32, 1),
                          ("FCS_INIT2F", U32, 1), ("PHR_MODE",   U32, 2), ("DIS_STXP",   U32, 1),
                          ("X1",         U32, 3), ("RXM110K",    U32, 1), ("X2",         U32, 5),
                          ("RXWTOE",     U32, 1), ("RXAUTR",     U32, 1), ("AUTOACK",    U32, 1),
                          ("AACKPEND",   U32, 1))
SYS_TIME  = 0x6, 5, None,()
TX_FCTRL  = 0x8, 5, None,(("TFLEN",     U64, 7), ("TFLE",      U64, 3), ("R",         U64, 3),
                          ("TXBR",      U64, 2), ("TR",        U64, 1), ("TXPRF",     U64, 2),
                          ("TXPSR",     U64, 2), ("PE",        U64, 2), ("TXBOFFS",   U64, 10),
                          ("IFSDELAY",  U64, 8))
TX_BUFFER = 0x9, 1, None,()
DX_TIME   = 0xa, 5, None,()
RX_FWTO   = 0xc, 5, None,()
SYS_CTRL  = 0xd, 4, None,(("SFCST",      U32, 1), ("TXSTRT",     U32, 1), ("TXDLYS",     U32, 1),
                          ("CANSFCS",    U32, 1), ("X1",         U32, 2), ("TRXOFF",     U32, 1),
                          ("WAIT4RESP",  U32, 1), ("RXENAB",     U32, 1), ("RXDLYE",     U32, 1),
                          ("X2",         U32, 14),("HRBPT",      U32, 1), ("X3",         U32, 7))
SYS_MASK  = 0xe, 4, None,(("X1",         U32, 1), ("MCPLOCK",    U32, 1), ("MESYNCR",    U32, 1),
                          ("MAAT",       U32, 1), ("MTXFRB",     U32, 1), ("MTXPRS",     U32, 1),
                          ("MTXPHS",     U32, 1), ("MTXFRS",     U32, 1), ("MRXPRD",     U32, 1),
                          ("MRXSFDD",    U32, 1), ("MLDEDON",    U32, 1), ("MRXPHD",     U32, 1),
                          ("MRXPHE",     U32, 1), ("MRXDFR",     U32, 1), ("MRXFCG",     U32, 1),
                          ("MRXFCE",     U32, 1), ("MRXRFSL",    U32, 1), ("MRXRFTO",    U32, 1),
                          ("MLDEERR",    U32, 1), ("X2",         U32, 1), ("MRXOVRR",    U32, 1),
                          ("MRXPTO",     U32, 1), ("MGPIOIRQ",   U32, 1), ("MSLP2INIT",  U32, 1),
                          ("MRFPLLLL",   U32, 1), ("MCPLLLL",    U32, 1), ("MRXSFDTO",   U32, 1),
                          ("MHPDWAR",    U32, 1), ("MTXBERR",    U32, 1), ("MAFFREJ",    U32, 1),
                          ("X3",         U32, 2))
SYS_STATUS= 0xf, 5, None,(("IRQS",      U64, 1), ("CPLOCK",    U64, 1), ("ESYNCR",    U64, 1),
                          ("AAT",       U64, 1), ("TXFRB",     U64, 1), ("TXPRS",     U64, 1),
                          ("TXPHS",     U64, 1), ("TXFRS",     U64, 1), ("RXPRD",     U64, 1),
                          ("RXSFDD",    U64, 1), ("LDEDONE",   U64, 1), ("RXPHD",     U64, 1),
                          ("RXPHE",     U64, 1), ("RXDFR",     U64, 1), ("RXFCG",     U64, 1),
                          ("RXFCE",     U64, 1), ("RXRFSL",    U64, 1), ("RXRFTO",    U64, 1),
                          ("LDEERR",    U64, 1), ("X1",        U64, 1), ("RXOVRR",    U64, 1),
                          ("RXPTO",     U64, 1), ("GPIOIRQ",   U64, 1), ("SLP2INIT",  U64, 1),
                          ("RFPLL_LL",  U64, 1), ("CLKPLL_LL", U64, 1), ("RXSFDTO",   U64, 1),
                          ("HPDWARN",   U64, 1), ("TXBERR",    U64, 1), ("AFFREJ",    U64, 1),
                          ("HSRBP",     U64, 1), ("ICRBP",     U64, 1), ("RXRSCS",    U64, 1),
                          ("RXPREJ",    U64, 1), ("TXPUTE",    U64, 1), ("X2",        U64, 5))
RX_FINFO  = 0x10, 4,None,(("RXFLEN",     U32, 7), ("RXFLE",      U32, 3), ("X1",         U32, 1),
                          ("RXNSPL",     U32, 2), ("RXBR",       U32, 2), ("RNG",        U32, 1),
                          ("RXPRFR",     U32, 2), ("RXPSR",      U32, 2), ("RXPACC",     U32,12))
RX_BUFFER = 0x11, 1,None,()
RX_FQUAL  = 0x12, 8,None,(("STD_NOISE", U64,16), ("FP_AMPL2",  U64,16), ("PP_AMPL3",  U64,16),
                          ("CIR_PWR",   U64,16))
RX_TTCKI  = 0x13, 4,None,()
RX_TTCKO  = 0x14, 5,None,(("RXTOFS",    U64,19), ("X1",        U64, 5), ("RSMPDEL",   U64, 8),
                          ("RCPHASE",   U64, 7), ("X2",        U64, 1))
#RX_TIME   = 0x15,14,None,(("RX_STAMP",  U64,40), ("FP_INDEX",  U64,16), ("FP_AMPL1",  U64,16),
#                          ("RX_RAWST",  U64,40))
RX_TIME1  = 0x15, 7,0x00,(("RX_STAMP",  U64,40), ("FP_INDEX",  U64,16))
RX_TIME2  = 0x15, 7,0x07,(("FP_AMPL1",  U64,16), ("RX_RAWST",  U64,40))
#TX_TIME   = 0x17,10,None,(("TX_STAMP",  U64,40), ("TX_RAWST",  U64,40))
TX_TIME1  = 0x17, 5,0x00,(("TX_STAMP",  U64,40),)
TX_TIME2  = 0x17, 5,0x05,(("TX_RAWST",  U64,40),)
TX_ANTD   = 0x18, 2,None,()
ACK_RESP_T= 0x1a, 4,None,(("W4R_TIM",    U32,20), ("X1",         U32, 4), ("ACK_TIM",    U32, 8))
RX_SNIFF  = 0x1d, 4,None,(("SNIFF_ONT",  U32, 4), ("X1",         U32, 4), ("SNIFF_OFFT", U32, 8),
                          ("X2",         U32, 16))
TX_POWER  = 0x1e, 4,None,(("BOOSTNORM",  U32, 8), ("BOOSTP500",  U32, 8), ("BOOSTP250",  U32, 8),
                         ("BOOSTP125",  U32, 8))
CHAN_CTRL = 0x1f, 4,None,(("TX_CHAN",    U32, 4), ("RX_CHAN",    U32, 4), ("X1",         U32, 9),
                          ("DWSFD",      U32, 1), ("RXPRF",      U32, 2), ("TNSSFD",     U32, 1),
                          ("RNSSFD",     U32, 1), ("TX_PCODE",   U32, 5), ("RX_PCODE",   U32, 5))
SFD_LENGTH= 0x21, 2,0x00,()
AGC_CTRL1 = 0x23, 2,0x02,(("DIS_AM",     U32, 1), ("X1",         U32,15))
AGC_TUNE1 = 0x23, 2,0x04,()
AGC_TUNE2 = 0x23, 4,0x0c,()
AGC_TUNE3 = 0x23, 2,0x12,()
AGC_STAT1 = 0x23, 3,0x1e,(("X1",         U32, 6), ("EDG1",       U32, 5), ("EDV2",       U32, 9),
                          ("X2",         U32, 4),)
EC_CTRL   = 0x24, 4,0x00,(("OSTSM",      U32, 1), ("OSRSM",      U32, 1), ("PLLLDT",     U32, 1),
                          ("WAIT",       U32, 8), ("OSTRM",      U32, 1), ("X1",         U32, 20))
EC_RXTC   = 0x24, 4,0x04,(("RX_TS_EST",  U32,32),)
EC_GOLP   = 0x24, 4,0x08,(("OFFSET_EXT", U32, 6), ("X1",         U32,26))
ACC_MEM   = 0x25,4064,None,(())
GPIO_MODE = 0x26, 4,0x00,(("X1",         U32, 6), ("MSGP0",      U32, 2), ("MSGP1",      U32, 2),
                          ("MSGP2",      U32, 2), ("MSGP3",      U32, 2), ("MSGP4",      U32, 2),
                          ("MSGP5",      U32, 2), ("MSGP6",      U32, 2), ("MSGP7",      U32, 2),
                          ("MSGP8",      U32, 2), ("X2",         U32, 8))
GPIO_DIR  = 0x26, 4,0x08,(("GDP0",       U32, 1), ("GDP1",       U32, 1), ("GDP2",       U32, 1),
                          ("GDP3",       U32, 1), ("GDM0",       U32, 1), ("GDM1",       U32, 1),
                          ("GDM2",       U32, 1), ("GDM3",       U32, 1), ("GDP4",       U32, 1),
                          ("GDP5",       U32, 1), ("GDP6",       U32, 1), ("GDP7",       U32, 1),
                          ("GDM4",       U32, 1), ("GDM5",       U32, 1), ("GDM6",       U32, 1),
                          ("GDM7",       U32, 1), ("GDP8",       U32, 1), ("X1",         U32, 3),
                          ("GDM8",       U32, 1), ("X2",         U32,11))
GPIO_DOUT = 0x26, 4,0x0c,(("GOP0",       U32, 1), ("GOP1",       U32, 1), ("GOP2",       U32, 1),
                          ("GOP3",       U32, 1), ("GOM0",       U32, 1), ("GOM1",       U32, 1),
                          ("GOM2",       U32, 1), ("GOM3",       U32, 1), ("GOP4",       U32, 1),
                          ("GOP5",       U32, 1), ("GOP6",       U32, 1), ("GOP7",       U32, 1),
                          ("GOM4",       U32, 1), ("GOM5",       U32, 1), ("GOM6",       U32, 1),
                          ("GOM7",       U32, 1), ("GOP8",       U32, 1), ("X1",         U32, 3),
                          ("GOM8",       U32, 1), ("X2",         U32,11))
GPIO_IRQE = 0x26, 4,0x10,(("GIRQE0",     U32, 1), ("GIRQE1",     U32, 1), ("GIRQE2",     U32, 1),
                          ("GIRQE3",     U32, 1), ("GIRQE4",     U32, 1), ("GIRQE5",     U32, 1),
                          ("GIRQE6",     U32, 1), ("GIRQE7",     U32, 1), ("GIRQE8",     U32, 1),
                          ("X1",         U32, 23))
GPIO_ISEN = 0x26, 4,0x14,(("GISEN0",     U32, 1), ("GISEN1",     U32, 1), ("GISEN2",     U32, 1),
                          ("GISEN3",     U32, 1), ("GISEN4",     U32, 1), ("GISEN5",     U32, 1),
                          ("GISEN6",     U32, 1), ("GISEN7",     U32, 1), ("GISEN8",     U32, 1),
                          ("X1",         U32, 23))
GPIO_IMODE= 0x26, 4,0x18,(("GIMOD0",     U32, 1), ("GIMOD1",     U32, 1), ("GIMOD2",     U32, 1),
                          ("GIMOD3",     U32, 1), ("GIMOD4",     U32, 1), ("GIMOD5",     U32, 1),
                          ("GIMOD6",     U32, 1), ("GIMOD7",     U32, 1), ("GIMOD8",     U32, 1),
                          ("X1",         U32, 23))
GPIO_IBES = 0x26, 4,0x1c,(("GIBES0",     U32, 1), ("GIBES1",     U32, 1), ("GIBES2",     U32, 1),
                          ("GIBES3",     U32, 1), ("GIBES4",     U32, 1), ("GIBES5",     U32, 1),
                          ("GIBES6",     U32, 1), ("GIBES7",     U32, 1), ("GIBES8",     U32, 1),
                          ("X1",         U32, 23))
GPIO_ICLR = 0x26, 4,0x20,(("GICLR0",     U32, 1), ("GICLR1",     U32, 1), ("GICLR2",     U32, 1),
                          ("GICLR3",     U32, 1), ("GICLR4",     U32, 1), ("GICLR5",     U32, 1),
                          ("GICLR6",     U32, 1), ("GICLR7",     U32, 1), ("GICLR8",     U32, 1),
                          ("X1",         U32, 23))
GPIO_IDBE = 0x26, 4,0x24,(("GIDBE0",     U32, 1), ("GIDBE1",     U32, 1), ("GIDBE2",     U32, 1),
                          ("GIDBE3",     U32, 1), ("GIDBE4",     U32, 1), ("GIDBE5",     U32, 1),
                          ("GIDBE6",     U32, 1), ("GIDBE7",     U32, 1), ("GIDBE8",     U32, 1),
                          ("X1",         U32, 23))
GPIO_RAW  = 0x26, 4,0x28,(("GRAWP0",     U32, 1), ("GRAWP1",     U32, 1), ("GRAWP2",     U32, 1),
                          ("GRAWP3",     U32, 1), ("GRAWP4",     U32, 1), ("GRAWP5",     U32, 1),
                          ("GRAWP6",     U32, 1), ("GRAWP7",     U32, 1), ("GRAWP8",     U32, 1),
                          ("X1",         U32, 23))
DRX_TUNE0b= 0x27, 2,0x02,()
DRX_TUNE1a= 0x27, 2,0x04,()
DRX_TUNE1b= 0x27, 2,0x06,()
DRX_TUNE2 = 0x27, 4,0x08,()
DRX_SFDTOC= 0x27, 2,0x20,()
DRX_PRETOC= 0x27, 2,0x24,()
DRX_TUNE4H= 0x27, 2,0x26,()
DRX_CAR_INT=0x27, 2,0x28,()
RXPACC_NOSAT=0x27,2,0x2c,()
RF_CONF   = 0x28, 4,0x00,(("X1",         U32, 8), ("TXFEN",      U32, 5), ("PLLFEN",     U32, 3),
                          ("LDOFEN",     U32, 5), ("TXRXSW",     U32, 2), ("X2",         U32, 9))
RF_RXCTRLH= 0x28, 1,0x0b,()
RF_TXCTRL = 0x28, 3,0x0c,()
RF_STATUS = 0x28, 4,0x2c,(("CPLLLOCK",   U32, 1), ("CPLLLOW",    U32, 1), ("CPLLHIGH",   U32, 1),
                          ("RFPLLLOCK",  U32, 1), ("X1",         U32,28))
LDOTUNE   = 0x28, 5,0x30,()
TC_SARC   = 0x2a, 2,0x00,(("SAR_CTRL",   U32, 1), ("X1",         U32,15))
TC_SARL   = 0x2a, 3,0x03,(("SAR_LVBAT",  U32, 8), ("SAR_LTEMP",  U32, 8), ("X1",          U32, 8))
TC_SARW   = 0x2a, 2,0x06,(("SAR_WBAT",   U32, 8), ("SAR_WTEMP",  U32, 8))
TC_PG_CTRL= 0x2a, 4,0x08,(("PG_START",   U32, 1), ("X1",         U32, 1), ("PG_TMEAS",    U32, 3),
                          ("X2",         U32,27))
TC_PG_STATUS=0x2a,4,0x09,(("PG_DELAY_CNT",U32,12),("X1",         U32,20))
TC_PGDELAY= 0x2a, 1,0x0b,()
TC_PGTEST = 0x2a, 1,0x0c,()
FS_PLLCFG = 0x2b, 4,0x07,()
FS_PLLTUNE= 0x2b, 1,0x0b,()
FS_XTALT  = 0x2b, 1,0x0e,()
AON_WCFG  = 0x2c, 2,0x00,(("ONV_RAD",    U32, 1), ("ONW_RX",     U32, 1), ("X1",         U32, 1),
                          ("ONW_LEUI",   U32, 1), ("X2",         U32, 2), ("ONW_LDC",    U32, 1),
                          ("ONW_L64",    U32, 1), ("PRES_SLEE",  U32, 1), ("X2",         U32, 2),
                          ("ONW_LLDE",   U32, 1), ("ONW_LLD",    U32, 1), ("X1",         U32, 3))
AON_CTRL  = 0x2c, 1,0x02,(("RESTORE",    U32, 1), ("SAVE",       U32, 1), ("UPL_CFG",    U32, 1),
                          ("DCA_READ",   U32, 1), ("X1",         U32, 3), ("DCA_ENAB",   U32, 1))
AON_RDAT  = 0x2c, 1,0x03,()
AON_ADDR  = 0x2c, 1,0x04,()
AON_CFG0  = 0x2c, 4,0x06,(("SLEEP_EN",   U32, 1), ("WAKE_PIN",   U32, 1), ("WAKE_SPI",   U32, 1),
                          ("WAKE_CNT",   U32, 1), ("LPDIV_EN",   U32, 1), ("LPCLKDIVA",  U32,11),
                          ("SLEEP_TIM",  U32,16))
AON_CFG1  = 0x2c, 2,0x0a,(("SLEEP_CE",   U32, 1), ("SMXX",       U32, 1), ("LPOSC_C",    U32, 1),
                          ("X1",         U32,13))
OTP_WDAT  = 0x2d, 4,0x00,()
OTP_ADDR  = 0x2d, 2,0x04,(("OTP_ADDR",   U32,11), ("X1",         U32, 5))
OTP_CTRL  = 0x2d, 2,0x06,(("OTPRDEN",    U32, 1), ("OTPREAD",    U32, 1), ("X1",         U32, 1),
                          ("OTPMRWR",    U32, 1), ("X2",         U32, 2), ("OTPPROG",    U32, 1),
                          ("OTPMR",      U32, 4), ("X3",         U32, 4), ("LDELOAD",    U32, 1))
OTP_STATUS= 0x2d, 2,0x08,(("OTPPRGD",    U32, 1), ("OTPVPOK",    U32, 1), ("X1",         U32,14))
OTP_RDAT  = 0x2d, 4,0x0a,()
OTP_SRDAT = 0x2d, 4,0x0e,()
OTP_SF    = 0x2d, 1,0x12,(("OPS_KICK",   U32, 1), ("LDO_KICK",   U32, 1), ("X1",         U32, 3),
                          ("OPS_SEL",    U32, 2), ("X2",         U32, 1))
LDE_CFG1  = 0x2e, 1,0x0806,(("NTM",      U32, 5), ("PMULT",      U32, 3))
LDE_PPINDX= 0x2e, 2,0x1000,()
LDE_PPAMPL= 0x2e, 2,0x1002,()
LDE_RXANTD= 0x2e, 2,0x1804,()
LDE_CFG2  = 0x2e, 2,0x1806,()
LDE_REPC  = 0x2e, 2,0x2804,()
EVC_CTRL  = 0x2f, 4,0x00,(('EVC_EN',     U32, 1), ('EVC_CLR',    U32, 1), ('X1',         U32,30))
EVC_PHE   = 0x2f, 2,0x04,(('EVC_PHE',    U32,12), ('X1',         U32, 4))
EVC_RSE   = 0x2f, 2,0x06,(('EVC_RSE',    U32,12), ('X1',         U32, 4))
EVC_FCG   = 0x2f, 2,0x08,(('EVC_FCG',    U32,12), ('X1',         U32, 4))
EVC_FCE   = 0x2f, 2,0x0a,(('EVC_FCE',    U32,12), ('X1',         U32, 4))
EVC_FFR   = 0x2f, 2,0x0c,(('EVC_FFR',    U32,12), ('X1',         U32, 4))
EVC_OVR   = 0x2f, 2,0x0e,(('EVC_OVR',    U32,12), ('X1',         U32, 4))
EVC_STO   = 0x2f, 2,0x10,(('EVC_STO',    U32,12), ('X1',         U32, 4))
EVC_PTO   = 0x2f, 2,0x12,(('EVC_PTO',    U32,12), ('X1',         U32, 4))
EVC_FWTO  = 0x2f, 2,0x14,(('EVC_FWTO',   U32,12), ('X1',         U32, 4))
EVC_TXFS  = 0x2f, 2,0x16,(('EVC_TXFS',   U32,12), ('X1',         U32, 4))
EVC_HPW   = 0x2f, 2,0x18,(('EVC_HPW',    U32,12), ('X1',         U32, 4))
EVC_TPW   = 0x2f, 2,0x1a,(('EVC_TPW',    U32,12), ('X1',         U32, 4))
DIAG_TMC  = 0x2f, 2,0x24,(('X1',         U32, 4), ('TX_PSTM',    U32, 1), ('X2',         U32,11))
PMSC_CTRL0= 0x36, 4,0x00,(("SYSCLKS",    U32, 2), ("RXCLKS",     U32, 2), ("TXCLKS",     U32, 2),
                          ("FACE",       U32, 1), ("X1",         U32, 3), ("ADCCE",      U32, 1),
                          ("X2",         U32, 4), ("AMCE",       U32, 1), ("GPCE",       U32, 1),
                          ("GPRN",       U32, 1), ("GPDCE",      U32, 1), ("GPDRN",      U32, 1),
                          ("X3",         U32, 3), ("KHZCLKEN",   U32, 1), ("X4",         U32, 4),
                          ("SOFTRESET",  U32, 4))
PMSC_CTRL1= 0x36, 4,0x04,(("X1",         U32, 1), ("ARX2INIT",   U32, 1), ("X2",         U32, 1),
                          ("PKTSEQ",     U32, 8), ("ATXSLP",     U32, 1), ("ARXSLP",     U32, 1),
                          ("SNOZE",      U32, 1), ("SNOZR",      U32, 1), ("PLLSYN",     U32, 1),
                          ("X3",         U32, 1), ("LDERUNE",    U32, 1), ("X4",         U32, 8),
                          ("KHZCLKDIV",  U32, 6))
PMSC_SNOZT= 0x36, 1,0x0c,()
PMSC_TXFSEQ=0x36, 2,0x26,()
PMSC_LEDC = 0x36, 4,0x28,(("BLINK_TIM",  U32, 8), ("BLINKEN",    U32, 1), ("X1",          U32, 7),
                          ("BLNKNOW",    U32, 4), ("X1",         U32,12))

# Convert Tx channel to TXCTRL and PGDELAY and PLLTUNE values (tables 38, 40 & 44)
CHAN_RF_TXCTRL  = {1:0x5c40, 2:0x45ca0, 3:0x86cc0, 4:0x45c80, 5:0x1e3fe0, 7:0x1e7de0}
CHAN_TC_PGDELAY = {1:0xc9, 2:0xc2, 3:0xc5, 4:0x95, 5:0xc0, 7:0x93}
CHAN_FS_PLLTUNE = {1:0x1e, 2:0x26, 3:0x56, 4:0x26, 5:0xbe, 7:0xbe}

# Configuration values for Tx & Rx
TRX_RATES      = {110:0, 850:1, 6800:2}
PULSE_FREQS    = {16:1, 64:2}
PREAM_LEN_PE   = {64:0, 128:1, 256:2, 512:3, 1024:0, 1536:1, 2048:2, 4096:0}
PREAM_LEN_PSR  = {64:1, 128:1, 256:1, 512:1, 1024:2, 1536:2, 2048:2, 4096:3}
PREAM_CODES    = {1:(1,9), 2:(3,9), 3:(5,9), 4:(7,17), 5:(3,9), 7:(7,17)}
PAC_SIZES      = {64:8, 128:8, 256:16, 512:16, 1024:32, 2048:64, 4096:64}
FS_PLLCFGS     = {1:0x09000407, 2:0x08400508, 3:0x08401009, 4:0x08400508,
                  5:0x0800041D, 7:0x0800041D}
DRX_TUNE2S     = {8:(0x311A002D,0x313B006B), 16:(0x331A0052,0x333B00BE),
                 32:(0x351A009A,0x353B015E), 64:(0x371A011D,0x373B0296)}
PCODE_REPCS    = {1:0x5998,13:0x3AE0, 2:0x5998,14:0x35C2, 3:0x51EA,15:0x2B84,
                  4:0x428E,16:0x35C2, 5:0x451E,17:0x3332, 6:0x2E14,18:0x35C2,
                  7:0x8000,19:0x35C2, 8:0x51EA,20:0x47AE, 9:0x28F4,21:0x3AE0,
                 10:0x3332,22:0x3850,11:0x3AE0,23:0x30A2,12:0x3D70,24:0x3850}
TX_PWRS_SMRT   = {1:(0x15355575,0x07274767), 2:(0x15355575,0x07274767),
                  3:(0x0F2F4F6F,0x2B4B6B8B), 4:(0x1F1F3F5F,0x3A5A7A9A),
                  5:(0x0E082848,0x25456585), 7:(0x32527292,0x5171B1D1)}
TX_PWRS_DUMB   = {1:(0x75757575,0x67676767), 2:(0x75757575,0x67676767),
                  3:(0x6F6F6F6F,0x8B8B8B8B), 4:(0x5F5F5F5F,0x9A9A9A9A),
                  5:(0x48484848,0x85858585), 7:(0x92929292,0xD1D1D1D1)}
TX_PWRS        = TX_PWRS_SMRT if SMART_TX_POWER else TX_PWRS_DUMB

# Enable RXPHE, RXFCG, RXFCE, RXRFSL, RXRFTO, RXSFDTO, AFFREJ
SYS_MASK_VAL   = 0x2403D000

# Dictionary to track register values (for debugging)
regvals = {}

# DW1000 register class
class Reg(object):
    def __init__(self, regdef, val=0):
        self.name, self.value = regdef, val
        self.id, self.len, self.sub, self.fields = globals()[regdef]
        class struct(Structure):
            _fields_ = self.fields
        class union(Union):
            _fields_ = [("reg", struct), ("value", U64)]
        self.u = union()
        self.u.value = val
        self.reg = self.u.reg

    # Return the 1, 2 or 3-byte register address header
    def addr_hdr(self):
        return([self.id] if self.sub is None else
               [0x40+self.id, self.sub] if self.sub < 0x80 else
               [0x40+self.id, 0x80+(self.sub&0x7f), self.sub>>7])

    # Read a register value (optionally specify number of bytes)
    def read(self, spi, nbytes=None):
        nbytes = self.len if nbytes is None else nbytes
        hdr = self.addr_hdr()
        msg = nbytes*[0]
        resp = spi.xfer(hdr+msg)
        self.value = 0
        for n,b in enumerate(resp[len(hdr):]):
            self.value += b << (n*8)
        self.u.value = self.value
        return self

    # Write a register value (optionally specify number of bytes)
    def write(self, spi, nbytes=None):
        nbytes = self.len if nbytes is None else nbytes
        hdr = self.addr_hdr()
        hdr[0] |= 0x80
        msg = nbytes*[0]
        value = self.value
        for n in range(0, nbytes):
            msg[n] = value & 0xff
            value >>= 8
        spi.xfer(hdr+msg)
        if self.name not in regvals:
            regvals[self.name] = []
        regvals[self.name].append(self.value)
        return self

    # Set a field within a register
    def set(self, field, val):
        if hasattr(self.reg, field):
            setattr(self.reg, field, val)
        else:
            print("Unknown attribute: '%s'" % field)
        self.value = self.u.value
        return self

    # Return string with field values, optionally including zero values
    def field_vals(self, zeros=True):
        flds = [f[0] for f in self.fields if not f[0].startswith('X')]
        return " ".join([("%s:%x" % (f,getattr(self.reg, f))) for f in flds
                         if zeros or getattr(self.reg, f)])

# DW1000 chip class
class DW1000(object):
    def __init__(self, spi):
        self.spi = spi
        self.eui = None

    # Hardware reset
    def reset(self):
        self.spi.reset(True)
        msdelay(1)
        self.spi.reset(False)
        msdelay(10)
        Reg('DEV_ID').read(self.spi)

    # Soft reset
    def softreset(self):
        Reg('DEV_ID').read(self.spi)
        r = Reg('PMSC_CTRL0').read(self.spi)
        r.set('SYSCLKS', 1).write(self.spi)
        msdelay(5)
        r.set('SOFTRESET', 0).write(self.spi)
        r.set('SOFTRESET', 0xf).write(self.spi)
        r.set('SYSCLKS', 0).write(self.spi)
        msdelay(5)

    # Disable Tx and Rx
    def idle(spi):
        Reg('SYS_CTRL').set('TRXOFF', 1).write(spi)
        self.clear_status()

    # Clear status flags
    def clear_status(self):
        Reg('SYS_STATUS').read(self.spi).write(self.spi)

    # Initialise Dw1000
    def initialise(self, chan=DEF_CHAN, rate=DEF_RATE, prf=DEF_PULSE_FREQ, plen=DEF_PREAM_LEN):
      # Get preamble code
        pcode = PREAM_CODES[chan][prf==64]
      # Soft reset, read OTP
        self.softreset()
        self.read_otp(4)

      # Set leading-edge detection (LDE)
        r = Reg('PMSC_CTRL0').read(self.spi)
        r.set('SYSCLKS', 1).write(self.spi)
        msdelay(5)
        Reg('EC_CTRL').set('PLLLDT', 1).write(self.spi)
        Reg('OTP_SF').set('LDO_KICK', 1).write(self.spi)
        Reg('OTP_CTRL', 0x8000).write(self.spi)
        msdelay(5)
        r.set('GPDCE', 1).set('KHZCLKEN', 1).write(self.spi)
        r.set('SYSCLKS', 0).write(self.spi)
        msdelay(5)

      # Select required events
        Reg('SYS_MASK', SYS_MASK_VAL).write(self.spi)
      # Leading edge detection
        r = Reg('PMSC_CTRL1').set('PKTSEQ', 0xe7).set('LDERUNE', 1)
      # Enable slow clock, Rx & Tx LED pins
        r.set('KHZCLKDIV', 20).write(self.spi)
        Reg('GPIO_MODE').set('MSGP2', 1).set('MSGP3', 1).write(self.spi)
      # Set LED blink time, and blink LEDs
        r = Reg('PMSC_LEDC').set('BLINK_TIM', 10)
        r.set('BLINKEN', 1).write(self.spi)
        self.blink_leds()
      # Clear & enable event counters
        r = Reg('EVC_CTRL').set('EVC_CLR', 1).write(self.spi)
        r.set('EVC_CLR', 1).set('EVC_EN', 1).write(self.spi)
      # System config reg
        r = Reg('SYS_CFG').set('DIS_STXP', 0 if SMART_TX_POWER else 1)
        r.set('DIS_DRXB', 0 if RX_DOUBLE_BUFF else 1)
        r.set('PHR_MODE', 3 if LONG_FRAMES else 0)
        r.set('RXAUTR', RX_AUTO_EN).set('AUTOACK', AUTO_ACK)
        r.set('RXM110K', rate==110).set('HIRQ_POL', 1).write(self.spi)
      # Leading edge detection
        Reg('LDE_REPC', PCODE_REPCS[pcode] >> (3*(rate==110))).write(self.spi)
        Reg('LDE_CFG1').set('NTM', 0xd).set('PMULT', 3).write(self.spi)
        Reg('LDE_CFG2', 0x1607 if prf==16 else 0x0607).write(self.spi)
      # Frequency synthesiser
        Reg('FS_PLLCFG', FS_PLLCFGS[chan]).write(self.spi)
        Reg('FS_XTALT', 0x72).write(self.spi)
      # Channel selection
        Reg('RF_RXCTRLH', 0xbc if (chan==4 or chan==7) else 0xd8).write(self.spi)
        Reg('RF_TXCTRL', CHAN_RF_TXCTRL[chan]).write(self.spi)
      # Digital tuning
        Reg('DRX_TUNE0b', 0x16 if rate==110 else 6 if rate==850 else 1).write(self.spi)
        Reg('DRX_TUNE1a', 0x87 if prf==16 else 0x8d).write(self.spi)
        Reg('DRX_TUNE1b', 0x64 if rate==110 and plen>1024 else
                          0x10 if rate==6800 and plen==64 else 0x20).write(self.spi)
        Reg('DRX_TUNE2', DRX_TUNE2S[PAC_SIZES[plen]][prf==64]).write(self.spi)
        Reg('DRX_TUNE4H', 0x10 if plen==64 else 0x28).write(self.spi)
        Reg('AGC_TUNE1', 0x8870 if prf==16 else 0x889b).write(self.spi)
        Reg('AGC_TUNE2', 0x2502A907).write(self.spi)
        Reg('AGC_TUNE3', 0x0035).write(self.spi)
      # Set channels and preamble code
        r = Reg('CHAN_CTRL').set('TX_CHAN', chan).set('RX_CHAN', chan)
        r.set('RXPRF', PULSE_FREQS[prf]).set('TX_PCODE', pcode)
        r.set('RX_PCODE', pcode).write(self.spi)
      # Set transmit frame control
        r = Reg('TX_FCTRL').set('TXBR', TRX_RATES[rate])
        r.set('TXPRF', PULSE_FREQS[prf]).set('PE', PREAM_LEN_PE[plen])
        r.set('TXPSR', PREAM_LEN_PSR[plen]).set('TR', 1).write(self.spi)
      # Set Rx & Tx delays, and Tx power
        Reg('LDE_RXANTD').write(self.spi)
        Reg('TX_ANTD').write(self.spi)
        Reg('TC_PGDELAY', CHAN_TC_PGDELAY[chan]).write(self.spi)
        Reg('TX_POWER', TX_PWRS[chan][prf==64]).write(self.spi)
      # Clear status flags
        self.clear_status()

    # Set LEDs on for 85 msec
    def blink_leds(self):
        r = Reg('PMSC_LEDC').read(self.spi).set('BLNKNOW', 0xf).write(self.spi)
        r.set('BLNKNOW', 0).write(self.spi)

    # Send data to Tx buffer
    def set_txdata(self, data):
        hdr = [TX_BUFFER[0] + 0x80]
        self.spi.xfer(hdr + data)
        Reg('TX_FCTRL').read(self.spi).set('TFLEN', len(data)+2).write(self.spi)

    # Get Tx timestamp
    def tx_time(self):
        return Reg('TX_TIME1').read(self.spi).reg.TX_STAMP

    # Transmit with optional delay, and enabling receiver afterwards
    def start_tx(self, delay=None, rx=False):
        ctrl = Reg('SYS_CTRL')
        if delay is not None:
            t = Reg('SYS_TIME').read(self.spi).value + delay
            Reg('DX_TIME', t).write(self.spi)
            ctrl.set('TXDLYS', 1)
        ctrl.set('TXSTRT', 1).set('WAIT4RESP', rx).write(self.spi)

    # Enable receiver
    def start_rx(self):
        self.clear_interrupt()
        Reg('SYS_CTRL').set('RXENAB', 1).write(self.spi)

    # Restart receiver after error
    def restart_rx(self):
        self.idle()
        self.softreset()
        #if RX_AUTO_EN:
        self.start_rx()

    # Check receiver
    def check_rx(self):
        rxdata = []
        status = Reg('SYS_STATUS')
        if USE_INTERRUPT:
            irq = self.check_interrupt()
            if irq:
                status.read(self.spi)
        else:
            status.read(self.spi)
            irq = status.irqs
        if irq:
            if status.reg.LDEDONE:
                rxdata = self.rx_data()
            status.write(self.spi)
        return rxdata

    # Get Rx data
    def get_rxdata(self):
        rxdata = []
        if self.check_interrupt():
            status = Reg('SYS_STATUS').read(self.spi)
            if status.reg.RXDFR:
                rxdata = self.rx_data()
        return rxdata

    # Return status string
    def sys_status(self):
        status = Reg('SYS_STATUS').read(self.spi)
        print("Status %s %s" % (self.spi.ident, status.field_vals(False)))

    # Pulse hardware IRQ pin
    def pulse_irq(self):
        mode = Reg('GPIO_MODE').read(self.spi).set('MSGP8', 1).write(self.spi)
        dirn = Reg('GPIO_DIR').read(self.spi).set('GDP8', 0).set('GDM8', 1).write(self.spi)
        dout = Reg('GPIO_DOUT').read(self.spi).set('GOP8', 1).set('GOM8', 1).write(self.spi)
        msdelay(10)
        dout.set('GOP8', 0).write(self.spi)
        mode.set('MSGP8', 0).write(self.spi)

    # Clear events in interrupt register
    def clear_irq(self):
        Reg('SYS_STATUS').read(self.spi).write(self.spi)

    # Check for IRQ from network
    def check_irq(self):
        if not self.spi.interrupt:
            self.spi.receive(True)
        return self.spi.interrupt

    # Clear interrupt flag
    def clear_interrupt(self):
        self.spi.interrupt = False

    # Test IRQ pin operation
    def test_irq(self):
        self.pulse_irq()
        ret = self.check_irq()
        self.clear_interrupt()
        return ret

    # Check for interrupt; if no IRQ, check status reg
    def check_interrupt(self):
        interrupt = self.check_irq()
        if not interrupt:
            print("Missed interrupt")
            interrupt = Reg('SYS_STATUS').read(self.spi).reg.IRQS
        return interrupt

    # Get data from Rx buffer, excluding CRC
    def rx_data(self):
        nbytes = Reg('RX_FINFO').read(self.spi).reg.RXFLEN
        if not LONG_FRAMES:
              nbytes &= 0x7f
        if nbytes > 2:
            hdr = [RX_BUFFER[0]]
            data = nbytes * [0]
            resp = self.spi.xfer(hdr + data)
            return tuple(resp[1:-2])
        return []

    # Get Rx timestamp
    def rx_time(self):
        return Reg('RX_TIME1').read(self.spi).reg.RX_STAMP

    # Cancel Tx or Rx, return to idle state
    def idle(self):
        Reg('SYS_CTRL').set('TRXOFF', 1).write(self.spi)

    # Set PAN ID and short address
    def set_panadr(self, pan=DEF_PAN, addr=DEF_ADDR):
        Reg('PANADR').set('PAN_ID', pan).set('SHORT_ADDR', addr).write(self.spi)

    # Read 4 to 8-byte value from OTP memory
    def read_otp(self, addr, nbytes=4):
        self.set_clock("xti")
        Reg('OTP_ADDR').set('OTP_ADDR', addr).write(self.spi)
        r = Reg('OTP_CTRL').set('OTPRDEN', 1).set('OTPREAD', 1).write(self.spi)
        r.set('OTPREAD', 0).write(self.spi)
        val = Reg('OTP_RDAT').read(self.spi).value
        if nbytes > 4:
            Reg('OTP_ADDR').set('OTP_ADDR', addr+4).write(self.spi)
            r.set('OTPREAD', 1).write(self.spi)
            r.set('OTPREAD', 0).write(self.spi)
            val |= Reg('OTP_RDAT').read(self.spi, nbytes-4).value << 32
        r.set('OTPRDEN', 0).write(self.spi)
        self.set_clock("auto")
        return val

    # Set the system clocks
    def set_clock(self, clk="auto"):
        r = Reg('PMSC_CTRL0').read(self.spi)
        if clk == "auto":
            r.set('SYSCLKS', 0).set('RXCLKS', 0).set('TXCLKS', 0)
        elif clk == "xti":
            r.set('SYSCLKS', 1)
        elif clk == "pll":
            r.set('SYSCLKS', 2)
        r.write(self.spi)
        msdelay(5)

# Millisecond time delay
def msdelay(msec):
    time.sleep(msec / 1000.0)

# Return length of address header
def hdr_len(data):
    return 0 if len(data)<2 else 1 if (data[0]&0x40)==0 else 2 if (data[1]&0x80==0) else 3

# Return string with hex header & data values, separated by ':'
def data_str(data, oset=0):
    hlen = hdr_len(data) + oset
    s = "" if len(data)<2 else " ".join(["%02X" % b for b in data[:hlen]]) + ':'
    return s + " ".join(["%02X" % b for b in data[hlen:]])

# EOF
