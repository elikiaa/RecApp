import serial
from general import constants


class SerialConnection(object):
    def __init__(self, port='COM9'):
        self.ser = None
        self.status = None
        self.current_port = port

    def connect(self, baudrate=constants.BAUDRATE, port ='COM9'):
        try:
            self.ser = serial.Serial(port, baudrate, timeout=None)
        except Exception:
            self.status = "Serial Status: Failed to open port {}".format(port)
        else:
            self.current_port = port
            self.status =  "Serial Status: Port {} opened".format(port)

    def close_ser(self):
        if not(self.ser is None) and self.ser.isOpen():
            self.ser.close()
            print('ser closed')
    
    def get_serial(self):
        return self.ser

    def get_current_port(self):
        return self.current_port

    def get_serial_status(self):
        return self.status




