import sys
import time
import threading

class Interpreter:
    def __init__(self, max_recursion=1000, max_time=5.0):
        self.env = Environment()
        self.max_recursion = max_recursion
        self.max_time = max_time
        self.start_time = None
        self._recursion_depth = 0

    def _check_limits(self):
        if self._recursion_depth > self.max_recursion:
            raise RecursionError("Max recursion depth exceeded")
        if self.start_time and (time.time() - self.start_time) > self.max_time:
            raise TimeoutError("Execution time limit exceeded")

    def _parse_number(self, val):
        try:
            return int(val)
        except ValueError:
            pass
        try:
            return float(val)
        except ValueError:
            return val

    def _load_module(self, module_path, alias=None):
        import importlib
        import os

        # Check if it's a native Hpie module (.hpy)
        if module_path.endswith(".hpy") or os.path.exists(module_path + ".hpy"):
            path = module_path if module_path.endswith(".hpy") else module_path + ".hpy"
            # ... existing logic for .hpy ...
            with open(path, "r") as f:
                code = f.read()
            tokens = lex(code)
            parser = Parser(tokens, code)
            ast = parser.parse()
            module_env = Environment()
            previous_env = self.env
            self.env = module_env
            for stmt in ast:
                if isinstance(stmt, FunctionDefinition):
                    module_env.define_function(stmt.name, stmt)
            for stmt in ast:
                if not isinstance(stmt, FunctionDefinition):
                    self.execute(stmt)
            self.env = previous_env
            previous_env.register_module(alias or module_path, {"vars": module_env.variables, "functions": module_env.functions})
        else:
            # Dynamic Python module import
            try:
                mod = importlib.import_module(module_path)
                # Register module
                self.env.register_module(alias or module_path, {"native_mod": mod})
            except ImportError:
                raise Exception(f"Python module '{module_path}' not found")

    def interpret(self, statements):
        if self.start_time is None:
            self.start_time = time.time()
            
        for stmt in statements:
            self._check_limits()
            if isinstance(stmt, FunctionDefinition):
                self.env.define_function(stmt.name, stmt)
            else:
                res = self.execute(stmt)
                if res is not None:
                    return res

    def execute(self, stmt):
        self._check_limits()
        if isinstance(stmt, Assignment):
            self.env.set_var(stmt.target, self.evaluate(stmt.value))
        elif isinstance(stmt, PrintStatement):
            print("".join([str(self.evaluate(e)) for e in stmt.expressions]))
        elif isinstance(stmt, IfStatement):
            if self.evaluate(stmt.condition):
                return self.interpret(stmt.then_block)
            elif stmt.else_block:
                return self.interpret(stmt.else_block)
        elif isinstance(stmt, WhileLoop):
            while self.evaluate(stmt.condition):
                self._check_limits()
                res = self.interpret(stmt.block)
                if res is not None:
                    return res
        elif isinstance(stmt, RepeatLoop):
            for _ in range(int(self.evaluate(stmt.times))):
                self._check_limits()
                res = self.interpret(stmt.block)
                if res is not None:
                    return res
        elif isinstance(stmt, InputStatement):
            val = input(f"Enter value for {stmt.target}: ")
            parsed = self._parse_number(val)
            self.env.set_var(stmt.target, parsed)
        elif isinstance(stmt, ChangeStatement):
            amount = self.evaluate(stmt.amount)
            val = self.env.get_var(stmt.target)
            self.env.set_var(
                stmt.target,
                val + amount if stmt.operation == "Increase" else val - amount,
            )
        elif isinstance(stmt, FunctionCall):
            return self.call_function(stmt)
        elif isinstance(stmt, ReturnStatement):
            return self.evaluate(stmt.value)
        elif isinstance(stmt, ImportStatement):
            self._load_module(stmt.module_path, stmt.alias)

    def call_function(self, call):
        self._recursion_depth += 1
        self._check_limits()
        try:
            name = call.name
            # Handle dict lookups like lib["add"]
            if "[" in name:
                var_name, key = name.split("[")
                key = key.replace('"', "").replace("]", "")
                obj = self.env.get_var(var_name)
                func = obj[key]
            else:
                func = self.env.get_function(name)

                # Check if function is in a loaded module (lib.function syntax)
                if not func and "." in name:
                    # Check if it's a variable attribute (object.method)
                    var_name, attr_name = name.split(".", 1)

                    # Debugging
                    print(f"DEBUG: Looking for module '{var_name}'")

                    module = self.env.get_module(var_name)
                    if module and "native_mod" in module:
                        native_mod = module["native_mod"]
                        func = getattr(native_mod, attr_name, None)
                    elif module:
                        func = module["functions"].get(attr_name)
                    else:
                        obj = self.env.get_var(var_name)
                        if obj:
                            func = getattr(obj, attr_name, None)


            if not func:
                raise UndefinedFunctionError(name)

            # Check if it's a built-in (function object, not AST node)
            if callable(func):
                args = [self.evaluate(a) for a in call.args]
                return func(*args)

            # User defined function
            new_env = Environment(parent=self.env)
            for i, param in enumerate(func.params):
                new_env.set_var(param, self.evaluate(call.args[i]))

            self.env = new_env
            result = self.interpret(func.block)
            self.env = self.env.parent
            return result
        finally:
            self._recursion_depth -= 1

    def evaluate(self, expr):
        self._check_limits()
        if isinstance(expr, Literal):
            return expr.value
        if isinstance(expr, Identifier):
            return self.env.get_var(expr.name)
        if isinstance(expr, FunctionCall):
            return self.call_function(expr)
        if isinstance(expr, BinaryOp):
            left, right = self.evaluate(expr.left), self.evaluate(expr.right)
            ops = {
                "is": lambda l, r: l == r,
                "is not": lambda l, r: l != r,
                ">": lambda l, r: l > r,
                "<": lambda l, r: l < r,
                "+": lambda l, r: l + r,
                "-": lambda l, r: l - r,
                "*": lambda l, r: l * r,
                "/": lambda l, r: (
                    l / r if r != 0 else float("inf") if l >= 0 else float("-inf")
                ),
                "and": lambda l, r: str(l) + str(r),
            }
            return ops[expr.op](left, right)
        raise EvaluationError(type(expr))

# Keep imports at top, assuming the original imports exist as well.
from .lexer import lex
from .parser import *
from .ast_nodes import *
from .stdlib import BUILTINS
from .diagnostics import UndefinedVariableError, UndefinedFunctionError, EvaluationError
from .environment import Environment
