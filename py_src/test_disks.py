#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
test_disks.py

This script is intended to poll disks
and record related data
'''

#############################################################
#IMPORT MODULES
#############################################################
import os
import sys
import csv
import time
import json
import psutil
from datetime import datetime


#############################################################
# SUPPORT FUNCTIONS
#############################################################
def disk_test(data_dirname):

    #load inputs
    with open('data.json') as f:
        data = json.load(f)
    data_save_interval = data['data_save_interval']
    test_cycle_time = data['test_cycle_time']

    #define vars
    ttime=[]
    num_detected_disks=[]
    disk_space_total=[]
    disk_space_used=[]
    disk_space_free=[]
    disk_space_used_pct=[]
    disk_info=[]

    print(str(time.time()) + ': starting disk monitor!')

    disks = psutil.disk_partitions()
    old_num_detected_disks = len(disks)

    #probably create list of drives here for data storage

    start = time.time()
    while True:

        time.sleep(test_cycle_time)
        end = time.time()

        ttime+=[time.time()]
        disks = psutil.disk_partitions()
        num_detected_disks+=[len(disks)]
# how to deal with variable number of disks?

        disk_space_total+=[psutil.disk_usage(disks[1][0])[0]]
        disk_space_used+=[psutil.disk_usage(disks[1][0])[1]]
        disk_space_free+=[psutil.disk_usage(disks[1][0])[2]]
        disk_space_used_pct+=[psutil.disk_usage(disks[1][0])[3]]
        disk_info+=[disks]

        if num_detected_disks[-1] != old_num_detected_disks:
            print('\n\n     NUMBER OF DISKS HAS CHANGED!\n\n')
            print(old_num_detected_disks)
            print(num_detected_disks)
            old_num_detected_disks = num_detected_disks

        if end-start > data_save_interval:
            time1 = time.time()

            data = {'time':ttime,'num_detected_disks':num_detected_disks, 'disk_info':disk_info}

            now = str(datetime.now())
            now = now.split('.')
            now = now[0]
            now = now.replace(' ','_')
            now = now.replace(':','-')

            #write stuff
            keys=sorted(data.keys())
            with open(os.path.join(data_dirname, now+'disk_log.csv'),'w', newline='') as csv_file:
                 writer=csv.writer(csv_file)
                 writer.writerow(keys)
                 writer.writerows(zip(*[data[key] for key in keys]))

            #reset vars
            ttime=[]
            num_detected_disks=[]
            disk_space_total=[]
            disk_space_used=[]
            disk_space_free=[]
            disk_space_used_pct=[]
            disk_info=[]


            #reset time
            start = time.time()


#############################################################
# MAIN CODE
#############################################################
if __name__ == '__main__':

    try:
        data_dirname = sys.argv[1]
    except:
        data_dirname = '../data/demo'
    if os.path.exists(os.path.join(data_dirname)):
        pass
    else:
        os.makedirs(os.path.join(data_dirname))
    #print(data_dirname)
    disk_test(data_dirname)



