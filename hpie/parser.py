from .ast_nodes import *
from .diagnostics import Diagnostic, SyntaxError


class Parser:
    def __init__(self, tokens, source_code):
        self.tokens = tokens
        self.source_lines = source_code.split("\n")
        self.pos = 0

    def peek(self, offset=0):
        if self.pos + offset < len(self.tokens):
            return self.tokens[self.pos + offset]
        return None

    def consume(self, type=None, value=None, error_msg=None):
        token = self.peek()
        if not token:
            self.fail(
                error_msg or f"Unexpected end of input",
                self.tokens[-1] if self.tokens else None,
                err_type="SyntaxError",
            )
        if (type and token.type != type) or (value and token.value != value):
            self.fail(
                error_msg or f"Expected {type} {value}, got {token.type} {token.value}",
                token,
                err_type="SyntaxError",
            )
        self.pos += 1
        return token

    def fail(self, message, token, err_type="SyntaxError"):
        # Handle cases where token might be None (e.g. end of input)
        line = token.line if token and hasattr(token, 'line') else 1
        col = token.column if token and hasattr(token, 'column') else 1
        val = str(token.value) if token and hasattr(token, 'value') else ""
        
        line_content = self.source_lines[line - 1] if line <= len(self.source_lines) else ""
        diag = Diagnostic(
            err_type,
            message,
            line,
            col,
            len(val),
            line_content,
        )
        raise SyntaxError(diag.render(), diag=diag)

    def parse(self):
        try:
            statements = []
            while self.peek() and self.peek().type != "DEDENT":
                stmt = self.parse_statement()
                if stmt:
                    statements.append(stmt)
                while self.peek() and self.peek().type == "NEWLINE":
                    self.consume("NEWLINE")
            return statements
        except (IndexError, TypeError, AttributeError) as e:
            # Handle unexpected structure in fuzzer output gracefully
            self.fail(f"Invalid syntax structure: {e}", self.peek() if self.peek() else None)

    def parse_statement(self):
        token = self.peek()
        if not token or token.type in ["NEWLINE", "DEDENT"]:
            return None

        if token.type == "INDENT":
            self.consume("INDENT")
            return self.parse_statement()

        if token.type == "KEYWORD":
            if token.value == "Set":
                return self.parse_assignment()
            elif token.value == "Say":
                return self.parse_say()
            elif token.value == "Ask for":
                return self.parse_ask()
            elif token.value == "If":
                return self.parse_if()
            elif token.value == "While":
                return self.parse_while()
            elif token.value == "Repeat":
                return self.parse_repeat()
            elif token.value in ["Increase", "Decrease"]:
                return self.parse_change()
            elif token.value == "To define":
                return self.parse_function_def()
            elif token.value == "Return":
                return self.parse_return()
            elif token.value == "Call":
                return self.parse_function_call()
            elif token.value == "import":
                return self.parse_import()

        if token.type == "IDENTIFIER" and self.peek(1) and self.peek(1).value == "(":
            return self.parse_function_call()

        self.fail(
            f"Unexpected statement starting with {token.value}",
            token,
            err_type="SyntaxError",
        )

    def parse_assignment(self):
        self.consume("KEYWORD", "Set")
        target_token = self.consume("IDENTIFIER")
        self.consume("KEYWORD", "to", error_msg='Expected "to" after variable name')
        value = self.parse_expression()
        return Assignment(target_token.value, value)

    def parse_say(self):
        self.consume("KEYWORD", "Say")
        expressions = [self.parse_expression()]
        while self.peek() and self.peek().value == "and":
            self.consume("KEYWORD", "and")
            expressions.append(self.parse_expression())
        return PrintStatement(expressions)

    def parse_ask(self):
        self.consume("KEYWORD", "Ask for")
        target = self.consume("IDENTIFIER").value
        return InputStatement(target)

    def parse_return(self):
        self.consume("KEYWORD", "Return")
        return ReturnStatement(self.parse_expression())

    def parse_function_def(self):
        self.consume("KEYWORD", "To define")
        name = self.consume("IDENTIFIER").value
        params = []
        if self.peek() and self.peek().value == "(":
            self.consume("OPERATOR", "(")
            while self.peek() and self.peek().type == "IDENTIFIER":
                params.append(self.consume("IDENTIFIER").value)
                if self.peek() and self.peek().value == ",":
                    self.consume("OPERATOR", ",")
            self.consume("OPERATOR", ")")
        block = self.parse_block()
        return FunctionDefinition(name, params, block)

    def parse_function_call(self):
        if self.peek().value == "Call":
            self.consume("KEYWORD", "Call")
        name = self.consume("IDENTIFIER").value

        # Handle module.function syntax
        while self.peek() and self.peek().value == ".":
            self.consume("OPERATOR", ".")
            name = name + "." + self.consume("IDENTIFIER").value

        if self.peek() and self.peek().value == "[":
            self.consume("OPERATOR", "[")
            key = self.consume("STRING").value
            self.consume("OPERATOR", "]")
            name = f"{name}[{key}]"

        self.consume("OPERATOR", "(")
        args = []
        while self.peek() and self.peek().value != ")":
            args.append(self.parse_expression())
            if self.peek() and self.peek().value == ",":
                self.consume("OPERATOR", ",")
        self.consume("OPERATOR", ")")
        return FunctionCall(name, args)

    def parse_expression(self):
        return self.parse_and()

    def parse_and(self):
        left = self.parse_comparison()
        while self.peek() and self.peek().value == "and":
            self.consume("KEYWORD", "and")
            right = self.parse_comparison()
            left = BinaryOp(left, "and", right)
        return left

    def parse_comparison(self):
        left = self.parse_sum()
        token = self.peek()
        if token and token.value == "is":
            self.consume("KEYWORD", "is")
            op = "is"
            if self.peek() and self.peek().value == "not":
                self.consume("KEYWORD", "not")
                op = "is not"
            elif self.peek() and self.peek().value == "greater":
                self.consume("KEYWORD", "greater")
                self.consume("KEYWORD", "than")
                op = ">"
            elif self.peek() and self.peek().value == "less":
                self.consume("KEYWORD", "less")
                self.consume("KEYWORD", "than")
                op = "<"
            right = self.parse_sum()
            return BinaryOp(left, op, right)
        return left

    def parse_sum(self):
        left = self.parse_product()
        while self.peek() and self.peek().value in ["+", "-"]:
            op = self.consume("OPERATOR").value
            right = self.parse_product()
            left = BinaryOp(left, op, right)
        return left

    def parse_product(self):
        left = self.parse_primary()
        while self.peek() and self.peek().value in ["*", "/"]:
            op = self.consume("OPERATOR").value
            right = self.parse_primary()
            left = BinaryOp(left, op, right)
        return left


    def parse_primary(self):
        token = self.consume()
        if token.type == "NUMBER":
            return Literal(float(token.value) if "." in token.value else int(token.value))
        if token.type == "STRING":
            return Literal(token.value[1:-1])
        if token.type == "IDENTIFIER":
            if self.peek() and self.peek().value == "(":
                return self.parse_function_call()
            # Handle member access: identifier.identifier
            if self.peek() and self.peek().value == ".":
                self.consume("OPERATOR", ".")
                member = self.consume("IDENTIFIER").value
                return MemberAccess(Identifier(token.value), member)
            return Identifier(token.value)
        if token.value == "Call":
            return self.parse_function_call()
        if token.value == "(":
            expr = self.parse_expression()
            self.consume("OPERATOR", ")", error_msg='Expected closing ")" after expression')
            return expr
        self.fail(f"Expected expression, got {token.value}", token, err_type="SyntaxError")

    def parse_block(self):
        self.consume("COLON", error_msg="Blocks must start with a colon ':'")
        self.consume("NEWLINE", error_msg="Expected newline after ':'")

        indent_token = self.peek()
        if not indent_token or indent_token.type != "INDENT":
            self.fail(
                "Expected an indented block",
                indent_token if indent_token else self.tokens[self.pos - 1] if self.tokens else None,
                err_type="SyntaxError",
            )

        self.consume("INDENT")
        statements = []
        while self.peek() and self.peek().type != "DEDENT":
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
            while self.peek() and self.peek().type == "NEWLINE":
                self.consume("NEWLINE")

        self.consume("DEDENT", error_msg="Block not properly closed (dedent expected)")
        return statements

    def parse_if(self):
        self.consume("KEYWORD", "If")
        condition = self.parse_expression()
        self.consume("KEYWORD", "then")
        then_block = self.parse_block()
        else_block = None

        temp_pos = self.pos
        while temp_pos < len(self.tokens) and self.tokens[temp_pos].type == "NEWLINE":
            temp_pos += 1

        if temp_pos < len(self.tokens) and self.tokens[temp_pos].value == "Otherwise":
            self.pos = temp_pos
            self.consume("KEYWORD", "Otherwise")
            else_block = self.parse_block()

        return IfStatement(condition, then_block, else_block)

    def parse_while(self):
        self.consume("KEYWORD", "While")
        condition = self.parse_expression()
        block = self.parse_block()
        return WhileLoop(condition, block)

    def parse_repeat(self):
        self.consume("KEYWORD", "Repeat")
        times = self.parse_expression()
        self.consume("KEYWORD", "times")
        block = self.parse_block()
        return RepeatLoop(times, block)

    def parse_change(self):
        op = self.consume("KEYWORD").value
        target = self.consume("IDENTIFIER").value
        self.consume("KEYWORD", "by")
        amount = self.parse_expression()
        return ChangeStatement(target, amount, op)

    def parse_import(self):
        self.consume("KEYWORD", "import")
        self.consume("OPERATOR", "(")
        path_token = self.consume("STRING")
        module_path = path_token.value[1:-1]  # Remove quotes

        alias = None
        if self.peek() and self.peek().value == "as":
            self.consume("KEYWORD", "as")
            alias = self.consume("IDENTIFIER").value
        
        self.consume("OPERATOR", ")")

        return ImportStatement(module_path, alias)
