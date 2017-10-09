import pywinusb.hid as hid


class LuxDev(object):
    def __init__(self):
        self.dev = hid.HidDeviceFilter(vendor_id=0x04D8,
                                       product_id=0xF372).get_devices()[0]

    def write(self, data):
        self.dev.open()
        reports = self.dev.find_output_reports()
        values = [0] + data
        # Retrieve Data
        # Set Data
        reports[0].set_raw_data(values)
        reports[0].send()
        # Close Device
        self.dev.close()
