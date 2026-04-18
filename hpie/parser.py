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

class Parser:
    def __init__(self, tokens, source_code):
        self.tokens = tokens
        self.source_lines = source_code.split('\n')
        self.pos = 0

    def peek(self, offset=0):
        if self.pos + offset < len(self.tokens):
            return self.tokens[self.pos + offset]
        return None

    def consume(self, type=None, value=None, error_msg=None):
        token = self.peek()
        if not token:
            self.fail(error_msg or f"Unexpected end of input", self.tokens[-1])
        if (type and token.type != type) or (value and token.value != value):
            self.fail(error_msg or f"Expected {type} {value}, got {token.type} {token.value}", token)
        self.pos += 1
        return token

    def fail(self, message, token):
        line_content = self.source_lines[token.line - 1]
        diag = Diagnostic(message, token.line, token.column, len(str(token.value)), line_content)
        print(diag.render())
        raise SystemExit(1)

    def parse(self):
        statements = []
        while self.peek() and self.peek().type != 'DEDENT':
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
            while self.peek() and self.peek().type == 'NEWLINE':
                self.consume('NEWLINE')
        return statements

    def parse_statement(self):
        token = self.peek()
        if not token or token.type in ['NEWLINE', 'DEDENT']:
            return None
        
        if token.type == 'INDENT':
            self.consume('INDENT')
            return self.parse_statement()

        if token.type == 'KEYWORD':
            if token.value == 'Set':
                return self.parse_assignment()
            elif token.value == 'Say':
                return self.parse_say()
            elif token.value == 'Ask for':
                return self.parse_ask()
            elif token.value == 'If':
                return self.parse_if()
            elif token.value == 'While':
                return self.parse_while()
            elif token.value == 'Repeat':
                return self.parse_repeat()
            elif token.value in ['Increase', 'Decrease']:
                return self.parse_change()
        
        self.fail(f"Unexpected statement starting with {token.value}", token)

    def parse_assignment(self):
        self.consume('KEYWORD', 'Set')
        target_token = self.consume('IDENTIFIER')
        self.consume('KEYWORD', 'to', error_msg='Expected "to" after variable name')
        value = self.parse_expression()
        return Assignment(target_token.value, value)

    def parse_say(self):
        self.consume('KEYWORD', 'Say')
        expressions = [self.parse_expression()]
        while self.peek() and self.peek().value == 'and':
            self.consume('KEYWORD', 'and')
            expressions.append(self.parse_expression())
        return PrintStatement(expressions)

    def parse_ask(self):
        self.consume('KEYWORD', 'Ask for')
        target = self.consume('IDENTIFIER').value
        return InputStatement(target)

    # Expression parsing with precedence
    def parse_expression(self):
        return self.parse_comparison()

    def parse_comparison(self):
        left = self.parse_sum()
        token = self.peek()
        if token and token.value == 'is':
            self.consume('KEYWORD', 'is')
            op = 'is'
            if self.peek() and self.peek().value == 'not':
                self.consume('KEYWORD', 'not')
                op = 'is not'
            elif self.peek() and self.peek().value == 'greater':
                self.consume('KEYWORD', 'greater')
                self.consume('KEYWORD', 'than')
                op = '>'
            elif self.peek() and self.peek().value == 'less':
                self.consume('KEYWORD', 'less')
                self.consume('KEYWORD', 'than')
                op = '<'
            right = self.parse_sum()
            return BinaryOp(left, op, right)
        return left

    def parse_sum(self):
        left = self.parse_product()
        while self.peek() and self.peek().value in ['+', '-']:
            op = self.consume('OPERATOR').value
            right = self.parse_product()
            left = BinaryOp(left, op, right)
        return left

    def parse_product(self):
        left = self.parse_primary()
        while self.peek() and self.peek().value in ['*', '/']:
            op = self.consume('OPERATOR').value
            right = self.parse_primary()
            left = BinaryOp(left, op, right)
        return left

    def parse_primary(self):
        token = self.consume()
        if token.type == 'NUMBER':
            return Literal(float(token.value) if '.' in token.value else int(token.value))
        if token.type == 'STRING':
            return Literal(token.value[1:-1])
        if token.type == 'IDENTIFIER':
            return Identifier(token.value)
        if token.value == '(':
            expr = self.parse_expression()
            self.consume('OPERATOR', ')', error_msg='Expected closing ")" after expression')
            return expr
        self.fail(f"Expected expression, got {token.value}", token)

    def parse_block(self):
        self.consume('COLON', error_msg="Blocks must start with a colon ':'")
        self.consume('NEWLINE', error_msg="Expected newline after ':'")
        
        # Expect INDENT token
        indent_token = self.peek()
        if not indent_token or indent_token.type != 'INDENT':
            self.fail("Expected an indented block", indent_token if indent_token else self.tokens[self.pos-1])
        
        self.consume('INDENT')
        statements = []
        
        # Parse statements until we see the matching DEDENT
        while self.peek() and self.peek().type != 'DEDENT':
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
            while self.peek() and self.peek().type == 'NEWLINE':
                self.consume('NEWLINE')
        
        self.consume('DEDENT', error_msg="Block not properly closed (dedent expected)")
        return statements

    def parse_if(self):
        self.consume('KEYWORD', 'If')
        condition = self.parse_expression()
        self.consume('KEYWORD', 'then')
        then_block = self.parse_block()
        else_block = None
        
        # Check for Otherwise at the same indentation level
        temp_pos = self.pos
        while temp_pos < len(self.tokens) and self.tokens[temp_pos].type == 'NEWLINE':
            temp_pos += 1
        
        if temp_pos < len(self.tokens) and self.tokens[temp_pos].value == 'Otherwise':
            self.pos = temp_pos
            self.consume('KEYWORD', 'Otherwise')
            else_block = self.parse_block()
            
        return IfStatement(condition, then_block, else_block)

    def parse_while(self):
        self.consume('KEYWORD', 'While')
        condition = self.parse_expression()
        block = self.parse_block()
        return WhileLoop(condition, block)

    def parse_repeat(self):
        self.consume('KEYWORD', 'Repeat')
        times = self.parse_expression()
        self.consume('KEYWORD', 'times')
        block = self.parse_block()
        return RepeatLoop(times, block)

    def parse_change(self):
        op = self.consume('KEYWORD').value
        target = self.consume('IDENTIFIER').value
        self.consume('KEYWORD', 'by')
        amount = self.parse_expression()
        return ChangeStatement(target, amount, op)
