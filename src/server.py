'''
	Main entry point
'''

from platform import uname
arch = uname().machine
running_on_arm = (arch != 'x86_64')

print('We are running on: ', arch)

from r_server.web_server import start_web_server

if __name__ == '__main__':
	start_web_server(running_on_arm)