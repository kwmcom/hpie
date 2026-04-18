# Define the structure of the program
class ASTNode:
    pass

class Statement(ASTNode):
    pass

class Expression(ASTNode):
    pass

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

# Turn tokens into an executable structure
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def peek(self, offset=0):
        if self.pos + offset < len(self.tokens):
            return self.tokens[self.pos + offset]
        return None

    def consume(self, type=None, value=None):
        token = self.peek()
        if not token:
            raise Exception(f"Unexpected end of input, expected {type} {value}")
        if (type and token.type != type) or (value and token.value != value):
            raise Exception(f"Expected {type} {value}, got {token.type} {token.value} at line {token.line}")
        self.pos += 1
        return token

    def parse(self):
        statements = []
        while self.peek():
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
            while self.peek() and self.peek().type == 'NEWLINE':
                self.consume('NEWLINE')
        return statements

    def parse_statement(self):
        token = self.peek()
        if not token: return None
        
        if token.type == 'INDENT':
            self.consume('INDENT')
            token = self.peek()

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
        
        self.pos += 1
        return None

    def parse_assignment(self):
        self.consume('KEYWORD', 'Set')
        target_token = self.consume('IDENTIFIER')
        target = target_token.value
        try:
            self.consume('KEYWORD', 'to')
        except Exception:
            raise Exception('Expected "to" after variable name')
        value = self.parse_expression()
        return Assignment(target, value)

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

    def parse_expression(self):
        left = self.parse_primary()
        
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
            
            right = self.parse_expression()
            return BinaryOp(left, op, right)
            
        return left

    def parse_primary(self):
        token = self.consume()
        if token.type == 'NUMBER':
            return Literal(float(token.value) if '.' in token.value else int(token.value))
        if token.type == 'STRING':
            return Literal(token.value[1:-1])
        if token.type == 'IDENTIFIER':
            return Identifier(token.value)
        raise Exception(f"Unexpected token {token}")

    def parse_block(self):
        colon_token = self.consume('COLON')
        self.consume('NEWLINE')
        
        next_token = self.peek()
        if not next_token or next_token.type != 'INDENT' or next_token.value == 0:
            line_num = next_token.line if next_token else colon_token.line + 1
            raise Exception(f"Invalid indentation on line {line_num}")
        
        block_indent = next_token.value
        statements = []
        
        while self.peek() and self.peek().type == 'INDENT' and self.peek().value >= block_indent:
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
            while self.peek() and self.peek().type == 'NEWLINE':
                self.consume('NEWLINE')
        
        return statements

    def parse_if(self):
        self.consume('KEYWORD', 'If')
        condition = self.parse_expression()
        self.consume('KEYWORD', 'then')
        then_block = self.parse_block()
        else_block = None
        
        temp_pos = self.pos
        while temp_pos < len(self.tokens) and self.tokens[temp_pos].type in ['NEWLINE', 'INDENT']:
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
