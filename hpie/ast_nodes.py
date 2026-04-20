class ASTNode:
    def evaluate(self, env):
        raise NotImplementedError

    def execute(self, env):
        raise NotImplementedError


class Statement(ASTNode):
    def execute(self, env):
        raise NotImplementedError

    def evaluate(self, env):
        raise NotImplementedError


class Expression(ASTNode):
    def evaluate(self, env):
        raise NotImplementedError

    def execute(self, env):
        return self.evaluate(env)


class Assignment(Statement):
    def __init__(self, target, value):
        self.target = target
        self.value = value

    def execute(self, env):
        val = self.value.evaluate(env)
        env.set(self.target, val)


class PrintStatement(Statement):
    def __init__(self, expressions):
        self.expressions = expressions

    def execute(self, env):
        values = [str(expr.evaluate(env)) for expr in self.expressions]
        print(" ".join(values))


class IfStatement(Statement):
    def __init__(self, condition, then_block, else_block=None):
        self.condition = condition
        self.then_block = then_block
        self.else_block = else_block

    def execute(self, env):
        if self.condition.evaluate(env):
            for stmt in self.then_block:
                stmt.execute(env)
        elif self.else_block:
            for stmt in self.else_block:
                stmt.execute(env)


class WhileLoop(Statement):
    def __init__(self, condition, block):
        self.condition = condition
        self.block = block

    def execute(self, env):
        while self.condition.evaluate(env):
            for stmt in self.block:
                stmt.execute(env)


class RepeatLoop(Statement):
    def __init__(self, times, block):
        self.times = times
        self.block = block

    def execute(self, env):
        times = int(self.times.evaluate(env))
        for _ in range(times):
            for stmt in self.block:
                stmt.execute(env)


class InputStatement(Statement):
    def __init__(self, target):
        self.target = target

    def execute(self, env):
        val = input(f"{self.target}: ")
        env.set(self.target, val)


class ChangeStatement(Statement):
    def __init__(self, target, amount, operation):
        self.target = target
        self.amount = amount
        self.operation = operation

    def execute(self, env):
        val = env.get(self.target)
        amt = self.amount.evaluate(env)
        if self.operation == "Increase":
            env.set(self.target, val + amt)
        elif self.operation == "Decrease":
            env.set(self.target, val - amt)


class ImportStatement(Statement):
    def __init__(self, module_path, alias=None):
        self.module_path = module_path
        self.alias = alias

    def execute(self, env):
        # Implementation depends on how Interpreter handles imports
        # For now, placeholder
        pass


class BinaryOp(Expression):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def evaluate(self, env):
        left = self.left.evaluate(env)
        right = self.right.evaluate(env)
        if self.op == "+": return left + right
        if self.op == "-": return left - right
        if self.op == "*": return left * right
        if self.op == "/": return left / right
        if self.op == "and": return left and right
        if self.op == "is": return left == right
        if self.op == "is not": return left != right
        if self.op == ">": return left > right
        if self.op == "<": return left < right
        return None


class Literal(Expression):
    def __init__(self, value):
        self.value = value

    def evaluate(self, env):
        return self.value


class Identifier(Expression):
    def __init__(self, name):
        self.name = name

    def evaluate(self, env):
        return env.get(self.name)


class MemberAccess(Expression):
    def __init__(self, obj, member):
        self.object = obj
        self.member = member

    def evaluate(self, env):
        # Implementation placeholder
        return None


class FunctionDefinition(Statement):
    def __init__(self, name, params, block):
        self.name = name
        self.params = params
        self.block = block

    def execute(self, env):
        env.define_function(self.name, self.params, self.block)


class FunctionCall(Expression, Statement):
    def __init__(self, name, args):
        self.name = name
        self.args = args

    def evaluate(self, env):
        args = [a.evaluate(env) for a in self.args]
        return env.call_function(self.name, args)

    def execute(self, env):
        return self.evaluate(env)


class ReturnStatement(Statement):
    def __init__(self, value):
        self.value = value

    def execute(self, env):
        val = self.value.evaluate(env)
        raise ReturnSignal(val)

class ReturnSignal(Exception):
    def __init__(self, value):
        self.value = value
