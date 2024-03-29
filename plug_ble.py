import sys
import logging
from argparse import ArgumentParser
from datetime import datetime
import json
import asyncio
from bleak import BleakScanner
from switchbot_ble import SERV_UUID
from switchbot_ble import device_types 
from switchbot_ble import print_ble_info

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))

plugs = {}

def detection_callback(device, advertisement_data):
    if SERV_UUID not in advertisement_data.service_data:
        return

    sd = advertisement_data.service_data.get(SERV_UUID)
    type = device_types[sd[0]]
    if not type.startswith('SwitchBot Plug Mini'):
        return
    
    md = advertisement_data.manufacturer_data
    logger.debug('manufacturer_data: ', md)

    if 2409 in md: 
        data = md[2409]
        deviceId = data[0:6].hex().upper()
        seq = data[6]
        status = 'on' if int.from_bytes(data[7:8], byteorder='little')==0x80 else 'off'
        dts = data[8]
        delay = True if dts & 0x01 > 0 else False
        timer = True if dts & 0x02 > 0 else False
        sync_utc = True if dts & 0x04 > 0 else False
        rssi = data[9]
        overload = True if data[10] & 0xE0 > 0 else False
        power = int.from_bytes(data[10:12], byteorder='big') & 0x7FFF

        plug = {}
        plug['datetime'] = datetime.now().strftime('%Y/%m/%d %H:%M:%S.%f')
        plug['deviceId'] = deviceId
        plug['seq'] = seq
        plug['status'] = status
        plug['delay'] = delay
        plug['timer'] = timer
        plug['sync_utc'] = sync_utc
        plug['rssi'] = rssi
        plug['overload'] = overload
        plug['power'] = power
        plugs[deviceId] = plug

        logger.debug(json.dumps(plug))

async def main(sleep_time):
    scanner = BleakScanner()
    logger.debug('scanner: created')
    scanner.register_detection_callback(detection_callback)
    logger.debug('scanner: registered')
    await scanner.start()
    logger.debug('scanner: started')
    await asyncio.sleep(sleep_time)
    logger.debug('scanner: slept')
    await scanner.stop()
    logger.debug('scanner: stopped')
    print(json.dumps(plugs))

if __name__ == '__main__':
    argparser = ArgumentParser(description='SwitchBot Plug mini.')
    argparser.add_argument('-w', '--wait',    type=int, dest='wait_time',  default='1',  help='advertisement wait time[sec]')
    argparser.add_argument('-d', '--debug',   action='store_true',  help='Debug output')
    args = argparser.parse_args()
    if args.debug:
        logger.setLevel(logging.DEBUG)

    asyncio.run(main(args.wait_time))
