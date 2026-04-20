class Diagnostic:
    def __init__(self, err_type, message, line, column, length, line_content):
        self.err_type = err_type
        self.message = message
        self.line = line
        self.column = column
        self.length = length
        self.line_content = line_content

    def render(self):
        arrows = " " * self.column + "^" * self.length
        return f"{self.err_type} on line {self.line}: {self.message}\n{self.line_content}\n{arrows}"


class HpieError(Exception):
    """Base exception for Hpie runtime errors."""
    def __init__(self, message, diag=None):
        super().__init__(message)
        self.diag = diag


class SyntaxError(HpieError):
    pass


class UndefinedVariableError(HpieError):
    def __init__(self, name):
        self.name = name
        super().__init__(f"Unknown variable '{name}'")


class UndefinedFunctionError(HpieError):
    def __init__(self, name):
        self.name = name
        super().__init__(f"Unknown function '{name}'")


class EvaluationError(HpieError):
    def __init__(self, expr_type):
        self.expr_type = expr_type
        super().__init__(f"Unknown expression: {expr_type}")
