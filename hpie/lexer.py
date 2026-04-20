import re

# Define the basic patterns for our language
TOKEN_TYPES = [
    (
        "KEYWORD",
        r"\b(Set|to|Say|Ask for|If|import|as|is|then|Otherwise|While|Repeat|times|Increase|Decrease|by|not|greater|less|than|and|To define|Call|Return)\b",
    ),
    ("NUMBER", r"\d+(\.\d+)?"),
    ("STRING", r'"[^"]*"'),
    ("OPERATOR", r"[\+\-\*/\(\),\[\]\.]"),
    ("COMMENT", r"#.*"),
    ("IDENTIFIER", r"[a-zA-Z_][a-zA-Z0-9_]*"),
    ("COLON", r":"),
    ("NEWLINE", r"\n"),
    ("WHITESPACE", r"[ \t]+"),
]

TOKEN_PATTERNS = [
    (token_type, re.compile(pattern)) for token_type, pattern in TOKEN_TYPES
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
    lines = code.split("\n")
    indent_stack = [0]

    for line_num, line in enumerate(lines, 1):
        stripped = line.lstrip()
        if not stripped or stripped.startswith("#"):
            continue

        # Track indentation levels
        current_indent = len(line) - len(stripped)

        # Emit INDENT or DEDENT tokens
        if current_indent > indent_stack[-1]:
            indent_stack.append(current_indent)
            tokens.append(Token("INDENT", current_indent, line_num, 0))
        elif current_indent < indent_stack[-1]:
            while current_indent < indent_stack[-1]:
                indent_stack.pop()
                tokens.append(Token("DEDENT", current_indent, line_num, 0))

        pos = current_indent
        while pos < len(line):
            match = None
            for token_type, regex in TOKEN_PATTERNS:
                match = regex.match(line, pos)
                if match:
                    value = match.group(0)
                    if token_type not in ["WHITESPACE", "COMMENT"]:
                        tokens.append(Token(token_type, value, line_num, pos))
                    pos = match.end(0)
                    break
            if not match:
                pos += 1

        tokens.append(Token("NEWLINE", "\n", line_num, len(line)))

    # Close any remaining blocks
    while len(indent_stack) > 1:
        indent_stack.pop()
        tokens.append(Token("DEDENT", 0, len(lines), 0))

    return tokens
