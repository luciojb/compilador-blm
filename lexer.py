from rply import LexerGenerator


class Lexer():
    def __init__(self):
        self.lexer = LexerGenerator()

    def _add_tokens(self):
        # Print
        self.lexer.add('PRINT', r'print')
        # Parenthesis
        self.lexer.add('OPEN_PAREN', r'\(')
        self.lexer.add('CLOSE_PAREN', r'\)')
        #KEYS
        self.lexer.add('LBRACE', r'\{')
        self.lexer.add('RBRACE', r'\}')
        #BRACKETS
        self.lexer.add('OPEN_BRACKETS', r'\[')
        self.lexer.add('CLOSE_BRACKETS', r'\]')
        
        # Operators
        self.lexer.add('SUM', r'\+')
        self.lexer.add('SUB', r'\-')
        self.lexer.add('DIV', r'\/')
        self.lexer.add('MULT', r'\*')
        # Number
        self.lexer.add('NUMBER', r'\d+')
        # Semi Colon
        self.lexer.add('SEMI_COLON', r'\;')
        # COMMA
        self.lexer.add('COMMA', r'\,')
        # LESS
        self.lexer.add('LESS', r'\<')
        # GREATER
        self.lexer.add('GREATER', r'\>')
        # EQUAL
        self.lexer.add('EQUAL', r'\=')
        # EQEQUAL
        self.lexer.add('EQEQUAL', r'\=\=')
        # DOT
        self.lexer.add('DOT', r'\.')
        # PERCENT
        self.lexer.add('PERCENT', r'\%')
        # NOTEEQUAL
        self.lexer.add('NOTEQUAL', r'\!\=')
        # LESSEQUAL
        self.lexer.add('LESSEQUAL', r'\<\=')
        # GREATEQUAL
        self.lexer.add('GREATEQUAL', r'\>\=')
        # IF
        self.lexer.add('IF', r'\I\F')
        # VBAR
        self.lexer.add('VBAR', r'\|')
        # AMPER
        self.lexer.add('AMPER', r'\&')

        # Ignore spaces
        self.lexer.ignore('\s+')

    def get_lexer(self):
        self._add_tokens()
        return self.lexer.build()
