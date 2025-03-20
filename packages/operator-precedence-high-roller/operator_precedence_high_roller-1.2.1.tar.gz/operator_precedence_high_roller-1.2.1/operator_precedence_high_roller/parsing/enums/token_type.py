from enum import Enum

class TokenType(Enum):
    COMMAND_START = 0
    PLUS = 1
    MINUS = 2
    MULT = 3
    DIV = 4
    LPAREN = 5
    RPAREN = 6
    COMMA = 7
    ROLL = 8
    NUM = 9
    GAMBLE = 10
    BET = 11
    RECALL = 12
    END_OF_FILE = 13
    ERROR = 14