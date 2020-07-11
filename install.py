#!/usr/bin/env python3
import os

exec(open("./setup_drivers.py").read())
exec(open("./setup_gadget.py").read())
print("\033[0;0m") # reset colors
os.system('reboot')

