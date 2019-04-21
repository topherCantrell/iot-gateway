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

root = os.path.dirname(__file__)

cont = os.path.join(root,'webroot')

handlers = [
    (r"/(.*)", tornado.web.StaticFileHandler, {"path": cont, 'default_filename': 'index.html'})
]

app = tornado.web.Application(handlers)
app.listen(80)
tornado.ioloop.IOLoop.current().start()