import sys
from hpie.lexer import lex
from hpie.parser import Parser
from hpie.interpreter import Interpreter

# Main tool to run Hpie files
def main():
    if len(sys.argv) < 2:
        print("Usage: python3 hs.py <filename.hs>")
        sys.exit(1)

    filename = sys.argv[1]
    try:
        with open(filename, 'r') as f:
            code = f.read()
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found")
        sys.exit(1)

    try:
        tokens = lex(code)
        parser = Parser(tokens, code)
        ast = parser.parse()
        interpreter = Interpreter()
        interpreter.interpret(ast)
    except Exception as e:
        # Don't print stack trace for Parser failures (handled by diagnostics)
        if not isinstance(e, SystemExit):
            print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
