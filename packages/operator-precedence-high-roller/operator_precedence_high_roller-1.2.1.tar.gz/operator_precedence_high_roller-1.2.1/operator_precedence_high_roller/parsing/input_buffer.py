class InputBuffer:
    def __init__(self, input_string: str):
        self.input_string = input_string
        self.eof = False
        self.input_buffer = []

    def end_of_input(self):
        if self.input_buffer:
            return False
        else:
            return self.eof
        
    def unget_char(self, c: str):
        if len(c) > 1:
            raise TypeError("input c in unget_char was given" + c + "instead of a char value.")
        if (c != '$'):
            self.input_buffer.append(c)
    
    def get_char(self):
        if self.input_buffer:
            return self.input_buffer.pop()
        elif(len(self.input_string) > 0):
            c = self.input_string[0]
            self.input_string = self.input_string[1:len(self.input_string)]
            return c
        else:
            self.eof = True
            return '$'