from .command_token import Token
from operator_precedence_high_roller.parsing.enums.token_type import TokenType

class StackNode:
    def __init__(self):
        self.is_terminal: bool = True
        self.token_info: Token = Token()
        self.oper: TokenType = None
        self.left: StackNode = None
        self.right: StackNode = None