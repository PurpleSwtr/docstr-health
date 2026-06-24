from enum import Enum


class StatusDocstring(Enum):
    BAD = "bad"
    GOOD = "good"
    SPECIAL = "special"
    EPIC = "epic"


class StatusTypechecking(Enum):
    NONE = "bad"
    ARGS = "waning"
    RETURN = "waning"
    FULL = "good"
