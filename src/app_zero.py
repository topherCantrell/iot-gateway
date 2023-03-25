
import asyncio
import aiohttp.web  # sudo python3 -m pip install aiohttp
import hardware

''' 
- Add this line to /etc/rc.local (before the exit 0):
-   /home/pi/ONBOOT.sh 2> /home/pi/ONBOOT.errors > /home/pi/ONBOOT.stdout &
- Add the following ONBOOT.sh script to /home/pi and make it executable:
  
#!/bin/bash
cd /home/pi/iot-gateway
python3 app_zero.py  
'''
TIME_POLL = 100  # tenths of a second between pollings (10)

COLOR_START = (100, 100, 100)
COLOR_OK = (0, 10, 0)
COLOR_BAD = (255, 0, 0)
COLOR_COMM = (0xFF,0xE9,0x00)

HARD = hardware.Hardware()

async def get_color():
    try:
        async with aiohttp.ClientSession() as session:
            url = 'http://192.168.1.108/data/freezer'
            async with session.get(url) as resp: 
                data = await resp.json()                    
                temperature = data['value']       
                # print(temperature)                         
                if temperature > -5:
                    return COLOR_BAD                        
                else:
                    return COLOR_OK                        
    except Exception as f:
        # print(f)
        return COLOR_COMM

async def task_check_temperature():  
    
    brightness = 1.0
    color = COLOR_START
    pulse = -1  # Which way the brigtness is changing    
    tick = 0.1 # Tenths of a second tick

    while True:
        await asyncio.sleep(0.1) # Tenth of a second
        tick -= 1        
        if tick <= 0:
            tick = TIME_POLL
            color = await get_color()
        HARD.set_color(color,brightness)
        # We pulse in the main loop instead of a separate task. That way
        # we show visual evidence that the polling loop is running.
        brightness = brightness+(pulse*0.1)
        if brightness > 1.0:
            pulse = -1  # Going down now
            brightness = 1.0
        elif brightness < 0.1:
            pulse = 1
            brightness = 0.1         


# In the future, this will be a full website with info
asyncio.run(task_check_temperature())
