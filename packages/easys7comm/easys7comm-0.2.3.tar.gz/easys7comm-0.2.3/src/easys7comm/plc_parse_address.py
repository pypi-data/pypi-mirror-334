from .plc_types import DataType
import re

class PlcParseAddress:
   
    @staticmethod
    def parse_address(addr: str):
        if addr.upper().startswith("DB"):
            m = re.match(r"DB(\d+)\.([A-Za-z]+)(\d+)(?:\.(\d+))?", addr, re.IGNORECASE)
            if m:
                db = int(m.group(1))
                typ = m.group(2).upper()
                byte_offset = int(m.group(3))
                bit = int(m.group(4)) if m.group(4) is not None else None
                if typ == "DBX" and bit is None:
                    raise ValueError(f"Bit value required for DBX address: {addr}")
                if typ != "DBX" and bit is not None:
                    raise ValueError(f"Unexpected bit value for {typ}: {addr}")
                return {
                    "address_category": "DB", 
                    "db": db, 
                    "addr_type": typ, 
                    "byte_offset": byte_offset, 
                    "bit": bit
                }
            raise ValueError(f"Invalid DB address format: {addr}")

        m = re.match(r"^([MIQ])(\d+)(?:\.(\d+))?$", addr, re.IGNORECASE)
        if m:
            return {
                "address_category": m.group(1).upper(),
                "address": int(m.group(2)),
                "bit": int(m.group(3)) if m.group(3) is not None else None,
            }
        raise ValueError(f"Invalid address format: {addr}")