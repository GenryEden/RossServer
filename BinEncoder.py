from enum import Enum
from typing import List

from MessagersInterfaces import Listener, Notifier, T
from RossServer import *
from UMDDecoder import *


def translation(local_list) -> bytes:
    a = bytes()
    a[0] = 32
    for i in range(1, 33):
        a[i] += local_list[i * 8 - 7]
        a[i] <<= 1
        'now length 2'
        a[i] += local_list[i * 8 - 6]
        a[i] <<= 1
        'now length 4'
        a[i] += local_list[i * 8 - 5]
        a[i] += local_list[i * 8 - 4]
        a[i] <<= 1
        'now length 8'
        a[i] += local_list[i * 8 - 3]
        a[i] += local_list[i * 8 - 2]
        a[i] += local_list[i * 8 - 1]
        a[i] += local_list[i * 8]
    return a


class RossEventToJson(Listener[RossEvent], Notifier[bytes]):
    def __init__(self, listener: Listener[bytes], num_of_cam=127):
        """Fills the "list_of_cam" with the corresponding states ["RossState.OUT.value"]
        of the corresponding cameras ["cam_num"]"""
        self._listener = listener
        self._cam_num = num_of_cam
        self._list_of_cam = [RossState.OUT.value] * self._cam_num

    def on_message(self, message: RossEvent, notifier: Notifier[RossEvent]):
        """
        Recieves int "num_of_cam and RossState.OUT.value and give both variables
        to listener in ascii form
        Param:
        Returns:
        """
        self._list_of_cam[message.get_camera_id()] = message.get_camera_state()
        local_list: list[int] = self._list_of_cam
        a = translation(self._list_of_cam)
        self._listener(a, self)

        'Написать чистую функцию, которая по листо оф кэм генерит байтс' \
        'может быть оверхэд'
