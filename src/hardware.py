import board
import neopixel  # sudo python3 -m pip install adafruit-io rpi_ws281x adafruit-circuitpython-neopixel


class Hardware:

    def __init__(self, pin=board.D18):        
        self._pixels = neopixel.NeoPixel(pin,1)
        self._pixels[0] = (0,0,0)

    def set_color(self, rgb, brightness=1.0):
        self._pixels[0] = (rgb[0]*brightness, rgb[1]*brightness, rgb[2]*brightness)
