import sys
from ctypes import CFUNCTYPE, c_int
from time import time

import llvmlite.binding as llvm

from sly_way.Lexer import PLexer
from sly_way.Parser import PParser
from sly_way.compiler import Compiler


def run_code(code):
    compiler = Compiler()
    lexer = PLexer()
    tokens = lexer.tokenize(code)
    # try:
    #     pprint([token.type + " : " + token.value for token in tokens])
    # except Exception as e:
    #     pprint(e)
    parser = PParser()
    parser.parse(tokens)
    ast = parser.ast
    ast = ast[1]['body']
    # print(pprint.pformat(ast))
    compiler.compile(ast)
    module = compiler.module

    module.triple = llvm.get_default_triple()
    llvm.initialize()
    llvm.initialize_native_target()
    llvm.initialize_native_asmprinter()

    llvm_ir_parsed = llvm.parse_assembly(str(module))
    llvm_ir_parsed.verify()

    target_machine = llvm.Target.from_default_triple().create_target_machine()
    engine = llvm.create_mcjit_compiler(llvm_ir_parsed, target_machine)
    engine.finalize_object()

    # Run the function with name func_name. This is why it makes sense to have a 'main' function that calls other functions.
    entry = engine.get_function_address('main')
    cfunc = CFUNCTYPE(c_int)(entry)

    with open('output.ll', 'w') as output_file:
        output_file.write(str(module))
    print('The llvm IR generated is:')
    print(module)
    print()
    start_time = time()
    result = cfunc()
    end_time = time()

    print(f'It returns {result}')
    print('\nExecuted in {:f} sec'.format(end_time - start_time))


if len(sys.argv) >= 2:
    with open(sys.argv[1], 'r') as file:
        code = file.read()
    run_code(code)
else:
    print('Usage: python3 main.py <filename>')
    raise TypeError('Expected a <file>')
