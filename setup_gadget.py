#!/usr/bin/env python3
import os, sys, argparse, subprocess
from bcolors import bcolors 

if not os.geteuid()==0:
    sys.exit(f'{bcolors.FAIL}This script must be run as root!')

parser = argparse.ArgumentParser()

default_gadget_name = "usb_gadget"
parser.add_argument("--gadgetname", "-gn",
                    default=default_gadget_name,
                    help=f"set the name of the gadget (default: {default_gadget_name})")
default_function_name = "hid"
parser.add_argument("--functionname", "-fn",
                    default=default_function_name,
                    help=f"set name of usb function (default: {default_function_name})")

args = parser.parse_args()

gadget_path = f"/usr/bin/{args.gadgetname}"
if os.path.isfile(gadget_path):
    sys.exit(f"{bcolors.FAIL}Gadget {args.gadgetname} does already exist at {gadget_path}")

print(f"\n{bcolors.HEADER}Create actual gadget file\n");


rcLocal = "/etc/rc.local"
with open(rcLocal, 'r') as f:
    content = f.read()
    if gadget_path not in content:
        with open(rcLocal, 'w') as fw:
            key = "exit 0"
            k = content.rfind(key)
            new_string = content[:k] + f"{gadget_path}\n{key}" + content[k+len(key):]

            fw.write(new_string)
            print(f"{bcolors.OKGREEN}Wrote {gadget_path} to {rcLocal}") 
    else:
        print(f"{bcolors.OKGREEN}{gadget_path} already in {rcLocal}")

with open(gadget_path, 'w') as f:
    idVendor = 0x1d6b  # Linux Foundation
    idProduct = 0x0104 # Multifunction Composite Gadget
    bcdDevice = 0x0100 # v1.0.0
    bcdUSB = 0x0200    # USB2

    serialNumber = "cat /sys/firmware/devicetree/base/serial-number"
    manufacturer = "Raspberry Pi Foundation"
    product = args.gadgetname

    f.write("#!/bin/bash\n")
    f.write("cd /sys/kernel/config/usb_gadget/\n")
    f.write(f"mkdir {args.gadgetname}\n")
    f.write(f"cd {args.gadgetname}\n")
    f.write(f'echo "{idVendor}" > idVendor\n')
    f.write(f'echo "{idProduct}" > idProduct\n')
    f.write(f'echo "{bcdDevice}" > bcdDevice\n')
    f.write(f'echo "{bcdUSB}" > bcdUSB\n')
    
    strings_dir = "strings/0x409"
    f.write(f"mkdir -p {strings_dir}\n")
    f.write(f"cat /sys/firmware/devicetree/base/serial-number > {strings_dir}/serialnumber\n")
    f.write(f'echo "{manufacturer}" > {strings_dir}/manufacturer\n')
    f.write(f'echo "{product}" > {strings_dir}/product\n')

    config_dir = "configs/c.1"
    f.write(f"mkdir -p {config_dir}/{strings_dir}\n")
    f.write(f'echo "Config 1: USB Gadget" > {config_dir}/{strings_dir}/configuration\n')
    f.write(f"echo 250 > {config_dir}/MaxPower\n")

    f_instance_name = "usb0"
    function_dir = f"functions/{default_function_name}.{f_instance_name}"
    f.write(f"mkdir -p {function_dir}\n")
    f.write(f"ln -s {function_dir} {config_dir}\n")

    f.write("ls /sys/class/udc > UDC")

# make gadget file executable
subprocess.Popen(["chmod", "+x", gadget_path])
