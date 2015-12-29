import argparse
import pywinusb.hid as hid

def main():
    # Get Device, catch exception if not found
    try:
        device = hid.HidDeviceFilter(vendor_id = 0x04D8, product_id = 0xF372).get_devices()[0]
    except:
        print 'Device Error'
        raise SystemExit

    # Setup argument parser
    parser = initArgParser()
    args = parser.parse_args()

    # Determine which action
    if args.action == 'color':
        setColor(device, args)
    elif args.action == 'fade':
        setFade(device, args)
    elif args.action == 'strobe':
        setStrobe(device, args)
    elif args.action == 'wave':
        setWave(device, args)
    elif args.action == 'pattern':
        setPattern(device, args)

def setPattern(device, args):
    # Check for arguments & set values if needed
    if not args.t:
        args.t = 5
    if not args.p or args.p > 8:
        args.p = 1
    # Open device
    device.open()
    # Retrieve Data
    reports = device.find_output_reports()
    # Set Data
    values = [0,6,args.p,args.t,0,0,0,0,0]
    reports[0].set_raw_data(values)
    reports[0].send()
    # Close Device
    device.close()

def setWave(device, args):
    # Check for arguments & set values if needed
    if not args.r:
        args.r = 0
    if not args.g:
        args.g = 0
    if not args.b:
        args.b = 0
    if not args.w or args.w > 5:
        args.w = 1
    if not args.s:
        args.s = 30
    if not args.t:
        args.t = 5
    
    # Open Device
    device.open()
    # Retrieve Data
    reports = device.find_output_reports()
    # Set Data
    values = [0,4,args.w,args.r,args.g,args.b,0,args.t,args.s]
    reports[0].set_raw_data(values)
    reports[0].send()
    # Close Device
    device.close()

def setStrobe(device, args):
    # Check for arguments & set values if needed
    if not args.r:
        args.r = 0
    if not args.g:
        args.g = 0
    if not args.b:
        args.b = 0
    if not args.l:
        args.l = 255
    if not args.s:
        args.s = 30
    if not args.t:
        args.t = 5
    
    # Open Device
    device.open()
    # Retrieve Data
    reports = device.find_output_reports()
    values = [0,3,args.l,args.r,args.g,args.b,args.s,0,args.t]
    reports[0].set_raw_data(values)
    reports[0].send()
    # Close Device
    device.close()

def setFade(device, args):
    # Check for arguments & set values if needed
    if not args.r:
        args.r = 0
    if not args.g:
        args.g = 0
    if not args.b:
        args.b = 0
    if not args.l:
        args.l = 255
    if not args.s:
        args.s = 30
    
    # Open Device
    device.open()
    # Retrieve Data
    reports = device.find_output_reports()
    values = [0,2,args.l,args.r,args.g,args.b,args.s,0,0]
    reports[0].set_raw_data(values)
    reports[0].send()
    # Close Device
    device.close()

def setColor(device, args):
    # Check for arguments & set values if needed
    if not args.r:
        args.r = 0
    if not args.g:
        args.g = 0
    if not args.b:
        args.b = 0
    if not args.l:
        args.l = 255
    
    # Open Device
    device.open()
    # Retrieve Data
    reports = device.find_output_reports()
    values = [0,1,args.l,args.r,args.g,args.b,0,0,0]
    reports[0].set_raw_data(values)
    reports[0].send()
    # Close Device
    device.close()

def initArgParser():
    
    # Setup argument parser
    parser = argparse.ArgumentParser(description='Luxafor Arguments')
    parser.add_argument('action', help='Action', choices=["color", "fade", "wave", "strobe", "pattern"])
    parser.add_argument('-l', help='LED', type=int)
    parser.add_argument('-b', help='Blue Value', type=int)
    parser.add_argument('-r', help='Red Value', type=int)
    parser.add_argument('-g', help='Green Value', type=int)
    parser.add_argument('-s', help='Speed Value', type=int)
    parser.add_argument('-t', help='Repeat Value', type=int)
    parser.add_argument('-w', help='Wave Value', type=int)
    parser.add_argument('-p', help='Pattern Value', type=int)

    return parser

if __name__ == '__main__':
    main()