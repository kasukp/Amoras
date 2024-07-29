import machine
import utime
from ws2812 import WS2812
ws = WS2812(machine.Pin(28),12)

btn1 = machine.Pin(18,machine.Pin.IN)
btn2 = machine.Pin(19,machine.Pin.IN)
btn3 = machine.Pin(20,machine.Pin.IN)
btn4 = machine.Pin(21,machine.Pin.IN)

btn1_state = 0
btn2_state = 0
btn3_state = 0
btn4_state = 0

while True:
    btn1_state = btn1.value()
    btn2_state = btn2.value()
    btn3_state = btn3.value()
    btn4_state = btn4.value()
    
    if btn1_state == 1:
        ws.write_all(0x444444)
    elif btn2_state == 1:
        ws.write_all(0x888888)
    elif btn3_state == 1:
        ws.write_all(0xFFFFFF)
    elif btn4_state == 1:
        ws.write_all(0x000000)
        utime.sleep(0.01)
