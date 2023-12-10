import sys
import json
import asyncio
from bleak import BleakScanner
from switchbot_ble import SERV_UUID
from switchbot_ble import CHAR_UUID
from switchbot_ble import device_types 

meters = {}

def detection_callback(device, advertisement_data):
    if SERV_UUID not in advertisement_data.service_data:
        return
    
    sd = advertisement_data.service_data.get(SERV_UUID)
    md = advertisement_data.manufacturer_data.get(CHAR_UUID)
    type = device_types[sd[0]]
    if not type.startswith('SwitchBot Meter'):
        return
    
    deviceId = md[0:6].hex().upper()
    deviceType = 'Meter'
    temp = (md[9] & 0x7f) + (md[8] & 0x0f)/10
    humi = (md[10] & 0x7f)
    meter = { 'deviceId' : deviceId, 'deviceType' : deviceType, 'temperature' : temp, 'humidity' : humi}
    meters[deviceId] = meter

async def main():
    scanner = BleakScanner()
#    print('scanner: created')
    scanner.register_detection_callback(detection_callback)
#    print('scanner: registered')
    await scanner.start()
#    print('scanner: started')
    await asyncio.sleep(20.0)
#    print('wait end')
    await scanner.stop()
#    print('scanner: stopped')
    print(json.dumps(meters))

asyncio.run(main())
