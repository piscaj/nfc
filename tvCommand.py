#!/usr/bin/env python3
import time
import tvConnect

# API commands

def powerStatus():
    status = tvConnect.makeRequest("system",{"id": 1,"method": "getPowerStatus","params": [],"version": "1.0"})
    return status

def powerOn():
    tvConnect.wakeOnLan()
    time.sleep(2)
    tvConnect.makeRequest("system",{"id": 1,"method": "setPowerStatus","params": [{"status": True}],"version": "1.0"})

def powerOff():
    tvConnect.makeRequest("system",{"id": 1,"method": "setPowerStatus","params": [{"status": False}],"version": "1.0"})

def powerToggle():
    status = powerStatus()
    
    for stat in status["result"]:
        power = stat.get("status")
        print("TV Power Status: ",power)
    
    if power == "active":
        tvConnect.makeRequest("system",{"id": 1,"method": "setPowerStatus","params": [{"status": False}],"version": "1.0"})
    else:
        tvConnect.makeRequest("system",{"id": 1,"method": "setPowerStatus","params": [{"status": True}],"version": "1.0"})
        #tvConnect.wakeOnLan()
        #time.sleep(3)
        launchNetflix()
        

def audioVolumeUp():
    tvConnect.makeRequest("audio",{"id": 1,"method": "setAudioVolume","params": [{"volume": "+1","ui": "on","target": "speaker"}],"version": "1.0"})    

def audioVolumeDown():
    tvConnect.makeRequest("audio",{"id": 1,"method": "setAudioVolume","params": [{"volume": "-1","ui": "on","target": "speaker"}],"version": "1.0"})    

def audioVolumeMute():
    tvConnect.makeRequest("audio",{"id": 1,"method": "setAudioMute","params": [{"status": True}],"version": "1.0"})    

def audioVolumeUnmute():
    tvConnect.makeRequest("audio",{"id": 1,"method": "setAudioMute","params": [{"status": False}],"version": "1.0"})    

def inputHDMI(num):
    tvConnect.makeRequest("avContent",{"id": 1,"method": "setPlayContent","params": [{"uri": "extInput:hdmi?port="+num}],"version": "1.0"})    

def getAppList():
    apps = tvConnect.makeRequest("appControl",{"id": 1,"method": "getApplicationList","params": [],"version": "1.0"})    
    return apps

def getSysInfo():
    tvConnect.makeRequest("system",{"id": 1,"method": "getSystemInformation","params": [],"version": "1.0"})

def launchNetflix():
    apps = getAppList()
    for result in apps["result"]:
        for Item in result:
            if Item.get("title") == "Netflix":
                
                Netflix = Item.get("uri")
                tvConnect.makeRequest("appControl",{"id": 1,"method": "setActiveApp","params":[{"uri": Netflix }],"version": "1.0"})
                break

