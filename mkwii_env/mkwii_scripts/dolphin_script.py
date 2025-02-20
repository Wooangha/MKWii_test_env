import os
import sys
import asyncio
import json
import time


sys.path.append(os.environ.get("MKWII_ENV_PATH", "/root/mkwii_env"))
from actions import GCAction
from enums import Commands
from pipe_manager import PipeManager
from mkwii_scripts.dolphin_manager import DolphinManager


PIPE_PATH, DOLPHIN_ID = json.loads(sys.stdin.readline())
pipe = PipeManager(PIPE_PATH=PIPE_PATH, DOLPHIN_ID=DOLPHIN_ID, remake=False)
manager = DolphinManager()

red = 0xFFFF0000

steps = 0
start = time.time()
while True:
    command = pipe.get_command()
    match command:
        case Commands.DO_ACTION:
            action = pipe.get_data()
            manager.set_action(action)
            await manager.step()
            pipe.send_data(manager.get_frame())
        case Commands.GET_FRAME:
            pipe.send_data(manager.get_frame())
        case Commands.GET_STATE:
            # manager.get_state()  # TODO: Not Implemented get_state
            pipe.send_data(None)
        case Commands.SET_WIIMOTE_POINTER:
            controller_id, x, y = pipe.get_data()
            manager.set_wiimote_pointer(controller_id, x, y)
        case Commands.END:
            break
    # print(f"Step: {steps}")
    steps += 1
    if steps % 100 == 0:
        print(f"Avg FPS: {steps / (time.time() - start)}")
while True:
    await manager.step()
