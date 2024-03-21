'''
https://learn.adafruit.com/multi-tasking-with-circuitpython/multiple-leds
https://learn.adafruit.com/cooperative-multitasking-in-circuitpython-with-asyncio/concurrent-tasks


'''

import asyncio

class TaskSync:
    def __init__(self):
        self.hello_done = False

async def print_hello(task_sync):
    while True:
        if task_sync.hello_done:
           await asyncio.sleep(0)
           print("@")
        else:   
            print("hello ")
            task_sync.hello_done = True
        await asyncio.sleep(2.5)
    
async def print_world(task_sync):
    while True:
        if not task_sync.hello_done:
            await asyncio.sleep(0.1)
            print("#")
        else:    
            print("world ")
            task_sync.hello_done = False
        # await asyncio.sleep(1.0)

async def main():
    task_sync = TaskSync()
    hello_task = asyncio.create_task(print_hello(task_sync))
    world_task = asyncio.create_task(print_world(task_sync))
    await asyncio.gather(hello_task, world_task)
    
asyncio.run(main())

