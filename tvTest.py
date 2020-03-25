# importing requests library 
import requests
import json
import time

#Set TV ip adress and PSK here
IP = "192.168.2.92"
PSK = "13579"

#Build api request
def request(service,api):
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
    print("Printing JSON response")
    
    for result in data["result"]:
        for Item in result:
            print(Item.get("icon"))
            
            
            
        
        

# API commands
def powerOn():
    request("system",{"id": 1,"method": "setPowerStatus","params": [{"status": True}],"version": "1.0"})

def powerOff():
    request("system",{"id": 1,"method": "setPowerStatus","params": [{"status": False}],"version": "1.0"})
    
def powerStatus():
    request("system",{"id": 1,"method": "getPowerStatus","params": [],"version": "1.0"})
    
def audioVolumeUp():
    request("audio",{"id": 1,"method": "setAudioVolume","params": [{"volume": "+1","ui": "on","target": "speaker"}],"version": "1.0"})    

def audioVolumeDown():
    request("audio",{"id": 1,"method": "setAudioVolume","params": [{"volume": "-1","ui": "on","target": "speaker"}],"version": "1.0"})    

def audioVolumeMute():
    request("audio",{"id": 1,"method": "setAudioMute","params": [{"status": True}],"version": "1.0"})    

def audioVolumeUnmute():
    request("audio",{"id": 1,"method": "setAudioMute","params": [{"status": False}],"version": "1.0"})    

def inputHDMI(num):
    request("avContent",{"id": 1,"method": "setPlayContent","params": [{"uri": "extInput:hdmi?port="+num}],"version": "1.0"})    

def getAppList():
    request("appControl",{"id": 1,"method": "getApplicationList","params": [],"version": "1.0"})    


getAppList()




 