from __future__ import annotations

from typing import Dict, Optional, Callable

from EzTSLUMDEncoder import RossEventToEzTSLUMD
from Filter import Filter
from RossEventMultiplexor import Multiplexor
from JSONEncoder import RossEventToJson
from MessagersInterfaces import Notifier, OutputServer, NetworkOutputServer, T
from RossServer import RossDecoder
from RossEvent import RossEvent
from ServerDescriptor import Descriptor, OutputProto, NetworkTransport
from TCPServer import TCPServer
from TSLUMDEncoder import RossEventToTSLUMD
from UDPServer import UDPServer
from UMDDecoder import UMDDecoder
from SoundEncoder import SoundEncoder
import json

class TSLTCPServer(NetworkOutputServer):
    def __init__(self, ip: str, port: int, repeat_for_new=False):
        self._tcp_server = TCPServer(ip, port, repeat_for_new)
        self._ross_event_to_tsl_umd = RossEventToTSLUMD(self._tcp_server)

    def get_ip(self) -> str:
        return self._tcp_server.get_ip()

    def get_port(self) -> int:
        return self._tcp_server.get_port()

    def get_transport(self) -> NetworkTransport:
        return NetworkTransport.TCP

    def get_proto(self) -> OutputProto:
        return OutputProto.TSLUMD

    def start(self):
        self._tcp_server.start()

    def stop(self):
        self._tcp_server.stop()

    def on_message(self, message: RossEvent, notifier: Notifier[RossEvent]):
        self._ross_event_to_tsl_umd(message, notifier)


class EzTSLTCPServer(NetworkOutputServer):
    def __init__(self, ip: str, port: int, repeat_for_new=False):
        self._tcp_server = TCPServer(ip, port, repeat_for_new)
        self._ross_event_to_tsl_umd = RossEventToEzTSLUMD(self._tcp_server)

    def get_ip(self) -> str:
        return self._tcp_server.get_ip()

    def get_port(self) -> int:
        return self._tcp_server.get_port()

    def get_transport(self) -> NetworkTransport:
        return NetworkTransport.TCP

    def get_proto(self) -> OutputProto:
        return OutputProto.EZTSLUMD

    def start(self):
        self._tcp_server.start()

    def stop(self):
        self._tcp_server.stop()

    def on_message(self, message: RossEvent, notifier: Notifier[RossEvent]):
        self._ross_event_to_tsl_umd(message, notifier)


class FilteredTSLTCPServer(NetworkOutputServer):
    """
        Boxing for the TSLTCPServer that also includes
        set of the necessary cameras
    """
    def __init__(self, ip: str, port: int, filtered_cameras: set[int], repeat_for_new=False):
        self._tsltcp = TSLTCPServer(ip, port, repeat_for_new)
        self._filter = Filter(self._tsltcp, filtered_cameras)

    def get_ip(self) -> str:
        return self._tsltcp.get_ip()

    def get_port(self) -> int:
        return self._tsltcp.get_port()

    def get_transport(self) -> NetworkTransport:
        return self._tsltcp.get_transport()

    def start(self):
        self._tsltcp.start()

    def stop(self):
        self._tsltcp.stop()

    def get_proto(self) -> OutputProto:
        return self._tsltcp.get_proto()

    def on_message(self, message: T, notifier: Notifier[T]):
        self._filter.on_message(message, notifier)

    def get_descriptor(self) -> Descriptor:
        ans = super().get_descriptor()
        ans.ip = self.get_ip()
        ans.port = self.get_port()
        ans.transport = self.get_transport()
        ans.filtered_cameras = self._filter.get_filter_set()
        return ans


class FilteredEzTSLTCPServer(NetworkOutputServer):
    """
        Boxing for the TSLTCPServer that also includes
        set of the necessary cameras
    """
    def __init__(self, ip: str, port: int, filtered_cameras: set[int], repeat_for_new=False):
        self._tsltcp = EzTSLTCPServer(ip, port, repeat_for_new)
        self._filter = Filter(self._tsltcp, filtered_cameras)

    def get_ip(self) -> str:
        return self._tsltcp.get_ip()

    def get_port(self) -> int:
        return self._tsltcp.get_port()

    def get_transport(self) -> NetworkTransport:
        return self._tsltcp.get_transport()

    def start(self):
        self._tsltcp.start()

    def stop(self):
        self._tsltcp.stop()

    def get_proto(self) -> OutputProto:
        return self._tsltcp.get_proto()

    def on_message(self, message: T, notifier: Notifier[T]):
        self._filter.on_message(message, notifier)

    def get_descriptor(self) -> Descriptor:
        ans = super().get_descriptor()
        ans.ip = self.get_ip()
        ans.port = self.get_port()
        ans.transport = self.get_transport()
        ans.filtered_cameras = self._filter.get_filter_set()
        return ans


class JsonTCPServer(NetworkOutputServer):
    def __init__(self, ip: str, port: int, repeat_for_new=False):
        self._tcp_server = TCPServer(ip, port, repeat_for_new)
        self._json_encoder = RossEventToJson(self._tcp_server)

    def get_ip(self) -> str:
        return self._tcp_server.get_ip()

    def get_port(self) -> int:
        return self._tcp_server.get_port()

    def get_transport(self) -> NetworkTransport:
        return NetworkTransport.TCP

    def start(self):
        self._tcp_server.start()

    def stop(self):
        self._tcp_server.stop()

    def get_proto(self) -> OutputProto:
        return OutputProto.JSON

    def on_message(self, message: RossEvent, notifier: Notifier[RossEvent]):
        self._json_encoder(message, notifier)


class ServersModel:
    def __init__(self, ip: str, listener_port=1337):
        self._multiplexor: Multiplexor = Multiplexor()
        ross_decoder = RossDecoder(self._multiplexor)
        umd_decoder = UMDDecoder(ross_decoder)
        self._udp_server = UDPServer(umd_decoder, host=ip, port=listener_port)
        self._ip = ip
        self._listener_port = listener_port

    def run(self):
        """
            starts a listening for incoming packets
        """
        self._udp_server.run()

    def get_descriptors(self) -> Dict[int, Descriptor]:
        """
            returns dict from id of server to its descriptor
        """
        return dict((k, v.get_descriptor()) for k, v in self._multiplexor.get_listeners().items())

    def delete_server(self, listener_id: int):
        """
            deletes listener by its id
            the listener will be stopped (if possible)
            and it will not get any new messages from the model
        """
        listener = self._multiplexor.delete_listener(listener_id)
        if issubclass(type(listener), OutputServer):
            listener.stop()

    def add_tslumd(self, port, repeat_for_new=False) -> int:
        """
            creates and starts a new TSLTCPServer
        """
        server = TSLTCPServer(self._ip, port, repeat_for_new)
        server.start()
        return self._multiplexor.add_listener(server)

    def add_eztslumd(self, port, repeat_for_new=False) -> int:
        """
            creates and starts a new EzTSLTCPServer
        """
        server = EzTSLTCPServer(self._ip, port, repeat_for_new)
        server.start()
        return self._multiplexor.add_listener(server)

    def add_filtered_tslumd(self, port, filtered_cameras, repeat_for_new=False) -> int:
        """
            creates and starts a new FilteredTSLTCPServer
        """
        server = FilteredTSLTCPServer(self._ip, port, filtered_cameras, repeat_for_new)
        server.start()
        return self._multiplexor.add_listener(server)

    def add_filtered_eztslumd(self, port, filtered_cameras, repeat_for_new=False) -> int:
        """
            creates and starts a new FilteredEzTSLTCPServer
        """
        server = FilteredEzTSLTCPServer(self._ip, port, filtered_cameras, repeat_for_new)
        server.start()
        return self._multiplexor.add_listener(server)

    def add_sound(self, sound_directory="./sounds/", file_name_fun: Optional[Callable[[RossEvent], str]] = None) -> int:
        """
            creates and starts a new SoundServer (SoundEncoder)
        """
        server = SoundEncoder(sound_directory)
        server.start()
        return self._multiplexor.add_listener(server)

    def add_json(self, port, repeat_for_new=False) -> int:
        """
            creates and starts a new JsonTCPServer
        """
        server = JsonTCPServer(self._ip, port, repeat_for_new)
        server.start()
        return self._multiplexor.add_listener(server)

    def write_json_config(self, filename):
        config_dict = {"ip": self._ip, "listener_port": self._listener_port, 'descriptors': {}}

        for key, value in self.get_descriptors().items():
            config_dict['descriptors'][key] = value.to_dict()

        print(config_dict)
        with open(filename, 'w') as f:
            json.dump(config_dict, f, indent=4)


def get_model_from_json(filename) -> ServersModel:
    with open(filename) as f:
        config_dict = json.load(f)
    ip = config_dict.pop('ip')
    listener_port = config_dict.pop('listener_port')
    model = ServersModel(ip, listener_port)
    desc_dict = config_dict['descriptors']
    for key, value in desc_dict.items():
        proto = OutputProto(value['protocol'])
        if proto == OutputProto.SOUND:
            model.add_sound()
        if proto == OutputProto.JSON:
            model.add_json(value['port'])
        if proto == OutputProto.TSLUMD:
            if 'filtered_cameras' in value:
                model.add_filtered_tslumd(value['port'], set(value['filtered_cameras']))
            else:
                model.add_tslumd(value['port'])
        if proto == OutputProto.EZTSLUMD:
            if 'filtered_cameras' in value:
                model.add_filtered_eztslumd(value['port'], set(value['filtered_cameras']))
            else:
                model.add_eztslumd(value['port'])
    model.run()
    return model
