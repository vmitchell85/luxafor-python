#!/usr/bin/env python
import usb.core
import usb.util
import sys
import argparse

DEVICES = []
ACTION = None
LED = None

HEX = None
RED = None
GREEN = None
BLUE = None
SPEED = None
REPEAT = None
WAVE = None
PATTERN = None


def main():
    global RED
    global GREEN
    global BLUE
    setupDevices()
    setupArgs()

    if HEX:
        rgb = hex_to_rgb(HEX)
        RED = rgb[0]
        GREEN = rgb[1]
        BLUE = rgb[2]

    # Determine which action
    if ACTION == 'color':
        setColor()
    elif ACTION == 'fade':
        setFade()
    elif ACTION == 'strobe':
        setStrobe()
    elif ACTION == 'wave':
        setWave()
    elif ACTION == 'pattern':
        setPattern()

def setupArgs():
    global DEVICE
    global RED
    global GREEN
    global BLUE
    global SPEED
    global REPEAT
    global WAVE
    global PATTERN
    global ACTION
    global LED
    global HEX
    
    parser = initArgParser()
    args = parser.parse_args()

    ACTION  = args.action if args.action else 'color'
    DEVICE  = args.d if args.d else 0
    RED     = args.r if args.r else 0
    GREEN   = args.g if args.g else 0
    BLUE    = args.b if args.b else 0
    SPEED   = args.s if args.s else 0
    REPEAT  = args.t if args.t else 0
    WAVE    = args.w if args.w else 0
    PATTERN = args.p if args.p else 0
    LED     = args.l if args.l else 255
    HEX     = args.x if args.x else 0


def hex_to_rgb(value): # http://stackoverflow.com/a/214657
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

def setupDevices():
    global DEVICES

    for flag in usb.core.find(find_all=True, idProduct=0xf372):
        DEVICES.append(flag)

    # Device found?
    if len(DEVICES) < 1:
        raise ValueError('Device(s) not found')

    # Linux kernel sets up a device driver for USB device, which you have to detach.
    # Otherwise trying to interact with the device gives a 'Resource Busy' error.
    for flag in DEVICES:
        try:
            flag.detach_kernel_driver(0)
        except Exception:
            pass
     
        flag.set_configuration()

def writeValue(values):
    if (DEVICE > 0):
        doWriteValue(DEVICES[DEVICE-1], values)
        return

    for flag in DEVICES:
        doWriteValue(flag, values)

def doWriteValue(target, values):
    # Run it twice to ensure it works.
    target.write(1, values)
    target.write(1, values)

def setPattern():
    writeValue( [6,PATTERN,REPEAT,0,0,0,0] )

def setWave():
    writeValue( [4,WAVE,RED,GREEN,BLUE,0,REPEAT,SPEED] )

def setStrobe():
    writeValue( [3,LED,RED,GREEN,BLUE,SPEED,0,REPEAT] )

def setFade():    
    writeValue( [2,LED,RED,GREEN,BLUE,SPEED,0] )

def setColor():
    writeValue( [1,LED,RED,GREEN,BLUE,0,0] )

def initArgParser():
    
    # Setup argument parser
    parser = argparse.ArgumentParser(description='Luxafor Arguments')
    parser.add_argument('action', help='Action', choices=["color", "fade", "wave", "strobe", "pattern"])
    parser.add_argument('-d', help='Device (blank/0 for all, 1 for first device, etc.', type=int)
    parser.add_argument('-l', help='LED', type=int)
    parser.add_argument('-b', help='Blue Value', type=int)
    parser.add_argument('-r', help='Red Value', type=int)
    parser.add_argument('-g', help='Green Value', type=int)
    parser.add_argument('-s', help='Speed Value', type=int)
    parser.add_argument('-t', help='Repeat Value', type=int)
    parser.add_argument('-w', help='Wave Value', type=int)
    parser.add_argument('-p', help='Pattern Value', type=int)
    parser.add_argument('-x', help='Hex Color', type=str)

    return parser

if __name__ == '__main__':
    main()
