#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Created on Fri Feb 21 12:02:01 2020

@author: hella
"""

import os, sys, serial, getopt, time
import pandas as pd
import numpy as np


baudrate = 115200       # transmission rate
folder   = os.getcwd() + "//data//0503//" 
samples  = list()

MAP = {1: 'grinding', 
       2: 'clenching', 
       3: 'chewing', 
       4: 'yawning',
       5: 'resting'}

def main(argv):
    global samples
    port     = ''                   # port connected to Arduino Leonardo
    
    filename = 'sig-out.xlsx'       # default filename  
    serial_connection = False       # boolean to check serial connection status
    
    
    # get input arguments
    try:
        opts, args = getopt.getopt(argv,"hp:o:",["port=","ofile="])
    except getopt.GetoptError:
        print ('readEMG.py -p <PORT> -o <outputfile>')
        sys.exit(2)
        
    # parse input arguments
    for opt, arg in opts:
        if opt == '-h':
            print ('readEMG.py -p <PORT> -o <outputfile>')
            sys.exit()
        elif opt in ("-p", "--port"):
            port = arg
        elif opt in ("-o", "--ofile"):
            filename = arg
            
    
       
    # establish serial connection
    try:
        # pySerial timeout=None:  wait forever / until requested number of bytes are received
        ser = serial.Serial(port, baudrate, timeout=None)  
    except Exception:
        print('Failed to open port {}'.format(port))
    else:
        print('Port {} opened'.format(port))
        serial_connection = True
        
    # get input from serial interface
    try:
        if serial_connection:
            writer = pd.ExcelWriter(folder + filename, engine = 'xlsxwriter') 
            #samples = np.empty([100, 1024])

            for i in range(1,6):
                #task_no = get_task_no()
                samples = list()
                print('Task: {}'.format(MAP[i]))
                time.sleep(3)
                print('Start')
                if i == 5:
                    s = []
                    end = time.time() + 60
                    while time.time() < end:
                        s.append(ser.readline().decode('utf-8', 'ignore').rstrip())
                    samples = s
                else:
                    end = time.time() + 60
                    while time.time() < end:
                        read_serial_input(ser)
                        entspannen()
                
                #samples = np.divide(np.multiply(np.array(samples, dtype='float'), 5), 1023)
                samples = np.array(samples).reshape(len(samples), 1)
                emg_df = pd.DataFrame(data = samples)
                emg_df.to_excel(writer, sheet_name=MAP[i])
                
            
            writer.save()
            writer.close()
                
            ser.close()     # close serial port    
    except KeyboardInterrupt:   # kill process on keyboard interrupt (Strg+C)
        ser.close() 
        
def entspannen():
    print('{}: entspannen'.format(time.time()))
    time.sleep(4)
    print('{}: Bewegung wieder aufnehmen'.format(time.time()))
        
def read_serial_input(ser):
    global samples
    s = []
    start = time.time()
    while time.time() < start + 4:
        s.append(ser.readline().decode('utf-8', 'ignore').rstrip())
    samples = np.append(samples, s)
   

if __name__ == "__main__":
    main(sys.argv[1:])