class Diagnostic:
    def __init__(self, err_type, message, line, column, length, source_line):
        self.err_type = err_type
        self.message = message
        self.line = line
        self.column = column
        self.length = length
        self.source_line = source_line

    def render(self):
        header = f"{self.err_type}: {self.message}"
        context = f"Line {self.line}: {self.source_line.strip()}"
        
        prefix = f"Line {self.line}: "
        original_indent = len(self.source_line) - len(self.source_line.lstrip())
        caret_pos = len(prefix) + (self.column - original_indent)
        
        caret = " " * caret_pos + "^" * max(1, self.length)
        return f"{header}\n{context}\n{caret}"

def report_error(err_type, message, token, source_lines):
    line_content = source_lines[token.line - 1]
    diag = Diagnostic(err_type, message, token.line, token.column, len(str(token.value)), line_content)
    print(diag.render())
