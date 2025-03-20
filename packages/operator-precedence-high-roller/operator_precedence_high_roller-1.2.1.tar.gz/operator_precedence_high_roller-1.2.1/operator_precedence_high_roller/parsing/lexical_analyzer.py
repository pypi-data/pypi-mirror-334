from .command_token import Token
from .enums.token_type import TokenType
from .input_buffer import InputBuffer

class LexicalAnalyzer:
    def __init__(self, input_string: str):
        self.input_string = input_string
        self.token_list = []
        self.index = 0
        self.tmp = Token()
        self.tmp.lexeme = ""
        self.tmp.TokenType = TokenType.ERROR
        self.input = InputBuffer(input_string)
        token = self.get_token_main()
        while token.TokenType != TokenType.END_OF_FILE:
            self.token_list.append(token)
            token = self.get_token_main()
        pass

    def isspace(self, c):
        return (
            c == ' ' or
            c == '\t' or
            c == '\v' or
            c == '\n' or
            c == '\r' or
            c == '\f'
        )
    
    def isdigit(self, c):
        return (
            c == '0' or
            c == '1' or
            c == '2' or
            c == '3' or
            c == '4' or
            c == '5' or
            c == '6' or
            c == '7' or
            c == '8' or
            c == '9'
        )

    def skip_space_and_escape_chars(self):
        c = self.input.get_char()
        while not self.input.end_of_input() and (self.isspace(c) or c == '\\'):
            c = self.input.get_char()
        if not self.input.end_of_input():
            self.input.unget_char(c)
    
    def scan_error(self, tmp: Token, c):
        if not self.input.end_of_input():
            self.input.unget_char(c)
        tmp.TokenType = TokenType.ERROR
        return tmp
    
    def scan_num_sides_or_num_keeps(self, tmp: Token, c):
        while not self.input.end_of_input() and self.isdigit(c):
            tmp.lexeme += c
            c = self.input.get_char()
        if not self.input.end_of_input():
            self.input.unget_char(c)
        tmp.TokenType = TokenType.ROLL
        return tmp

    def scan_potential_roll_mod(self, tmp: Token, c):
        tmp = self.scan_num_sides_or_num_keeps(tmp, c)
        c1 = self.input.get_char()
        c2 = self.input.get_char()
        if (c1 + c2) == 'kh':
            tmp.lexeme += (c1 + c2)
            c = self.input.get_char()
            if(self.isdigit(c)):
                return self.scan_num_sides_or_num_keeps(tmp, c)
            else:
                if not self.input.end_of_input():
                    self.input.unget_char(c)
                tmp.TokenType = TokenType.ROLL
                return tmp
        else:
            if not self.input.end_of_input():
                self.input.unget_char(c2)
                self.input.unget_char(c1)
            tmp.TokenType = TokenType.ROLL
            return tmp

    def scan_number_or_roll(self):
        tmp = Token()
        tmp.lexeme = ""
        c = self.input.get_char()
        if self.isdigit(c):
            while not self.input.end_of_input() and self.isdigit(c):
                tmp.lexeme += c
                c = self.input.get_char()
            if c in ['d', 'e']:
                tmp.lexeme += c
                c = self.input.get_char()
                if self.isdigit(c):
                    return self.scan_potential_roll_mod(tmp, c)
                else:
                    return self.scan_error(tmp, c)
            if not self.input.end_of_input():
                self.input.unget_char(c)
            tmp.TokenType = TokenType.NUM
            return tmp
        else:
            return self.scan_error(tmp, c)
        
    def scan_roll(self):
        tmp = Token()
        tmp.lexeme = ""
        c = self.input.get_char()
        if c in ['d', 'e']:
            tmp.lexeme += c
            c = self.input.get_char()
            if self.isdigit(c):
                return self.scan_num_sides_or_num_keeps(tmp, c)
            else:
                return self.scan_error(tmp, c)
        else:
            return self.scan_error(tmp, c)
        
    def scan_gamble(self):
        tmp = Token()
        tmp.lexeme = ""
        c = self.input.get_char()
        while(c in 'gamble'):
            tmp.lexeme += c
            c = self.input.get_char()
        self.input.unget_char(c)
        if tmp.lexeme == 'gamble':
            tmp.TokenType = TokenType.GAMBLE
            return tmp
        else:
            return self.scan_error(tmp, c)

    def scan_odds(self, tmp: Token, c):
        while(c in 'odds'):
            tmp.lexeme += c
            c = self.input.get_char()
        if tmp.lexeme == 'odds':
            tmp.TokenType = TokenType.BET
            return tmp
        else:
            return self.scan_error(tmp, c)

    def scan_evens(self, tmp: Token, c):
        while(c in 'evens'):
            tmp.lexeme += c
            c = self.input.get_char()
        if tmp.lexeme == 'evens':
            tmp.TokenType = TokenType.BET
            return tmp
        else:
            return self.scan_error(tmp, c)
        
    def scan_bet(self):
        tmp = Token()
        tmp.lexeme = ""
        c = self.input.get_char()
        if c == 'o':
            return self.scan_odds(tmp, c)
        elif c == 'e':
            return self.scan_evens(tmp, c)
        else:
            return self.scan_error(tmp, c)
        
    def scan_recall(self):
        tmp = Token()
        tmp.lexeme = ""
        c = self.input.get_char()
        if c == 'h':
            tmp.lexeme += c
            tmp.TokenType = TokenType.RECALL
            return tmp
        else:
            return self.scan_error(tmp, c)
    
    def get_token(self):
        token = Token()
        if self.index == len(self.token_list):
            token.lexeme = ""
            token.TokenType = TokenType.END_OF_FILE
        else:
            token = self.token_list[self.index]
            self.index += 1
        return token
    
    def peek(self, how_far) -> Token:
        if how_far <= 0:
            print("cannot peek a non-positive amount")
            return
        peekIndex = self.index + how_far - 1
        if peekIndex > len(self.token_list) - 1:
            token = Token()
            token.lexeme = ""
            token.TokenType = TokenType.END_OF_FILE
            return token
        else:
            return self.token_list[peekIndex]

    def get_token_main(self):
        c1 = None
        self.skip_space_and_escape_chars()
        tmp = Token()
        tmp.lexeme = ""
        tmp.TokenType = TokenType.END_OF_FILE
        if not self.input.end_of_input():
            c1 = self.input.get_char()
        else:
            return tmp
        match c1:
            case '!': tmp.TokenType = TokenType.COMMAND_START
            case '+': tmp.TokenType = TokenType.PLUS
            case '-': tmp.TokenType = TokenType.MINUS
            case '*': tmp.TokenType = TokenType.MULT
            case '/': tmp.TokenType = TokenType.DIV
            case '(': tmp.TokenType = TokenType.LPAREN
            case ')': tmp.TokenType = TokenType.RPAREN
            case ',': tmp.TokenType = TokenType.COMMA
            case _:
                if self.isdigit(c1):
                    self.input.unget_char(c1)
                    tmp = self.scan_number_or_roll()
                elif c1 == 'd':
                    self.input.unget_char(c1)
                    tmp = self.scan_roll()
                elif c1 == 'e':
                    c2 = self.input.get_char()
                    if c2 == 'v':
                        self.input.unget_char(c2)
                        self.input.unget_char(c1)
                        tmp = self.scan_bet()
                    else:
                        self.input.unget_char(c2)
                        self.input.unget_char(c1)
                        tmp = self.scan_roll()
                elif c1 == 'o':
                    self.input.unget_char(c1)
                    tmp = self.scan_bet()
                elif c1 == 'g':
                    self.input.unget_char(c1)
                    tmp = self.scan_gamble()
                elif c1 == 'h':
                    self.input.unget_char(c1)
                    tmp = self.scan_recall()
                else:
                    tmp.TokenType = TokenType.ERROR
        return tmp