class Diagnostic:
    def __init__(self, message, line, column, length, source_line):
        self.message = message
        self.line = line
        self.column = column
        self.length = length
        self.source_line = source_line

    def render(self):
        # Format: Error: message
        #         Line 5: source_code
        #                 ^ (caret at column)
        header = f"Error: {self.message}"
        context = f"Line {self.line}: {self.source_line.strip()}"
        
        # Calculate padding for caret
        # The line starts with "Line X: " which we need to account for
        prefix = f"Line {self.line}: "
        # Find where the actual code starts relative to the original line
        # to align the caret correctly
        original_indent = len(self.source_line) - len(self.source_line.lstrip())
        caret_pos = len(prefix) + (self.column - original_indent)
        
        caret = " " * caret_pos + "^" * max(1, self.length)
        return f"{header}\n{context}\n{caret}"

def report_error(message, token, source_lines):
    line_content = source_lines[token.line - 1]
    diag = Diagnostic(message, token.line, token.column, len(str(token.value)), line_content)
    print(diag.render())
