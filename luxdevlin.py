import usb


class LuxDev(object):
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
        self.dev.write(1, [])  # this is needed for unclear reasons
