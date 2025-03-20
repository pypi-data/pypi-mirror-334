import snap7
from .plc_reader import PLCReader
from .plc_writer import PLCWriter
from .plc_types import DataType

class PLC:
    def __init__(self, ip: str, rack: int = 0, slot: int = 1):
        """
        Initializes a PLC object with the given IP, rack, and slot.
        """
        self.ip = ip
        self.rack = rack
        self.slot = slot
        self.client = snap7.client.Client()
        self.client.connect(self.ip, self.rack, self.slot)

    def get_connected(self):
        return self.client.get_connected()

    def read(self, address: str, data_type: DataType):
        """
        Reads a block of data from the PLC.
        """
        reader = PLCReader(self.client)
        return reader.read(address, data_type)
    

    def write(self, address: str, value, data_type: DataType):
        """
        Writes a block of data to the PLC.
        """
        writer = PLCWriter(self.client)
        return writer.write(address, value, data_type)
        

    def close(self):
        """
        Closes the connection to the PLC.
        """
        self.client.disconnect()
        self.client.destroy()
        
