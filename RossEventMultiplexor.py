import threading
from typing import List, Set, Dict

from MessagersInterfaces import Listener, T, Notifier
from RossEvent import RossEvent
from loguru import logger as lg

class Multiplexor(Listener[RossEvent], Notifier[RossEvent]):
    """
        class that listens to one Listener[RossEvent] and notifies multiple Listeners[RossEvent]
    """
    def __init__(self):
        lg.info(f"{self} created")
        self._listenerMap: Dict[int, Listener[RossEvent]] = {}
        self._mapMutex = threading.Lock()
        self._cnt = 1

    def add_listener(self, listener: Listener[RossEvent]) -> int:
        """
        add a listener that will be notified by the multiplexor

        :param listener: listener to add
        :type listener: Listener[RossEvent]

        :return: id of listener
        """
        with self._mapMutex:
            self._listenerMap[self._cnt] = listener
            self._cnt += 1
            lg.info(f"{self} new listener, listeners: {self._listenerMap}")
            return self._cnt - 1

    def on_message(self, message: RossEvent, notifier: Notifier[RossEvent]):
        lg.info(f"{self} got {message} from {notifier}, i must send it to {self._listenerMap}")
        with self._mapMutex:
            for listener in self._listenerMap.values():
                lg.info("sending message to {listener}")
                listener(message, self)

    def get_listeners(self) -> Dict[int, Listener[RossEvent]]:
        """
        :return: set of listener that multiplexor notifies
        """
        with self._mapMutex:
            return self._listenerMap.copy()

    def delete_listener(self, listener_id: int) -> Listener[RossEvent]:
        """
        removes listener from set of listeners to be notified

        :param listener_id: id of listener to not notify anymore
        :return: the listener
        """
        with self._mapMutex:
            return self._listenerMap.pop(listener_id)
