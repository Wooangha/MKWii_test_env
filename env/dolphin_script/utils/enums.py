import enum


@enum.unique
class Commands(enum.Enum):
    DO_ACTION = 0
    GET_FRAME = 1
    GET_STATE = 2
    SET_WIIMOTE_POINTER = 3
    END = 4


@enum.unique
class MemoryTypes(enum.Enum):
    """
    u8: 1 byte unsigned integer\n
    u16: 2 byte unsigned integer\n
    u32: 4 byte unsigned integer\n
    u64: 8 byte unsigned integer\n
    s8: 1 byte signed integer\n
    s16: 2 byte signed integer\n
    s32: 4 byte signed integer\n
    s64: 8 byte signed integer\n
    f32: 4 byte float\n
    f64: 8 byte float
    """

    u8 = 0
    u16 = 1
    u32 = 2
    u64 = 3
    s8 = 4
    s16 = 5
    s32 = 6
    s64 = 7
    f32 = 8
    f64 = 9


@enum.unique
class Controllers(enum.Enum):
    """
    GCAction: GameCube controller
    WiimoteAction: Wiimote
    WiiClassicAction: Wii Classic controller
    WiiNunchukAction: Wii Nunchuk
    GBAAction: Game Boy Advance
    """

    GCAction = 0
    WiimoteAction = 1
    WiiClassicAction = 2
    WiiNunchukAction = 3
    GBAAction = 4
