# importing requests library 
import requests
import json
import time

# Address 
URL = "http://192.168.2.92/sony/system"

headers = {"content-type": "application/json","X-Auth-PSK": "13579"}

# API commands
PARAMS = {"id": 1,"method": "setPowerStatus","params": [{"status": True}],"version": "1.0"} 

try:
    r = requests.post(url = URL, headers = headers , json = PARAMS)
    r.raise_for_status()
except requests.exceptions.HTTPError as errh:
    print ("Http Error:",errh)
except requests.exceptions.ConnectionError as errc:
    print ("Error Connecting:",errc)
except requests.exceptions.Timeout as errt:
    print ("Timeout Error:",errt)
except requests.exceptions.RequestException as err:
    print ("OOps: Something Else",err)
    
data = r.json()
print(data)


 