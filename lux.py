#!/usr/bin/env python

import usb
import argparse


def hex_to_rgb(value):  # http://stackoverflow.com/a/214657
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))


class Lux(object):

    class Cmd:
        COLOR = 1
        FADE = 2
        STROBE = 3
        WAVE = 4
        PATTERN = 6

    def __init__(self):
        self.dev = usb.core.find(idVendor=0x04d8, idProduct=0xf372)
        if self.dev is None:
            raise IOError("device not found")

        # Linux kernel sets up a device driver for USB device, which you have
        # to detach. Otherwise trying to interact with the device gives a
        # 'Resource Busy' error.
        try:
            self.dev.detach_kernel_driver(0)
        except usb.USBError:
            pass

        self.dev.set_configuration()

    def write(self, data):
        self.dev.write(1, data)
        self.dev.write(1, [])  # needed for some reason, need more doc

    def color(self, led, r, g, b):
        self.write([self.Cmd.COLOR, led, r, g, b, 0, 0, 0])

    def pattern(self, pattern, repeat):
        self.write([self.Cmd.PATTERN, pattern, repeat, 0, 0, 0, 0, 0])

    def wave(self, wave, r, g, b, repeat, speed):
        self.write([self.Cmd.WAVE, wave, r, g, b, 0, repeat, speed])

    def strobe(self, led, r, g, b, speed, repeat):
        self.write([self.Cmd.STROBE, led, r, g, b, speed, 0, repeat])

    def fade(self, led, r, g, b, speed):
        self.write([self.Cmd.FADE, led, r, g, b, speed, 0, 0])


def cmd_color(lux, args):
    r, g, b = hex_to_rgb(args.hex)
    lux.color(args.led, r, g, b)


def cmd_fade(lux, args):
    r, g, b = hex_to_rgb(args.hex)
    lux.fade(args.led, r, g, b, args.speed)


def cmd_wave(lux, args):
    r, g, b = hex_to_rgb(args.hex)
    lux.wave(args.wave, r, g, b, args.repeat, args.speed)


def cmd_strobe(lux, args):
    r, g, b = hex_to_rgb(args.hex)
    lux.strobe(args.led, r, g, b, args.speed, args.repeat)


def cmd_pattern(lux, args):
    lux.pattern(args.patt, args.repeat)


def main():
    lux = Lux()
    args = parse_args()
    args.func(lux, args)


def parse_args():
    parser = argparse.ArgumentParser(description='Luxafor Arguments')
    sp = parser.add_subparsers(title='commands',
                               description='command to control the luxafor',
                               help='use {command} -h for more help')

    p = sp.add_parser('color', help='solid color')
    p.add_argument('hex', help='color hex value (e.g. "#ff3355")')
    p.set_defaults(func=cmd_color)
    p.add_argument('-l', dest='led', type=int, default=255,
                   help='which LED (1-6) default: all')

    p = sp.add_parser('fade', help='fade to a different color')
    p.add_argument('hex', help='color hex value (e.g. "#ff3355")')
    p.set_defaults(func=cmd_fade)
    p.add_argument('-l', dest='led', type=int, default=255,
                   help='which LED (1-6) default: all')
    p.add_argument('-s', dest='speed', help='speed Value (0-255)', type=int,
                   default=10)

    p = sp.add_parser('wave', help='rotate a color')
    p.add_argument('hex', help='color hex value (e.g. "#ff3355")')
    p.set_defaults(func=cmd_wave)
    p.add_argument('-s', dest='speed', help='speed Value (0-255)', type=int,
                   default=10)
    p.add_argument('-t', dest='repeat', help='repeat Value (0-255)', type=int,
                   default=0)
    p.add_argument('-w', dest='wave',
                   help='wave Value (1-5)', type=int, default=1)

    p = sp.add_parser('strobe', help='stroby thinggie')
    p.add_argument('hex', help='color hex value (e.g. "#ff3355")')
    p.set_defaults(func=cmd_strobe)
    p.add_argument('-l', dest='led', type=int, default=255,
                   help='which LED (1-6) default: all')
    p.add_argument('-s', dest='speed', help='speed Value (0-255)', type=int,
                   default=10)
    p.add_argument('-t', dest='repeat', help='repeat Value (0-255)', type=int,
                   default=0)

    p = sp.add_parser('pattern', help='stroby thinggie')
    p.add_argument('patt', help='pattern number (0-8)', type=int)
    p.set_defaults(func=cmd_pattern)
    p.add_argument('-t', dest='repeat', help='repeat Value (0-255)', type=int,
                   default=0)

    return parser.parse_args()


if __name__ == '__main__':
    main()
