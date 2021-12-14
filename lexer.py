from rply import LexerGenerator

lexerTokens = {
    'E': r'-?__E__',
    'PI': r'-?__PI__',
    'FLOAT': r'-?\d+\.\d+',
    'INTEGER': r'-?\d+',
    'STRING': r'(""".*""")|(".*")|(\'.*\')',
    'BOOLEAN': r'true(?!\w)|false(?!\w)|True(?!\w)|False(?!\w)|TRUE(?!\w)|FALSE(?!\w)',
    # Mathematical Operators
    'SUM': r'\+',
    'SUB': r'\-',
    'MUL': r'\*',
    'DIV': r'\/',
    # Binary Operator
    'AND': r'and(?!\w)',
    'OR': r'or(?!\w)',
    'SYM_AND': r'\&\&',
    'SYM_OR': r'\|\|',
    # LESS
    'LESS': r'\<',
    # GREATER
    'GREATER': r'\>',
    # EQUAL
    'EQUAL': r'\=',
    # EQEQUAL
    'EQEQUAL': r'\=\=',
    # DOT
    # 'DOT': r'\.',
    # PERCENT
    # 'PERCENT': r'\%',
    # NOTEEQUAL
    'NOTEQUAL': r'\!\=',
    # LESSEQUAL
    'LESSEQUAL': r'\<\=',
    # GREATEQUAL
    'GREATEQUAL': r'\>\=',
    # VBAR
    # 'VBAR': r'\|',
    # Statement
    'IF': r'if(?!\w)',
    'ELSE': r'else(?!\w)',
    'NOT': r'not(?!\w)',
    # Semi Colon
    'SEMICOLON': r'\;',
    'COMMA': r'\,',
    # Parenthesis
    'OPEN_PAREN': r'\(',
    'CLOSE_PAREN': r'\)',
    # KEYS
    'LBRACE': r'\{',
    'RBRACE': r'\}',
    # BRACKETS
    # 'OPEN_BRACKETS': r'\[',
    # 'CLOSE_BRACKETS': r'\]',

    # Function
    'CONSOLE_INPUT': r'input',
    'FUNCTION': r'function',
    'PRINT': r'print',
    'ABSOLUTE': r'abs',
    'SIN': r'sin',
    'COS': r'cos',
    'TAN': r'tan',
    'POWER': r'pow',
    # Assignment
    'VAR': r'var(?!\w)',
    'IDENTIFIER': "[a-zA-Z_][a-zA-Z0-9_]*"
}


class Lexer():
    def __init__(self):
        self.lexer = LexerGenerator()

    def _add_tokens(self):
        self.lexer.add('E', r'-?__E__')

        self.lexer.add('PI', r'-?__PI__')
        self.lexer.add('FLOAT', r'-?\d+\.\d+')
        self.lexer.add('INTEGER', r'-?\d+')
        self.lexer.add('STRING', r'(""".*""")|(".*")|(\'.*\')')
        self.lexer.add('BOOLEAN', r'true(?!\w)|false(?!\w)|True(?!\w)|False(?!\w)|TRUE(?!\w)|FALSE(?!\w)')
        # Mathematical Operators
        self.lexer.add('SUM', r'\+')
        self.lexer.add('SUB', r'\-')
        self.lexer.add('MUL', r'\*')
        self.lexer.add('DIV', r'\/')
        # Binary Operator
        self.lexer.add('AND', r'and(?!\w)')
        self.lexer.add('OR', r'or(?!\w)')
        self.lexer.add('SYM_AND', r'\&\&')
        self.lexer.add('SYM_OR', r'\|\|')
        # LESS
        self.lexer.add('LESS', r'\<')
        # GREATER
        self.lexer.add('GREATER', r'\>')
        # EQUAL
        self.lexer.add('EQUAL', r'\=')
        # EQEQUAL
        self.lexer.add('EQEQUAL', r'\=\=')
        # # DOT
        # self.lexer.add('DOT',  r'\.')
        # # PERCENT
        # self.lexer.add('PERCENT',  r'\%')
        # NOTEEQUAL
        self.lexer.add('NOTEQUAL', r'\!\=')
        # LESSEQUAL
        self.lexer.add('LESSEQUAL', r'\<\=')
        # GREATEQUAL
        self.lexer.add('GREATEQUAL', r'\>\=')
        # # VBAR
        # self.lexer.add('VBAR',  r'\|')
        # Statement
        self.lexer.add('IF', r'if(?!\w)')
        self.lexer.add('ELSE', r'else(?!\w)')
        self.lexer.add('NOT', r'not(?!\w)')
        # Semi Colon
        self.lexer.add('SEMICOLON', r'\;')
        self.lexer.add('COMMA', r'\,')
        # Parenthesis
        self.lexer.add('OPEN_PAREN', r'\(')
        self.lexer.add('CLOSE_PAREN', r'\)')
        # KEYS
        self.lexer.add('LBRACE', r'\{')
        self.lexer.add('RBRACE', r'\}')
        # BRACKETS
        # self.lexer.add( 'OPEN_BRACKETS',  r'\[')
        # self.lexer.add('CLOSE_BRACKETS',  r'\]')

        # Function
        self.lexer.add('CONSOLE_INPUT', r'input')
        self.lexer.add('FUNCTION', r'function')
        self.lexer.add('PRINT', r'print')
        self.lexer.add('ABSOLUTE', r'abs')
        self.lexer.add('SIN', r'sin')
        self.lexer.add('COS', r'cos')
        self.lexer.add('TAN', r'tan')
        self.lexer.add('POWER', r'pow')
        # Assignment
        self.lexer.add('VAR', r'var(?!\w)')
        self.lexer.add('IDENTIFIER', "[a-zA-Z_][a-zA-Z0-9_]*")
        # Ignore spaces
        self.lexer.ignore('\s+')

    def build(self):
        self._add_tokens()
        return self.lexer.build()
