import asyncio
import degit5161as_esp
import ws2812_esp

async def task1():
    while True:
        degit5161as_esp.test()
        await asyncio.sleep(1)

async def task2():
    while True:
        ws2812_esp.demo()
        await asyncio.sleep(1)

async def main():
    asyncio.create_task(task1())
    asyncio.create_task(task2())
    await asyncio.sleep(1000)

asyncio.run(main())
