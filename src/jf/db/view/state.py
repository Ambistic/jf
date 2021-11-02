from enum import Enum


class _DBViewState(Enum):
    Raw = 0
    Rel = 1
    # Obj = 2
    RelObj = 3
    RelObjAttr = 4
    Pointer = 5