
#!/usr/bin/env python3
import requests
import json
import time
import wol
import os

class braviaTV:
    
    def __init__(self, ip, psk, mac):  
        self.ip  = ip 
        self.psk = psk
        self.mac = mac      
    
    def __makeRequest(self,service,api):
        url = "http://"+self.ip+"/sony/"+service
        headers = {"content-type": "application/json","X-Auth-PSK": self.psk}
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
        return data
    
    def wol(self):
        wol.wake_on_lan(self.ip,self.mac) 
        
    def getSysInfo(self):
        info = self.__makeRequest("system",{"id": 1,"method": "getSystemInformation","params": [],"version": "1.0"})
        return info
    
    def launchNetflix(self):
        apps = self.getAppList()
        for result in apps["result"]:
            for Item in result:
                if Item.get("title") == "Netflix":
                
                    Netflix = Item.get("uri")
                    self.__makeRequest("appControl",{"id": 1,"method": "setActiveApp","params":[{"uri": Netflix }],"version": "1.0"})
                    break
        
    def powerStatus(self):
        status = self.__makeRequest("system",{"id": 1,"method": "getPowerStatus","params": [],"version": "1.0"})
        return status
    
    def powerOn(self):
        self.__makeRequest("system",{"id": 1,"method": "setPowerStatus","params": [{"status": True}],"version": "1.0"})
        status = self.powerStatus()
        for state in status["result"]:
            theState = state.get("status")
            return theState
        
    def powerOff(self):
        self.__makeRequest("system",{"id": 1,"method": "setPowerStatus","params": [{"status": False}],"version": "1.0"})
        status = self.powerStatus()
        for state in status["result"]:
            theState = state.get("status")
            return theState
    
    def powerToggle(self):
        status = self.powerStatus()
        for state in status["result"]:
            power = state.get("status")
        if power == "active":
            self.__makeRequest("system",{"id": 1,"method": "setPowerStatus","params": [{"status": False}],"version": "1.0"})
            status = self.powerStatus()
            for state in status["result"]:
                theState = state.get("status")
                return theState
        else:
            self.__makeRequest("system",{"id": 1,"method": "setPowerStatus","params": [{"status": True}],"version": "1.0"})
            status = self.powerStatus()
            for state in status["result"]:
                theState = state.get("status")
            time.sleep(1)
            self.launchNetflix()
            return theState
    
    def audioVolumeUp(self):
        self.__makeRequest("audio",{"id": 1,"method": "setAudioVolume","params": [{"volume": "+1","ui": "on","target": "speaker"}],"version": "1.0"})    

    def audioVolumeDown(self):
        self.__makeRequest("audio",{"id": 1,"method": "setAudioVolume","params": [{"volume": "-1","ui": "on","target": "speaker"}],"version": "1.0"})    

    def audioVolumeMute(self):
        self.__makeRequest("audio",{"id": 1,"method": "setAudioMute","params": [{"status": True}],"version": "1.0"})    

    def audioVolumeUnmute(self):
        self.__makeRequest("audio",{"id": 1,"method": "setAudioMute","params": [{"status": False}],"version": "1.0"})
    
    def inputHDMI(self,num):
        self.__makeRequest("avContent",{"id": 1,"method": "setPlayContent","params": [{"uri": "extInput:hdmi?port="+num}],"version": "1.0"})    
    
    def getAppList(self):
        apps = self.__makeRequest("appControl",{"id": 1,"method": "getApplicationList","params": [],"version": "1.0"})    
        return apps
    
    
