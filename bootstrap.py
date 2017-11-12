#!/usr/bin/env python3
'''
    Script to run the server on a button press
'''

import evdev
import sys
import subprocess

devices = [evdev.InputDevice(fn) for fn in evdev.list_devices()]

device = None
for dev in devices:
    if dev.name == 'Sony Computer Entertainment Wireless Controller':
        device = dev
        print('Found controller')
        break

if device:
    print('Waiting for input')
    for event in device.read_loop():
        # Start pressed, yo!
        if event.type == 1 and event.code == 291 and event.value == 1:
            # Bootstrap our server
            device.close()
            print('Start pressed, good job!')
            err = subprocess.check_call(['./run_server.sh'])
            print('Process result: ', err)
            sys.exit(0)
