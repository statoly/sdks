from enum import Enum

class Monitor_type(str, Enum):
    Http = "http",
    Ping = "ping",
    Story = "story",
    Certificate = "certificate",
    Heartbeat = "heartbeat",

