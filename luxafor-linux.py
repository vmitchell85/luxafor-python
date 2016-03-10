import usb.core
import usb.util
import sys
import argparse

def main():
    # Get Device, catch exception if not found
    device = setupDevice()

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

def setupDevice():
    device = usb.core.find(idVendor=0x04d8, idProduct=0xf372)

    # was it found?
    if device is None:
        raise ValueError('Device not found')

    # Linux kernel sets up a device driver for USB device, which you have
    # to detach. Otherwise trying to interact with the device gives a
    # 'Resource Busy' error.
    try:
      device.detach_kernel_driver(0)
    except Exception, e:
      pass                       
     
    device.set_configuration()

    return device


def setPattern(device, args):
    # Check for arguments & set values if needed
    if not args.t:
        args.t = 5
    if not args.p or args.p > 8:
        args.p = 1
    # Set Data
    values = [6,args.p,args.t,0,0,0,0]
    device.write(1, values)

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
    
    # Set Data
    values = [4,args.w,args.r,args.g,args.b,0,args.t,args.s]
    device.write(1, values)

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
    
    values = [3,args.l,args.r,args.g,args.b,args.s,0,args.t]
    device.write(1, values)

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
    
    values = [2,args.l,args.r,args.g,args.b,args.s,0]
    device.write(1, values)

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
    
    values = [1,args.l,args.r,args.g,args.b,0,0]
    device.write(1, values)

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