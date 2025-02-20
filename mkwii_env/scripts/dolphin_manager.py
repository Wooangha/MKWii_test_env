import os
import sys

sys.path.append("/root/mkwii_env")
from dolphin import event, memory, controller
from utils.enums import MemoryTypes, Controllers
from utils.actions import GCAction, WiiClassicAction, WiimoteAction, WiiNunchukAction, GBAAction


class DolphinManager:
    """Interface class to manage communication with the Dolphin emulator.

    This class provides methods to:
    - Retrieve and step through frame data.
    - Access and modify emulator memory with support for different memory types.
    - Configure actions for various controller types (GameCube, Wiimote, Wii Classic, Wii Nunchuk, and GBA).

    It serves as a central point for managing simulator state and input events.
    """
    def __init__(self):
        self.width = None
        self.height = None
        self.frame_data = None

    async def step(self) -> tuple[int, int, bytes]:
        (self.width, self.height, self.frame_data) = await event.framedrawn()
        return self.width, self.height, self.frame_data

    def get_frame(self) -> tuple[int, int, bytes]:
        return self.width, self.height, self.frame_data

    def get_state(self) -> None:
        raise NotImplementedError

    def set_gc_action(self, action: dict[int, GCAction]) -> None:
        for controller_id, gc_action in action.items():
            controller.set_gc_buttons(controller_id, gc_action.get_inputs())

    def set_wiimote_action(self, action: dict[int, WiimoteAction]) -> None:
        for controller_id, wiimote_action in action.items():
            controller.set_wiimote_buttons(controller_id, wiimote_action.get_inputs())

    def set_wiimote_pointer(self, controller_id: int, x: float, y: float) -> None:
        controller.set_wiimote_pointer(controller_id, x, y)

    def set_wii_classic_action(self, action: dict[int, WiiClassicAction]) -> None:
        for controller_id, wii_classic_action in action.items():
            controller.set_wii_classic_buttons(controller_id, wii_classic_action.get_inputs())

    def set_wii_nunchuk_action(self, action: dict[int, WiiNunchukAction]) -> None:
        for controller_id, wii_nunchuk_action in action.items():
            controller.set_wii_nunchuk_buttons(controller_id, wii_nunchuk_action.get_inputs())

    def set_gba_action(self, action: dict[int, GBAAction]) -> None:
        for controller_id, gba_action in action.items():
            controller.set_gba_buttons(controller_id, gba_action.get_inputs())

    def set_action(
        self,
        action: dict[int, GCAction | WiimoteAction | WiiClassicAction | WiiNunchukAction | GBAAction],
    ) -> None:
        for controller_id, controller_action in action.items():
            if isinstance(controller_action, GCAction):
                self.set_gc_action({controller_id: controller_action})
            elif isinstance(controller_action, WiimoteAction):
                self.set_wiimote_action({controller_id: controller_action})
            elif isinstance(controller_action, WiiClassicAction):
                self.set_wii_classic_action({controller_id: controller_action})
            elif isinstance(controller_action, WiiNunchukAction):
                self.set_wii_nunchuk_action({controller_id: controller_action})
            elif isinstance(controller_action, GBAAction):
                self.set_gba_action({controller_id: controller_action})
            else:
                raise ValueError("Invalid controller action")

    def get_memory(self, address: int, memory_type: MemoryTypes) -> int | float:
        match memory_type:
            case MemoryTypes.u8:
                return memory.read_u8(address)
            case MemoryTypes.u16:
                return memory.read_u16(address)
            case MemoryTypes.u32:
                return memory.read_u32(address)
            case MemoryTypes.u64:
                return memory.read_u64(address)
            case MemoryTypes.s8:
                return memory.read_s8(address)
            case MemoryTypes.s16:
                return memory.read_s16(address)
            case MemoryTypes.s32:
                return memory.read_s32(address)
            case MemoryTypes.s64:
                return memory.read_s64(address)
            case MemoryTypes.f32:
                return memory.read_f32(address)
            case MemoryTypes.f64:
                return memory.read_f64(address)
            case _:
                raise ValueError("Invalid memory type")

    def set_memory(self, address: int, value: int | float, memory_type: MemoryTypes) -> None:
        match memory_type:
            case MemoryTypes.u8:
                memory.write_u8(address, value)
            case MemoryTypes.u16:
                memory.write_u16(address, value)
            case MemoryTypes.u32:
                memory.write_u32(address, value)
            case MemoryTypes.u64:
                memory.write_u64(address, value)
            case MemoryTypes.s8:
                memory.write_s8(address, value)
            case MemoryTypes.s16:
                memory.write_s16(address, value)
            case MemoryTypes.s32:
                memory.write_s32(address, value)
            case MemoryTypes.s64:
                memory.write_s64(address, value)
            case MemoryTypes.f32:
                memory.write_f32(address, value)
            case MemoryTypes.f64:
                memory.write_f64(address, value)
            case _:
                raise ValueError("Invalid memory type")
