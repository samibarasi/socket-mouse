import asyncio, evdev

touch1 = evdev.InputDevice('/dev/input/event13')
touch2 = evdev.InputDevice('/dev/input/event15')

async def print_events(device):
    async for event in device.async_read_loop():
        print(device.path, evdev.categorize(event), sep=': ')

for device in touch1, touch2:
    asyncio.ensure_future(print_events(device))

loop = asyncio.get_event_loop()
loop.run_forever()
