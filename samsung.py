import sys
import os
import logging
from wakeonlan import send_magic_packet
from smartTV import SmartTV 

sys.path.append('../')

# Increase debug level
logging.basicConfig(level=logging.INFO)

# Normal constructor
#tv = SamsungTVWS('192.168.2.232')

# Autosave token to file 
token_file = os.path.dirname(os.path.realpath(__file__)) + '/tv-token.txt'
tv = SmartTV(host='192.168.2.232', port=8002, token_file=token_file)



# Power On
send_magic_packet('84:C0:EF:EA:6D:DE')


# Toggle power
#tv.shortcuts().volume_up()
power =  tv.shortcuts().power()
#print(power)

# Open web in browser
#tv.open_browser('https://duckduckgo.com/')

# View installed apps
#apps = tv.app_list()
#logging.info(apps)
# Open app (Spotify)
#tv.run_app('3201606009684')

# Get app status (Spotify)
#app = tv.rest_app_status('3201606009684')
#logging.info(app)

# Open app (Spotify)
#app = tv.rest_app_run('3201606009684')
#logging.info(app)

# Close app (Spotify)
#app = tv.rest_app_close('3201606009684')
#logging.info(app)

# Install from official store (Spotify)
#app = tv.rest_app_install('3201606009684')
#logging.info(app)

# Get device info (device name, model, supported features..)
#info = tv.rest_device_info()
#logging.info(info)
#print(info)

#info = tv.powerStatus()
#logging.info(info)



if __name__ == '__main__':
    pass