import os
import yaml
import time

from marioenv import MKWiiEnv
from dolphin_script.utils.actions import GCAction

from PIL import Image

if __name__ == "__main__":
    try:
        config = yaml.safe_load(open("dolphin_config.yaml", "r"))
        os.environ["ENV_PATH"] = config["ENV_PATH"]

        action = GCAction()
        action.press_Button("A")
        env = MKWiiEnv(
            dolphin_config={
                "DOLPHIN_PATH": config["DOLPHIN_PATH"],
                "DOLPHIN_ID": config["DOLPHIN_ID"][0],
                "SCRIPT_PATH": "./dolphin_script/script.py",
                "ISO_PATH": config["ISO_PATH"],
                "PIPE_PATH": config["PIPE_PATH"],
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
