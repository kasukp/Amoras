from machine import Pin
import LCD
from colour import colour
import random
import framebuf
import utime

led = Pin(15, Pin.OUT)
led.value(0)

display = LCD.LCD_1inch3()
path = r"/assets/kasu.txt"
with open(path, "rt") as f:
    read = f.read()
print(read[6740])
#fbuf = framebuf.FrameBuffer(bytearray(100*10*2), 100, 10, framebuf.RGB565)
#fbuf.fill(0)
#fbuf.text("hello world!", 0, 0, 0xffff)
#fbuf.hline(0, 9, 96, 0xffff)
print(machine.freq())
start = utime.time()

# for x in range(0, 120):
#     for y in range(0, 120):
#         display.pixel(x, y, colour(255,0,0))
#     display.show()
for y in range(120):
    yline = y * 122
    for x in range(120):
        pix = yline + x
        #print(pix, read[pix], x, y)
        if read[pix] == '1':
            display.pixel(x,y, colour(255,0,0))
        elif read[pix] == '0':
            display.pixel(x,y, colour(0,0,255))
        else:
            pass
    display.show()
#        display.pixel(x, y, colour(R,G,B))
        #print(f"x:{x} y:{y}\nR:{R} G:{G} B:{B}\n")
display.show()
print(utime.time() - start)
#for i in range(400):
#    display.pixel(None, bytearray([random.getrandbits(8)]))
#display.show()


led.value(1)