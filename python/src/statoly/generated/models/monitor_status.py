from enum import Enum

class Monitor_status(str, Enum):
    Up = "up",
    Down = "down",
    Degraded = "degraded",

