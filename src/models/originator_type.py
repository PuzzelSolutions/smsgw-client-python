from enum import Enum

class OriginatorType(str, Enum):
    International = "International",
    Alphanumeric = "Alphanumeric",
    Network = "Network",

