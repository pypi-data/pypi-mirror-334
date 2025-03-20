# easys7comm/plc_connection.py
"""
PLC Connection Module

This module provides the PLCConnection class, which handles establishing and closing
connections to a PLC using the snap7 library.
"""

import snap7
from typing import Any


class PLCConnection:
    """
    A base class for establishing a connection to a PLC.

    This class encapsulates the connection logic and can be used as a context manager.
    """
    def __init__(self, ip_address: str, rack: int, slot: int, port: int = 102) -> None:
        """
        Initialize the PLC connection.

        Args:
            ip_address (str): The PLC's IP address.
            rack (int): The PLC rack number.
            slot (int): The PLC slot number.
            port (int, optional): The connection port (default is 102).
        
        Raises:
            ConnectionError: If unable to connect to the PLC.
        """
        self.ip_address = ip_address
        self.rack = rack
        self.slot = slot
        self.port = port

        self.client = snap7.client.Client()
        try:
            self.client.connect(ip_address, rack, slot, port)
        except Exception as exc:
            raise ConnectionError(f"Error connecting to PLC at {ip_address}:{port} - {exc}") from exc

        if not self.client.get_connected():
            raise ConnectionError(f"Unable to connect to PLC at {ip_address}:{port}.")

    def disconnect(self) -> None:
        """
        Disconnect from the PLC if currently connected.
        """
        if self.client.get_connected():
            self.client.disconnect()

    def __enter__(self) -> "PLCConnection":
        """
        Enter the runtime context related to this object.
        """
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """
        Exit the runtime context and disconnect from the PLC.
        """
        self.disconnect()
