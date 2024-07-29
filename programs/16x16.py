from machine import Pin
import LCD
from colour import colour
import asyncio
import framebuf
import utime
import math

display = LCD.LCD_1inch3()
display.fill(0)

upButton = Pin(18, Pin.IN, Pin.PULL_UP)
downButton = Pin(19, Pin.IN, Pin.PULL_UP)
leftButton = Pin(20, Pin.IN, Pin.PULL_UP)
rightButton = Pin(21, Pin.IN, Pin.PULL_UP)

paintButton = Pin(22, Pin.IN, Pin.PULL_UP)

last_paint_time = 0
debounce = 250

def handle_interrupt(pin):
    current_time = utime.ticks_ms()
    if pin == upButton:
        cursor.move("right")
    elif pin == downButton:
        cursor.move("up")
    elif pin == leftButton:
        cursor.set("hueUP")
    elif pin == rightButton:
        cursor.set("delete")
    elif pin == paintButton:
        if utime.ticks_diff(current_time, last_paint_time) > debounce:
            print("hey listen")
        else:
            print("fuck")


upButton.irq(trigger=Pin.IRQ_RISING, handler=handle_interrupt)
downButton.irq(trigger=Pin.IRQ_RISING, handler=handle_interrupt)
leftButton.irq(trigger=Pin.IRQ_RISING, handler=handle_interrupt)
rightButton.irq(trigger=Pin.IRQ_RISING, handler=handle_interrupt)
paintButton.irq(trigger=Pin.IRQ_RISING, handler=handle_interrupt)

async def display_loop():
    while True:
        display.fill(0)
        for idx, color in enumerate(screen.pixels):
            if not color:
                pass
            else:
                rgb_color = hsv_to_rgb(color[0], color[1], color[2])
                display.rect((idx//16*16), (idx%16*16), 15, 15, rgb_color, True)
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
            else: self.y = 14

        elif direction == "left":
            if self.x > 0:
                self.x -= 1
            else: self.x = 0

        elif direction == "right":
            if self.x < 14:
                self.x += 1
            else: self.x = 0

    def set(self, set):
        print(screen.get_color())
        hue = screen.get_color()[0]
        if set == "hueUP":
            print("hueUP:", hue)
            if hue == 1:
                hue = 0.0625
            else: hue += 0.0625
            screen.paint([hue, 0.8,1])
        elif set == "delete":
            screen.paint([0,0,0])

    async def draw(self):
        while True:
            display.rect(self.x*16,self.y*16,15,15, colour(0,255,0))
            # print(f"\r{self.x}  {self.y} ", end="")
            await asyncio.sleep(0.017)

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


cursor = Cursor(0,14)
screen = Display()
async def main():
    global cursor
    await asyncio.gather(cursor.draw(), display_loop())
    


if __name__ == "__main__":
    asyncio.run(main())