from machine import Pin
import utime

led = Pin(15, Pin.OUT)

led.toggle()