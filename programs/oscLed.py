import machine
import utime

led = machine.PWM(machine.Pin(15))
led.freq(1000)

for brilho in range(0,65535,50):
    led.duty_u16(brilho)
    utime.sleep_ms(10)
led.duty_u16(0)