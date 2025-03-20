# easys7comm/plc_types.py

from enum import Enum

class DataType(Enum):
    BOOL    = ("get_bool",   "set_bool",   1)
    BYTE    = ("get_byte",   "set_byte",   1)
    WORD    = ("get_word",   "set_word",   2)
    DWORD   = ("get_dword",  "set_dword",  4)
    INT     = ("get_int",    "set_int",    2)
    DINT    = ("get_dint",   "set_dint",   4)
    UINT    = ("get_uint",   "set_uint",   2)
    UDINT   = ("get_udint",  "set_udint",  4)
    REAL    = ("get_real",   "set_real",   4)
    LREAL   = ("get_lreal",  "set_lreal",  8)
    CHAR    = ("get_char",   None,         1)   # No corresponding setter
    STRING  = ("get_string", "set_string", 254)  # Default size
    FS_STRING = ("get_fstring", "set_fstring", 254)
    TIME    = ("get_time",   "set_time",   4)
    DATE    = (None,         "set_date",   2)   # No corresponding getter
    USINT   = ("get_usint",  "set_usint",  1)
    SINT    = ("get_sint",   "set_sint",   1)
    WCHAR   = ("get_wchar",  None,         2)   # No corresponding setter
    WSTRING = ("get_wstring", None,        508)  # Wide string, default size

    def __init__(self, method_get_name, method_set_name, size):
        self.method_get_name = method_get_name
        self.method_set_name = method_set_name
        self.size = size
