from enum import Enum

class CommandType(Enum):
    EXPR = 0
    GAMBLE_START = 1
    GAMBLE_BET = 2
    RECALL_ROLLS = 3
    ERROR = 4