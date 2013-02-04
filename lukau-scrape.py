#!/usr/bin/env python

import os
import socket
import sys
import simplejson as json
import yaml

f = open('config.yml')
config = yaml.load(f)
f.close()

def scrd_connect(HOST, PORT=12908):
    # Create a socket (SOCK_STREAM means a TCP socket)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Connect to server and send data
    sock.connect((HOST, PORT))
    # Receive data from the server and shut down
    received = sock.recv(4096)
    sock.close()
    #print("Received: %s" % received)
    return received



for server in config["servers"]: 
    try:
        rawdata=scrd_connect(config["servers"][server]["host"], config["servers"][server]["port"])
    except:
        rawdata=""
    if rawdata != "":
        f=open('tmp/_'+server, 'w')
        f.write(rawdata)
        f.close()   
    else:
        f=open('tmp/_'+server+'_down', 'w')
        f.write(rawdata)
        f.close()
 
