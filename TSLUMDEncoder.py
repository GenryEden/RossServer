from enum import Enum
from typing import List

from MessagersInterfaces import Listener, Notifier, T
from RossServer import *
from UMDDecoder import *

class RossEventToTSLUMD(Listener[RossEvent], Notifier[bytes]):
    def __init__(self, listener: Listener[bytes]):
        self._a = bytes()
        self._a = []
        self._listener = listener

    def on_message(self, message: RossEvent, notifier: Notifier[RossEvent]):
        """
        Param:
        Returns:
        """
        mes_state = message.get_camera_state()
        b = bytes
        if mes_state == 0:
            list_of_tallies = [False, False, False, False]
        elif mes_state == 1:
            list_of_tallies = [True, False, False, False]
        elif mes_state == 2:
            list_of_tallies = [False, True, False, False]
        elif mes_state == 3:
            list_of_tallies = [True, True, False, False]
        b = TSLEvent(message.get_camera_id(), list_of_tallies, 1.0)
        self._a.append(b)
        for i in range (0, 16):
            self._a.append(0)
        self._listener(self._a, self)