from enum import Enum

class NodeRole(str, Enum):
    MEDIA_SERVER = "MEDIA_SERVER"
    LOAD_SERVER = "LOAD_SERVER"

class NodeStatus(str, Enum):
    UNKNOWN = "UNKNOWN"
    ONLINE = "ONLINE"
    OFFLINE = "OFFLINE"