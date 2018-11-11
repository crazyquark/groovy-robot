#!/bin/python3
from datetime import datetime as dt

with open('timer.txt','w') as ft:
    ft.write(dt.now().strftime('Started: %H:%M %d-%m-%y'))
    while True:
        ft.write(dt.now().strftime('\r%H:%M %d-%m-%y'))

