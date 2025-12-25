from machine import UART, Pin
import time

uart = UART(0, baudrate=9600, tx=Pin(12), rx=Pin(13))

def send(cmd, wait=2):
    uart.write(cmd + "\r\n")
    time.sleep(wait)
    resp = b""
    while uart.any():
        resp += uart.read()
    print(resp.decode(errors="ignore"))

time.sleep(5)

send("AT")
send("ATE0")
send("AT+CPIN?")
send("AT+CSQ")
send("AT+CREG?")
send("AT+CGATT=1")

send('AT+CSTT="internet","",""')
send("AT+CIICR", 5)
send("AT+CIFSR")

send("AT+CIPSTATUS")
