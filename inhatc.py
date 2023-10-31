#!/usr/bin/python3

import time
import requests, json
from influxdb import InfluxDBClient as influxdb
import serial

port = '/dev/ttyACM0'
brate = 9600
cmd = 'temp'

seri = serial.Serial(port, baudrate = brate, timeout = None)

while(True):
    
    if seri.in_waiting !=0 :
        content = seri.readline()
        a = content.decode()
        a = int(a)
        data = [{
            'measurement' : 'lux',        
            'tags':{
                'VisionUni' : '2410',
            },
            'fields':{
                'lux' : a,
            }
        }]
        client = None
        try:
            client = influxdb('localhost',8086,'root','root','lux')
        except Exception as e:
            print ("Exception" + str(e))
        if client is not None:
            try:
                client.write_points(data)
            except Exception as e:
                print("Exception write " + str(e))
            finally:
                client.close()
