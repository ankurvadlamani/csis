from machine import SPI, Pin
import time

SCK = 2
MOSI = 3
MISO = 4
CS = 5
RST = 6
DIO0 = 7

spi = SPI(
    0,
    baudrate=5_000_000,
    polarity=0,
    phase=0,
    bits=8,
    firstbit=SPI.MSB,
    sck=Pin(SCK),
    mosi=Pin(MOSI),
    miso=Pin(MISO)
)

cs = Pin(CS, Pin.OUT, value=1)
rst = Pin(RST, Pin.OUT)
dio0 = Pin(DIO0, Pin.IN)

def write_reg(addr, value):
    cs.value(0)
    spi.write(bytearray([addr | 0x80, value]))
    cs.value(1)

def read_reg(addr):
    cs.value(0)
    spi.write(bytearray([addr & 0x7F]))
    val = spi.read(1)[0]
    cs.value(1)
    return val

def lora_reset():
    rst.value(0)
    time.sleep(0.1)
    rst.value(1)
    time.sleep(0.1)

def set_frequency(freq_hz):
    frf = int(freq_hz / 61.03515625)
    write_reg(0x06, (frf >> 16) & 0xFF)
    write_reg(0x07, (frf >> 8) & 0xFF)
    write_reg(0x08, frf & 0xFF)

def lora_init():
    lora_reset()
    version = read_reg(0x42)
    if version != 0x12:
        raise Exception("LoRa not detected")
    write_reg(0x01, 0x80)
    time.sleep(0.1)
    write_reg(0x01, 0x81)
    set_frequency(433_000_000)
    write_reg(0x09, 0x8F)
    write_reg(0x0C, 0x23)
    write_reg(0x1D, 0x72)
    write_reg(0x1E, 0x74)
    write_reg(0x20, 0x00)
    write_reg(0x21, 0x08)

def lora_send(payload):
    write_reg(0x01, 0x81)
    write_reg(0x0E, 0x00)
    write_reg(0x0D, 0x00)
    for b in payload:
        write_reg(0x00, b)
    write_reg(0x22, len(payload))
    write_reg(0x01, 0x83)
    while dio0.value() == 0:
        pass
    write_reg(0x12, 0x08)

lora_init()

while True:
    lora_send(b"HELLO LORA")
    time.sleep(3)
