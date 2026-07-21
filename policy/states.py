from enum import Enum, auto

class State(Enum):
    IDLE = auto()
    AUTHENTICATING = auto()
    SECURE_RENDER = auto()
    REVOKED = auto()
    SANITIZING = auto()
    TERMINATED = auto()