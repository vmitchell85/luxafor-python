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

#### Avoid Sudo Prompt
By default python will not let use usb libs and you will need to run command with `sudo` everytime. To prevent this you will need to do the following:

1: Create a file, `/lib/udev/rules.d/50-luxafor.rules` with the following contents:

```
# Allow Luxafor USB control
ACTION=="add", SUBSYSTEMS=="usb", ATTRS{idVendor}=="04d8", ATTRS{idProduct}=="f372", MODE="660", GROUP="plugdev"
```

2: Reload the `udevadm` using the following commands:  
`sudo udevadm control --reload`  
`sudo udevadm trigger`

3: Unplug and reinsert your Luxafor device

### Windows
- Seems the Luxafor app has to be at least running in the tray for commands to persist
- Opening the Luxafor app switches the color to Green/Red (depeding on last used?)
- Seems that it doesn't always return to the exact same state it was in before a strobe or pattern is ran

## Common parameters

-l = LED - 1-6 for specific LED, 65 for front, 66 for back, 0 for all, 255 for all one color
-s = Speed value - Determines speed of strobe or fade (0-255)
-t = Repeat value - Determines the frequency of strobe or wave (0-255)
-w = Wave value - 5 Different Patterns available (1-5)
-p = Built In Patterns - 8 built in patterns

## Actions

### Color

Set the specified LED to the specified color

    lux.py color -l 255 ff0000

### Fade

    lux.py fade -l 255 00ff00

### Strobe

    lux.py strobe -l 255 0000ff -s 20 -t 5

### Wave

    lux.py wave -w 4 0000ff -s 20 -t 3

### Pattern

    lux.py pattern 2 -r 3

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
