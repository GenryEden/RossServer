import os.path
from typing import Any, Callable, Optional

from MessagersInterfaces import Listener, Notifier, OutputServer
from RossEvent import RossState, RossEvent
from loguru import logger as lg
import pygame
from ServerDescriptor import OutputProto


class SoundEncoder(OutputServer):

    def __init__(self, directory="./sounds/", file_name_fun: Optional[Callable[[RossEvent], str]] = None):
        self._directory = directory
        self._get_file_name = file_name_fun
        self._mx = pygame.mixer
        self._mx.init()
        self._lives: dict[int, bool] = dict()
        lg.info(f"created SoundEncoder in {directory}")

    def get_file_name(self, event: RossEvent) -> str:
        """
            returns the name of the mp3 file to play
        """
        if self._get_file_name:
            return self._get_file_name(event)
        else:
            return f"{event.camera_id}.mp3"

    def on_message(self, message: RossEvent, notifier: Notifier[RossEvent]):
        """
            sends a message about camera statement
        """
        lg.info(f"got {message} from {notifier}")
        if (message.state == RossState.PGM or message.state == RossState.BOTH) and \
                self._lives.get(message.camera_id) is not True:
            lg.info(f"playing {self._directory + self.get_file_name(message)}")
            filename = self._directory + self.get_file_name(message)
            if os.path.isfile(filename):
                self._mx.music.stop()
                self._mx.music.load(self._directory + self.get_file_name(message))
                self._mx.music.play()
            else:
                lg.info("file not found")

        if message.state == RossState.PGM or message.state == RossState.BOTH:
            self._lives[message.camera_id] = True
        else:
            self._lives[message.camera_id] = False

    def get_proto(self) -> OutputProto:
        """
            returns output protocol
        """
        return OutputProto.SOUND

    def start(self):
        pass

    def stop(self):
        pass
