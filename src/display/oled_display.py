'''
    Display module
'''
from threading import Thread

import subprocess
import time

try:
    # TODO https://github.com/adafruit/Adafruit_CircuitPython_RGB_Display
    from luma.core.interface.serial import i2c, spi
    from luma.core.render import canvas
    from luma.oled.device import ssd1306, ssd1325, ssd1331, sh1106

    from PIL import Image, ImageDraw, ImageFont

    RUNNING_ON_ARM = True
except ImportError as err:
    print(err)
    RUNNING_ON_ARM = False

# Raspberry Pi pin configuration:
RST = 24
# Note the following are only used with SPI:
DC = 23

class Text:
    def __init__(self, text, color = None):
        self.text = text
        self.color = color
        if not self.color:
            self.color = 'green'

class OledDisplay(Thread):
    def __init__(self):
        if not RUNNING_ON_ARM:
            print('Display disabled')
            self.disp = None
            return

        # rev.1 users set port=0
        # substitute spi(device=0, port=0) below if using that interface
        serial = spi(gpio_DC=DC, gpio_RST=RST)

        # substitute ssd1331(...) or sh1106(...) below if using that device
        self.device = ssd1331(serial)

        self.refresh = True
        self.text = [Text('Ready')]
        self.draw_text()

        Thread.__init__(self)
        self.running = True
        self.start()

    def run(self):
        if not RUNNING_ON_ARM:
            return

        while self.running:
            if self.refresh:
                # self.device.clear()
                self.draw_text()
                self.refresh = False

            time.sleep(.1)

    def draw_text(self):
        # Box and text rendered in portrait mode
        with canvas(self.device) as draw:
            draw.rectangle(self.device.bounding_box,
                           outline='orange', fill='black')
            height = 10
            for line in self.text:
                draw.text((10, height), line.text, fill=line.color)
                height += 10

    def set_text(self, text, color = None, refresh = False):
        self.text = []
        for line in text:
            self.text.append(Text(line, color))

        self.refresh = refresh

    def append_text(self, text, color = None, refresh = False):
        self.text.append(Text(text, color))
        self.refresh = refresh

    def set_refresh(self, refresh):
        self.refresh = refresh

    def halt(self):
        self.device.cleanup()
        self.running = False
        self.join()
