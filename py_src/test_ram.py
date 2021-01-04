#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
test_ram.py

This script is intended to consume RAM
and monitor it for changed values
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
def ram_test(data_dirname):

    #load inputs
    with open('data.json') as f:
        data = json.load(f)
    data_save_interval = data['data_save_interval']
    test_cycle_time = data['test_cycle_time']
    ram_pct_to_use = data['ram_pct_to_use']

    #define vars
    ttime=[]
    upsets=[]
    ram_pct_used=[]

    print(str(time.time()) + ': starting RAM monitor!')

    #allocate available mem
    ram_soaker = []
    ram_info = psutil.virtual_memory()
    ram_pct = int(ram_info[2])
    old_pct = ram_pct

    print('allocating ram...')
    while ram_pct < ram_pct_to_use:

        ram_soaker += ['1' * 512000]
        ram_info = psutil.virtual_memory()
        ram_pct = int(ram_info[2])
        if ram_pct != old_pct:
            print(ram_pct)
            old_pct = ram_pct


    print('...RAM allocation complete!')
    ram_info = psutil.virtual_memory()
    ram_pct = int(ram_info[2])
    print(ram_pct)
    print(len(ram_soaker))

    print('\n\nWatching for changed RAM vals...')
    start = time.time()
    while True:

        time.sleep(test_cycle_time)

        outliers = [i for i in range(1,len(ram_soaker)) if ram_soaker[i]!=ram_soaker[i-1] ]
        if len(outliers) > 0:
            print('\n\n     RAM STATE CHANGE DETECTED!\n\n')
            upsets+=[1]
        else:
            upsets+=[0]

        end = time.time()

        ttime+=[time.time()]
        ram_info = psutil.virtual_memory()
        ram_pct = ram_info[2]
        ram_pct_used+=[ram_pct]

        if end-start > data_save_interval:
            time1 = time.time()

            data = {'time':ttime,'ram_pct_used':ram_pct_used,'upsets':upsets}

            now = str(datetime.now())
            now = now.split('.')
            now = now[0]
            now = now.replace(' ','_')
            now = now.replace(':','-')

            #write stuff
            keys=sorted(data.keys())
            with open(os.path.join(data_dirname, now+'ram_log.csv'),'w', newline='') as csv_file:
                 writer=csv.writer(csv_file)
                 writer.writerow(keys)
                 writer.writerows(zip(*[data[key] for key in keys]))

            #reset vars
            ttime=[]
            upsets=[]
            ram_pct_used=[]

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
    ram_test(data_dirname)



