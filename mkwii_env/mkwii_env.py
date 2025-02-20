import os
import signal
import subprocess
import pickle
import json

import enum
import sys

from actions import GCAction, WiiClassicAction, WiimoteAction, WiiNunchukAction, GBAAction
from enums import Commands
from pipe_manager import PipeManager

import gym
from gym.spaces import Box, Discrete, Tuple


class Dolphin:
    def __init__(
        self,
        DOLPHIN_PATH="/root/dolphin/build/Binaries",
        DOLPHIN_ID=0,
        SCRIPT_PATH="/root/mkwii_env/dolphin_scripts/dolphin_script.py",
        ISO_PATH="/root/Mario Kart Wii (USA) (En,Fr,Es).wbfs",
        PIPE_PATH="/root/mkwii_env/Pipes",
    ):
        self.DOLPHIN_PATH = DOLPHIN_PATH
        self.DOLPHIN_ID = DOLPHIN_ID
        self.SCRIPT_PATH = SCRIPT_PATH,
        self.ISO_PATH = ISO_PATH
        self.PIPE_PATH = PIPE_PATH

        self.pipes = PipeManager(PIPE_PATH, DOLPHIN_ID)

        self.dolphin = None
        self.connect()

    def connect(self):
        if self.dolphin is None:
            self.dolphin = subprocess.Popen(
                f'"{self.DOLPHIN_PATH}/dolphin-emu" --script "{self.SCRIPT_PATH}" "{self.ISO_PATH}"',
                stdin=subprocess.PIPE,
                shell=True,
                text=True,
                # input=json.dumps([self.PIPE_PATH, self.DOLPHIN_ID]).encode(),
            )
            self.dolphin.stdin.write(json.dumps([self.PIPE_PATH, self.DOLPHIN_ID]) + "\n")
            self.dolphin.stdin.flush()
        else:
            print("Dolphin is already running.")

    def mkfifo(self, path):
        if not os.path.exists(os.path.dirname(path)):
            os.makedirs(os.path.dirname(path))
        try:
            os.mkfifo(path)
        except OSError as e:
            print(e)
            os.remove(path)
            os.mkfifo(path)

    def step(
        self,
        action: (
            dict[int, GCAction | WiiClassicAction | WiimoteAction | WiiNunchukAction | GBAAction]
            | GCAction
            | WiiClassicAction
            | WiimoteAction
            | WiiNunchukAction
            | GBAAction
        ),
    ):
        """
        Args:
            action (dict[int, GCAction | WiiClassicAction | WiimoteAction | WiiNunchukAction | GBAAction] | GCAction | WiiClassicAction | WiimoteAction | WiiNunchukAction | GBAAction): The action to be performed by the emulator.
        """
        if not isinstance(action, dict):
            action = {0: action}
        for controller_id, action in action.items():
            action.__module__ = "actions"
        self.pipes.send_command(Commands.DO_ACTION)
        self.pipes.send_data(action)
        state = self.pipes.get_data()

        return state

    def set_wiimote_pointer(self, controller_id: int, x: float, y: float):
        self.pipes.send_command(Commands.SET_WIIMOTE_POINTER)
        self.pipes.send_data((controller_id, x, y))

    def get_frame(self) -> tuple[int, int, bytes]:
        self.pipes.send_command(Commands.GET_FRAME)
        (width, height, data) = self.pipes.get_data()

        return width, height, data

    def get_state(self):
        self.pipes.send_command(Commands.GET_STATE)
        state = self.pipes.get_data()

        return state

    def disconnect_pipe(self):
        self.pipes.send_command(Commands.END)

    def reset(self):
        self.kill()
        self.connect()

    def kill(self):
        if self.dolphin.poll() is None:
            os.killpg(os.getpgid(self.dolphin.pid), signal.SIGKILL)
            self.dolphin = None


class MKWiiEnv(gym.Env):
    def __init__(
        self,
        dolphin_config={
            "DOLPHIN_PATH": "/root/dolphin/build/Binaries",
            "DOLPHIN_ID": 0,
            "SCRIPT_PATH": "/root/mkwii_env/dolphin_scripts/dolphin_script.py",
            "ISO_PATH": "/root/Mario Kart Wii (USA) (En,Fr,Es).wbfs",
            "PIPE_PATH": "/root/mkwii_env/Pipes",
        },
    ):
        self.dolphin = Dolphin(**dolphin_config)
        self.n = 0
        self.observation_space = Tuple(
            [
                Box(low=0, high=255, shape=(640, 348, 4), dtype=int),  # image RGBA
                Box(low=0, high=1, shape=(1,), dtype=float),
            ]
        )

    def step(
        self,
        action: (
            dict[int, GCAction | WiiClassicAction | WiimoteAction | WiiNunchukAction | GBAAction]
            | GCAction
            | WiiClassicAction
            | WiimoteAction
            | WiiNunchukAction
            | GBAAction
        ) = GCAction(),
    ):
        """
        Args:
            action (GCAction | WiiClassicAction | WiimoteAction | WiiNunchukAction | GBAAction, optional): The action to be performed by the emulator. Defaults to GCAction().
        """
        return self.dolphin.step(action), 0, False, {}

    def set_wiimote_pointer(self, controller_id: int, x: float, y: float):
        self.dolphin.set_wiimote_pointer(controller_id, x, y)

    def get_obs(self):
        return (self.dolphin.get_frame(), self.dolphin.get_state())

    def get_frame(self):
        return self.dolphin.get_frame()

    def get_state(self):
        return self.dolphin.get_state()

    def reset(self):
        return self.dolphin.reset()

    def disconnect_pipe(self):
        self.dolphin.disconnect_pipe()

    def close(self):
        self.dolphin.kill()
        super().close()

    @enum.unique
    class MacroFlags(enum.Flag):
        NONE = 0
