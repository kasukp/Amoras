from machine import Pin, ADC
import LCD
from colour import colour
import asyncio
import math
import sys

print(sys.version)

hue_potentiometer = ADC(26)
analog_x = ADC(27)
analog_y = ADC(28)

display = LCD.LCD_1inch3()
display.fill(0)

upButton = Pin(18, Pin.IN, Pin.PULL_UP)
downButton = Pin(19, Pin.IN, Pin.PULL_UP)
leftButton = Pin(20, Pin.IN, Pin.PULL_UP)
rightButton = Pin(21, Pin.IN, Pin.PULL_UP)

analog_button = Pin(16, Pin.IN, Pin.PULL_UP)


last_paint_time = 0
debounce = 250
        
    
async def read_cursor():
    counter = 0
    while True:
        read = [analog_x.read_u16() / 65536, analog_y.read_u16() / 65536]
        await asyncio.sleep(0.01)
        counter += 1
        print(counter)
        await get_analog_button()
        if read[0] > 0.8:
            await cursor.move("down")
            asyncio.sleep(1)
        elif read[0] < 0.2:
            await cursor.move("up")
            asyncio.sleep(1)
        if read[1] > 0.8:
            await cursor.move("right")
            asyncio.sleep(1)
        elif read[1] < 0.2:
            await cursor.move("left")
            asyncio.sleep(1)
        await asyncio.sleep(0.01)
        
        
async def get_analog_button():
    paint_mode = False
    while True:
        if not analog_button.value():
            paint_mode = not paint_mode
            print(paint_mode)
            await asyncio.sleep(0.1)
        if paint_mode:
            cursor.set(0, hue_potentiometer.read_u16() / 65536)
        await asyncio.sleep(0.05)
        break
        

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
    
    async def move(self, direction):
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
        await asyncio.sleep(0.2)

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
        
# adapted from:
# https://github.com/bottosson/bottosson.github.io/blob/master/misc/colorpicker/colorconversion.js
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


# testing fn
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