'''
	Main entry point
'''

from platform import uname
arch = uname()[4]
running_on_arm = arch.startswith('arm')

print('We are running on: ', arch)

from r_server.web_server import start_web_server

if __name__ == '__main__':
	start_web_server(running_on_arm)