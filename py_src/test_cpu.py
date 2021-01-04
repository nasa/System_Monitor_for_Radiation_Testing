#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
test_cpu.py

This script is intended to 
monitor CPU usage
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
def cpu_test(data_dirname):

    #load inputs
    with open('data.json') as f:
        data = json.load(f)
    data_save_interval = data['data_save_interval']
    test_cycle_time = data['test_cycle_time']

    #define vars
    ttime=[]
    upsets=[]
    cpu_pct_used=[]
    cpu_temp=[]
    cpu_freq=[]

    print(str(time.time()) + ': starting CPU monitor!')
    
    #one day we might have user-configurable CPU usage here

    start = time.time()
    while True:

        time.sleep(test_cycle_time)
        end = time.time()

        ttime+=[time.time()]
        cpu_pct_used+=[psutil.cpu_percent()]
        cpu_freq+=[psutil.cpu_freq(percpu=False)[0]] #NOTE that as of 12/2020 this is the rated val on windows, not current


        if 'linux' in sys.platform:
            cpu_temp+=[psutil.sensors_temperatures()['cpu-thermal'][0][1]]
        else:
            cpu_temp+=[9999] #TODO figure out how to do this on Windows


        if end-start > data_save_interval:
            time1 = time.time()

            data = {'time':ttime,'cpu_pct_used':cpu_pct_used,'cpu_temp':cpu_temp,'cpu_freq':cpu_freq}

            now = str(datetime.now())
            now = now.split('.')
            now = now[0]
            now = now.replace(' ','_')
            now = now.replace(':','-')

            #write stuff
            keys=sorted(data.keys())
            with open(os.path.join(data_dirname, now+'cpu_log.csv'),'w', newline='') as csv_file:
                 writer=csv.writer(csv_file)
                 writer.writerow(keys)  
                 writer.writerows(zip(*[data[key] for key in keys]))

            #reset vars
            ttime=[]
            cpu_temp=[]
            cpu_pct_used=[]
            cpu_freq=[]

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
    cpu_test(data_dirname)




