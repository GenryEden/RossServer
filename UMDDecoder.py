from __future__ import annotations

from functools import reduce

import ServersExceptions
from MessagersInterfaces import Listener, Notifier
from loguru import logger as lg


class TSLEvent:
    """
        class to represent info from TSL messages
    """

    def __init__(self, camera_num: int, tallies: list[bool], brightness: float, message: str = ""):
        """
        :param camera_num: unique ID of camera
        :param tallies: list of bools to represent state of each tally
        :param brightness: brightness of tally
        :param message: text field from TSL message
        """
        self.cameraNum = camera_num
        self.tallies = tallies.copy()
        self.message = message[:16].ljust(16)
        self.brightness = brightness

    def __str__(self) -> str:
        return f"#{self.cameraNum},\tstate {list(map(int, self.tallies))},\tbrght={self.brightness},\tmsg=\"{self.message}\""

    def to_bytes(self) -> bytes:
        ans = [self.cameraNum + 0x80, 0]
        if self.brightness == 0:
            pass
        elif self.brightness == 1 / 2:
            ans[1] += 1
        elif self.brightness == 1 / 7:
            ans[1] += 2
        else:
            ans[1] += 3
        for tally in self.tallies[::-1]:
            ans[1] <<= 1
            ans[1] += tally
        return bytes(ans) + self.message.encode()


def get_event_by_message(message: bytes) -> TSLEvent:
    """
    converts bytes of TSL message to TSLEvent class

    :param message: 18 bytes of TSL message
    :return: TSLEvent
    """
    if len(message) != 18:
        raise ServersExceptions.IncorrectTSLMessage(f"Length of message was {len(message)}")
    found_id = message[0] - 0x80
    control = message[1]
    tallies: list[bool] = []
    for _ in range(4):
        tallies.append(bool(control % 2))
        control >>= 1
    control %= 4
    if control == 0:
        brightness = 0
    elif control == 1:
        brightness = 0.5
    elif control == 2:
        brightness = 1 / 7
    else:
        brightness = 1
    return TSLEvent(
        camera_num=found_id,
        tallies=tallies,
        brightness=brightness,
        message=message[2:].decode('ascii')
    )


class UMDDecoder(Listener[bytes], Notifier[TSLEvent]):
    """
        converter of TSL messages to TSL events
    """

    def __init__(self, listener: Listener[TSLEvent]):
        self._listener = listener

    def on_message(self, message: bytes, notifier: Notifier[bytes]):
        start = 0
        while start < len(message):
            submessage = message[start:start + 18]
            if type(submessage) == int:
                lg.warning(f"Got incorrect message of len {len(message)}, last part is {submessage}")
                break
            if len(submessage) != 18:
                lg.warning(f"Got incorrect message of len {len(message)}, last part is {submessage}")
                break
            self._listener(get_event_by_message(submessage), self)
            start += 18
