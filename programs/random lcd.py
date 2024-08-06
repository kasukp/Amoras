from machine import Pin
import LCD
from colour import colour
import time
import asyncio
import random


display = LCD.LCD_1inch3()
display.fill(0)

path = r"/assets/kasu.txt"
with open(path, "rt") as f:
    read = f.read()
print(read[6740])

start = time.time()

async def draw_image():
    while True:
        print("world")
        for y in range(120):
            yline = y * 122
            for x in range(120):
                pix = yline + x
                print(pix, read[pix], x, y)
                if read[pix] == '1':
                    display.pixel(x,y, colour(255,0,0))
                elif read[pix] == '0':
                    display.pixel(x,y, colour(0,0,255))
                else:
                    pass
            await asyncio.sleep(0.017)

async def display_loop():
    while True:
        display.fill(0)
        await asyncio.sleep(0.1)
        display.show()
        

async def main():    
    asyncio.gather(draw_image(), display_loop())

if __name__ == "__main__":
    asyncio.run(main())