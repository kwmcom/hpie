from .diagnostics import Diagnostic

class ASTNode: pass
class Statement(ASTNode): pass
class Expression(ASTNode): pass

class Assignment(Statement):
    def __init__(self, target, value):
        self.target = target
        self.value = value

class PrintStatement(Statement):
    def __init__(self, expressions):
        self.expressions = expressions

class IfStatement(Statement):
    def __init__(self, condition, then_block, else_block=None):
        self.condition = condition
        self.then_block = then_block
        self.else_block = else_block

class WhileLoop(Statement):
    def __init__(self, condition, block):
        self.condition = condition
        self.block = block

class RepeatLoop(Statement):
    def __init__(self, times, block):
        self.times = times
        self.block = block

class InputStatement(Statement):
    def __init__(self, target):
        self.target = target

class ChangeStatement(Statement):
    def __init__(self, target, amount, operation):
        self.target = target
        self.amount = amount
        self.operation = operation

class BinaryOp(Expression):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class Literal(Expression):
    def __init__(self, value):
        self.value = value

class Identifier(Expression):
    def __init__(self, name):
        self.name = name

class FunctionDefinition(Statement):
    def __init__(self, name, params, block):
        self.name = name
        self.params = params
        self.block = block

class FunctionCall(Expression, Statement):
    def __init__(self, name, args):
        self.name = name
        self.args = args

class ReturnStatement(Statement):
    def __init__(self, value):
        self.value = value
