# from lexer import Lexer
# from parser import Parser


#
# fname = "input.blm"
# with open(fname) as f:
#     text_input = f.read()
#
# lexer = Lexer().get_lexer()
# tokens = lexer.lex(text_input)


# pg.parse()
# parser = pg.get_parser()
# parser.parse(tokens).eval()
#
# codegen.create_ir()
# codegen.save_ir("output.ll")

import traceback
from copy import copy
from pprint import pprint

from rply.lexer import LexerStream

from ArvoreJSON import Node
from codegen import CodeGen
from lexer import Lexer
from parser import ParserState, Parser

codegen = CodeGen()

module = codegen.module
builder = codegen.builder
printf = codegen.printf
pg = Parser(module, builder, printf)

basic_assignment = """
    var initial = 60;
    var rate = 2;
    var position = initial + rate * 60;
    print(position);
    print(rate);
"""
function_declaration = """
function main() {
    var initial = 60;
    var rate = 2;
    var position = initial + rate * 60;
    print(position);
}
main();
"""
if_else_statement = """
if (False) {
    print(False == (5 != 5));
    print(5.1111 != 5.1);
    print(5 != 5);
    print(not True);
} else {
    print(abs(3.5 - 4));
    print(sin(3.5 - 4));
    print(cos(__E__ - __PI__));
    print(tan(__PI__ - __E__));
    print(pow(-2, 5));
}
"""
assignment_and_variables = """
    var a = 5 - 2;
    var b = 5;
    print(sin(a));
    print(a); print(b); print(b - a);
    print(not False);
"""
call_declared_functions = """
function userDefined() {
    var pi = __PI__;
    var e = __E__;
    print(2 * (pi + e - 1) / 3);
    print(abs(e - pi));
    print(sin(pi));
    print(cos(pi));
    print(tan(pi));
    print(pow(pi, e));
}
function main() {
    var i = input("Please input the number: ");
    if (i > 0 and i < 5) {
        print("i > 0 and i < 5 -> Call User Defined Function !");
        userDefined();
    } else {
        if (i > 5 && i < 10) {
            print("i > 5 && i < 10 -> Call User Defined Function !");
            userDefined();
        } else {
            print();
            print("Input value equal to or less than 0 !");
        }
    }
}
main();
"""

# lexer = Lexer().build()  # Build the lexer using LexerGenerator
# tokens: LexerStream
# try:
#     tokens = lexer.lex(call_declared_functions)  # Stream the input to analysis the lexical syntax
#     tokenType = map(lambda x: x.gettokentype(), copy(tokens))
#     tokenName = map(lambda x: x.getstr(), copy(tokens))
#     pprint(list(copy(tokens)))
#     # pprint(list(copy(tokenType)))
#     # pprint(list(copy(tokenName)))
# except (BaseException, Exception) as e:
#     traceback.print_exc()
#     print(e)
# finally:
#     print("Finish lexical analysis !")
#
# SymbolTable = ParserState()
# try:
#     pg.build().parse(copy(tokens), state=SymbolTable)  # Get syntax tree !
#     pg.build().parse(copy(tokens), state=SymbolTable).eval(node)  # Get semantic tree !
# except (BaseException, Exception) as e:
#     traceback.print_exc()
#     print(e)
# finally:
#     print("------------------------------Declared Variables & Functions are:------------------------------")
#     pprint(SymbolTable.variables)
#     pprint(SymbolTable.functions)

lexer = Lexer().build()  # Build the lexer using LexerGenerator
tokens: LexerStream
try:
    tokens = lexer.lex(call_declared_functions)  # Stream the input to analysis the lexical syntax
    tokenType = map(lambda x: x.gettokentype(), copy(tokens))
    tokenName = map(lambda x: x.getstr(), copy(tokens))
    pprint(list(copy(tokens)))
    # pprint(list(copy(tokenType)))
    # pprint(list(copy(tokenName)))
except (BaseException, Exception):
    traceback.print_exc()
finally:
    print("Finish lexical analysis !")

SymbolTable = ParserState()
syntaxRoot: Node
semanticRoot = Node("main")
try:
    syntaxRoot = Node("main", pg.build().parse(copy(tokens), state=SymbolTable))  # Get syntax tree !
    pg.build().parse(copy(tokens), state=SymbolTable).eval(semanticRoot)  # Get semantic tree !
except (BaseException, Exception):
    traceback.print_exc()
codegen.create_ir()
codegen.save_ir("output.ll")
