#!/usr/bin/env python3
import requests
import json
import time
import wol
import os

#Load config
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
with open(os.path.join(__location__,"settings.json")) as settings:
    data = json.load(settings)
        
for settings in data["tvSettings"]:
    IP  = settings.get("ip")
    PSK = settings.get("psk")
    MAC = settings.get("mac")

def wakeOnLan():
    wol.wake_on_lan(IP,MAC) 
    time.sleep(1)
    wol.wake_on_lan(IP,MAC)

#Build api request
def makeRequest(service,api):
    url = "http://"+IP+"/sony/"+service
    headers = {"content-type": "application/json","X-Auth-PSK": PSK}
    api = api
    try:
        r = requests.post(url = url, headers = headers , json = api)
        r.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        print ("Http Error:",errh)
    except requests.exceptions.ConnectionError as errc:
        print ("Error Connecting:",errc)
    except requests.exceptions.Timeout as errt:
        print ("Timeout Error:",errt)
    except requests.exceptions.RequestException as err:
        print ("Request Error:",err)
    else:
        print('Successful Request!')
    data = r.json()  
    #print(data)  
    return data

   
            