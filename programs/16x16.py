from machine import Pin, ADC
import LCD
from colour import colour
import asyncio
import time
import math
import sys

print(sys.version)

hue_potentiometer = ADC(26)
analog_x = ADC(27)
analog_y = ADC(28)
# while True:
#     print(f"\rX = {analog_x.read_u16()}\n\rY = {analog_y.read_u16()}\n\r{hue_potentiometer.read_u16()}")
#     time.sleep(0.05)

display = LCD.LCD_1inch3()
display.fill(0)

upButton = Pin(18, Pin.IN, Pin.PULL_UP)
downButton = Pin(19, Pin.IN, Pin.PULL_UP)
leftButton = Pin(20, Pin.IN, Pin.PULL_UP)
rightButton = Pin(21, Pin.IN, Pin.PULL_UP)

analog_button = Pin(16, Pin.IN, Pin.PULL_UP)


last_paint_time = 0
debounce = 250

def read_analog_stick(x, y, filter):
    return [x.read_u16() / 65536, y.read_u16() / 65536]
    # while True:
    #     x_list, y_list = list(), list()
    #     for i in range(filter):
    #         x_list.append(x.read_u16() / 65536)
    #         y_list.append(y.read_u16() / 65536)
    #     x_out = sum(x_list) / filter
    #     y_out = sum(y_list) / filter
    #     asyncio.sleep(0.3)
    #     yield [x_out, y_out]
        
    
async def read_cursor():
    while True:
        read = [analog_x.read_u16() / 65536, analog_y.read_u16() / 65536]
        print(f"\r{read}", end="")
        await asyncio.sleep(0.02)
        if not analog_button.value():
            prev_x, prev_y = cursor.x, cursor.y
            print(prev_x, cursor.x)
            while prev_x == cursor.x and prev_y == cursor.y:
                cursor.set(0, hue_potentiometer.read_u16() / 65536)
                await asyncio.sleep(0.02)


        if read[0] > 0.8:
            cursor.move("left")
        elif read[0] < 0.2:
            cursor.move("right")
        if read[1] > 0.8:
            cursor.move("up")
        elif read[1] < 0.2:
            cursor.move("down")
        await asyncio.sleep(0.2)
            



# Buttons are temporarily incorrectly assigned for lack of components
async def handle_interrupt(pin):
    if pin == upButton:
        cursor.move("right")
    elif pin == downButton:
        cursor.move("up")
    elif pin == leftButton:
        cursor.set("hueUP")
    elif pin == rightButton:
        cursor.set("delete")
    


        
    


upButton.irq(trigger=Pin.IRQ_RISING, handler=handle_interrupt)
downButton.irq(trigger=Pin.IRQ_RISING, handler=handle_interrupt)
leftButton.irq(trigger=Pin.IRQ_RISING, handler=handle_interrupt)
rightButton.irq(trigger=Pin.IRQ_RISING, handler=handle_interrupt)

async def hue_selector():
    while True:
        hue_list = list()
        for i in range(50):
            hue_list.append(hue_potentiometer.read_u16() / 65536)
        hue = sum(hue_list) / 50
        #print(f"\r{hue:<3}", end="")
        await asyncio.sleep(0.05)

async def display_loop():
    while True:
        display.fill(0)
        for idx, color in enumerate(screen.pixels):
            if not color:
                pass
            else:
                x_pos, y_pos = divmod(idx,16)
                rgb_color = hsv_to_rgb(color[0], color[1], color[2])
                display.rect((x_pos*16), (y_pos*16), 15, 15, rgb_color, True)
        await asyncio.sleep(0.017)
        display.show()
        
class Cursor():
    def __init__(self, x = 0, y = 0, color = colour(0,0,0)):
        self.x = x
        self.y = y
        self.color = color
    
    def move(self, direction):
        if direction == "up":
            if self.y > 0:
                self.y -= 1
            else: self.y = 14

        elif direction == "down":
            if self.y < 14:
                self.y += 1
            else: self.y = 0

        elif direction == "left":
            if self.x > 0:
                self.x -= 1
            else: self.x = 14

        elif direction == "right":
            if self.x < 14:
                self.x += 1
            else: self.x = 0

    def set(self, set, pot):
        print(screen.get_color())
        hue = screen.get_color()[0]
        if pot:
            screen.paint([pot, 0.8, 1])
            return
        if set == "hueUP":
            print("hueUP:", hue)
            if hue >= 1:
                hue = 0.0625
            else: hue += 0.0625
            screen.paint([hue, 0.8,1])
        elif set == "delete":
            screen.paint([0,0,0])

    async def draw(self):
        while True:
            display.rect(self.x*16,self.y*16,15,15, colour(0,255,0))
            # print(f"\r{self.x}  {self.y} ", end="")
            await asyncio.sleep(0.03)

class Display():
    def __init__(self):
        self.pixels = [[0,0,0] for i in range(16*16)]
    
    def paint(self, color):
        print("paint:", color)
        pos = cursor.x * 16 + cursor.y
        self.pixels[pos] = color
    
    def get_color(self):
        return self.pixels[cursor.x * 16 + cursor.y]
        

def hsv_to_rgb(h,s,v):
    r,g,b = 0,0,0
    
    i = math.floor(h*6)
    f = h * 6 - i
    p = v * (1 - s)
    q = v * (1 - f * s)
    t = v * (1 - (1 - f) * s)

    if i % 6 == 0:
        r,g,b = v,t,p
    elif i % 6 == 1:
        r,g,b = q,v,p
    elif i % 6 == 2:
        r,g,b = p,v,t
    elif i % 6 == 3:
        r,g,b = p,q,v
    elif i % 6 == 4:
        r,g,b = t,p,v
    elif i % 6 == 5:
        r,g,b = v,p,q
    
    # return [r * 255, g * 255, b * 255]
    return colour(r * 255, g * 255, b * 255)

def draw_rainbow():
    for i in range(16):
        for j in range(16):
            display.rect(i*16,j*16,15,15,hsv_to_rgb(i*j/256,0.8,0.9),True)


async def main():
    global cursor
    global screen
    cursor = Cursor(0,14)
    screen = Display()
    
    await asyncio.gather(cursor.draw(), read_cursor(), hue_selector(), display_loop())
    
    


if __name__ == "__main__":
    asyncio.run(main())