from machine import Pin, ADC
import asyncio
import utime

led = Pin(15, Pin.OUT)
mic = ADC(26)

ambient_noise = sum(mic.read_u16() for i in range(100)) / 100
print("ambient: ", ambient_noise*1.8)
utime.sleep(1)
noise = 0
lastclap = 0


# async def getnoise():
#     global noise
#     while True:
#         noise = mic.read_u16()
#         await asyncio.sleep(0.1)

# async def clap():
#     global noise, lastclap
#     while True:
#         if (noise > ambient_noise*1.8) and (utime.ticks_ms() - lastclap > 500):
#             led.toggle()
#             print(" last: ",noise)
#             print(utime.ticks_ms() - lastclap)
#             lastclap = utime.ticks_ms()
#         await asyncio.sleep(0.1)

# async def shownoise():
#     global noise
#     while True:
#         print(f"\r{noise}", end="")
#         await asyncio.sleep(0.1)
        


# async def main():
#     # threading.Thread(target=getnoise(), daemon=True).start()
#     await asyncio.gather(getnoise(),shownoise(), clap())
#     # await asyncio.gather(shownoise(noise), clap(noise))
        
# if __name__ == "__main__":
#     asyncio.run(main())


while True:
    noise = mic.read_u16()
    print("\r",noise, end="")
    if (noise > ambient_noise*2):
        led.toggle()
        print(" last: ",noise)
        utime.sleep(0.5)