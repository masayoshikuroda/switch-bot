import json
from switchbot import SwitchBot


sb = SwitchBot()

devices = sb.get_devices()

dict = {}
for device in devices:
    if (device['deviceType'] == 'Meter'):
        id = device['deviceId']
        status = sb.get_status(id)
        dict[id] = status

print(json.dumps(dict))
