import unittest
from hpie.lexer import lex
from hpie.parser import Parser
from hpie.ast_nodes import *

class TestParser(unittest.TestCase):
    def test_assignment(self):
        code = 'Set x to 10'
        tokens = lex(code)
        parser = Parser(tokens, code)
        ast = parser.parse()
        self.assertIsInstance(ast[0], Assignment)
        self.assertEqual(ast[0].target, 'x')
        self.assertIsInstance(ast[0].value, Literal)
        self.assertEqual(ast[0].value.value, 10)

    def test_binary_op(self):
        code = 'Set x to 1 + 2'
        tokens = lex(code)
        parser = Parser(tokens, code)
        ast = parser.parse()
        self.assertIsInstance(ast[0].value, BinaryOp)
        self.assertEqual(ast[0].value.op, '+')
