import Tkinter as tk
import ttk

class ApplicationFrame(tk.Frame):
    """The main application frame"""
    
    def __init__(self, parent, session, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.parent.title('Application')
        self.parent.resizable(False, False)
        self.data = {}
        self.initialize(session)
        
    def initialize(self, session):
        self.tab_parent = ttk.Notebook(self.parent)
        self.tabs = []

        self.interfaces = self.get_interfaces(session)

        for interface in self.interfaces:
            self.create_tab(interface)
        
        self.tab_parent.pack(expand=1, fill='both')

    def get_ip_addresses(self, session):
        ip_addr_table = session.walk('ipAdEntAddr')
        ip_addresses = {}
        for entry in ip_addr_table:
            ip_index = session.get('ipAdEntIfIndex.' + entry.value).value
            ip_addresses[ip_index] = entry.value
        
        return ip_addresses

    def get_interfaces(self, session):
        if_table = session.walk('ifDescr')
        if_descs = []
        for entry in if_table:
            if_descs.append(entry.value)
        
        if_table = session.walk('ifPhysAddress')
        for entry in if_table:
            pass

        return if_descs    

    def create_tab(self, interface):
        self.tabs.append(tk.Frame(self.tab_parent))
        frame = self.tabs[-1]

        self.data[interface] = {}

        num_rows = 0
        
        self.add_standalone_data_row('MAC Address', 'mac_address', interface, frame, num_rows)
        num_rows += 1

        self.add_standalone_data_row('Bandwidth (bit/s)', 'speed', interface, frame, num_rows)
        num_rows += 1
        
        self.add_in_out_data_row('Total octets', 'in_octets_total' ,'out_octets_total', interface, frame, num_rows)
        num_rows += 1

        self.add_in_out_data_row('Packets with error', 'in_errors_packets' ,'out_errors_packets', interface, frame, num_rows)
        num_rows += 1

        self.add_in_out_data_row('Discarded packets', 'in_discards_packets' ,'out_discards_packets', interface, frame, num_rows)
        num_rows += 1
    
        self.tab_parent.add(self.tabs[-1], text=interface)

    def add_standalone_data_row(self, label, var_name, interface, frame, row):
        data_label = tk.Label(frame, text=label)
        data_label.grid(row=row, column=0)
        
        self.data[interface][var_name] = tk.StringVar()
        data = tk.Entry(frame, textvariable = self.data[interface][var_name])
        data.grid(row=row, column=1)
        data.config(state='readonly')

    def add_in_out_data_row(self, label, in_var_name, out_var_name, interface, frame, row):
        in_data_label = tk.Label(frame, text='[IN] ' + label)
        in_data_label.grid(row=row, column=0)
        
        self.data[interface][in_var_name] = tk.StringVar()
        in_data = tk.Entry(frame, textvariable = self.data[interface][in_var_name])
        in_data.grid(row=row, column=1)
        in_data.config(state='readonly')

        out_data_label = tk.Label(frame, text='[OUT] ' + label)
        out_data_label.grid(row=row, column=2)
        
        self.data[interface][out_var_name] = tk.StringVar()
        out_data = tk.Entry(frame, textvariable = self.data[interface][out_var_name])
        out_data.grid(row=row, column=3)
        out_data.config(state='readonly')
