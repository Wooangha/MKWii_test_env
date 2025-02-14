import os
import pickle
import time
import sys

from .enums import Commands, Controllers, MemoryTypes
from .actions import GCAction, WiiClassicAction, WiimoteAction, WiiNunchukAction, GBAAction

class PipeManager:
    def __init__(self, PIPE_PATH="/home/username/mario/Pipes", DOLPHIN_ID=0, remake=True):
        self.PIPE_PATH = PIPE_PATH
        self.DOLPHIN_ID = DOLPHIN_ID

        self.MAIN_PIPE = os.path.join(PIPE_PATH, f"{DOLPHIN_ID}/main_pipe")
        self.COMMAND_PIPE = os.path.join(PIPE_PATH, f"{DOLPHIN_ID}/command_pipe")
        self.WAITING_PIPE = os.path.join(PIPE_PATH, f"{DOLPHIN_ID}/waiting_pipe")

        self.remake = remake

        self.mkfifo(self.MAIN_PIPE)
        self.mkfifo(self.COMMAND_PIPE)
        self.mkfifo(self.WAITING_PIPE)

    def mkfifo(self, path):
        if not os.path.exists(os.path.dirname(path)):
            os.makedirs(os.path.dirname(path))
        try:
            os.mkfifo(path)
        except OSError as e:
            print(e)
            if self.remake:
                os.remove(path)
                os.mkfifo(path)

    def send_command(self, command: Commands):
        with open(self.COMMAND_PIPE, "wb") as command_pipe:
            pickle.dump(command, command_pipe)
            command_pipe.flush()
        time.sleep(0.0001)
        # open(self.WAITING_PIPE, "rb").close()

    def get_command(self) -> Commands:
        with open(self.COMMAND_PIPE, "rb") as command_pipe:
            # open(self.WAITING_PIPE, "wb").close()
            command = pickle.load(command_pipe)
        return command

    def send_data(self, data):
        with open(self.MAIN_PIPE, "wb") as main_pipe:
            pickle.dump(data, main_pipe)
            main_pipe.flush()
        time.sleep(0.0001)
        # open(self.WAITING_PIPE, "rb").close()

    def get_data(self):
        with open(self.MAIN_PIPE, "rb") as main_pipe:
            data = pickle.load(main_pipe)
            # open(self.WAITING_PIPE, "wb").close()
        return data
