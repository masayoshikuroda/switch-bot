import sys
import json
import asyncio
from bleak import BleakScanner

SERV_UUID = '0000fd3d-0000-1000-8000-00805f9b34fb'
CHAR_UUID = 2409

device_types = {
    0x48 : 'SwitchBot Bot (WoHand)',
    0x42 : 'WoButton',
    0x4C : 'SwitchBot Hub (WoLink)/Add Mode',
    0x6C : 'SwitchBot Hub (WoLink)/Normal',
    0x50 : 'SwitchBot Hub Plus (WoLink Plus)/Add Mode',
    0x70 : 'SwitchBot Hub Plus (WoLink Plus)/Normal Mode',
    0x46 : 'SwitchBot Fan (WoFan)/Add Mode',
    0x66 : 'SwitchBot Fan (WoFan)/Normal Mode',
    0x74 : 'SwitchBot MeterTH (WoSensorTH)/Add Mode',
    0x54 : 'SwitchBot MeterTH (WoSensorTH)/Normal',
    0x4D : 'SwitchBot Mini (HubMini)/Add Mode',
    0x6D : 'SwitchBot Mini (HubMini)/Normal Mode',
    0x64 : 'Unknown d',
    0x6A : 'Unknwon j',
    0x6D : 'Unknown m',
    0x76 : 'Unknwon v',
    0x77 : 'SwitchBot MeterOutdoor(WoIOSensor)/w',
}

meters = {}

def detection_callback(device, advertisement_data):
#    print(device.address, end=' ')
#    print(device.name,    end = ' ')
#    print(device.rssi,    end=' ')
#    print(advertisement_data.local_name,        end=' ')
#    print(advertisement_data.manufacturer_data, end=' ')
#    print(advertisement_data.service_uuids,     end=' ')
#    print(advertisement_data.service_data,      end=' ')
#    print()
    if SERV_UUID in advertisement_data.service_data:
        sd = advertisement_data.service_data.get(SERV_UUID)
        md = advertisement_data.manufacturer_data.get(CHAR_UUID)
        type = device_types[sd[0]]
        if type.startswith('SwitchBot Meter'):
            deviceId = md[0:6].hex(':')
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
