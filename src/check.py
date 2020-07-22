

import requests
import time

while True:
    url = 'http://192.168.1.108/data/freezer'
    r = requests.get(url)
    data = r.json()
    
    print(data['value'])
    time.sleep(10)