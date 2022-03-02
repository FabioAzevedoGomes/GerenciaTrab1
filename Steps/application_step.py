import logging
from random import randint
from step import Step
from GUI.application import ApplicationFrame
from globals import root
from config import getConfiguration

def getOctetAsString(octet_string):
    return ':'.join(['%0.2x' % ord(_) for _ in octet_string])

class ApplicationStep(Step):
    """The application main menu step"""
    
    def execute(self, data=None):
        global root
        self.session = data
        self.application_frame = ApplicationFrame(parent=root, session=data)
        root.after(getConfiguration('monitor_delay_millis'), self.update)
        root.mainloop()

        self.complete(None)

    def update(self):

        # Get interface addresses
        mac_addresses = self.session.walk('ifPhysAddress')
        for i in range(len(self.application_frame.interfaces)):
            address = getOctetAsString(mac_addresses[i].value)
            if not address:
                address = "-"
            self.application_frame.data[self.application_frame.interfaces[i]]['mac_address'].set(address)

        # Get interface bandwidths
        speeds = self.session.walk('ifSpeed')
        for i in range(len(self.application_frame.interfaces)):
            speed = speeds[i]
            self.application_frame.data[self.application_frame.interfaces[i]]['speed'].set(str(int(speed.value)))

        # Get in/out octets per interface
        countBulk = self.session.get_bulk(['ifInOctets', 'ifOutOctets'], 0, len(self.application_frame.interfaces))
        for i in range(len(self.application_frame.interfaces)):
            in_octets = countBulk[(2 * i)]
            out_octets = countBulk[(2 * i) + 1]
            self.application_frame.data[self.application_frame.interfaces[i]]['in_octets_total'].set(str(int(in_octets.value)))
            self.application_frame.data[self.application_frame.interfaces[i]]['out_octets_total'].set(str(int(out_octets.value)))

        # Get errors per interface
        countBulk = self.session.get_bulk(['ifInErrors', 'ifOutErrors'], 0, len(self.application_frame.interfaces))
        for i in range(len(self.application_frame.interfaces)):
            in_errors_packets = countBulk[(2 * i)]
            out_errors_packets = countBulk[(2 * i) + 1]
            self.application_frame.data[self.application_frame.interfaces[i]]['in_errors_packets'].set(str(int(in_errors_packets.value)))
            self.application_frame.data[self.application_frame.interfaces[i]]['out_errors_packets'].set(str(int(out_errors_packets.value)))

        # Get discarded packets per interface
        
        countBulk = self.session.get_bulk(['ifInDiscards', 'ifOutDiscards'], 0, len(self.application_frame.interfaces))
        for i in range(len(self.application_frame.interfaces)):
            in_discards_packets = countBulk[(2 * i)]
            out_discards_packets = countBulk[(2 * i) + 1]
            self.application_frame.data[self.application_frame.interfaces[i]]['in_discards_packets'].set(str(int(in_discards_packets.value)))
            self.application_frame.data[self.application_frame.interfaces[i]]['out_discards_packets'].set(str(int(out_discards_packets.value)))

        root.update()
        root.after(getConfiguration('monitor_delay_millis'), self.update)
        logging.info('update ran')
