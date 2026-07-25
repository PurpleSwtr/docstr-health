from enum import Enum, auto


class ModuleStatus(Enum):
    COMMON = "common"
    BAD = "bad"
    WARNING = "warning"
    GOOD = "good"
    SPECIAL = "special"
    EPIC = "epic"


class StatusDocstring(Enum):
    BAD = "bad"
    GOOD = "good"
    SPECIAL = "special"
    EPIC = "epic"

class StatusProject(Enum):
    BAD = "bad"
    WARNING = "warning"
    GOOD = "good"
    SPECIAL = "special"
    EPIC = "epic"

class StatusProjectPrioritized(Enum):
    BAD = auto()
    WARNING = auto()
    GOOD = auto()
    SPECIAL = auto()
    EPIC = auto()

class StatusTypechecking(Enum):
    NONE = "bad"
    ARGS = "warning"
    RETURN = "warning"
    FULL = "good"
