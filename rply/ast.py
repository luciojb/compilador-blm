from rply.token import BaseBox

from ArvoreJSON import Node
from errors import *


# All token types inherit rply's basebox as rpython needs this
# These classes represent our Abstract Syntax Tree
# TODO: deprecate eval(env) as we move to compiling and then interpreting

class Program(BaseBox):
    def __init__(self, statement, program, state):
        self.state = state
        if type(program) is Program:
            self.statements = program.get_statements()
            self.statements.insert(0, statement)
        else:
            self.statements = [statement]

    def add_statement(self, statement):
        self.statements.insert(0, statement)

    def get_statements(self):
        return self.statements

    def eval(self, node):
        # print("Program<%s> statement's counter: %s" % (self, len(self.statements)))
        result = None
        for i, statement in enumerate(self.statements):
            left = Node('statement_full')
            right = Node('program')
            if i == len(self.statements) - 1:  # If last statement then stop appending Node("program") to the right !
                node.children.extend([left])
            else:
                node.children.extend([left, right])
            node = right
            result = statement.eval(left)  # Only now the statement.eval(node) does effect !
        return result  # The result is not been used yet !

    def rep(self):
        result = 'Program('
        for statement in self.statements:
            result += '\n\t' + statement.rep()
        result += '\n)'
        return result


class Block(BaseBox):
    def __init__(self, statement, block, state):
        self.state = state
        if type(block) is Block:
            self.statements = block.get_statements()
            self.statements.insert(0, statement)
        else:
            self.statements = [statement]

    def add_statement(self, statement):
        self.statements.insert(0, statement)

    def get_statements(self):
        return self.statements

    def eval(self, node):
        # print("Block<%s> statement's counter: %s" % (self, len(self.statements)))
        result = None
        for i, statement in enumerate(self.statements):
            left = Node('statement_full')
            right = Node('block')
            if i == len(self.statements) - 1:  # If last statement then stop appending Node("block") to the right !
                node.children.extend([left])
            else:
                node.children.extend([left, right])
            node = right
            result = statement.eval(left)  # Only now the statement.eval(node) does effect !
        return result  # The result is not been used yet !

    def rep(self):
        result = 'Block('
        for statement in self.statements:
            result += '\n\t' + statement.rep()
        result += '\n)'
        return result


class If(BaseBox):
    def __init__(self, condition, body, else_body=None, state=None):
        self.condition = condition
        self.body = body
        self.else_body = else_body
        self.state = state

    def eval(self, node):
        expression = Node("expression")
        node.children.extend([Node("IF"), Node("OPEN_PAREN"), expression, Node("CLOSE_PAREN")])
        condition = self.condition.eval(expression)
        block = Node("block")
        node.children.extend([Node("LBRACE"), block, Node("RBRACE")])
        else_block = Node("block")
        if self.else_body is not None:
            node.children.extend([Node("else"), Node("LBRACE"), else_block, Node("RBRACE")])
        if bool(condition) is True:
            return self.body.eval(block)
        else:
            if self.else_body is not None:
                return self.else_body.eval(else_block)
        return None

    def rep(self):
        return 'If(%s) Then(%s) Else(%s)' % (self.condition.rep(), self.body.rep(), self.else_body.rep())


class Variable(BaseBox):
    def __init__(self, name, state):
        self.name = str(name)
        self.value = None
        self.state = state

    def get_name(self):
        return str(self.name)

    def eval(self, node):
        identifier = Node("IDENTIFIER")
        node.children.extend([identifier])
        if dict(self.state.variables).get(self.name) is not None:
            self.value = self.state.variables[self.name]
            identifier.children.extend([Node(self.name, [Node(self.value)])])
            return self.value
        identifier.children.extend([Node("Variable <%s> is not yet defined" % str(self.name))])
        raise LogicError("Variable <%s> is not yet defined" % str(self.name))

    def to_string(self):
        return str(self.name)

    def rep(self):
        return 'Variable(%s)' % self.name


class FunctionDeclaration(BaseBox):
    def __init__(self, name, args, block, state):
        self.name = name
        self.args = args
        self.block = block
        state.functions[self.name] = self

    def eval(self, node):
        identifier = Node(self.name)
        node.children.extend([Node("FUNCTION"), identifier, Node("LBRACE"), Node("block"), Node("RBRACE")])
        return self

    def to_string(self):
        return "<function '%s'>" % self.name


class CallFunction(BaseBox):
    def __init__(self, name, args, state):
        self.name = name
        self.args = args
        self.state = state

    def eval(self, node):
        identifier = Node(self.name + " OPEN_PAREN CLOSE_PAREN")
        node.children.extend([identifier])
        return self.state.functions[self.name].block.eval(identifier)

    def to_string(self):
        return "<call '%s'>" % self.name


class BaseFunction(BaseBox):
    def __init__(self, expression, state):
        self.expression = expression
        self.value = None
        self.state = state
        self.roundOffDigits = 10

    def eval(self, node):
        raise NotImplementedError("This is abstract method from abstract class BaseFunction(BaseBox){...} !")

    def to_string(self):
        return str(self.value)

    def rep(self):
        return 'BaseFunction(%s)' % self.value


class Absolute(BaseFunction):
    def __init__(self, expression, state):
        super().__init__(expression, state)

    def eval(self, node):
        import re as regex
        expression = Node("expression")
        node.children.extend([Node("ABSOLUTE"), Node("OPEN_PAREN"), expression, Node("CLOSE_PAREN"), Node("SEMICOLON")])
        self.value = self.expression.eval(expression)
        if regex.search('^-?\d+(\.\d+)?$', str(self.value)):
            self.value = abs(self.value)
            return self.value
        else:
            raise ValueError("Cannot abs() not numerical values !")

    def rep(self):
        return 'Absolute(%s)' % self.value


class Sin(BaseFunction):
    def __init__(self, expression, state):
        super().__init__(expression, state)

    def eval(self, node):
        import re as regex
        expression = Node("expression")
        node.children.extend([Node("SIN"), Node("OPEN_PAREN"), expression, Node("CLOSE_PAREN")])
        self.value = self.expression.eval(expression)
        if regex.search('^-?\d+(\.\d+)?$', str(self.value)):
            import math
            self.value = round(math.sin(self.value), self.roundOffDigits)
            return self.value
        else:
            raise ValueError("Cannot sin() not numerical values !")

    def rep(self):
        return 'Sin(%s)' % self.value


class Cos(BaseFunction):
    def __init__(self, expression, state):
        super().__init__(expression, state)

    def eval(self, node):
        import re as regex
        expression = Node("expression")
        node.children.extend([Node("COS"), Node("OPEN_PAREN"), expression, Node("CLOSE_PAREN")])
        self.value = self.expression.eval(expression)
        if regex.search('^-?\d+(\.\d+)?$', str(self.value)):
            import math
            self.value = round(math.cos(self.value), self.roundOffDigits)
            return self.value
        else:
            raise ValueError("Cannot cos() not numerical values !")

    def rep(self):
        return 'Cos(%s)' % self.value


class Tan(BaseFunction):
    def __init__(self, expression, state):
        super().__init__(expression, state)

    def eval(self, node):
        import re as regex
        expression = Node("expression")
        node.children.extend([Node("TAN"), Node("OPEN_PAREN"), expression, Node("CLOSE_PAREN")])
        self.value = self.expression.eval(expression)
        if regex.search('^-?\d+(\.\d+)?$', str(self.value)):
            import math
            self.value = round(math.tan(self.value), self.roundOffDigits)
            return self.value
        else:
            raise ValueError("Cannot tan() not numerical values !")

    def rep(self):
        return 'Tan(%s)' % self.value


class Pow(BaseFunction):
    def __init__(self, expression, expression2, state):
        super().__init__(expression, state)
        self.expression2 = expression2
        self.value2 = None

    def eval(self, node):
        expression = Node("expression")
        expression2 = Node("expression")
        node.children.extend([Node("POWER"), Node("OPEN_PAREN"), expression, Node("COMMA"), expression2, Node("CLOSE_PAREN")])
        self.value = self.expression.eval(expression)
        self.value2 = self.expression2.eval(expression2)
        import re as regex
        match1 = regex.search('^-?\d+(\.\d+)?$', str(self.value))
        match2 = regex.search('^-?\d+(\.\d+)?$', str(self.value2))
        if match1 and match2:
            import math
            self.value = math.pow(self.value, self.value2)
            return self.value
        else:
            raise ValueError("Cannot pow() not numerical values !")

    def rep(self):
        return 'Pow(%s)' % self.value


# ABSTRACT CLASS! DO NOT USE!
class Constant(BaseBox):
    def __init__(self, state):
        self.value = None
        self.state = state

    def eval(self, node):
        value = Node(self.value)
        typed = Node(self.__class__.__name__.upper(), [value])
        constant = Node("const", [typed])
        node.children.extend([constant])
        return self.value

    def to_string(self):
        return str(self.value)

    def rep(self):
        return 'Constant(%s)' % self.value


class Boolean(Constant):
    def __init__(self, value, state):
        super().__init__(state)
        if ["true", "false", "True", "False", "TRUE", "FALSE", ].__contains__(value):
            if value.lower().__eq__("true"):
                self.value = True
            if value.lower().__eq__("false"):
                self.value = False
        else:
            raise TypeError("Cannot cast boolean value while initiating Constant !")

    def rep(self):
        return 'Boolean(%s)' % self.value


class Integer(Constant):
    def __init__(self, value, state):
        super().__init__(state)
        self.value = int(value)

    def rep(self):
        return 'Integer(%s)' % self.value


class Float(Constant):
    def __init__(self, value, state):
        super().__init__(state)
        self.value = float(value)

    def rep(self):
        return 'Float(%s)' % self.value


class String(Constant):
    def __init__(self, value, state):
        super().__init__(state)
        self.value = str(value)

    def to_string(self):
        return '"%s"' % str(self.value)

    def rep(self):
        return 'String("%s")' % self.value


class ConstantPI(Constant):
    def __init__(self, name, state):
        super().__init__(state)
        import math
        self.name = str(name)
        if str(name).__contains__('SUB'):
            self.value = float(-math.pi)
        else:
            self.value = float(math.pi)

    def rep(self):
        return '%s(%f)' % (self.name, self.value)


class ConstantE(Constant):
    def __init__(self, name, state):
        super().__init__(state)
        import math
        self.name = str(name)
        if str(name).__contains__('SUB'):
            self.value = float(-math.e)
        else:
            self.value = float(math.e)

    def rep(self):
        return '%s(%f)' % (self.name, self.value)


class BinaryOp(BaseBox):
    def __init__(self, left, right, state):
        self.left = left
        self.right = right
        self.state = state


class Assignment(BinaryOp):
    def eval(self, node):
        if isinstance(self.left, Variable):
            var_name = self.left.get_name()
            if dict(self.state.variables).get(var_name) is None:
                identifier = Node("IDENTIFIER", [Node(var_name)])
                expression = Node("expression")
                node.children.extend([Node("VAR"), identifier, Node("EQUAL"), expression])
                self.state.variables[var_name] = self.right.eval(expression)
                # print(self.state.variables)
                return self.state.variables  # Return the ParserState() that hold the variables.

            # Otherwise raise error
            raise ImmutableError(var_name)

        else:
            raise LogicError("Cannot assign to <%s>" % self)

    def rep(self):
        return 'Assignment(%s, %s)' % (self.left.rep(), self.right.rep())


class Sum(BinaryOp):
    def eval(self, node):
        left = Node("expression")
        right = Node("expression")
        node.children.extend([left, Node("SUM"), right])
        return self.left.eval(left) + self.right.eval(right)


class Sub(BinaryOp):
    def eval(self, node):
        left = Node("expression")
        right = Node("expression")
        node.children.extend([left, Node("SUB"), right])
        return self.left.eval(left) - self.right.eval(right)


class Mul(BinaryOp):
    def eval(self, node):
        left = Node("expression")
        right = Node("expression")
        node.children.extend([left, Node("MUL"), right])
        return self.left.eval(left) * self.right.eval(right)


class Div(BinaryOp):
    def eval(self, node):
        left = Node("expression")
        right = Node("expression")
        node.children.extend([left, Node("DIV"), right])
        return self.left.eval(left) / self.right.eval(right)


class Equal(BinaryOp):
    def eval(self, node):
        left = Node("expression")
        right = Node("expression")
        node.children.extend([left, Node("EQEQUAL"), right])
        return self.left.eval(left) == self.right.eval(right)


class NotEqual(BinaryOp):
    def eval(self, node):
        left = Node("expression")
        right = Node("expression")
        node.children.extend([left, Node("NOTEQUAL"), right])
        return self.left.eval(left) != self.right.eval(right)


class GreaterThan(BinaryOp):
    def eval(self, node):
        left = Node("expression")
        right = Node("expression")
        node.children.extend([left, Node("GREATER"), right])
        return self.left.eval(left) > self.right.eval(right)


class LessThan(BinaryOp):
    def eval(self, node):
        left = Node("expression")
        right = Node("expression")
        node.children.extend([left, Node("LESS"), right])
        return self.left.eval(left) < self.right.eval(right)


class GreaterThanEqual(BinaryOp):
    def eval(self, node):
        left = Node("expression")
        right = Node("expression")
        node.children.extend([left, Node("GREATEQUAL"), right])
        return self.left.eval(left) >= self.right.eval(right)


class LessThanEqual(BinaryOp):
    def eval(self, node):
        left = Node("expression")
        right = Node("expression")
        node.children.extend([left, Node("LESSEQUAL"), right])
        return self.left.eval(left) <= self.right.eval(right)


class And(BinaryOp):
    def eval(self, node):
        left = Node("expression")
        right = Node("expression")
        node.children.extend([left, Node("AND"), right])
        return self.left.eval(left) and self.right.eval(right)


class Or(BinaryOp):
    def eval(self, node):
        left = Node("expression")
        right = Node("expression")
        node.children.extend([left, Node("OR"), right])
        return self.left.eval(left) or self.right.eval(right)


class Not(BaseBox):
    def __init__(self, expression, state):
        self.value = expression
        self.state = state

    def eval(self, node):
        expression = Node("expression")
        node.children.extend([Node("NOT"), expression])
        self.value = self.value.eval(expression)
        if isinstance(self.value, bool):
            return not bool(self.value)
        raise LogicError("Cannot 'not' that")


class Print(BaseBox):
    def __init__(self, expression=None, state=None):
        self.value = expression
        self.state = state

    def eval(self, node):
        node.children.extend([Node("PRINT"), Node("OPEN_PAREN")])
        if self.value is None:
            print()
        else:
            expression = Node("expression")
            node.children.extend([expression])
            print(self.value.eval(expression))
        node.children.extend([Node("CLOSE_PAREN")])


class Input(BaseBox):
    def __init__(self, expression=None, state=None):
        self.value = expression
        self.state = state

    def eval(self, node):
        node.children.extend([Node("CONSOLE_INPUT"), Node("OPEN_PAREN")])
        if self.value is None:
            result = input()
        else:
            expression = Node("expression")
            node.children.extend([expression])
            result = input(self.value.eval(expression))
        node.children.extend([Node("CLOSE_PAREN")])
        import re as regex
        if regex.search('^-?\d+(\.\d+)?$', str(result)):
            return float(result)
        else:
            return str(result)


class Main(BaseBox):
    def __init__(self, program):
        self.program = program

    def eval(self, node):
        program = Node("program")
        node.children.extend([program])
        return self.program.eval(program)


class ExpressParenthesis(BaseBox):
    def __init__(self, expression):
        self.expression = expression

    def eval(self, node):
        expression = Node("expression")
        node.children.extend([Node("OPEN_PAREN"), expression, Node("CLOSE_PAREN")])
        return self.expression.eval(expression)


class StatementFull(BaseBox):
    def __init__(self, statement):
        self.statement = statement

    def eval(self, node):
        statement = Node("statement")
        node.children.extend([statement, Node("SEMICOLON")])
        return self.statement.eval(statement)


class Statement(BaseBox):
    def __init__(self, expression):
        self.expression = expression

    def eval(self, node):
        expression = Node("expression")
        node.children.extend([expression])
        return self.expression.eval(expression)
