#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
test_networks.py

This script is intended to
check and record network information
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
def network_test(data_dirname):

    #load inputs
    with open('data.json') as f:
        data = json.load(f)
    data_save_interval = data['data_save_interval']
    test_cycle_time = data['test_cycle_time']

    #define vars
    ttime=[]
    net_info=[]
    num_detected_adapters=[]

    print(str(time.time()) + ': starting network monitor!')

    onetime_net_info=psutil.net_io_counters(pernic=True)
    old_num_detected_adapters=len(onetime_net_info)

    start = time.time()
    while True:

        time.sleep(test_cycle_time)

        end = time.time()

        #grab network information
        ttime+=[time.time()]
        net_info+=[psutil.net_io_counters(pernic=True)]
        num_detected_adapters+=[len(net_info[-1])]


        if num_detected_adapters[-1] != old_num_detected_adapters:
            print('\n\n     NUMBER OF NETWORK ADAPTERS HAS CHANGED!\n\n')
            print(old_num_detected_adapters)
            print(num_detected_adapters)
            old_num_detected_adapters = num_detected_adapters[-1]


        if end-start > data_save_interval:
            time1 = time.time()

            data = {'time':ttime,'net_info':net_info,'num_detected_adapters':num_detected_adapters}

            now = str(datetime.now())
            now = now.split('.')
            now = now[0]
            now = now.replace(' ','_')
            now = now.replace(':','-')

            #write stuff
            keys=sorted(data.keys())
            with open(os.path.join(data_dirname, now+'net_log.csv'),'w', newline='') as csv_file:
                 writer=csv.writer(csv_file)
                 writer.writerow(keys)
                 writer.writerows(zip(*[data[key] for key in keys]))

            #reset vars
            ttime=[]
            net_info=[]
            num_detected_adapters=[]

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
    network_test(data_dirname)



