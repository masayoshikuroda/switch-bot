
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
    0x4D : 'SwitchBot Hub Mini (HubMini)/Add Mode',
    0x6D : 'SwitchBot Hub Mini (HubMini)/Normal Mode',
    0x64 : 'Unknown d',
    0x67 : 'SwitchBot Plug Mini',
    0x6A : 'Unknwon j',
    0x6D : 'Unknown m',
    0x76 : 'Unknwon v',
    0x77 : 'SwitchBot MeterOutdoor(WoIOSensor)/w',
}

def print_ble_info(device, advertisement_data):
    print(device.address, end=' ')
    print(device.name,    end = ' ')
    print(device.rssi,    end=' ')
    print(advertisement_data.local_name,        end=' ')
    print(advertisement_data.manufacturer_data, end=' ')
    print(advertisement_data.service_uuids,     end=' ')
    print(advertisement_data.service_data,      end=' ')
    print()
