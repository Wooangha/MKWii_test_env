from copy import deepcopy

from typing import TypedDict


class GCInputs(TypedDict, total=False):
    """
    Dictionary describing the state of a GameCube controller.
    Boolean keys (buttons): True means pressed, False means released.
    Float keys for triggers: 0 means fully released, 1 means fully pressed.
    Float keys for sticks: 0 means neutral, ranges from -1 to 1.
    """

    A: bool
    B: bool
    X: bool
    Y: bool
    Z: bool
    Start: bool
    Up: bool
    Down: bool
    Left: bool
    Right: bool
    L: bool
    R: bool
    StickX: float
    StickY: float
    CStickX: float
    CStickY: float
    TriggerLeft: float
    TriggerRight: float


class WiimoteInputs(TypedDict, total=False):
    """
    Dictionary describing the state of a Wii Remote controller.
    Boolean keys (buttons): True means pressed, False means released.
    """

    A: bool
    B: bool
    One: bool
    Two: bool
    Plus: bool
    Minus: bool
    Home: bool
    Up: bool
    Down: bool
    Left: bool
    Right: bool


class WiiClassicInputs(TypedDict, total=False):
    """
    Dictionary describing the state of a Wii Classic controller.
    Boolean keys: True means pressed, False means released.
    Float keys for triggers: 0 means fully released, 1 means fully pressed.
    Float keys for sticks: 0 means neutral, ranges from -1 to 1.
    """

    A: bool
    B: bool
    X: bool
    Y: bool
    ZL: bool
    ZR: bool
    Plus: bool
    Minus: bool
    Home: bool
    Up: bool
    Down: bool
    Left: bool
    Right: bool
    L: bool
    R: bool
    TriggerLeft: float
    TriggerRight: float
    LeftStickX: float
    LeftStickY: float
    RightStickX: float
    RightStickY: float


class WiiNunchukInputs(TypedDict, total=False):
    """
    Dictionary describing the state of a Wii Nunchuk controller.
    Boolean keys (buttons): True means pressed, False means released.
    Float keys for sticks: 0 means neutral, ranges from -1 to 1.
    """

    C: bool
    Z: bool
    StickX: float
    StickY: float


class GBAInputs(TypedDict, total=False):
    """
    Dictionary describing the state of a GameBoy Advance controller.
    Boolean keys (buttons): True means pressed, False means released.
    """

    A: bool
    B: bool
    L: bool
    R: bool
    Start: bool
    Select: bool
    Up: bool
    Down: bool
    Left: bool
    Right: bool


class GCAction:
    """
    A class to represent the action of a GameCube controller.
    """

    __RESET_INPUTS = GCInputs(
        A=False,
        B=False,
        X=False,
        Y=False,
        Z=False,
        Start=False,
        Up=False,
        Down=False,
        Left=False,
        Right=False,
        L=False,
        R=False,
        StickX=0.0,
        StickY=0.0,
        CStickX=0.0,
        CStickY=0.0,
        TriggerLeft=0.0,
        TriggerRight=0.0,
    )

    def __init__(self):
        self.__inputs = deepcopy(GCAction.__RESET_INPUTS)

    def get_inputs(self):
        """Get the inputs of the controller."""
        return self.__inputs

    def __getitem__(self, key):
        assert key in GCAction.__RESET_INPUTS
        return self.__inputs[key]

    def __setitem__(self, key, value):
        self.__inputs[key] = value

    def reset(self):
        self.__inputs = deepcopy(GCAction.__RESET_INPUTS)

    def copyfromGCInputs(self, other: GCInputs):
        self.__inputs = deepcopy(other)

    def copyfromGCAction(self, other: "GCAction"):
        self.__inputs = deepcopy(other.get_inputs())

    def press_Button(self, button):
        """
        Press a button on the controller.

        Args:
            button (str): One of "A", "B", "X", "Y", "Z", "Start", "Up", "Down", "Left", "Right", "L", "R".
            value (bool): True means pressed, False means released.
        """
        assert button in ["A", "B", "X", "Y", "Z", "Start", "Up", "Down", "Left", "Right", "L", "R"]
        self.__inputs[button] = True

    def release_Button(self, button):
        """
        Release a button on the controller.

        Args:
            button (str): One of "A", "B", "X", "Y", "Z", "Start", "Up", "Down", "Left", "Right", "L", "R".
        """
        assert button in ["A", "B", "X", "Y", "Z", "Start", "Up", "Down", "Left", "Right", "L", "R"]
        self.__inputs[button] = False

    def set_Stick(self, stick, x, y):
        """
        Set the position of a stick on the controller.

        Args:
            stick (str): One of "Stick", "CStick".
            x (float): Ranges from -1 to 1.
            y (float): Ranges from -1 to 1.
        """
        assert stick in ["Stick", "CStick"]
        assert -1 <= x <= 1 and -1 <= y <= 1
        self.__inputs[stick + "X"] = x
        self.__inputs[stick + "Y"] = y

    def reset_Stick(self, stick):
        """
        Set the position of a stick on the controller to neutral.

        Args:
            stick (str): One of "Stick", "CStick".
        """
        assert stick in ["Stick", "CStick"]
        self.__inputs[stick + "X"] = 0.0
        self.__inputs[stick + "Y"] = 0.0

    def set_Trigger(self, trigger, value):
        """
        Set the position of a trigger on the controller.

        Args:
            trigger (str): One of "TriggerLeft", "TriggerRight".
            value (float): Ranges from 0 to 1.
        """
        assert trigger in ["TriggerLeft", "TriggerRight"]
        assert 0 <= value <= 1
        self.__inputs[trigger] = value

    def reset_Trigger(self, trigger):
        """
        Set the position of a trigger on the controller to fully released.

        Args:
            trigger (str): One of "TriggerLeft", "TriggerRight".
        """
        assert trigger in ["TriggerLeft", "TriggerRight"]
        self.__inputs[trigger] = 0.0

    @property
    def A(self):
        return self.__inputs["A"]

    @property
    def B(self):
        return self.__inputs["B"]

    @property
    def X(self):
        return self.__inputs["X"]

    @property
    def Y(self):
        return self.__inputs["Y"]

    @property
    def Z(self):
        return self.__inputs["Z"]

    @property
    def Start(self):
        return self.__inputs["Start"]

    @property
    def Up(self):
        return self.__inputs["Up"]

    @property
    def Down(self):
        return self.__inputs["Down"]

    @property
    def Left(self):
        return self.__inputs["Left"]

    @property
    def Right(self):
        return self.__inputs["Right"]

    @property
    def L(self):
        return self.__inputs["L"]

    @property
    def R(self):
        return self.__inputs["R"]

    @property
    def StickX(self):
        return self.__inputs["StickX"]

    @property
    def StickY(self):
        return self.__inputs["StickY"]

    @property
    def CStickX(self):
        return self.__inputs["CStickX"]

    @property
    def CStickY(self):
        return self.__inputs["CStickY"]

    @property
    def TriggerLeft(self):
        return self.__inputs["TriggerLeft"]

    @property
    def TriggerRight(self):
        return self.__inputs["TriggerRight"]


class WiimoteAction:
    """
    A class to represent the action of a Wii Remote controller.
    """

    __RESET_INPUTS = WiimoteInputs(
        A=False,
        B=False,
        One=False,
        Two=False,
        Plus=False,
        Minus=False,
        Home=False,
        Up=False,
        Down=False,
        Left=False,
        Right=False,
    )

    def __init__(self):
        self.__inputs = deepcopy(WiimoteAction.__RESET_INPUTS)

    def get_inputs(self):
        """Get the inputs of the controller."""
        return self.__inputs

    def __getitem__(self, key):
        assert key in WiimoteAction.__RESET_INPUTS
        return self.__inputs[key]

    def __setitem__(self, key, value):
        self.__inputs[key] = value

    def reset(self):
        self.__inputs = deepcopy(WiimoteAction.__RESET_INPUTS)

    def copyfromWiimoteInputs(self, other: WiimoteInputs):
        self.__inputs = deepcopy(other)

    def copyfromWiimoteAction(self, other: "WiimoteAction"):
        self.__inputs = deepcopy(other.get_inputs())

    def press_Button(self, button):
        """
        Press a button on the controller.

        Args:
            button (str): One of "A", "B", "One", "Two", "Plus", "Minus", "Home", "Up", "Down", "Left", "Right".
            value (bool): True means pressed, False means released.
        """
        assert button in ["A", "B", "One", "Two", "Plus", "Minus", "Home", "Up", "Down", "Left", "Right"]
        self.__inputs[button] = True

    def release_Button(self, button):
        """
        Release a button on the controller.

        Args:
            button (str): One of "A", "B", "One", "Two", "Plus", "Minus", "Home", "Up", "Down", "Left", "Right".
        """
        assert button in ["A", "B", "One", "Two", "Plus", "Minus", "Home", "Up", "Down", "Left", "Right"]
        self.__inputs[button] = False

    @property
    def A(self):
        return self.__inputs["A"]

    @property
    def B(self):
        return self.__inputs["B"]

    @property
    def One(self):
        return self.__inputs["One"]

    @property
    def Two(self):
        return self.__inputs["Two"]

    @property
    def Plus(self):
        return self.__inputs["Plus"]

    @property
    def Minus(self):
        return self.__inputs["Minus"]

    @property
    def Home(self):
        return self.__inputs["Home"]

    @property
    def Up(self):
        return self.__inputs["Up"]

    @property
    def Down(self):
        return self.__inputs["Down"]

    @property
    def Left(self):
        return self.__inputs["Left"]

    @property
    def Right(self):
        return self.__inputs["Right"]


class WiiClassicAction:
    """
    A class to represent the action of a Wii Classic controller.
    """

    __RESET_INPUTS = WiiClassicInputs(
        A=False,
        B=False,
        X=False,
        Y=False,
        ZL=False,
        ZR=False,
        Plus=False,
        Minus=False,
        Home=False,
        Up=False,
        Down=False,
        Left=False,
        Right=False,
        L=False,
        R=False,
        TriggerLeft=0.0,
        TriggerRight=0.0,
        LeftStickX=0.0,
        LeftStickY=0.0,
        RightStickX=0.0,
        RightStickY=0.0,
    )

    def __init__(self):
        self.__inputs = deepcopy(WiiClassicAction.__RESET_INPUTS)

    def get_inputs(self):
        """Get the inputs of the controller."""
        return self.__inputs

    def __getitem__(self, key):
        assert key in WiiClassicAction.__RESET_INPUTS
        return self.__inputs[key]

    def __setitem__(self, key, value):
        self.__inputs[key] = value

    def reset(self):
        self.__inputs = deepcopy(WiiClassicAction.__RESET_INPUTS)

    def copyfromWiiClassicInputs(self, other: WiiClassicInputs):
        self.__inputs = deepcopy(other)

    def copyfromWiiClassicAction(self, other: "WiiClassicAction"):
        self.__inputs = deepcopy(other.get_inputs())

    def press_Button(self, button):
        """
        Press a button on the controller.

        Args:
            button (str): One of "A", "B", "X", "Y", "ZL", "ZR", "Plus", "Minus", "Home", "Up", "Down", "Left", "Right", "L", "R".
            value (bool): True means pressed, False means released.
        """
        assert button in ["A", "B", "X", "Y", "ZL", "ZR", "Plus", "Minus", "Home", "Up", "Down", "Left", "Right", "L", "R"]
        self.__inputs[button] = True

    def release_Button(self, button):
        """
        Release a button on the controller.

        Args:
            button (str): One of "A", "B", "X", "Y", "ZL", "ZR", "Plus", "Minus", "Home", "Up", "Down", "Left", "Right", "L", "R".
        """
        assert button in [
            "A",
            "B",
            "X",
            "Y",
            "ZL",
            "ZR",
            "Plus",
            "Minus",
            "Home",
            "Up",
            "Down",
            "Left",
            "Right",
            "L",
            "R",
        ]
        self.__inputs[button] = False

    def set_Stick(self, stick, x, y):
        """
        Set the position of a stick on the controller.

        Args:
            stick (str): One of "LeftStick", "RightStick".
            x (float): Ranges from -1 to 1.
            y (float): Ranges from -1 to 1.
        """
        assert stick in ["LeftStick", "RightStick"]
        assert -1 <= x <= 1 and -1 <= y <= 1
        self.__inputs[stick + "X"] = x
        self.__inputs[stick + "Y"] = y

    def reset_Stick(self, stick):
        """
        Set the position of a stick on the controller to neutral.

        Args:
            stick (str): One of "LeftStick", "RightStick".
        """
        assert stick in ["LeftStick", "RightStick"]
        self.__inputs[stick + "X"] = 0.0
        self.__inputs[stick + "Y"] = 0.0

    def set_Trigger(self, trigger, value):
        """
        Set the position of a trigger on the controller.

        Args:
            trigger (str): One of "TriggerLeft", "TriggerRight".
            value (float): Ranges from 0 to 1.
        """
        assert trigger in ["TriggerLeft", "TriggerRight"]
        assert 0 <= value <= 1
        self.__inputs[trigger] = value

    def reset_Trigger(self, trigger):
        """
        Set the position of a trigger on the controller to fully released.

        Args:
            trigger (str): One of "TriggerLeft", "TriggerRight".
        """
        assert trigger in ["TriggerLeft", "TriggerRight"]
        self.__inputs[trigger] = 0.0

    @property
    def A(self):
        return self.__inputs["A"]

    @property
    def B(self):
        return self.__inputs["B"]

    @property
    def X(self):
        return self.__inputs["X"]

    @property
    def Y(self):
        return self.__inputs["Y"]

    @property
    def ZL(self):
        return self.__inputs["ZL"]

    @property
    def ZR(self):
        return self.__inputs["ZR"]

    @property
    def Plus(self):
        return self.__inputs["Plus"]

    @property
    def Minus(self):
        return self.__inputs["Minus"]

    @property
    def Home(self):
        return self.__inputs["Home"]

    @property
    def Up(self):
        return self.__inputs["Up"]

    @property
    def Down(self):
        return self.__inputs["Down"]

    @property
    def Left(self):
        return self.__inputs["Left"]

    @property
    def Right(self):
        return self.__inputs["Right"]

    @property
    def L(self):
        return self.__inputs["L"]

    @property
    def R(self):
        return self.__inputs["R"]

    @property
    def TriggerLeft(self):
        return self.__inputs["TriggerLeft"]

    @property
    def TriggerRight(self):
        return self.__inputs["TriggerRight"]

    @property
    def LeftStickX(self):
        return self.__inputs["LeftStickX"]

    @property
    def LeftStickY(self):
        return self.__inputs["LeftStickY"]

    @property
    def RightStickX(self):
        return self.__inputs["RightStickX"]

    @property
    def RightStickY(self):
        return self.__inputs["RightStickY"]


class WiiNunchukAction:
    """
    A class to represent the action of a Wii Nunchuk controller.
    """

    __RESET_INPUTS = WiiNunchukInputs(
        C=False,
        Z=False,
        StickX=0.0,
        StickY=0.0,
    )

    def __init__(self):
        self.__inputs = deepcopy(WiiNunchukAction.__RESET_INPUTS)

    def get_inputs(self):
        return self.__inputs

    def __getitem__(self, key):
        assert key in WiiNunchukAction.__RESET_INPUTS
        return self.__inputs[key]

    def __setitem__(self, key, value):
        self.__inputs[key] = value

    def reset(self):
        self.__inputs = deepcopy(WiiNunchukAction.__RESET_INPUTS)

    def copyfromWiiNunchukInputs(self, other: WiiNunchukInputs):
        self.__inputs = deepcopy(other)

    def copyfromWiiNunchukAction(self, other: "WiiNunchukAction"):
        self.__inputs = deepcopy(other.get_inputs())

    def press_Button(self, button):
        assert button in ["C", "Z"]
        self.__inputs[button] = True

    def release_Button(self, button):
        assert button in ["C", "Z"]
        self.__inputs[button] = False

    def set_Stick(self, x, y):
        assert -1 <= x <= 1 and -1 <= y <= 1
        self.__inputs["StickX"] = x
        self.__inputs["StickY"] = y

    def reset_Stick(self):
        self.__inputs["StickX"] = 0.0
        self.__inputs["StickY"] = 0.0

    @property
    def C(self):
        return self.__inputs["C"]

    @property
    def Z(self):
        return self.__inputs["Z"]

    @property
    def StickX(self):
        return self.__inputs["StickX"]

    @property
    def StickY(self):
        return self.__inputs["StickY"]


class GBAAction:
    """
    A class to represent the action of a GameBoy Advance
    """

    __RESET_INPUTS = GBAInputs(
        A=False,
        B=False,
        L=False,
        R=False,
        Start=False,
        Select=False,
        Up=False,
        Down=False,
        Left=False,
        Right=False,
    )

    def __init__(self):
        self.__inputs = deepcopy(GBAAction.__RESET_INPUTS)

    def get_inputs(self):
        return self.__inputs

    def __getitem__(self, key):
        assert key in GBAAction.__RESET_INPUTS
        return self.__inputs[key]

    def __setitem__(self, key, value):
        self.__inputs[key] = value

    def reset(self):
        self.__inputs = deepcopy(GBAAction.__RESET_INPUTS)

    def copyfromGBAInputs(self, other: GBAInputs):
        self.__inputs = deepcopy(other)

    def copyfromGBAAction(self, other: "GBAAction"):
        self.__inputs = deepcopy(other.get_inputs())

    def press_Button(self, button):
        assert button in ["A", "B", "L", "R", "Start", "Select", "Up", "Down", "Left", "Right"]
        self.__inputs[button] = True

    def release_Button(self, button):
        assert button in ["A", "B", "L", "R", "Start", "Select", "Up", "Down", "Left", "Right"]
        self.__inputs[button] = False

    @property
    def A(self):
        return self.__inputs["A"]

    @property
    def B(self):
        return self.__inputs["B"]

    @property
    def L(self):
        return self.__inputs["L"]

    @property
    def R(self):
        return self.__inputs["R"]

    @property
    def Start(self):
        return self.__inputs["Start"]

    @property
    def Select(self):
        return self.__inputs["Select"]

    @property
    def Up(self):
        return self.__inputs["Up"]

    @property
    def Down(self):
        return self.__inputs["Down"]

    @property
    def Left(self):
        return self.__inputs["Left"]

    @property
    def Right(self):
        return self.__inputs["Right"]
