'''
    Display module
'''
from threading import Thread

import subprocess
import time

try:
    import Adafruit_GPIO.SPI as SPI
    import Adafruit_SSD1306

    from PIL import Image
    from PIL import ImageDraw
    from PIL import ImageFont

    RUNNING_ON_PI = True
except ImportError as err:
    print(err)
    RUNNING_ON_PI = False

# Raspberry Pi pin configuration:
RST = None     # on the PiOLED this pin isnt used
# Note the following are only used with SPI:
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0


class PiDisplay(Thread):
    def __init__(self):
        if not RUNNING_ON_PI:
            print('Display disabled')
            self.disp = None
            return

        self.disp = Adafruit_SSD1306.SSD1306_128_64(
            rst=RST, dc=DC, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=8000000))

        # Initialize library.
        self.disp.begin()

        # Clear display.
        self.disp.clear()
        self.disp.display()

        # Create blank image for drawing.
        # Make sure to create image with mode '1' for 1-bit color.
        self.width = self.disp.width
        self.height = self.disp.height
        self.image = Image.new('1', (self.width, self.height))

        # Get drawing object to draw on image.
        self.draw = ImageDraw.Draw(self.image)

        # Draw a black filled box to clear the image.
        self.draw.rectangle((0, 0, self.width, self.height), outline=0, fill=0)

        # Draw some shapes.
        # First define some constants to allow easy resizing of shapes.
        padding = -2
        self.top = padding
        self.bottom = self.height - padding
        # Move left to right keeping track of the current x position for drawing shapes.

        # Load default font.
        self.font = ImageFont.load_default()

        # Alternatively load a TTF font.  Make sure the .ttf font file is in the same directory as the python script!
        # Some other nice fonts to try: http://www.dafont.com/bitmap.php
        # font = ImageFont.truetype('Minecraftia.ttf', 8)

        self.text = ['Hi there']
        self.refresh = True

        Thread.__init__(self)
        self.running = True
        self.start()

    def run(self):
        if not RUNNING_ON_PI:
            return

        while self.running:
            # Text has not changed
            # if not self.refresh:
            #     time.sleep(.1)
            #     continue

            # Draw a black filled box to clear the image.
            self.draw.rectangle(
                (0, 0, self.width, self.height), outline=0, fill=0)

            # Write the lines of text
            offset = 0
            x = 0
            for line in self.text:
                self.draw.text((x, self.top + offset),
                               line, font=self.font, fill=255)
                offset = offset + 8

            # Display image.
            self.disp.image(self.image)
            self.disp.display()
            time.sleep(.1)

            self.refresh = False

    def set_text(self, text):
        self.text = text
        self.refresh = True

    def append_text(self, text):
        self.text.append(text)
        self.refresh = True

    def halt(self):
        self.running = False
        self.join()
