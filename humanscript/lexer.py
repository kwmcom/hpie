import re

# Define the basic patterns for our language
TOKEN_TYPES = [
    ('KEYWORD', r'\b(Set|to|Say|Ask for|If|then|Otherwise|While|Repeat|times|Increase|Decrease|by|is|not|greater|less|than|and)\b'),
    ('NUMBER', r'\d+(\.\d+)?'),
    ('STRING', r'"[^"]*"'),
    ('IDENTIFIER', r'[a-zA-Z_][a-zA-Z0-9_]*'),
    ('COLON', r':'),
    ('NEWLINE', r'\n'),
    ('WHITESPACE', r'[ \t]+'),
]

class Token:
    def __init__(self, type, value, line, column):
        self.type = type
        self.value = value
        self.line = line
        self.column = column

    def __repr__(self):
        return f"Token({self.type}, {repr(self.value)}, {self.line}:{self.column})"

# Convert source code into a list of tokens
def lex(code):
    tokens = []
    lines = code.split('\n')
    
    for line_num, line in enumerate(lines, 1):
        if not line.strip() and line_num < len(lines):
            continue
            
        # Track indentation levels
        indent_match = re.match(r'^([ \t]*)', line)
        indent = len(indent_match.group(1)) if indent_match else 0
        if line.strip():
            tokens.append(Token('INDENT', indent, line_num, 0))

        pos = indent
        while pos < len(line):
            match = None
            for token_type, pattern in TOKEN_TYPES:
                regex = re.compile(pattern)
                match = regex.match(line, pos)
                if match:
                    value = match.group(0)
                    if token_type != 'WHITESPACE':
                        tokens.append(Token(token_type, value, line_num, pos))
                    pos = match.end(0)
                    break
            if not match:
                pos += 1
        
        tokens.append(Token('NEWLINE', '\n', line_num, len(line)))
    
    return tokens
