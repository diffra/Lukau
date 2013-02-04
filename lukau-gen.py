#!/usr/bin/env python

import datetime
import os
import socket
import sys
import simplejson as json
import yaml

f = open('config.yml')
config = yaml.load(f)
f.close()

#initialize output
hosts=""
for server in config["servers"]: 
    #load template
    try:
        timestamp=datetime.datetime.fromtimestamp(os.path.getmtime('tmp/_'+server))
        ptime=timestamp.strftime("%Y-%m-%d %H:%M:%S")
    except:
        ptime=""
    if not os.path.exists('tmp/_'+server+'_down'): 
        hosttmpl = open('templates/host.html', 'r')
        hosthtml=hosttmpl.read()
        hosttmpl.close()
        #print hosthtml
        #load status information
        hostjson = open('tmp/_'+server, 'r')
        h= json.load(hostjson)
        #print h
        hosthtml=hosthtml.replace('{host.status}', "up")
        hosthtml=hosthtml.replace('{hostname}', server)
        hosthtml=hosthtml.replace('{uplo.load5}', str(h["uplo"]["load5"]))
        hosthtml=hosthtml.replace('{ram.unused}', str(int(h["ram"]["free"]+int(h["ram"]["bufcac"]))))
        hosthtml=hosthtml.replace('{ram.total}', str(h["ram"]["total"]))
        hosthtml=hosthtml.replace('{uptime}', h["uplo"]["uptime"])
        hosthtml=hosthtml.replace('{disk.total.avail}', str(round(float(h["disk"]["total"]["avail"])/1048576)), 2)
        hosthtml=hosthtml.replace('{disk.total.total}', str(round(float(h["disk"]["total"]["total"])/1048576)), 2)
        hosthtml=hosthtml.replace('{ps.allps}', str(h["ps"]["allps"]))
        hosthtml=hosthtml.replace('{timestamp}', ptime)
        try: 
            svctmpl = open('templates/service.html', 'r')
            svchtml=hosttmpl.read()
            svctmpl.close()
            svchtml=""
            #for process in config["servers"][server][processes]:                
        except:
            svchtml=""
        hosthtml=hosthtml.replace('{process}',svchtml)
        #print hosthtml
    else:
        hosttmpl = open('templates/host.html', 'r')
        hosthtml=hosttmpl.read()
        hosttmpl.close()
        hosthtml=hosthtml.replace('{host.status}', "down")
        hosthtml=hosthtml.replace('{hostname}', server)
        hosthtml=hosthtml.replace('{uplo.load5}', "XX")
        hosthtml=hosthtml.replace('{ram.unused}', "XX")
        hosthtml=hosthtml.replace('{ram.total}', "XX")
        hosthtml=hosthtml.replace('{uptime}', "XX")
        hosthtml=hosthtml.replace('{disk.total.avail}', "XX")
        hosthtml=hosthtml.replace('{disk.total.total}', "XX")
        hosthtml=hosthtml.replace('{ps.allps}', "XX")
        hosthtml=hosthtml.replace('{timestamp}', ptime)

        hosthtml=hosthtml.replace('{process}',"")

    hosts = hosts+hosthtml

#load data into template

sitetmpl = open('templates/main.html', 'r')
sitehtml=sitetmpl.read()
sitetmpl.close()
#insert data
sitehtml = sitehtml.replace('{host}', hosts)

print sitehtml
f=open(config["outfile"], 'w')
f.write(sitehtml)
f.close()   
