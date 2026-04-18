from .parser import Assignment, PrintStatement, IfStatement, WhileLoop, RepeatLoop, ChangeStatement, BinaryOp, Literal, Identifier, InputStatement

# Run the program by following the instructions
class Interpreter:
    def __init__(self):
        self.variables = {}

    def interpret(self, statements):
        for stmt in statements:
            self.execute(stmt)

    def execute(self, stmt):
        if isinstance(stmt, Assignment):
            self.variables[stmt.target] = self.evaluate(stmt.value)
        elif isinstance(stmt, PrintStatement):
            values = [str(self.evaluate(expr)) for expr in stmt.expressions]
            print("".join(values))
        elif isinstance(stmt, IfStatement):
            if self.evaluate(stmt.condition):
                self.interpret(stmt.then_block)
            elif stmt.else_block:
                self.interpret(stmt.else_block)
        elif isinstance(stmt, WhileLoop):
            while self.evaluate(stmt.condition):
                self.interpret(stmt.block)
        elif isinstance(stmt, RepeatLoop):
            times = self.evaluate(stmt.times)
            for _ in range(int(times)):
                self.interpret(stmt.block)
        elif isinstance(stmt, InputStatement):
            val = input(f"Enter value for {stmt.target}: ")
            try:
                if '.' in val:
                    val = float(val)
                else:
                    val = int(val)
            except ValueError:
                pass
            self.variables[stmt.target] = val
        elif isinstance(stmt, ChangeStatement):
            amount = self.evaluate(stmt.amount)
            if stmt.target not in self.variables:
                self.variables[stmt.target] = 0
            if stmt.operation == 'Increase':
                self.variables[stmt.target] += amount
            else:
                self.variables[stmt.target] -= amount

    def evaluate(self, expr):
        if isinstance(expr, Literal):
            return expr.value
        elif isinstance(expr, Identifier):
            if expr.name not in self.variables:
                raise Exception(f"Unknown variable '{expr.name}'")
            return self.variables[expr.name]
        elif isinstance(expr, BinaryOp):
            left = self.evaluate(expr.left)
            right = self.evaluate(expr.right)
            if expr.op == 'is':
                return left == right
            elif expr.op == 'is not':
                return left != right
            elif expr.op == '>':
                return left > right
            elif expr.op == '<':
                return left < right
            elif expr.op == '+':
                return left + right
            elif expr.op == '-':
                return left - right
            elif expr.op == '*':
                return left * right
            elif expr.op == '/':
                return left / right
        raise Exception(f"Unknown expression type: {type(expr)}")
