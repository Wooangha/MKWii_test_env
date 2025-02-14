import time
from marioenv import MKWiiEnv

from dolphin_script.utils.actions import GCAction
from PIL import Image

if __name__ == "__main__":
    try:
        action = GCAction()
        action.press_Button("A")
        env = MKWiiEnv(
            dolphin_config={
                "DOLPHIN_PATH": "/root/dolphin/build/Binaries",
                "DOLPHIN_ID": 0,
                "SCRIPT_PATH": "./dolphin_script/script.py",
                "ISO_PATH": "/root/Mario Kart Wii (USA) (En,Fr,Es).wbfs",
                "PIPE_PATH": "/root/env/p",
            }
        )
        print("Connected to Dolphin")
        for i in range(100):
            env.step(action)
            (width, height, data) = env.get_frame()
            img = Image.frombytes("RGBA", (width, height), data, "raw")
            img.save(f"/root/frame_img/test_{i}.png", "PNG")
            print(f"Saved test_{i}.png")
        print("Stepped 100 times")
        for i in range(100):
            env.step(action)
        print("Stepped 100 more times")
        action.release_Button("A")
        env.step(action)

        print("Disconnecting from Dolphin")
        env.disconnect_pipe()
        time.sleep(20)

    finally:
        print("Killing Dolphin")
        env.close()
