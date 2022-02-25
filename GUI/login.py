import logging
import Tkinter as tk
from exceptions import MissingDataException
from error import ErrorFrame

auth_protocols = ['MD5', 'SHA']
priv_protocols = ['DES', 'AES']

class LoginFrame(tk.Frame):
    """Log in window"""
        
    def __init__(self, parent, connect_function, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent        
        self.parent.title('Log in')
        self.parent.resizable(False, False)
        self.initialize(connect_function)
        
    def initialize(self, connect_function):
        self.username_label = tk.Label(self.parent, text='Username')
        self.username_label.grid(row=0, column=0)
        self.username = tk.StringVar()
        self.username_entry = tk.Entry(self.parent, textvariable=self.username)
        self.username_entry.grid(row=0, column=1)
        
        self.password_label = tk.Label(self.parent, text='Password')
        self.password_label.grid(row=1, column=0)
        self.password = tk.StringVar()
        self.password_entry = tk.Entry(self.parent, textvariable=self.password)
        self.password_entry.grid(row=1, column=1)

        self.auth_protocol_label = tk.Label(self.parent, text='Authentication protocol')
        self.auth_protocol_label.grid(row=2, column=0)
        self.auth_protocol = tk.StringVar()
        self.auth_protocol_entry = tk.OptionMenu(self.parent, self.auth_protocol, *auth_protocols)
        self.auth_protocol_entry.grid(row=2, column=1)

        self.use_privacy = tk.BooleanVar()
        self.use_privacy.set(tk.TRUE)
        self.use_privacy_checkbutton = tk.Checkbutton(self.parent, text='Use privacy?',
                                                      command=self.hide_or_display_privacy,
                                                      variable=self.use_privacy)
        self.use_privacy_checkbutton.grid(row=3, column=0)

        self.priv_protocol_label = tk.Label(self.parent, text='Privacy protocol')
        self.priv_protocol_label.grid(row=4, column=0)
        self.priv_protocol = tk.StringVar()
        self.priv_protocol_option = tk.OptionMenu(self.parent, self.priv_protocol, *priv_protocols)
        self.priv_protocol_option.grid(row=4, column=1)
        
        self.priv_password_label = tk.Label(self.parent, text='Privacy password')
        self.priv_password_label.grid(row=5, column=0)
        self.priv_password = tk.StringVar()
        self.priv_password_entry = tk.Entry(self.parent, textvariable=self.priv_password)
        self.priv_password_entry.grid(row=5, column=1)

        self.connect_function = connect_function
        self.login_button = tk.Button(self.parent, text='Log in', command=self.attempt_connect).grid(row=6, column=1)

    def hide_or_display_privacy(self, event=None):
        if self.use_privacy.get():
            self.priv_protocol_label = tk.Label(self.parent, text='Privacy protocol')
            self.priv_protocol_label.grid(row=4, column=0)
            self.priv_protocol = tk.StringVar()
            self.priv_protocol_option = tk.OptionMenu(self.parent, self.priv_protocol, *priv_protocols)
            self.priv_protocol_option.grid(row=4, column=1)
            
            self.priv_password_label = tk.Label(self.parent, text='Privacy password')
            self.priv_password_label.grid(row=5, column=0)
            self.priv_password = tk.StringVar()
            self.priv_password_entry = tk.Entry(self.parent, textvariable=self.priv_password)
            self.priv_password_entry.grid(row=5, column=1)
        else:
            self.priv_protocol_label.grid_forget()
            self.priv_protocol_option.grid_forget()
            self.priv_password_label.grid_forget()
            self.priv_password_entry.grid_forget()

    def attempt_connect(self):
        try:
            data = self.pack_data()
            self.connect_function(data, self.login_successful)
        except MissingDataException as mde:
            logging.warning('Missing login data: ' + str(mde))
            self.show_error_message(str(mde))
        except Exception as e:
            logging.error('Unable to connect: ' + str(e))
            self.show_error_message(str(e))

    def show_error_message(self, message):
        error_popup = ErrorFrame(self, message)
        error_popup.wait_window()

    def pack_data(self):
        missing_data = []
        packaged_data = {}

        if (self.username.get()):
            packaged_data['username'] = self.username.get()
        else:
            missing_data.append('username')

        if (self.password.get()):
            packaged_data['password'] = self.password.get()
        else:
            missing_data.append('password')

        if (self.auth_protocol.get()):
            packaged_data['auth_protocol'] = self.auth_protocol.get()
        else:
            missing_data.append('authentication protocol')

        if (self.use_privacy.get()):

            if (self.priv_protocol.get()):
                packaged_data['privacy_protocol'] = self.priv_protocol.get()
            else:
                missing_data.append('privacy protocol')

            if (self.priv_password.get()):
                packaged_data['privacy_password'] = self.priv_password.get()
            else:
                missing_data.append('privacy password')

        if missing_data:
            raise MissingDataException('The following information is required: \n- ' + '\n- '.join(missing_data))
        else:
            return packaged_data

    def login_successful(self):
        for widget in self.parent.winfo_children():
            widget.destroy()
