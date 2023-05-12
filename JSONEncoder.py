from RossServer import *
from UMDDecoder import *
import json


class RossEventToJson(Listener[RossEvent], Notifier[bytes]):
    def __init__(self, listener: Listener[bytes], num_of_cam=127):
        """
        Fills the "list_of_cam" (length = num_of_cam) with the corresponding states ["RossState.OUT.value"]
        of the corresponding cameras ["cam_num"]
        """
        self._listener = listener
        self._cam_num = num_of_cam
        self._list_of_cam = [RossState.OUT.value] * self._cam_num

    def on_message(self, message: RossEvent, notifier: Notifier[RossEvent]):
        """
        Recieves int "num_of_cam and RossState.OUT.value and give both variables
        to listener in ascii form
        Param: RossState
        Notifies: json in ASCII
        """
        if message.get_camera_id() >= len(self._list_of_cam):
            return
        self._list_of_cam[message.get_camera_id()] = message.get_camera_state()
        local_list = self._list_of_cam
        local_list = json.dumps(self._list_of_cam, separators=(',', ':'))
        local_list = local_list.encode("ascii")
        self._listener(local_list, self)
