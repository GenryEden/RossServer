from __future__ import annotations

from enum import Enum
from typing import Optional


class OutputProto(Enum):
    """
        A enum of all supported output protocols
    """
    SOUND = 0
    TSLUMD = 1
    JSON = 2
    BIN = 3


class NetworkTransport(Enum):
    """
        A enum of network transports
    """
    UDP = 0
    TCP = 1


class Descriptor:
    """
        A descriptor of all known parameters that an output server can have
    """
    def __init__(self):
        self.protocol: Optional[OutputProto] = None
        self.ip: Optional[str] = None
        self.port: Optional[int] = None
        self.transport: Optional[NetworkTransport] = None

    def __repr__(self):
        ans = "Descriptor: \""

        if self.protocol is not None:
            ans += f"protocol: {self.protocol}; "
        if self.ip is not None:
            ans += f"ip: {self.ip}; "
        if self.port is not None:
            ans += f"port: {self.port}; "
        if self.transport is not None:
            ans += f"transport: {self.transport}; "
        return ans + "\""
