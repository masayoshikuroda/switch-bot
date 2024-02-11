import sys
import logging
import json
import asyncio
from bleak import BleakScanner
from switchbot_ble import SERV_UUID
from switchbot_ble import CHAR_UUID
from switchbot_ble import device_types 

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))

meters = {}

def detection_callback(device, advertisement_data):
    if SERV_UUID not in advertisement_data.service_data:
        return
    
    sd = advertisement_data.service_data.get(SERV_UUID)
    type = device_types[sd[0]]
    if not type.startswith('SwitchBot Meter'):
        return

    md = advertisement_data.manufacturer_data.get(CHAR_UUID)
    logger.debug('manufacturer_data: ', md)
 
    deviceId = md[0:6].hex().upper()
    deviceType = 'Meter'
    temp = (md[9] & 0x7f) + (md[8] & 0x0f)/10
    humi = (md[10] & 0x7f)
    meter = { 'deviceId' : deviceId, 'deviceType' : deviceType, 'temperature' : temp, 'humidity' : humi}
    meters[deviceId] = meter

async def main():
    scanner = BleakScanner()
    logger.debug('scanner: created')
    scanner.register_detection_callback(detection_callback)
    logger.debug('scanner: registered')
    await scanner.start()
    logger.debug('scanner: started')
    await asyncio.sleep(20.0)
    logger.debug('scanner: slept')
    await scanner.stop()
    logger.debug('scanner: stopped')
    print(json.dumps(meters))

if __name__ == '__main__':
    if len(sys.argv)>1 and sys.argv[1] == '-d':
        logger.setLevel(logging.DEBUG)
    
    asyncio.run(main())
