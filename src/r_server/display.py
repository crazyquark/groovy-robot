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


class PiDisplay(Thread):
    def __init__(self):
        if not RUNNING_ON_PI:
            print('Display disabled')
            self.disp = None
            return

        # rev.1 users set port=0
        # substitute spi(device=0, port=0) below if using that interface
        serial = i2c(port=1, address=0x70)

        # substitute ssd1331(...) or sh1106(...) below if using that device
        self.device = ssd1306(serial)

        # Create blank image for drawing.
        # Make sure to create image with mode '1' for 1-bit color.
        # self.width = self.disp.width
        # self.height = self.disp.height
        # self.image = Image.new('1', (self.width, self.height))

        # # Get drawing object to draw on image.
        # self.draw = ImageDraw.Draw(self.image)

        # # Draw a black filled box to clear the image.
        # self.draw.rectangle((0, 0, self.width, self.height), outline=0, fill=0)

        # # Draw some shapes.
        # # First define some constants to allow easy resizing of shapes.
        # padding = -2
        # self.top = padding
        # self.bottom = self.height - padding
        # # Move left to right keeping track of the current x position for drawing shapes.

        # # Load default font.
        # self.font = ImageFont.load_default()

        # # Alternatively load a TTF font.  Make sure the .ttf font file is in the same directory as the python script!
        # # Some other nice fonts to try: http://www.dafont.com/bitmap.php
        # # font = ImageFont.truetype('Minecraftia.ttf', 8)

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
            draw.rectangle(self.device.bounding_box, outline="white", fill="black")
            draw.text((10, 40), "Hello World", fill="white")

        # # Draw a black filled box to clear the image.
        # self.draw.rectangle(
        #     (0, 0, self.width, self.height), outline=0, fill=0)

        # # Write the lines of text
        # offset = 0
        # x = 0
        # for line in self.text:
        #     self.draw.text((x, self.top + offset),
        #                    line, font=self.font, fill=255)
        #     offset = offset + 8

        # # Display image.
        # self.disp.image(self.image)
        # self.disp.display()

    def set_text(self, text):
        self.text = text
        self.refresh = True

    def append_text(self, text):
        self.text.append(text)
        self.refresh = True

    def halt(self):
        self.running = False
        self.join()
