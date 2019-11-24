"""
  - Install tornado GLOBALLY like this: python -m pip install tornado
  - This file is in a directory named "iot". Copy the entire directory (and subs) to the pi home
  - Add this line to /etc/rc.local (before the exit 0):
  -   /home/pi/ONBOOT.sh 2> /home/pi/ONBOOT.errors > /home/pi/ONBOOT.stdout &
  - Add the following ONBOOT.sh script to /home/pi and make it executable:
  
#!/bin/bash
cd /home/pi/iot
python3 server.py
  
"""

import tornado.ioloop
import tornado.web
import os
import time
import threading

from RPi import GPIO
GPIO.setmode(GPIO.BCM)

PIN_GREEN_LED = 26

GPIO.setup(PIN_GREEN_LED,GPIO.OUT,initial=GPIO.LOW)

STATUS_OK = True

def _show_status():    
    while True:
        if STATUS_OK:
            GPIO.output(PIN_GREEN_LED,GPIO.HIGH)
        else:
            GPIO.output(PIN_GREEN_LED,GPIO.LOW)
        time.sleep(3.9)
        GPIO.output(PIN_GREEN_LED,GPIO.LOW)
        time.sleep(.1)
        
threading.Thread(target=_show_status).start()
    

class FreezerHandler(tornado.web.RequestHandler):
    def post(self):
        print('FREEZER')
        data = tornado.escape.json_decode(self.request.body)
        print(data)
        
class DungeonHumidityHandler(tornado.web.RequestHandler):
    def post(self):
        print('DUNGEONHUMIDITY')
        data = tornado.escape.json_decode(self.request.body)
        print(data)


root = os.path.dirname(__file__)

cont = os.path.join(root,'webroot')

handlers = [
    (r"/data/freezer",FreezerHandler),
    (r"/data/dungeonHumidity",DungeonHumidityHandler),
    (r"/(.*)", tornado.web.StaticFileHandler, {"path": cont, 'default_filename': 'index.html'})
]

app = tornado.web.Application(handlers)
app.listen(80)
tornado.ioloop.IOLoop.current().start()