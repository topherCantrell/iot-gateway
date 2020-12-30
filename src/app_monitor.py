"""

sudo vi /etc/xdg/lxsession/LXDE-pi/autostart

  @lxpanel --profile LXDE-pi
  @pcmanfm --desktop --profile LXDE-pi
  @xscreensaver -no-splash
  @bash /home/pi/myapp_start.sh
  point-rpi

"""

import tkinter
import requests
import time
import threading
import json

from adafruit_io import AdafruitIO

TEMPERATURE = 'NONE'
COLOR = 'red'

TEXT_COLOR = 'black'

root = tkinter.Tk()
root.configure(background='black')
root.attributes('-fullscreen', True)

status = tkinter.Label(root, text=TEMPERATURE, bg=COLOR, fg='black', width=20, height=5)
status.place(x=250, y=210)


def thread_check_temperature():
    global TEMPERATURE, COLOR
    while True:
        try:
            url = 'http://192.168.1.108/data/freezer'
            r = requests.get(url)
            data = r.json()
            TEMPERATURE = str(data['value'])
            if data['value'] > -10.0:
                COLOR = 'red'
            else:
                COLOR = 'green'
            fruit.add_data_retry('freezer-temperature', str(data['value']))
        except Exception:
            COLOR = 'red'
            TEMPERATURE = 'ERROR'
        finally:
            time.sleep(60)


def update_temperature():
    global status, TEXT_COLOR
    status.config(text=TEMPERATURE, bg=COLOR, fg=TEXT_COLOR)
    root.after(60000, update_temperature)
    if TEXT_COLOR == 'black':
        TEXT_COLOR = 'white'
    else:
        TEXT_COLOR = 'black'


with open('/home/pi/config.json') as f:
    cfg = json.load(f)

fruit = AdafruitIO(cfg['aio_user'], cfg['aio_key'])

threading.Thread(target=thread_check_temperature).start()
root.after(1000, update_temperature)

root.mainloop()
