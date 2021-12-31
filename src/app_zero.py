
from Adafruit_IO import Client
import json
import requests
import time

import board
import neopixel

''' 
- sudo python3 -m pip install adafruit-io rpi_ws281x adafruit-circuitpython-neopixel
- File /home/pi/config.json:
{
    "aio_user" : "topher_cantrell",
    "aio_key"  : "***insert key***"
}

- Add this line to /etc/rc.local (before the exit 0):
-   /home/pi/ONBOOT.sh 2> /home/pi/ONBOOT.errors > /home/pi/ONBOOT.stdout &
- Add the following ONBOOT.sh script to /home/pi and make it executable:
  
#!/bin/bash
cd /home/pi/iot-gateway
python3 app_zero.py  
'''

with open('/home/pi/config.json') as f:
    cfg = json.load(f)

fruit = Client(cfg['aio_user'], cfg['aio_key'])

pixels = neopixel.NeoPixel(board.D18,1)
pixels[0] = (0,0,0)

def thread_check_temperature():
    temperature = 0
    while True:
        try:
            url = 'http://192.168.1.108/data/freezer'
            r = requests.get(url)
            data = r.json()
            # print('#',data)
            temperature = str(data['value'])            
            fruit.send('freezer-temperature', str(data['value']))
            # print('# Sent')
            if data['value'] > -5:
                pixels[0] = (255,0,0)
                time.sleep(1) # Let the LED show before we try sending
            else:
                pixels[0] = (0,0,0)
                time.sleep(0.5)
                pixels[0] = (0,10,0)
                time.sleep(1) # Let the LED show before we try sending
        except Exception as f:
            # print('# Error sending',f)      
            pixels[0] = (0xFF,0xE9,0x00) # Yellow ... communication error
            time.sleep(1) # Let the LED show before we try again
        finally:
            time.sleep(60)

thread_check_temperature()