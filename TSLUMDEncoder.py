from MessagersInterfaces import Listener, Notifier, T
from RossServer import RossEvent
from UMDDecoder import TSLEvent


class RossEventToTSLUMD(Listener[RossEvent], Notifier[bytes]):
    def __init__(self, listener: Listener[bytes]):
        self._listener = listener

    def on_message(self, message: RossEvent, notifier: Notifier[RossEvent]):
        """
        with TSLEvent modul turns RossEvent message to bytes
        Param: RossEvent
        Returns: bytes
        """
        mes_state = message.get_camera_state()
        list_of_tallies = [False] * 4
        if mes_state == 1:
            list_of_tallies = [True, False, False, False]
        elif mes_state == 2:
            list_of_tallies = [False, True, False, False]
        elif mes_state == 3:
            list_of_tallies = [True, True, False, False]
        self._listener(TSLEvent(message.get_camera_id(), list_of_tallies, 1.0).to_bytes(), self)
