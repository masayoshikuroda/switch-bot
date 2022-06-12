import sys
import json
import asyncio
from bleak import BleakScanner

SERV_UUID = 'cba20d00-224d-11e6-9fb8-0002a5d5c51b'
CHAR_UUID = '00000d00-0000-1000-8000-00805f9b34fb'

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
    md = advertisement_data.manufacturer_data
    uuids = advertisement_data.service_uuids
    sd = advertisement_data.service_data
    if SERV_UUID in uuids:
        cd = sd.get(CHAR_UUID)
        type = device_types[cd[0]]
#        print(type, end=' ')
        if type.startswith('SwitchBot MeterTH '):
            deviceId   = device.address.replace(':', '')
            deviceType = 'Meter'
            temp = (cd[4] & 0x7f) + (cd[3] & 0x0f)/10
            humi = (cd[5] & 0x7f)
            meter = { 'deviceId' : deviceId, 'deviceType' : deviceType, 'temperature' : temp, 'humidity' : humi}
            meters[deviceId] = meter
#            print('Temperature', temp, 'degC', end=' ')
#            print('Humidity',    humi, '%',    end=' ')
#    print()

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
