#!/usr/bin/env python3
import os, sys, argparse
from bcolors import bcolors 

if not os.geteuid()==0:
    sys.exit(f'{bcolors.FAIL}This script must be run as root!')

print(f"\n{bcolors.HEADER}Setup neccessary drivers\n")

configFile = "/boot/config.txt"
with open(configFile, "a+") as f:
    f.seek(0) # move to start of file, otherwise .read() would return nothing
    line1 = "dtoverlay=dwc2"
    if line1 not in f.read():
        f.write(line1+"\n")
        print(f"{bcolors.OKGREEN}Wrote to {configFile}")
    else:
        print(f"{bcolors.OKGREEN}{line1} does already exist in {configFile}")

modulesFile = "/etc/modules"
with open(modulesFile, "a+") as f:
    f.seek(0)
    content = f.read()
    line1 = "dwc2"
    line2 = "libcomposite"
    
    if line1 not in content:
        f.write(line1+"\n")
        print(f"Wrote {line1} to {modulesFile}")
    else:
        print(f"{bcolors.OKGREEN}{line1} does already exist in {modulesFile}")
    if line2 not in content:
        f.write(line2+"\n")
        print(f"Wrote {line2} to {modulesFile}")
    else:
        print(f"{bcolors.OKGREEN}{line2} does already exist in {modulesFile}")

