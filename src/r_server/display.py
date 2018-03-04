'''
    Display module
'''
from threading import Thread

import subprocess
import time

try:
    from luma.core.interface.serial import i2c, spi
    from luma.core.render import canvas
    from luma.oled.device import ssd1306, ssd1325, ssd1331, sh1106

    from PIL import Image, ImageDraw, ImageFont

    RUNNING_ON_PI = True
except ImportError as err:
    print(err)
    RUNNING_ON_PI = False

# Raspberry Pi pin configuration:
RST = 24
# Note the following are only used with SPI:
DC = 23


class PiDisplay(Thread):
    def __init__(self):
        if not RUNNING_ON_PI:
            print('Display disabled')
            self.disp = None
            return

        # rev.1 users set port=0
        # substitute spi(device=0, port=0) below if using that interface
        serial = spi(gpio_DC=DC, gpio_RST=RST)

        # substitute ssd1331(...) or sh1106(...) below if using that device
        self.device = ssd1331(serial)

        self.refresh = True
        self.text = ['Hi there']
        self.draw_text()

        Thread.__init__(self)
        self.running = True
        self.start()

    def run(self):
        if not RUNNING_ON_PI:
            return

        while self.running:
            if self.refresh:
                self.draw_text()
                self.refresh = False

            time.sleep(.1)

    def draw_text(self):
        # Box and text rendered in portrait mode
        with canvas(self.device) as draw:
            draw.rectangle(self.device.bounding_box,
                           outline='orange', fill='black')
            for line in self.text:
                draw.text((10, 40), line, fill='green')

    def set_text(self, text):
        self.text = text
        self.refresh = True

    def append_text(self, text):
        self.text.append(text)
        self.refresh = True

    def halt(self):
        self.running = False
        self.join()
