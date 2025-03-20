from snap7 import util
from .plc_types import DataType
from .plc_parse_address import PlcParseAddress

class PLCReader:
    def __init__(self, plc):
        self.plc = plc

    def parse_value(self, bytearray, data_type: DataType):
        getter = getattr(util, data_type.method_get_name)
        if data_type == DataType.BOOL:
            return getter(bytearray, 0, 0)
        return getter(bytearray, 0)

    def read_db_row(self, db_number: int, offset: int, data_type: DataType):
        data = self.plc.db_read(db_number, offset, data_type.size)
        return self.parse_value(data, data_type)

    def read(self, address: str, data_type: DataType):
        info = PlcParseAddress.parse_address(address)
        if info["address_category"] == "DB":
            return self.read_db_row(info["db"], info["byte_offset"], data_type)
        raise NotImplementedError("Address type are still not supported.")