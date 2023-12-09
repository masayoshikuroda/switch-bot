import json
from switchbot import SwitchBot


sb = SwitchBot()

devices = sb.get_devices()

dict = {}
for device in devices:
    if (('deviceType' in device) and (device['deviceType'] == 'Meter' or device['deviceType'] == 'WoIOSensor')):
        id = device['deviceId']
        status = sb.get_status(id)
        dict[id] = status

print(json.dumps(dict))
