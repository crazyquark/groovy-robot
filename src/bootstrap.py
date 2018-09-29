#!/usr/bin/env python3
'''
    Script to run the server on a button press
'''
import evdev
import sys
import subprocess

from r_server import display

display = display.PiDisplay()
display.set_text(['Booting'])

device = None
while not device:
    devices = [evdev.InputDevice(fn) for fn in evdev.list_devices()]

    for dev in devices:
        if dev.name == 'Sony Computer Entertainment Wireless Controller':
            device = dev
            print('Found controller')
            display.append_text('Controller: ON')
            break

if device:
    print('Waiting for input')
    for event in device.read_loop():
	    # Start pressed, yo!
        if event.type == 3:
            print(event)
        if event.type == 1 and event.code == 291 and event.value == 1:
            display.append_text('Starting server')
            # Bootstrap our server
            break

    del device
    display.halt()

    print('Start pressed, good job!')
    err = subprocess.check_call(['/home/pi/groovy-robot/run_server.sh'])
    print('Process result: ', err)
    sys.exit(0)
