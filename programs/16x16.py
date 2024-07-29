from machine import Pin
import LCD
from colour import colour
import asyncio
import framebuf
import utime

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
        cursor.move("up")
    elif pin == downButton:
        cursor.move("down")
    elif pin == leftButton:
        cursor.move("left")
    elif pin == rightButton:
        cursor.move("right")
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
        await asyncio.sleep(0.017)
        display.show()
        


class Cursor():
    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y
    
    def move(self, direction):
        if direction == "up":
            if self.y > 0:
                self.y -= 1
            else: self.y = 0

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

    async def draw(self):
        while True:
            display.rect(self.x*16,self.y*16,15,15, colour(0,255,0))
            print(f"\r{self.x}  {self.y} ", end="")
            await asyncio.sleep(0.017)

cursor = Cursor(2,2)
async def main():
    global cursor
    await asyncio.gather(cursor.draw(), display_loop())
    


if __name__ == "__main__":
    asyncio.run(main())