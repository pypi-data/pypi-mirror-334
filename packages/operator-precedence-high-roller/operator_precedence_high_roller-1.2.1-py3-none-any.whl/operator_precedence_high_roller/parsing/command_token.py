from .enums.token_type import TokenType

class Token:
    def __init__(self):
        self.lexeme: str = ""
        self.TokenType: TokenType = TokenType.ERROR