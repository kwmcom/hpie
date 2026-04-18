from .parser import *
from .ast_nodes import *
from .stdlib import BUILTINS

class Interpreter:
    def __init__(self):
        self.scopes = [{}]
        self.functions = {}
        for name, func in BUILTINS.items():
            self.functions[name] = func

    def get_var(self, name):
        for scope in reversed(self.scopes):
            if name in scope: return scope[name]
        raise Exception(f"Unknown variable '{name}'")

    def set_var(self, name, value):
        self.scopes[-1][name] = value

    def interpret(self, statements):
        for stmt in statements:
            if isinstance(stmt, FunctionDefinition):
                self.functions[stmt.name] = stmt
            else:
                res = self.execute(stmt)
                if res is not None: return res

    def execute(self, stmt):
        if isinstance(stmt, Assignment): self.set_var(stmt.target, self.evaluate(stmt.value))
        elif isinstance(stmt, PrintStatement):
            print("".join([str(self.evaluate(e)) for e in stmt.expressions]))
        elif isinstance(stmt, IfStatement):
            if self.evaluate(stmt.condition): 
                return self.interpret(stmt.then_block)
            elif stmt.else_block: 
                return self.interpret(stmt.else_block)
        elif isinstance(stmt, WhileLoop):
            while self.evaluate(stmt.condition):
                res = self.interpret(stmt.block)
                if res is not None: return res
        elif isinstance(stmt, RepeatLoop):
            for _ in range(int(self.evaluate(stmt.times))):
                res = self.interpret(stmt.block)
                if res is not None: return res
        elif isinstance(stmt, InputStatement):
            val = input(f"Enter value for {stmt.target}: ")
            self.set_var(stmt.target, float(val) if '.' in val else int(val) if val.isdigit() else val)
        elif isinstance(stmt, ChangeStatement):
            amount = self.evaluate(stmt.amount)
            val = self.get_var(stmt.target)
            self.set_var(stmt.target, val + amount if stmt.operation == 'Increase' else val - amount)
        elif isinstance(stmt, FunctionCall):
            self.call_function(stmt)
        elif isinstance(stmt, ReturnStatement):
            return self.evaluate(stmt.value)

    def call_function(self, call):
        name = call.name
        # Handle dict lookups like lib["add"]
        if "[" in name:
            var_name, key = name.split("[")
            key = key.replace('"', '').replace(']', '')
            obj = self.get_var(var_name)
            func = obj[key]
        else:
            func = self.functions.get(name)

        if not func: raise Exception(f"Unknown function '{name}'")

        # Check if it's a built-in (function object, not AST node)
        if callable(func):
            args = [self.evaluate(a) for a in call.args]
            return func(*args)

        # User defined function
        new_scope = {}
        for i, param in enumerate(func.params):
            new_scope[param] = self.evaluate(call.args[i])

        self.scopes.append(new_scope)
        result = self.interpret(func.block)
        self.scopes.pop()
        return result

    def evaluate(self, expr):
        if isinstance(expr, Literal): return expr.value
        if isinstance(expr, Identifier): return self.get_var(expr.name)
        if isinstance(expr, FunctionCall): return self.call_function(expr)
        if isinstance(expr, BinaryOp):
            left, right = self.evaluate(expr.left), self.evaluate(expr.right)
            ops = {'is': lambda l, r: l == r, 'is not': lambda l, r: l != r, '>': lambda l, r: l > r, '<': lambda l, r: l < r, '+': lambda l, r: l + r, '-': lambda l, r: l - r, '*': lambda l, r: l * r, '/': lambda l, r: l / r}
            return ops[expr.op](left, right)
        raise Exception(f"Unknown expression: {type(expr)}")
