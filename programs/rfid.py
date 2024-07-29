from machine import Pin
from dht import DHT11
import asyncio
from ws2812 import WS2812
import utime

ws = WS2812(Pin(28), 12)
pin = Pin(13, Pin.IN, Pin.PULL_UP)
sensor = DHT11(pin)
led = Pin(15, Pin.OUT)
utime.sleep(1)
btn1 = Pin(6, Pin.IN)
print(0//12)
led.value(0)
print(f"on {led.value()}")

def handle_interrupt(pin):
    led.toggle()
    utime.sleep(0.5)

btn1.irq(trigger=Pin.IRQ_RISING, handler=handle_interrupt)
start=utime.time()
# async def Get_Button():
#     while True:
#         if btn1.value():
            
#             print(btn1.value())
#             led.toggle()
#             print(f"led value: {led.value()}")
#             await asyncio.sleep(1)
temp = 0
hum = 0
async def Get_Sensor():
    global temp, hum
    while True:
        if led.value():
            try:
                sensor.measure()
                temp = sensor.temperature()
                hum = sensor.humidity()
                print(f"\rTemp: {temp}\tHum: {hum}\tled: {led.value()}\tsince: {utime.time()-start}",end="")
                await asyncio.sleep(1)
            except OSError:
                print("oserror")
        else: 
            temp, hum = 0, 0
            print("led not true")
            await asyncio.sleep(0.5)

async def Show_WS():
    global temp, hum
    print(temp, temp-24)
    while True:
        newtemp = temp - 24
        newhum = hum // 8
        color=[0x000000 for i in range(12)]
        for i in range(12):
            if i+1 <= newtemp:
                color[i] += 0x010000
            if i+1 <= newhum:
                color[i] += 0x000001
            if i+1 > newtemp and i > newhum:
                color[i] = 0x000000
        for idx, i in enumerate(color):
            ws.write(idx, (i))
        await asyncio.sleep(1)


    
async def main():
    await asyncio.gather(Get_Sensor(), Show_WS())

if __name__ == "__main__":
    asyncio.run(main())
