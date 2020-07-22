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
    global TEMPERATURE,COLOR
    while True:
        try:
            time.sleep(10)
            url = 'http://192.168.1.108/data/freezer'
            r = requests.get(url)
            data = r.json()
            TEMPERATURE = str(data['value'])
            if data['value'] > -10.0:
                COLOR = 'red'
            else:
                COLOR = 'green'
            fruit.add_data_retry('freezer-temperature',str(data['value']))
        except:
            COLOR = 'red'
            TEMPERATURE = 'ERROR'
            
def update_temperature():
    global status,TEXT_COLOR
    status.config(text=TEMPERATURE,bg=COLOR,fg=TEXT_COLOR)    
    root.after(10000,update_temperature)
    if TEXT_COLOR=='black':
        TEXT_COLOR='white'
    else:
        TEXT_COLOR='black'

fruit = AdafruitIO('topher_cantrell','54ffe6dd2f2440ce99782dee243c3e71')
            
threading.Thread(target=thread_check_temperature).start()
root.after(10000,update_temperature)

root.mainloop()
