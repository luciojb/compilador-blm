from rply import ParserGenerator

from ast import *
from lexer import lexerTokens


# State instance which gets passed to parser !
class ParserState(object):
    def __init__(self):
        # We want to hold a dict of global-declared variables & functions.
        self.variables = {}
        self.functions = {}
        pass  # End ParserState's constructor !


class Parser():
    def __init__(self, module, builder, printf):
        self.pg = ParserGenerator(
            # A list of all token names accepted by the parser.
            [key for key in lexerTokens],
            precedence=(
                ('left', ['FUNCTION']),
                ('left', ['VAR']),
                ('left', ['EQUAL']),
                ('left', ['IF', 'ELSE', 'SEMICOLON']),
                ('left', ['AND', 'OR']),
                ('left', ['NOT']),
                ('left', ['EQEQUAL', 'NOTEQUAL', 'GREATEQUAL', 'GREATER', 'LESS', 'LESSEQUAL']),
                ('left', ['SUM', 'SUB']),
                ('left', ['MUL', 'DIV']),
                ('left', ['STRING', 'INTEGER', 'FLOAT', 'BOOLEAN', 'PI', 'E'])
            )
        )
        self.module = module
        self.builder = builder
        self.printf = printf
        self.parse()
        pass  # End Parser's constructor !

    def parse(self):
        @self.pg.production("main : program")
        def main_program(state, p):
            return Main(p[0])

        @self.pg.production('program : statement_full')
        def program_statement(state, p):
            return Program(p[0], None, state)

        @self.pg.production('program : statement_full program')
        def program_statement_program(state, p):
            return Program(p[0], p[1], state)

        @self.pg.production('expression : OPEN_PAREN expression CLOSE_PAREN')
        def expression_parenthesis(state, p):
            # In this case we need parenthesis only for precedence
            # so we just need to return the inner expression
            return ExpressParenthesis(p[1])

        @self.pg.production('statement_full : IF OPEN_PAREN expression CLOSE_PAREN LBRACE block RBRACE')
        def expression_if(state, p):
            return If(condition=p[2], body=p[5], state=state)

        @self.pg.production('statement_full : IF OPEN_PAREN expression CLOSE_PAREN LBRACE block RBRACE ELSE LBRACE block RBRACE')
        def expression_if_else(state, p):
            return If(condition=p[2], body=p[5], else_body=p[9], state=state)

        @self.pg.production('block : statement_full')
        def block_expr(state, p):
            return Block(p[0], None, state)

        @self.pg.production('block : statement_full block')
        def block_expr_block(state, p):

            return Block(p[0], p[1], state)

        @self.pg.production('statement_full : statement SEMICOLON')
        def statement_full(state, p):
            return StatementFull(p[0])

        @self.pg.production('statement : expression')
        def statement_expr(state, p):
            return Statement(p[0])

        @self.pg.production('statement : VAR IDENTIFIER EQUAL expression')
        def statement_assignment(state, p):
            return Assignment(Variable(p[1].getstr(), state), p[3], state)

        @self.pg.production('statement_full : FUNCTION IDENTIFIER OPEN_PAREN CLOSE_PAREN LBRACE block RBRACE')
        def statement_func_noargs(state, p):
            return FunctionDeclaration(name=p[1].getstr(), args=None, block=p[5], state=state)

        @self.pg.production('expression : NOT expression')
        def expression_not(state, p):
            return Not(p[1], state)

        @self.pg.production('expression : expression SUM expression')
        @self.pg.production('expression : expression SUB expression')
        @self.pg.production('expression : expression MUL expression')
        @self.pg.production('expression : expression DIV expression')
        def expression_binary_operator(state, p):
            if p[1].gettokentype() == 'SUM':
                return Sum(p[0], p[2], state)
            elif p[1].gettokentype() == 'SUB':
                return Sub(p[0], p[2], state)
            elif p[1].gettokentype() == 'MUL':
                return Mul(p[0], p[2], state)
            elif p[1].gettokentype() == 'DIV':
                return Div(p[0], p[2], state)
            else:
                raise LogicError('Oops, this should not be possible!')

        @self.pg.production('expression : expression NOTEQUAL expression')
        @self.pg.production('expression : expression EQEQUAL expression')
        @self.pg.production('expression : expression GREATEQUAL expression')
        @self.pg.production('expression : expression LESSEQUAL expression')
        @self.pg.production('expression : expression GREATER expression')
        @self.pg.production('expression : expression LESS expression')
        @self.pg.production('expression : expression AND expression')
        @self.pg.production('expression : expression OR expression')
        @self.pg.production('expression : expression SYM_AND expression')
        @self.pg.production('expression : expression SYM_OR expression')
        def expression_equality(state, p):
            if p[1].gettokentype() == 'EQEQUAL':
                return Equal(p[0], p[2], state)
            elif p[1].gettokentype() == 'NOTEQUAL':
                return NotEqual(p[0], p[2], state)
            elif p[1].gettokentype() == 'GREATEQUAL':
                return GreaterThanEqual(p[0], p[2], state)
            elif p[1].gettokentype() == 'LESSEQUAL':
                return LessThanEqual(p[0], p[2], state)
            elif p[1].gettokentype() == 'GREATER':
                return GreaterThan(p[0], p[2], state)
            elif p[1].gettokentype() == 'LESS':
                return LessThan(p[0], p[2], state)
            elif p[1].gettokentype() == 'AND':
                return And(p[0], p[2], state)
            elif p[1].gettokentype() == 'OR':
                return Or(p[0], p[2], state)
            elif p[1].gettokentype() == 'SYM_AND':
                return And(p[0], p[2], state)
            elif p[1].gettokentype() == 'SYM_OR':
                return Or(p[0], p[2], state)
            else:
                raise LogicError("Shouldn't be possible")

        @self.pg.production('expression : CONSOLE_INPUT OPEN_PAREN CLOSE_PAREN')
        def program(state, p):
            return Input()

        @self.pg.production('expression : CONSOLE_INPUT OPEN_PAREN expression CLOSE_PAREN')
        def program(state, p):
            return Input(expression=p[2], state=state)

        @self.pg.production('statement : PRINT OPEN_PAREN CLOSE_PAREN')
        def program(state, p):
            return Print()

        @self.pg.production('statement : PRINT OPEN_PAREN expression CLOSE_PAREN')
        def program(state, p):
            return Print(expression=p[2], state=state)

        @self.pg.production('expression : ABSOLUTE OPEN_PAREN expression CLOSE_PAREN')
        def expression_absolute(state, p):
            return Absolute(p[2], state)

        @self.pg.production('expression : SIN OPEN_PAREN expression CLOSE_PAREN')
        def expression_absolute(state, p):
            return Sin(p[2], state)

        @self.pg.production('expression : COS OPEN_PAREN expression CLOSE_PAREN')
        def expression_absolute(state, p):
            return Cos(p[2], state)

        @self.pg.production('expression : TAN OPEN_PAREN expression CLOSE_PAREN')
        def expression_absolute(state, p):
            return Tan(p[2], state)

        @self.pg.production('expression : POWER OPEN_PAREN expression COMMA expression CLOSE_PAREN')
        def expression_absolute(state, p):
            return Pow(p[2], p[4], state)

        @self.pg.production('expression : IDENTIFIER')
        def expression_variable(state, p):
            # Cannot return the value of a variable if it isn't yet defined
            return Variable(p[0].getstr(), state)

        @self.pg.production('expression : IDENTIFIER OPEN_PAREN CLOSE_PAREN')
        def expression_call_noargs(state, p):
            # Cannot return the value of a function if it isn't yet defined
            return CallFunction(name=p[0].getstr(), args=None, state=state)

        @self.pg.production('expression : const')
        def expression_const(state, p):
            return p[0]

        @self.pg.production('const : FLOAT')
        def constant_float(state, p):
            return Float(p[0].getstr(), state)

        @self.pg.production('const : BOOLEAN')
        def constant_boolean(state, p):
            return Boolean(p[0].getstr(), state)

        @self.pg.production('const : INTEGER')
        def constant_integer(state, p):
            return Integer(p[0].getstr(), state)

        @self.pg.production('const : STRING')
        def constant_string(state, p):
            return String(p[0].getstr().strip('"\''), state)

        @self.pg.production('const : PI')
        def constant_pi(state, p):
            return ConstantPI(p[0].getstr(), state)

        @self.pg.production('const : E')
        def constant_e(state, p):
            return ConstantE(p[0].getstr(), state)

        @self.pg.error
        def error_handle(state, token):
            print(state)
            raise ValueError(token)

    def build(self):
        return self.pg.build()
