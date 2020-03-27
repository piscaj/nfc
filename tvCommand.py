import time
import tvConnect

# API commands
def powerOn():
    tvConnect.wakeOnLan()
    time.sleep(3)
    tvConnect.makeRequest("system",{"id": 1,"method": "setPowerStatus","params": [{"status": True}],"version": "1.0"})

def powerOff():
    tvConnect.makeRequest("system",{"id": 1,"method": "setPowerStatus","params": [{"status": False}],"version": "1.0"})
    
def powerStatus():
    tvConnect.makeRequest("system",{"id": 1,"method": "getPowerStatus","params": [],"version": "1.0"})
    
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
    tvConnect.makeRequest("appControl",{"id": 1,"method": "getApplicationList","params": [],"version": "1.0"})    

def getSysInfo():
    tvConnect.makeRequest("system",{"id": 1,"method": "getSystemInformation","params": [],"version": "1.0"})
 