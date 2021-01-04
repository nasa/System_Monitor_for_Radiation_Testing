#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
install_tool.py

This script is intended to automatically
install the rad test script dependencies
'''

#############################################################
#IMPORT MODULES
#############################################################
import os
import sys



#############################################################
# MAIN CODE
#############################################################

print("\nInstalling...\n")

if 'linux' in sys.platform: pip_cmd = 'sudo pip3'
else: pip_cmd = 'pip3'

os.system(pip_cmd+' install --upgrade pip')
os.system(pip_cmd+' install opencv-python')
os.system(pip_cmd+' install psutil')

if 'linux' in sys.platform: os.system('sudo apt-get install libatlas-base-dev --yes')

print("\n\n...required install complete.")
response = input("\nInstall data visualization tools (not recommended for systems with < 1 GB RAM)? [y/n]: ")

print(response)
if response == 'y' or response == 'yes' or response == 'YES' or response == 'yeet' or response == 'Y':
    print("\ninstalling data visualization tools...\n")
    os.system(pip_cmd+' install pandas')
    os.system(pip_cmd+' --no-cache-dir install matplotlib')
    print("\n ...visualization tool install complete!")

print("\nComplete.  Exiting...\n")


