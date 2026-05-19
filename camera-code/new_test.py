import pyudev

def check_usb_drive():
    context = pyudev.Context()
    for device in context.list_devices(subsystem='block', DEVTYPE='partition'):
        if device.get('ID_BUS') == 'usb':
            print(f"USB Drive Detected: {device.get('DEVNAME')}")
            return True
    print("No USB drive found.")
    return False

check_usb_drive()
