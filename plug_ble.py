import sys
from datetime import datetime
import json
import asyncio
from bleak import BleakScanner

plugs = {}

def detection_callback(device, advertisement_data):
    md = advertisement_data.manufacturer_data
    if 2409 in md: 
        data = md[2409]
#        print('data:', data, end=' ')
        mac = '{:02x}:{:02x}:{:02x}:{:02x}:{:02x}:{:02x}'.format(data[0], data[1], data[2], data[3], data[4], data[5])
        seq = int.from_bytes(data[6:7], byteorder='little')
        status = 'on' if int.from_bytes(data[7:8], byteorder='little')==0x80 else 'off'
        dts = int.from_bytes(data[8:9], byteorder='little')
        delay = dts & 0x01
        timer = dts & 0x02
        sync_utc = dts & 0x04
        rssi = int.from_bytes(data[9:10], byteorder='little')
        power = int.from_bytes(data[10:12], byteorder='little')
      
#        now = datetime.now() 
#        print(now.strftime('%Y/%m/%d %H:%M:%S') + "," + str(power))

        plug = {} 
        plug['mac'] = mac
        plug['seq'] = seq
        plug['status'] = status
        plug['delay'] = delay
        plug['timer'] = timer
        plug['sync_utc'] = sync_utc
        plug['rssi'] = rssi
        plug['power'] = power
        plugs[mac] = plug

async def main():
    scanner = BleakScanner()
#    print('scanner: created')
    scanner.register_detection_callback(detection_callback)
#    print('scanner: registered')
    await scanner.start()
#    print('scanner: started')
    await asyncio.sleep(1)
#    print('wait end')
    await scanner.stop()
#    print('scanner: stopped')
    print(json.dumps(plugs))

asyncio.run(main())
