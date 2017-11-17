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
except ImportError:
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
            self.disp = None
            return

        self.disp = Adafruit_SSD1306.SSD1306_128_64(rst = RST, dc = DC, spi = SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=8000000))

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
        self.draw.rectangle((0, 0, self.width, self.height), outline = 0, fill = 0)

        # Draw some shapes.
        # First define some constants to allow easy resizing of shapes.
        padding = -2
        self.top = padding
        self.bottom = self.height - padding
        # Move left to right keeping track of the current x position for drawing shapes.
        self.x = 0


        # Load default font.
        self.font = ImageFont.load_default()

        # Alternatively load a TTF font.  Make sure the .ttf font file is in the same directory as the python script!
        # Some other nice fonts to try: http://www.dafont.com/bitmap.php
        # font = ImageFont.truetype('Minecraftia.ttf', 8)

        Thread.__init__(self)
        self.running = True
        self.start()

    def run(self):
        if not RUNNING_ON_PI:
            return

        while self.running:
            # Draw a black filled box to clear the image.
            self.draw.rectangle((0, 0, self.width, self.height), outline = 0, fill = 0)

            # Shell scripts for system monitoring from here : https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-disk-usage-and-cpu-load
            cmd = "hostname -I | cut -d\' \' -f1"
            IP = subprocess.check_output(cmd, shell = True )
            cmd = "top -bn1 | grep load | awk '{printf \"CPU Load: %.2f\", $(NF-2)}'"
            CPU = subprocess.check_output(cmd, shell = True )
            cmd = "free -m | awk 'NR==2{printf \"Mem: %s/%sMB %.2f%%\", $3,$2,$3*100/$2 }'"
            MemUsage = subprocess.check_output(cmd, shell = True )
            cmd = "df -h | awk '$NF==\"/\"{printf \"Disk: %d/%dGB %s\", $3,$2,$5}'"
            Disk = subprocess.check_output(cmd, shell = True )

            # Write two lines of text.

            self.draw.text((self.x, self.top),       "IP: " + str(IP),  font=self.font, fill=255)
            self.draw.text((self.x, self.top+8),     str(CPU), font = self.font, fill = 255)
            self.draw.text((self.x, self.top+16),    str(MemUsage),  font=self.font, fill=255)
            self.draw.text((self.x, self.top+25),    str(Disk),  font=self.font, fill=255)

            # Display image.
            self.disp.image(self.image)
            self.disp.display()
            time.sleep(.1)