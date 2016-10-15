#!/usr/bin/env python
'''
	Run the server
'''

from r_server import bottle_server
import sys

try:
	bottle_server.run()
except:
	bottle_server.halt()
	sys.exit(0)