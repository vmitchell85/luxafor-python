# Luxafor Python Script

Script written to modify the [Luxafor](http://www.luxafor.com) USB LED indicator via command line using python.

Any and all improvements welcome and appreciated.

Credit to gist by [dave-irvine](https://gist.github.com/dave-irvine/dbec2584e7508cbfc79e) for pyusb code.

## Requirements

### Linux

1. Luxafor LED Indicator
3. Python 2.7+
4. [PyUSB](https://walac.github.io/pyusb/)

### Windows

1. Luxafor LED Indicator
2. [Luxafor Software](http://luxafor.com/download)
3. Python 2.7+
4. [PyWinUSB](https://pypi.python.org/pypi/pywinusb/) (installable via pip)

## Confirmed Working Operating Systems
- Windows 10
- Ubuntu 15.10

## Known/Possible Issues

### Linux
- Sometimes first run doesn't work, have to run command a second time

### Allow usb permissions for python in Ubuntu 16.04
By default python will not let use usb libs and you will need to run command with `sudo` everythime. Let's no do that.

- find out device with `lsusb`. Should be something like `04d8:f372` where `04d8` is vendor id and `f372` is product id.
- create file `/lib/udev/rules.d/50-luxafor.rules`
> ACTION=="add", SUBSYSTEMS=="usb", ATTRS{idVendor}=="_VENDOR_ID_", ATTRS{idProduct}=="_PRODUCT_ID_", MODE="660", GROUP="plugdev"
- Reload rules:  
    - `sudo udevadm control --reload`
    - `sudo udevadm trigger`
- Unplug and replug the device or reboot your machine

### Windows
- Seems the Luxafor app has to be at least running in the tray for commands to persist
- Opening the Luxafor app switches the color to Green/Red (depeding on last used?)
- Seems that it doesn't always return to the exact same state it was in before a strobe or pattern is ran

## Parameters

-l = LED - 1-6 for specific LED, 65 for front, 66 for back, 0 for all, 255 for all one color  
-r = RED value (0-255)  
-g = GREEN value (0-255)  
-b = BLUE value (0-255)  
-s = Speed value - Determines speed of strobe or fade (0-255)  
-t = Repeat value - Determines the frequency of strobe or wave (0-255)  
-w = Wave value - 5 Different Patterns available (1-5)  
-p = Built In Patterns - 8 built in patterns
-x = Hex color value - ("#RRGGBB")

## Actions

### Color

Set the specified LED to the specified color

    luxafor-linux.py color -l 255 -r 255 -g 0 -b 0

#### Hex Color (Linux)
	
    luxafor-linux.py color -x "#F22613"

### Fade

    luxafor-linux.py fade -l 255 -r 0 -g 255 -b 0

### Strobe

    luxafor-linux.py strobe -l 255 -r 0 -g 0 -b 255 -s 20 -t 5

### Wave

    luxafor-linux.py wave -w 4 -r 0 -g 0 -b 255 -s 20 -t 3 

### Pattern

    luxafor-linux.py pattern -p 2 -r 3

## Raw Values

### Solid Color
Raw data array posisitions as follows:

0. Always 0
1. 1
2. 1-6 for specific LED, 65 for front, 66 for back, 0 for all, 255 for all one color
3. RED Value 0-255
4. GREEN Value 0-255
5. BLUE Value 0-255
6. N/A
7. N/A
8. N/A

### Fade Color
Raw data array posisitions as follows:

0. Always 0
1. 2
2. 1-6 for specific LED, 65 for front, 66 for back, 0 for all, 255 for all one color
3. RED Value 0-255
4. GREEN Value 0-255
5. BLUE Value 0-255
6. Changing Time (Duration)
7. N/A
8. N/A

### Strobe Color
Raw data array posisitions as follows:

0. Always 0
1. 3
2. 1-6 for specific LED, 65 for front, 66 for back, 0 for all, 255 for all one color
3. RED Value 0-255
4. GREEN Value 0-255
5. BLUE Value 0-255
6. Speed (30-40 is a fairly calm value)
7. N/A
8. N/A

### Wave Color

0. Always 0
1. 4
2. Wave Type
3. RED Value 0-255
4. GREEN Value 0-255
5. BLUE Value 0-255
6. N/A
7. Repeat (0-255)
8. Speed (10 is a fairly good value)

### Built In Patterns

0. Always 0
1. 6
2. Pattern Number (1-8)
3. Repeat (0-255)
4. N/A
5. N/A
6. N/A
7. N/A
8. N/A
