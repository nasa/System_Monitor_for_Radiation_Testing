#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
plot_results.py

This script is intended to plot
the data captured by the test
scripts
'''

#############################################################
#IMPORT MODULES
#############################################################
import os
import csv
import sys
import time
import pandas as pd
import matplotlib.pyplot as plt


#############################################################
# USER INPUT
#############################################################
title_prefix = 'Rad Test '
plot_prefix = 'rad_test_'
save_plot = True


#############################################################
# SUPPORT FUNCTIONS
#############################################################

def find_and_load_data(keyword):

    print("\nLoading: " + keyword)

    # list data
    dir_list = os.listdir('../data')
    dir_list.sort()
    if len(dir_list) > 1:
        try: dir_list.remove('demo')
        except: pass
    data_dir = dir_list[-1]

    print("Using folder: " + str(os.path.join('..','data',data_dir)))
    data_file_list = os.listdir(os.path.join('..','data',data_dir))

    the_files = []
    for filename in data_file_list:
        if keyword in filename: the_files+=[filename]

    the_data = []
    for filename in the_files:
        df = pd.read_csv(os.path.join('..','data',data_dir,filename))
        the_data+= [df]

    result = pd.concat(the_data)
    result.sort_values(by=['time'], inplace=True)

    return result


#############################################################
# MAIN CODE
#############################################################

# Load and concatenate data
try:
    ram_data = find_and_load_data("ram")
    ram_data_status = True
except:
    ram_data_status = False
    print('Error: failed to load RAM data!')
try:
    net_data = find_and_load_data("net")
    net_data_status = True
except:
    net_data_status = False
    print('Error: failed to load network data!')
try:
    cpu_data = find_and_load_data("cpu")
    cpu_data_status = True
except:
    cpu_data_status = False
    print('Error: failed to load CPU data!')
try:
    disk_data = find_and_load_data("disk")
    disk_data_status = True
except:
    disk_data_status = False
    print('Error: failed to load disk data!')


# Plot data
n=0

if ram_data_status:
    #Plot RAM upsets and use
    n+=1
    plt.figure(n)
    ax1=plt.subplot(211)
    plt.title(title_prefix+'RAM Upsets and % Use')
    plt.plot(ram_data['time'], ram_data['ram_pct_used'], '-o', markersize=3)
    plt.ylabel('% Used')

    plt.subplot(212, sharex=ax1)
    plt.plot(ram_data['time'], ram_data['upsets'], '-o', markersize=3)
    plt.ylabel('Upsets')
    plt.xlabel('System time (s)')
    if save_plot == True:
        plt.savefig(plot_prefix+'ram_combined.png')

if cpu_data_status:
    #Plot CPU use and temp
    n+=1
    plt.figure(n)
    ax1=plt.subplot(311)
    plt.plot(cpu_data['time'], cpu_data['cpu_pct_used'], '-o', markersize=3)
    plt.ylabel('% Used')
    plt.title(title_prefix+'CPU Temp and % Use')

    plt.subplot(312, sharex=ax1)
    plt.plot(cpu_data['time'], cpu_data['cpu_freq'], '-o', markersize=3)
    plt.ylabel('Freq (MHz)')

    plt.subplot(313, sharex=ax1)
    plt.plot(cpu_data['time'], cpu_data['cpu_temp'], '-o', markersize=3)
    plt.ylabel('Temp (C)')
    plt.xlabel('System time (s)')
    if save_plot == True:
        plt.savefig(plot_prefix+'cpu_combined.png')

if disk_data_status:
    #Plot num disks
    n+=1
    plt.figure(n)
    ax1=plt.subplot(111)
    plt.plot(disk_data['time'], disk_data['num_detected_disks'], '-o', markersize=3)
    plt.ylabel('#')
    plt.title(title_prefix+'Number of Disks Detected')
    plt.xlabel('System time (s)')
    if save_plot == True:
        plt.savefig(plot_prefix+'disk_combined.png')


if net_data_status:
    #Plot num adapters
    n+=1
    plt.figure(n)
    ax1=plt.subplot(111)
    plt.plot(net_data['time'], net_data['num_detected_adapters'], '-o', markersize=3)
    plt.ylabel('#')
    plt.title(title_prefix+'Number of Network Adapters Detected')
    plt.xlabel('System time (s)')
    if save_plot == True:
        plt.savefig(plot_prefix+'net_combined.png')



plt.show()  #show plots





