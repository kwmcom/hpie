import sys
from hpie.lexer import lex
from hpie.parser import Parser
from hpie.interpreter import Interpreter


def run_code(code, interpreter, filename="<stdin>"):
    try:
        tokens = lex(code)
        parser = Parser(tokens, code)
        ast = parser.parse()
        return interpreter.interpret(ast)
    except Exception as e:
        print(f"Error: {e}")


def main():
    if len(sys.argv) < 2:
        print("Hpie v1.0.0 Interactive Shell (Ctrl+C to exit)")
        interpreter = Interpreter()
        while True:
            try:
                line = input("hpie> ")
                if not line.strip():
                    continue
                run_code(line, interpreter)
            except EOFError:
                break
            except KeyboardInterrupt:
                break
        sys.exit(0)

    filename = sys.argv[1]
    try:
        with open(filename, "r") as f:
            code = f.read()
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found")
        sys.exit(1)

    interpreter = Interpreter()
    run_code(code, interpreter, filename)


if __name__ == "__main__":
    main()
