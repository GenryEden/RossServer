from __future__ import annotations

from enum import Enum
from typing import Optional, Any


class OutputProto(Enum):
    """
        A enum of all supported output protocols
    """
    SOUND = 0
    TSLUMD = 1
    JSON = 2
    BIN = 3
    EZTSLUMD = 4


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
        self.filtered_cameras: Optional[set[int]] = None

    def __repr__(self):
        ans = "Descriptor: \""
        if self.protocol is not None:
            ans += f"protocol: {self.protocol};"
        if self.ip is not None:
            ans += f" ip: {self.ip};"
        if self.port is not None:
            ans += f" port: {self.port};"
        if self.transport is not None:
            ans += f" transport: {self.transport};"
        if self.filtered_cameras is not None:
            str_camera_list = ', '.join(str(i) for i in self.filtered_cameras)
            ans += f" filtered cameras: {str_camera_list};"
        return ans + "\""

    def to_dict(self) -> dict[str, Any]:
        ans = {}
        if self.protocol is not None:
            ans['protocol'] = self.protocol.value
        if self.ip is not None:
            ans['ip'] = self.ip
        if self.port is not None:
            ans['port'] = self.port
        if self.transport is not None:
            ans['transport'] = self.transport.value
        if self.filtered_cameras is not None:
            ans['filtered_cameras'] = list(self.filtered_cameras)
        return ans
