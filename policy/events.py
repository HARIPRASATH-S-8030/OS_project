from enum import Enum, auto

class Event(Enum):
    OPEN_FILE = auto()
    AUTH_SUCCESS = auto()
    AUTH_FAILURE = auto()
    TIMER_EXPIRED = auto()
    VIEW_LIMIT_REACHED = auto()
    LOGOUT = auto()
    SANITIZE = auto()
    SANITIZE_COMPLETE = auto()