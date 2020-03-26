import requests
import json
import time
import wol

#Set TV ip adress and PSK here
IP  = "192.168.2.92"
PSK = "13579"
MAC = "B0:68:E6:7D:0B:F3"

def wakeOnLan():
    wol.wake_on_lan(IP,MAC)
    time.sleep(1)
    wol.wake_on_lan(IP,MAC)
    time.sleep(1)
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
    #print("Printing JSON response")
    
    #for result in data["result"]:
    #        print("TV adaptor address: ",result.get("macAddr","00:00:00:00:00:00"))
    
    #for result in data["result"]:
    #    for Item in result:
    #        print("Link for icon: ",Item.get("icon"))
   
            


 