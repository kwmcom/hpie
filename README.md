# Hpie

A simple, highly readable programming language that feels like natural English prose. Built with Python 3.

## Features

- **Prose-like Syntax**: Uses intuitive keywords like `Set`, `Say`, `Ask for`, `Increase`, and `Decrease`.
- **Natural Logic**: Supports `If/Otherwise`, `While` loops, and `Repeat [n] times`.
- **Readable Comparisons**: Uses `is`, `is not`, `is greater than`, and `is less than`.
- **Function Support**: Define reusable blocks with `To define [name]([params...]):` and execute with `Call [name]([args...])`.
- **Clean Blocks**: Indentation-based scoping enforced by the parser.
- **Strict Error Handling**: Categorized, visual diagnostics for syntax and runtime issues.

## Examples

### Functions
```prose
To define square(n):
    Return n * n

Set result to Call square(4)
Say "Square of 4 is " and result
```

### Loops and Logic
```prose
Set count to 1
While count is less than 4:
    Say "Looping... count is " and count
    Increase count by 1
```

## Error System

Hpie provides precise, visual feedback for development:
- Syntax Errors (with caret indicators)
- Runtime Errors (scope/undefined variables)

## Usage

Run any `.hs` file using the Hpie CLI:

```bash
python3 hs.py examples/functions2.hs
```

## File Structure

- `hs.py`: CLI entry point.
- `hpie/`: Core language implementation (Lexer, Parser, Interpreter, Diagnostics).
- `examples/`: Sample scripts to get you started.
